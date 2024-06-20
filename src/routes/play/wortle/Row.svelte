<script>
	export let guess, currentGuess;
	let letters = [];
	$: if (currentGuess) {
		letters = $currentGuess.split('');
	}
</script>

{#if guess}
	<div class="row past">
		{#each guess as letter, index (index)}
			<div class={letter.color}>{letter.key}</div>
		{/each}
	</div>
{:else if currentGuess}
	<div class="row current">
		{#each letters as letter, index (index)}
			<div class="filled">{letter}</div>
		{/each}
		{#each Array(5 - letters.length) as _, index (index)}
			<div></div>
		{/each}
	</div>
{:else}
	<div class="row">
		<div></div>
		<div></div>
		<div></div>
		<div></div>
		<div></div>
	</div>
{/if}

<style>
	.row {
		display: flex;
		text-align: center;
		justify-content: center;
	}
	.row > div {
		display: block;
		width: 60px;
		height: 60px;
		border: 1px solid #bbb;
		margin: 4px;
		text-align: center;
		line-height: 60px;
		text-transform: uppercase;
		font-weight: bold;
		font-size: 2em;
	}
	.grey {
		--background-color: #3a3a3c;
		--border-color: #3a3a3c;
		animation: flip 0.5s ease forwards;
	}
	.yellow {
		--background-color: #b49f3b;
		--border-color: #b49f3b;
		animation: flip 0.5s ease forwards;
	}
	.green {
		--background-color: #538d4e;
		--border-color: #538d4e;
		animation: flip 0.5s ease forwards;
	}
	.row > div:nth-child(2) {
		animation-delay: 0.2s;
	}
	.row > div:nth-child(3) {
		animation-delay: 0.4s;
	}
	.row > div:nth-child(4) {
		animation-delay: 0.6s;
	}
	.row > div:nth-child(5) {
		animation-delay: 0.8s;
	}

	.row.current > div.filled {
		animation: bounce 0.2s ease-in-out forwards;
	}

	/* Animations */
	@keyframes flip {
		0% {
			transform: rotateX(0deg);
			background: rgb(17 24 39);
			border-color: #bbb;
		}
		45% {
			transform: rotateX(90deg);
			background: rgb(17 24 39);
			border-color: #bbb;
		}
		55% {
			transform: rotateX(90deg);
			background: var(--background-color);
			border-color: var(--border-color);
		}
		100% {
			transform: rotateX(0deg);
			background: var(--background-color);
			border-color: var(--border-color);
		}
	}

	@keyframes bounce {
		0% {
			transform: scale(1);
			border-color: #bbb;
		}
		50% {
			transform: scale(1.2);
		}
		100% {
			transform: scale(1);
			border-color: #fff;
		}
	}
</style>
