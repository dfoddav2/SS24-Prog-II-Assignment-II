# David Fodor - Programming II. - Assignment 2

## About - Language Learning App

As I have written previously in my [proposal](./David%20Fodor%20-%20Assignment%202%20propsal.md):

> "My idea is a language learning web application which incorporates AI for conversation simulations / chats and explanations. The end goal would be to make a tool that even I would gladly use for my language learning journey, for this reason I have decided to only concentrate on English to German learning."

I think the current state of the application achieves this.

## How to run

My original idea was to dockerize the whole application, making the setup a whole lot more easier, however this way running `pytest` would have had to be ran through `docker exec` as well. This would have complicated things and we would have only shaved a few lines of setup commands, so I chose to opt out of Dockerizing everything.

Run and set up the parts seperately:

Backend:

> Tested on Python 3.12 and 3.10.4

- `cd backend` - Go into the backend directory
- `pip install -r requirements.txt` - To install the dependencies (you might want to create a venv beforehand)
- `docker compose up -d` - To run MongoDB in a docker container (Look out, it creates a container named `backend`)
- `python start.py` - To start the Flask server
  - SwaggerUI should be available at `http://127.0.0.1:7890`
- Don't forget to tear down the database after using `docker compose down -v`.

Backend (SwaggerUI):

> Requirements: node >= 18.13 (For SvelteKit)

> Tested on Node 20. on Windows with both Arc browser and Chrome

- To test routes using SwaggerUI you have to authorize yourself first. (of course only if you are not trying to test the need for authorization / routes that do not need it)
- To authorize yourself, navigate to the `User/login` endpoint and try using the JSON input to log in
- If you have successfully logged in you will receive a JWT token. For example `smre@241token`, copy the token, go to the top right corner of SwaggerUI and Authorize
- Use a combination of the word `Bearer` with the token you just received, such as `Bearer smre@241token`

> For testing purposes I generally advise using the User `asd@asd` with `123` as a password. It has some well tested predefined data in MongoDB.

> Of course you can also try out creating a new user and starting from there. Or some other predefined user like `abc@abc`, `456`.

Frontend: (in a seperate cmd)

- `cd fronted` - First `cd ..` if you are in backend directory
- `npm install` - To install node packages
- `npm run dev` - To run the Svelte development instance
- The frontend should be exposed at `http://localhost:5173/`

## How to test

You can test the application via `pytest`, I have written 19 in total, each testing an API endpoint. (Pytest coverage hasn't been implemented, however it isn't that hard to keep track of my 19 endpoints without it either.)

To test:

- `cd backend` - Go into the backend directory
- `docker compose up -d` - To run MongoDB in a docker container (Look out, it creates a container named `backend`)
- `pytest` to run pytest

## Tips

- Use `asd@asd` - `123` as a deafult user to look around
- When playing `Wortle` check the console.log, I deliberately left logs there (and many other places) so that you can see what the answer is

## Design choices

Throughout the creation of the application I had to make many design choices, some coencided with my proposal, others have not. This section serves as an additional expalantion for major choices I have made. (Here I will usually not be discussing component level details, those ahve all been documented according to the Flask standard.)

Firstly, I chose to separate my application's frontend and backend as much as possible, I had two seperate repositories for working in them, but for the sake of the assignment I have combined them into this one repository.

### Backend

The backend uses the Application factory pattern, I basically started from scratch with this application, kept running into circular imports and then it hit me why we used it for the first assignment too.

The backend is quite simple, there was no need for storing and managing object like we did with the Newspaper Agency previously. Thus, no MVC seperation is used here, I only simply have the setup / connection logic via the application factory (mainly `start.py`, `app.py`, `extensions.py`), the API endpoints / namespaces (in `/backend/src/api`) and all the socket logic in `/backend/src/socket/wortle.py`.

This way the backend just serves as an intermedierary between MongoDB, external APIs and my own frontend application.

I am also using the popular CORS library to circumvent CORS policy errors when interacting between frontend and backend.

I tried documenting everything using the Flask way and paid attention to use appropriate responses, response status codes everywhere.

