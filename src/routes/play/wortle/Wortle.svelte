<script>
	import { onMount } from 'svelte';
	import { user } from '../../../lib/userStore.js';
	import wordleSingle from '../../../lib/wordleSingleLogic.js';
	import Grid from './Grid.svelte';
	import Modal from './Modal.svelte';

	export let solution;

	const { currentGuess, handleKeyUp, guesses, isCorrect, turn, history } = wordleSingle(solution);
	let showModal = false;
	const closeModal = () => {
		showModal = false;
	};

	$: {
		console.log('IsCorrect:', $isCorrect, 'Turn:', $turn, 'Guesses:', $guesses);
	}

	onMount(() => {
		console.log('Solution:', solution);
		window.addEventListener('keyup', handleKeyUp);

		// Cleanup
		return () => {
			window.removeEventListener('keyup', handleKeyUp);
		};
	});

	$: if ($isCorrect) {
		window.removeEventListener('keyup', handleKeyUp);
		console.log('Congrats, you won!');

		// Send the outcome to the server
		async function win() {
			const response = await fetch('http://localhost:7890/play/wortle/singleplayer', {
				method: 'POST',
				headers: {
					"Content-Type": "application/json",
					"Authorization": `Bearer ${$user.access_token}`,
				},
				body: JSON.stringify({ outcome: true })
			});
			if (response.ok) {
				console.log('Outcome sent to server');
			} else {
				// handle error
				console.log('Error sending outcome to server');
			}
		}
		win();

		setTimeout(() => {
			showModal = true;
		}, 2000);
	}

	$: if ($turn > 5) {
		window.removeEventListener('keyup', handleKeyUp);
		console.log('Sorry, you lost!');
		setTimeout(() => {
			showModal = true;
		}, 2000);
	}
</script>

<div>
	<!-- <p>Wortle component</p> -->
	<!-- <p>Solution: {solution}</p> -->
	<!-- <p>currentGuess: {$currentGuess}</p> -->
	<Grid {currentGuess} {guesses} {turn} />
	{#if showModal}
		<Modal {isCorrect} {solution} {turn} {closeModal} />
	{/if}
</div>

<style>
</style>
