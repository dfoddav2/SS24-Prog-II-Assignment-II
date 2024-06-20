import { writable } from 'svelte/store';

const wordleSingle = (solution) => {
	let turn = writable(0);
	let turnValue = 0;
	turn.subscribe((value) => {
		turnValue = value;
	});

	let currentGuess = writable(''); // e.g. 'apple'
	let currentGuessValue = '';
	currentGuess.subscribe((value) => {
		currentGuessValue = value;
	});

	let guesses = writable([...Array(6)]); // Each guess is an array of letter objects
	let guessesValue = [];
	guesses.subscribe((value) => {
		guessesValue = value;
	});

	let history = writable([]); // Each guess is a string
	let historyValue = [];
	history.subscribe((value) => {
		historyValue = value;
	});

	let isCorrect = writable(false);

	// format a guess into an array of letter objects
	// e.g. [{key: "a", color: "yellow"}]
	const formatGuess = () => {
		let solutionArray = [...solution];
		let formattedGuess = [...currentGuessValue].map((letter) => {
			return { key: letter, color: 'grey' }; // by default the color is grey, update later
		});
		// console.log('formatting the guess - ', currentGuessValue);
		// find any green letters
		formattedGuess.forEach((letter, index) => {
			if (solutionArray[index] === letter.key) {
				letter.color = 'green';
				solutionArray[index] = null; // remove the letter from the solution array
			}
		});

		// find any yellow letters
		formattedGuess.forEach((letter, index) => {
			if (solutionArray.includes(letter.key) && letter.color !== 'green') {
				letter.color = 'yellow';
				solutionArray[solutionArray.indexOf(letter.key)] = null; // remove the letter from the solution array
			}
		});

		return formattedGuess;
	};

	// add a new guess to the guesses state
	// updatye isCorrect state if the guess is correct
	// add one to the turn state
	const addNewGuess = (formattedGuess) => {
		if (currentGuessValue === solution) {
			isCorrect.set(true);
		}
		guesses.update((prevGuesses) => {
			let newGuesses = [...prevGuesses];
			newGuesses[turnValue] = formattedGuess;
			return newGuesses;
		});
		history.update((prevHistory) => [...prevHistory, currentGuessValue]);
		turn.update((prevTurn) => prevTurn + 1);
		currentGuess.set('');
	};

	// handle keyup event & track current guess
	// if user presses enter, add the new guess (if all letters are filled, and guess is unique)
	const handleKeyUp = ({ key }) => {
		// console.log(key);
		if (/^[A-Za-z]$/.test(key)) {
			if (currentGuessValue.length < 5) {
				// Use currentGuessValue here
				currentGuess.update((value) => value + key.toLowerCase());
				console.log(currentGuessValue);
				return currentGuessValue;
			}
		} else if (key === 'Backspace') {
			if (currentGuessValue.length > 0) {
				currentGuess.update((value) => value.slice(0, -1));
				console.log(currentGuessValue);
				return currentGuessValue;
			}
		} else if (key === 'Enter') {
			// only add guess if turn is less than 5
			if (turnValue > 5) {
				console.log("You can't guess more than 5 times");
				return;
			}
			// do not  allow duplicate guesses
			if (historyValue.includes(currentGuessValue)) {
				console.log('You already guessed that');
				return;
			}
			// check word is 5 chars long
			if (currentGuessValue.length !== 5) {
				console.log('Word must be 5 characters long');
				return;
			}
			const formatted = formatGuess();
			addNewGuess(formatted);
			console.log(formatted);
		}
	};

	return {
		turn,
		currentGuess,
		guesses,
		isCorrect,
		handleKeyUp,
		history
	};
};

export default wordleSingle;
