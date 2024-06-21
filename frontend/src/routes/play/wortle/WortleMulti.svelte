<script>
	import { onMount } from 'svelte';
	import { user } from '../../../lib/userStore.js';
	import { writable } from 'svelte/store';
	// import wordleMulti from '../../../lib/wordleMultiLogic.js';
	import Grid from './Grid.svelte';
	import Modal from './Modal.svelte';

	export let gameState;
	export let socket;

	// Modal for showing win/lose state
	let showModal = false;
	const closeModal = () => {
		showModal = false;
	};

	// What do we need to keep track of?
	// - solution
	let solution = gameState.solution.toLowerCase();
	// - turn number
	let turn = writable(gameState.turn);
	// Check whose turn it is
	let hasTurn = false;
	if (($turn + 1) % 2 === 0) {
		if ($user.email === gameState.player2_mail) {
			hasTurn = true;
		} else {
			hasTurn = false;
		}
	} else {
		if ($user.email === gameState.player1_mail) {
			hasTurn = true;
		} else {
			hasTurn = false;
		}
	}
	// - current guess and current guess value
	let currentGuess = writable(''); // e.g. 'apple'
	let currentGuessValue = '';
	$: {
		currentGuessValue = $currentGuess;
	}
	// - guesses
	let guesses = writable(gameState.guesses);
	// - history of guesses
	let history = gameState.history;
	// - isCorrect
	let isCorrect = writable(gameState.is_correct);

	// Handle win / lose condtitions based on the received gameState
	// If at this point isCorrect is true, then the game is already over, the previous player won
	// If turn is greater than 5, then the game is already over, all players have lost
	if (gameState.is_correct) {
		console.log('Previous player has won!');
		if (hasTurn) {
			// TODO: Make call to server, adding 1 to played games
			async function lose() {
				const response = await fetch('http://localhost:7890/play/wortle/multiplayer', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${$user.access_token}`
					},
					body: JSON.stringify({ outcome: false })
				});
				if (response.ok) {
					console.log('Outcome sent to server');
				} else {
					// handle error
					console.log('Error sending outcome to server');
				}
			};
			lose();
			console.log('You have lost!');
			$isCorrect = false;
			// Show losing modal
			setTimeout(() => {
				showModal = true;
			}, 2000);
		} else {
			// TODO: Make call to server, adding 1 to score and played games
			async function win() {
				const response = await fetch('http://localhost:7890/play/wortle/multiplayer', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${$user.access_token}`
					},
					body: JSON.stringify({ outcome: true })
				});
				if (response.ok) {
					console.log('Outcome sent to server');
				} else {
					// handle error
					console.log('Error sending outcome to server');
				}
			};
			win();
			console.log('You have won!');
			$isCorrect = true;
			// Show winning modal
			setTimeout(() => {
				showModal = true;
			}, 2000);
		}
	}
	if ($turn > 5) {
		// window.removeEventListener('keyup', handleKeyUp);
		async function lose() {
				const response = await fetch('http://localhost:7890/play/wortle/multiplayer', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${$user.access_token}`
					},
					body: JSON.stringify({ outcome: false })
				});
				if (response.ok) {
					console.log('Outcome sent to server');
				} else {
					// handle error
					console.log('Error sending outcome to server');
				}
			};
		lose();
		console.log('All players have lost!');
		$isCorrect = false;
		setTimeout(() => {
			showModal = true;
		}, 2000);
		// TODO: Here make a call to the server updating the users data, adding one to the played games
	}

	// format a guess into an array of letter objects
	// - Called from: HandleKeyUp
	// - Needed for: addNewGuess
	// e.g. [{key: "a", color: "yellow"}, ...]
	const formatGuess = () => {
		// console.log('Formatting guess');
		let solutionArray = [...solution];
		// console.log('Solution array:', solutionArray);
		let formattedGuess = [...currentGuessValue].map((letter) => {
			return { key: letter, color: 'grey' }; // by default the color is grey, update later
		});

		// console.log('Checking for green letters');
		// find any green letters
		formattedGuess.forEach((letter, index) => {
			// console.log('Checking letter', letter.key, 'compared to', solutionArray[index]);
			if (solutionArray[index] === letter.key) {
				letter.color = 'green';
				solutionArray[index] = null; // remove the letter from the solution array
				// console.log('Found a green letter', letter.key);
			}
		});

		// console.log('Checking for yellow letters');
		// find any yellow letters
		formattedGuess.forEach((letter, index) => {
			if (solutionArray.includes(letter.key) && letter.color !== 'green') {
				letter.color = 'yellow';
				solutionArray[solutionArray.indexOf(letter.key)] = null; // remove the letter from the solution array
			}
		});

		return formattedGuess;
	};

	// This function does the following:
	// - Add a new guess to the guesses state
	// - update isCorrect state if the guess is correct
	// - add one to the turn state
	// - add the current guess to the history state
	// - reset the current guess
	// Called from: handleKeyUp
	const addNewGuess = (formattedGuess) => {
		// Add the new guess to the guesses array
		$guesses[$turn] = formattedGuess;

		// Check if the guess is correct - if it is update isCorrect
		if (currentGuessValue === solution) {
			$isCorrect = true;
		}

		// Add the current guess to the history array
		history = [...history, currentGuessValue];

		// Add one to the turn
		$turn = $turn + 1;
		$currentGuess = '';
	};

	// Handling keyups - only if the user has turn
	const handleKeyUp = ({ key }) => {
		// console.log(key);
		if (/^[A-Za-z]$/.test(key)) {
			if (currentGuessValue.length < 5) {
				$currentGuess = currentGuessValue + key.toLowerCase();
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
			console.log(history);
			// only add guess if turn is less than 5
			if (turn > 5) {
				console.log("You can't guess more than 5 times");
				return;
			}
			// do not  allow duplicate guesses
			if (history.includes(currentGuessValue)) {
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
			// Send the updated game state to the server
			console.log('Sending update to the server');
			socket.emit('update_game_state', {
				room_id: gameState.room_id,
				player1: gameState.player1,
				player1_mail: gameState.player1_mail,
				player2: gameState.player2,
				player2_mail: gameState.player2_mail,
				solution: gameState.solution,
				guesses: $guesses,
				history: history,
				turn: $turn,
				is_correct: $isCorrect
			});
		}
	};

	// Adding event listeners based on game state
	if (hasTurn) {
		onMount(() => {
			console.log('Solution:', gameState.solution);
			if (!$isCorrect && $turn <= 5) {
				window.addEventListener('keyup', handleKeyUp);
			}
			// window.addEventListener('keyup', handleKeyUp);

			// Cleanup
			return () => {
				window.removeEventListener('keyup', handleKeyUp);
			};
		});
	}
</script>

<div>
	<!-- <p>Wortle component</p> -->
	<!-- <p>Solution: {solution}</p> -->
	<!-- <p>currentGuess: {$currentGuess}</p> -->
	{#if hasTurn}
		<h3>It's your turn</h3>
	{:else}
		<h3>It's not your turn</h3>
	{/if}
	<p></p>
	<Grid {currentGuess} {guesses} {turn} />
	{#if showModal}
		<Modal {isCorrect} solution={gameState.solution} {turn} {closeModal} />
	{/if}
</div>

<style>
	h3 {
		font-family: 'OffBitBold', sans-serif;
		font-size: 2rem;
		margin-bottom: 0.5rem;
		/* margin-top: 1rem; */
	}
</style>