### Database

For the database I chose to use MongoDB, which I repopulate with each restart of the application / by test. This repopulation can be found in `app.py` where I basically copy all the raw data from a `mock_db_copy.json` into the database.

To see what my datastructure looks like you can check it out by opening either of the `mock_db.json` files, or connecting to the DB using MongoDB Compass.

### Frontend

On the frontend I am using SvelteKit with Tailwind. I tried choosing a simple design looks-wise that is fairly quick to implement, but this was done so at a later stage of the design.

I tried making things as close as possible to a real life application, e.g.there is data persistence between sites via stores, session tokens and user data are stored in session storage, similarly users with expired tokens are taken to the login screen. (this is done in a clever way, if whenever the backend gives a 401 response I reset the user on the frontend)

There are many-many small quality of life improvements and decisions with a frontend application and I tried ticking as many of the quicker boxes as possible. For some things I didn't have much time left, load indicators are just texts, no fancy animations there and unexpected errors are not handled. (only expected onse, e.g. Wordbank input word is already in the user's Wordbank so we handle the 409 response on frontend side)

### Features available - Deviations from the original proposition

#### Non-exhaustive features list:

- User management `/user`
  - New users can register `/login`
    - Users are identified by email which must be unique
    - Passwords are hashed and salted using `Bcrypt`
  - Users can log in and get authenticated via `JWTs` safely
  - A user may choose to change their personal name at any point
  - Similarly a user can delete themselves via the Profile page
- Wortle `(can be interacted with using keyboard, enter to submit, backspace to delete)` `this feature needed a lot of time on the frontend`
  - Leaderboard `/play/wortle`
    - The leaderboard data is queried from the database via an endpoint, pre-sorted by number of multiplayer wins descending. Additionally the users row is highlighted in the table.
  - Singleplayer `/play/wortle/single`
    - The singleplayer version of the game takes a random 5 letter word from the user's wordbank and initializes the game with that
    - If no such word is found then the word to guess is chosen from a random set of predefined words (of course to not be too repetitive in a real application there could be an additional constraint, like a minimum number of 5 letter words a user needs to have to chose from them)
    - The outcome is then handled via an API endpoint adding one to the played games and additionally one to the number of singleplayer wins if outcome is True
  - Multiplayer `/play/wortle/multi`
    - Users are first put into a lobby page where they can see all the currently active users on this page. They may choose to invite an other player for a game, but they can only do this once at a time. (They may also cancel the invitation.)
    - A user leaving the page gets rid of them from the lobby, invitation cancels and rejections are also cleaned up, however there is an edge case for now where disconnects after having sent an invitations are not cleaned up
    - Once an invitation is accepted, the two players play round by round the same game as in singleplayer, but this time with only randomly chosen predefined words, who goes first is chosen using the `random` module
    - Outcome is similarly handled as the singleplayer game, this time either both users lose, or just one
- Chat
  - At any moment users can see their previous chats or start a new chat on the left section, similar to ChatGPTs UI
  - New chat `/chat`
    - Users may start a new chat by giving a starting instruction to the Ai, e.g. "You are a cashier at Lidl, helping me find an item"
    - Then a new chat instance is created, assigned an UUID and they can be found via the dynamic path `/chat/[chatID]`
    - For now after giving the initial instruction, users need to initiate the conversation
  - Old chat `/chat/[chatID]`
    - The dynamic chatID is parsed and the messages according to that ID are loaded. The user may send a new message, which always gets a response from the `GPT-3.5 Turbo` using that initially described scenario and the context of the last 3 messages. (This was cut off at three as to not consume so many tokens, but can be adjusted whenever easily)
    - `Upon pressing a message`, a modal is opened up with several options,
      1. The user may choose to have the AI explain the sentence, which explains the `grammar` behind the sentence in some surface level detail. (This of course uses GPT 3.5 Turbo just like before)
      2. The user is able to have the sentence `translated using DeepL`.
      3. The user may split the sentence up into its word elements, and `add any word to the Wordbank` by clicking it. Words already in the wordbank won't get added (handled via 409)
