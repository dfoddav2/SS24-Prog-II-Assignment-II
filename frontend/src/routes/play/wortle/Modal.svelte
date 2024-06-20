<script>
	export let isCorrect, solution, turn, closeModal;
	import { goto } from '$app/navigation';
</script>

<div class="modal">
	{#if $isCorrect}
		<div>
			<h2>Congratulations!</h2>
			<hr />
			<p class="solution">{solution}</p>
			{#if $turn > 1}
				<p>You found the solution in {$turn} guesses.</p>
			{:else}
				<p>You found the solution in {$turn} guess.</p>
			{/if}
			<button
				class="text-white font-bold py-2 px-4 rounded"
				on:click|stopPropagation={closeModal}>Close Modal</button
			>
			<button
				class="text-white font-bold py-2 px-4 rounded"
				on:click={() => goto('/play/wortle')}>See Scoreboard</button
			>
		</div>
	{:else}
		<div>
			<h2>Sorry, you lost.</h2>
			<hr />
			<p>Solution:</p>
			<p class="solution">{solution}</p>
			<p>Better luck next time!</p>
			<button
				class="text-white font-bold py-2 px-4 rounded"
				on:click|stopPropagation={closeModal}>Close Modal</button
			>
			<button
				class="text-white font-bold py-2 px-4 rounded"
				on:click={() => goto('/play/wortle')}>See Scoreboard</button
			>
		</div>
	{/if}
</div>

<style>
	.modal {
		background: rgba(5, 1, 36, 0.5);
		position: fixed;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
	}

	h2 {
		font-family: 'OffBitBold', sans-serif;
		font-size: 3rem;
	}

	.modal div {
		max-width: 50%;
		padding: 40px;
		border-radius: 1rem;
		margin: 18% auto;
		display: flex;
		flex-direction: column;
        align-items: center;
		text-align: center;
		z-index: 1;
		border: 4px solid rgba(255, 255, 255, 0.25);
		backdrop-filter: blur(10px);
		background-color: rgba(31, 31, 221, 0.4);
		font-family: 'GeistMedium', sans-serif;
		font-size: 1.5rem;
	}

	.modal .solution {
		/* color: #ff0000; */
		font-weight: bold;
		font-size: 2em;
		text-transform: uppercase;
		letter-spacing: 3px;
	}

	button {
		margin-top: 20px;
		background-color: rgba(255, 166, 0, 0.5);
		transition: all 0.3s ease;
		font-size: 1rem;
		/* max-width: 60%; */
	}

	button:hover {
		background-color: rgba(255, 166, 0, 0.8);
	}
</style>
