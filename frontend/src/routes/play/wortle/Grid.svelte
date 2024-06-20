<script>
	import Row from './Row.svelte';
	export let currentGuess, guesses, turn;
</script>

<div>
	{#each $guesses as guess, index (index)}
		{#if index === $turn}
			<Row {currentGuess} guess={undefined} />
		{:else}
			<Row {guess} currentGuess={undefined} />
		{/if}
	{/each}
</div>