- Wordbank
  - The Wordbank shows users the list of words they have collected so far. Upon clicking a word, a modal shows up about that word, where users are able to
    - `Delete` that word from the Wordbank
    - Here my original goal was to get some data about the word using a dictionar api or scraping, but these did not come to fruition.
  - Users are also able to add lowercase words with no spaces to the wordbank using a form
    - Errors like incorrect word form or word already existing in the wordbank are both handled

#### What changed from my original plan:

- For my Database I am not using `Firebase`, but rather `MongoDB`, both are similar in practice, JSON styled NoSQL databases, but MongoDB had better support via `PyMongo` and easier initialization via `Docker`.
- For translation services I chose `DeepL` after all, which has a pretty generous free plan of 500,000 characters per month.

#### What features I haven't implemented yet from the proposal:

- Nice to haves
  - Reading materials - very static, didn't have time to get to it
  - Grammar cheat sheet - even more static, didn't get to it (nor might it make much sense)
  - Pre-planned situations for chat - the underlying logic works, which is the main point, populating it with a starting situation wouldn't have been too difficult, but a lot of frontend code would have been needed
- Duplicates
  - I only created one game after all, which was `Wortle` a Wordle styled german word guessing game. This by itself demonstrates the use of websockets and networking well and I didn't feel the need to further create similar games, like the meoji guesser or others.
- Wordbank
  - I couldn't find a free dictionary API after all and creating a stable / reliable scraper for Wiktionary would have taken a really long time, I decided against doing it for now.
  - With no meanings behind words no flash cards / der-die-das nor description features are viable.

### The issue of API Keys, external libraries and their tests

Right now the main problem I have is I use sensitive API keys, accessing OpenAI and DeepL, which I of course can not safely share via my GitHub repository. When testing the application you will only be seeing placeholders and even the `pytest` of these features use patching to make sure no call is bein made to these endpoints.

To make sure you can see these features work (without actually deploying) I thought I would share a Google Drive link

## Reflections on the assignment

I really liked this assignment and I think this setup was very satisfying, where we basically had our "hands held" with the first assignment, and then after we can actually create something unique to us with that base knowledge in the second assignment.

### What I have learned

As we have done Flask before, it wasn't really that new for me, however I had some interesting fights with circular imports, which led me to appreciate the Application Factory pattern even more.

On top of the usual challanges like the one I have mentioned before, I decided to try myself out in Svelte and Tailwind.

- Honestly, Tailwind was not that big of a timesave as I initially thought it would be, it was definitely a nice to have, but I am already used to creating custom CSS styles myself and I am not that bothered with the usual way of doing things.
- Svelte, however was a very nice experience, I have had some previous experience with Next.JS which is the same caliber as SvelteKit, but to me the syntax was more intuitive and it also felt much faster.

We were first introduced to Docker by Prof. Gambi in Database class, which I planto use a lot more, since it makes things much simpler. For example the setup of MongoDB was dead simple for this assignment.

### What I would have liked to do

- Of course, it would be great if I had the time to finish the Dictionary part of the application with the webscraping, but I am still also interested in implementing things like the reading materials from my proposal for example. (For scraping, German nouns starting with a capital letter hardens things considerably.)
- If I had just a little more time, I would have tried deploying the application via Vercel, MongoDB Atlas and PythonAnywhere, so that you can safely try out the features with API Keys.
- There are so many optimizations that could be done to the frontend too, better UI, testing with Playwright, and the fixing of some pesky bugs (here are the ones I was most annoyed with)
  - The multiplayer game of Wortle handles users disconnecting midgame, but the lobby doesn't handle users disconnecting after having sent an invite. There should be a cleanup function for this evoked in the frontend from the frontend.
  - (not so much of a bug, but unintentional bad design) When playing the multiplayer version of Wortle, the whole component gets rerendered with each step, making it look a bit janky.
  - The /chat page specifically accesses the user token in an unsafe way somehere, laeding to the development environment dying on some hot reloads.
