<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { user } from '../../lib/userStore.js';
	import { writable } from 'svelte/store';

	let isLoading = true;
	let wordbank = writable([]);
	let incorrectWord = false;
	let invalidWord = false;
	let selectedWord = null;

	function selectWord(word) {
		selectedWord = word;
	}

	async function deleteWord() {
		// Make the call to the server
		const response = await fetch('http://localhost:7890/wordbank/user', {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			},
			body: JSON.stringify({ wordbank_word: selectedWord })
		});

		if (response.status === 401) {
			user.reset();
			newWord = '';
			goto('/login');
		} else if (response.ok) {
			// Delete the selected word from the wordbank
			wordbank.update((words) => words.filter((word) => word !== selectedWord));
			// Close the modal
			selectedWord = null;
		} else {
			console.error('Failed to delete word');
		}
	}

	onMount(async () => {
		if ($user && $user.access_token) {
			const response = await fetch('http://localhost:7890/wordbank/user', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${$user.access_token}`
				}
			});

			if (response.ok) {
				console.log('response', response);
				let parsed_response = await response.json();
				console.log(parsed_response);
				wordbank.set(parsed_response.wordbank);
			} else if (response.status === 401) {
				user.reset();
				goto('/login');
			} else {
				console.error('Failed to fetch word:', response.status, response.statusText);
			}
			isLoading = false;
		} else {
			user.reset();
			goto('/login');
		}
	});

	let newWord = '';

	function isValidWord(word) {
		return /^[a-z]+$/.test(word);
	}

	async function handleAddWord() {
		if (!isValidWord(newWord)) {
			console.error('Invalid word. The word should be a single, lowercase word without spaces.');
			invalidWord = true;
			if (incorrectWord) {
				incorrectWord = false;
			}
			return;
		}

		const response = await fetch('http://localhost:7890/wordbank/user', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			},
			body: JSON.stringify({ wordbank_word: newWord })
		});

		if (response.status === 401) {
			user.reset();
			newWord = '';
			goto('/login');
		} else if (response.ok) {
			if (incorrectWord) {
				incorrectWord = false;
			}
			if (invalidWord) {
				invalidWord = false;
			}
			$wordbank = [...$wordbank, newWord];
			newWord = '';
		} else if (response.status === 409) {
			if (invalidWord) {
				invalidWord = false;
			}
			incorrectWord = true;
			newWord = '';
		} else {
			console.error('Failed to add word');
		}
	}
</script>

<main class="flex flex-col items-center justify-center">
	<div class="upper-decor decor">
		<div class="horizontal-scrolling-items">
			<div class="horizontal-scrolling-items__item">- Wordbank - Wordbank - Wordbank&nbsp</div>
			<div class="horizontal-scrolling-items__item">
				- Wordbank - Wordbank - Wordbank - Wordbank&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wordbank - Wordbank - Wordbank - Wordbank&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wordbank - Wordbank - Wordbank - Wordbank -&nbsp
			</div>
		</div>
	</div>
	<div class="card flex flex-col items-center gap-2 p-10">
		<h2>Wordbank</h2>
		<div class="add-word-container">
			<form></form>
		</div>
		{#if isLoading}
			<p>Loading...</p>
		{:else}
			<div class="add-word-container">
				<p>Add a new word (must be lowercase, and have no spaces)</p>
				<form>
					<input type="text" bind:value={newWord} />
					<button
						class="text-white font-bold py-2 px-4 rounded"
						on:click|preventDefault={handleAddWord}>Add</button
					>
				</form>
				{#if incorrectWord}
					<p>Word already in wordbank</p>
				{/if}
				{#if invalidWord}
					<p>Invalid word</p>
				{/if}
			</div>
			<div class="wordbank-container">
				{#each $wordbank as word}
					<button class="word" on:click={() => selectWord(word)}>{word}</button>
				{/each}
			</div>
		{/if}
	</div>
	{#if selectedWord}
		<div class="modal">
			<div>
				<h2>{selectedWord}</h2>
				<div class="mt-2">
					<p>Meaning:</p>
					<p>
						(TODO, scraping - <a
							style="text-decoration: underline;"
							target="_blank"
							href="https://de.wiktionary.org/wiki/{selectedWord}">this destination</a
						>)
					</p>
				</div>
				<div class="mt-6">
					<p>Do you want to delete this word?</p>
					<button
						class="delete-button text-white font-bold py-2 px-4 rounded mt-3"
						on:click={deleteWord}>Yes, delete it</button
					>
				</div>
				<button
					class="mt-10 text-white font-bold py-2 px-4 rounded"
					on:click={() => (selectedWord = null)}>Close modal</button
				>
			</div>
		</div>
	{/if}
	<div class="lower-decor decor">
		<div class="horizontal-scrolling-items-right">
			<div class="horizontal-scrolling-items__item">
				Wordbank - Wordbank - Wordbank - Wordbank&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wordbank - Wordbank - Wordbank - Wordbank&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wordbank - Wordbank - Wordbank - Wordbank&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wordbank - Wordbank - Wordbank - Wordbank -&nbsp
			</div>
		</div>
	</div>
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
		background-color: rgba(0, 0, 0, 0.6);
		border-radius: 1rem;
		transition: background-color 0.3s ease;
		backdrop-filter: blur(10px);
		max-width: 60%;
		max-height: 80%;
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

	.add-word-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 100%;
		gap: 1rem;
	}

	.add-word-container form {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 100%;
		gap: 1rem;
	}

	.add-word-container input {
		border: 4px solid rgba(255, 255, 255, 0.25);
		color: white;
		background-color: black;
		padding: 5px;
		border-radius: 0.5rem;
	}

	.wordbank-container {
		margin-top: 3rem;
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
		justify-content: center;
		width: 100%;
		gap: 1rem;
		overflow-y: scroll;

		/* Hide scrollbar for Chrome, Safari, and Opera */
		&::-webkit-scrollbar {
			display: none;
		}

		/* Hide scrollbar for IE, Edge, and Firefox */
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}

	.word {
		border: 4px solid rgba(255, 255, 255, 0.25);
		color: white;
		background-color: black;
		padding: 8px;
		border-radius: 0.5rem;
	}
	/* 
    .add-word-container button {
        padding: 1rem;
    } */

	.decor {
		z-index: 0;
		width: 100%;
		overflow-x: hidden;
		font-family: 'OffBitBold', sans-serif;
		opacity: 0.3;
		font-size: 200px;
		user-select: none;
	}

	.horizontal-scrolling-items {
		display: flex;
		width: max-content; /* Adjust to fit the content width */
		animation: infiniteScroll 80s linear infinite; /* Adjust duration as needed */
	}

	.horizontal-scrolling-items-right {
		display: flex;
		width: max-content; /* Adjust to fit the content width */
		animation: infiniteScrollRight 80s linear infinite; /* Adjust duration as needed */
	}

	.horizontal-scrolling-items__item {
		white-space: nowrap;
	}

	.upper-decor {
		position: absolute;
		top: 85px;
	}

	.lower-decor {
		position: absolute;
		bottom: 0;
	}

	@keyframes infiniteScroll {
		from {
			transform: translateX(0);
		}
		to {
			transform: translateX(-50%); /* Move by 50% of the total width for seamless looping */
		}
	}

	@keyframes infiniteScrollRight {
		from {
			transform: translateX(-50%);
		}
		to {
			transform: translateX(0); /* Move by 50% of the total width for seamless looping */
		}
	}

	.modal {
		background: rgba(5, 1, 36, 0.5);
		position: fixed;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		z-index: 1;
	}

	.modal > div {
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
	}

	.delete-button {
		background-color: rgba(255, 0, 0, 0.5);
		transition: all 0.3s ease;
	}

	.delete-button:hover {
		background-color: rgba(255, 0, 0, 0.8);
	}
</style>
