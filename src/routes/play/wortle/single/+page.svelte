<script>
	// Import necessary dependencies and components
	import { onMount } from 'svelte';
	import { user } from '../../../../lib/userStore.js';
	import { goto } from '$app/navigation';
	import Wortle from '../Wortle.svelte';

	// Get the word we are using for the game
	// TODO: Replace this with a call to the server
	// let solution = 'XXXXX';

	let solution = '';

	onMount(async () => {
		// let solution = 'xxxxx';
		if ($user && $user.access_token) {
			const response = await fetch('http://localhost:7890/play/wortle/singleplayer', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${$user.access_token}`
				}
			});
			if (response.status === 401) {
				user.reset();
				goto('/login');
			} else if (response.ok) {
				const data = await response.json();
				solution = data.word; // replace 'word' with the actual property name
			} else {
				console.error('Failed to fetch word:', response.status, response.statusText);
			}
		}
	});

	// let solution = '';
	// const words = ['ninja', 'apple', 'grape', 'mango', 'peach', 'cocos', 'guava', 'lemon'];
	// solution = words[Math.floor(Math.random() * words.length)];
</script>

<main class="flex flex-col items-center justify-center gap-5">
	<div class="card">
		<h2>Singleplayer Wortle Game</h2>
		<p class="text-center mb-8">(Simply start typing your guess, enter to confirm, backspace to delete)</p>
		{#if $user && $user.access_token}
			{#if solution}
				<Wortle {solution} />
			{/if}
		{:else}
			<p>You are not signed in. You need to sign in to play this game.</p>
			<button
				class="bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded"
				on:click={() => goto('/login')}>Go to Login</button
			>
		{/if}
	</div>
</main>

<style>
	.card {
		/* transition: all 0.5s ease-in-out; */
		z-index: 1;
		border: 4px solid rgba(255, 255, 255, 0.25);
		border-radius: 1rem;
		transition: background-color 0.3s ease;
		/* backdrop-filter: blur(10px); */
		padding: 3rem;
	}

	.card:hover {
		background-color: rgba(31, 31, 221, 0.6);
	}

	main {
		height: calc(100vh - 85px);
		font-family: 'GeistMedium', sans-serif;
	}

	h2 {
		font-family: 'OffBitBold', sans-serif;
		font-size: 3.5rem;
		/* margin-bottom: 1rem; */
	}
</style>
