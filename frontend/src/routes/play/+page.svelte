<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
</script>

<main class="flex flex-col items-center justify-center">
	<div class="card flex flex-col items-center gap-5 p-12">
		<h2>Wortle</h2>
		<p class="text-xl mb-4 text-center">
			Wortle is a german varitation of the popular game Wordle created by Josh Wardle.
		</p>
		<button
			class="text-white font-bold py-2 px-4 rounded"
			on:click={() => goto('/play/wortle')}>Play Wortle</button
		>
	</div>
	<p class="mt-3">Only this one for now...</p>
</main>

<style>
	main {
		height: calc(100vh - 85px);
		font-family: 'GeistMedium', sans-serif;
	}

	h2 {
		font-family: 'OffBitBold', sans-serif;
		font-size: 4rem;
	}

	.card {
		/* transition: all 0.5s ease-in-out; */
		z-index: 1;
		border: 4px solid rgba(255, 255, 255, 0.25);
		border-radius: 1rem;
		transition: background-color 0.3s ease;
		/* backdrop-filter: blur(10px); */
		max-width: 80%;
	}

	.card:hover {
		background-color: rgba(31, 31, 221, 0.6);
	}

	button {
		background-color: rgba(255, 166, 0, 0.5);
		transition: all 0.3s ease;
	}

	button:hover {
		background-color: rgba(255, 166, 0, 0.8);
	}
</style>