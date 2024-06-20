<script>
	import { user } from '../../../lib/userStore.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	export let data;

	let currentMessage = ''; // Variable to hold the current message
	let chatInstances = [];
	let messages = [];
	let currentPath;

	let selectedMessageIndex = null;
	function selectMessage(index) {
		selectedMessageIndex = index;
	}

	let splitMessage = null;
	function splitAndCleanWord() {
		splitMessage = messages[selectedMessageIndex].message.split(' ').map((word) => {
			return word.replace(/[^\p{L}]/gu, '').toLowerCase();
		});
		console.log(splitMessage);
	}

	$: {
		currentPath = $page.url.pathname;
	}

	// Fetch data on mount
	onMount(async () => {
		if ($user && $user.access_token) {
			// Fetch chat previews for left side
			const response = await fetch('http://localhost:7890/chat/preview', {
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
				let chats = await response.json();
				chatInstances = chats['chat_preview'];
				console.log(chatInstances);
			} else {
				console.error('Failed to fetch chat previews:', response.status, response.statusText);
			}

			// Fetch messages for right side
			const response2 = await fetch(`http://localhost:7890/chat/${data.chatId}`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${$user.access_token}`
				}
			});
			if (response.ok) {
				let chats = await response2.json();
				messages = chats['messages'];
				console.log(messages);
			} else {
				console.error('Failed to fetch chat messages:', response.status, response.statusText);
			}
		}
	});

	// Fetch data whenever the chatId / the route changes
	$: if (data && data.chatId) {
		fetchChatData(data.chatId);
	}

	async function fetchChatData(chatId) {
		const response = await fetch(`http://localhost:7890/chat/${chatId}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			}
		});
		if (response.ok) {
			let chats = await response.json();
			messages = chats['messages'];
			console.log(messages);
		} else {
			console.error('Failed to fetch chat messages:', response.status, response.statusText);
		}
	}

	// Handling the sending of messages - once sent we also want to wait for the response
	async function sendMessage() {
		// Add the message to the messages array
		messages = [...messages, { sender: 'user', message: currentMessage }];
		// Clear the input field
		let messageToSend = currentMessage;
		currentMessage = '';
		// Send the message to the server and get the response
		const response = await fetch(`http://localhost:7890/chat/${data.chatId}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			},
			body: JSON.stringify({ message: messageToSend })
		});
		if (response.ok) {
			let agent_message = await response.json();
			messages = [...messages, agent_message];
			console.log(messages);
		} else {
			console.error('Failed to fetch chat messages:', response.status, response.statusText);
		}
	}

	let successfulAdd = false;
	let incorrectWord = false;
	let selectedWord = null;

	async function handleAddWord() {
		const response = await fetch('http://localhost:7890/wordbank/user', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			},
			body: JSON.stringify({ wordbank_word: selectedWord })
		});

		if (response.status === 401) {
			user.reset();
			goto('/login');
		} else if (response.ok) {
			if (incorrectWord) {
				incorrectWord = false;
			}
			successfulAdd = true;
		} else if (response.status === 409) {
			incorrectWord = true;
		} else {
			console.error('Failed to add word');
		}
	}

	let grammarExplain = null;
	let grammarIsLoading = false;
	async function handleGrammarExplain() {
		grammarIsLoading = true;
		const response = await fetch('http://localhost:7890/chat/grammar', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			},
			body: JSON.stringify({ message: messages[selectedMessageIndex].message })
		});

		if (response.status === 401) {
			user.reset();
			goto('/login');
		} else if (response.ok) {
			let agent_message = await response.json();
			console.log(agent_message);
			grammarExplain = agent_message['explanation'];
			grammarIsLoading = false;
			console.log(grammarExplain);
		} else {
			console.error('Failed to explain grammar');
		}
	}

	let translation = null;
	let translationIsLoading = false;
	async function handleTranslation() {
		translationIsLoading = true;
		const response = await fetch('http://localhost:7890/chat/translate', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			},
			body: JSON.stringify({ message: messages[selectedMessageIndex].message })
		});

		if (response.status === 401) {
			user.reset();
			goto('/login');
		} else if (response.ok) {
			let agent_message = await response.json();
			console.log(agent_message);
			translation = agent_message['translation'];
			translationIsLoading = false;
			console.log(translation);
		} else {
			console.error('Failed to translate message');
		}
	}

	// Function to navigate to the chat (this is to circumvent the issue with the anchor tag)
	function navigateToChat(chat_id) {
		goto(`/chat/${chat_id}`);
	}
</script>

{#if $user && $user.access_token}
	<main>
		<div class="chat-container">
			<div class="prev-chats">
				<button class="new-chat text-white font-bold" on:click={() => goto('/chat')}
					>Start new chat</button
				>
				<!-- <div class="prev-title-container">
					<p>Previous chats:</p>
				</div> -->
				<!-- <div class="prev-instance-divider"></div> -->
				{#each chatInstances as instance (instance.chat_id)}
					<div
						class="prev-instance-container"
						class:active={currentPath === `/chat/${instance.chat_id}`}
						on:click={() => navigateToChat(instance.chat_id)}
						on:keydown={(e) => {
							if (e.key === 'Enter') navigateToChat(instance.chat_id);
						}}
						tabindex="0"
						role="button"
					>
						<div>
							<a href="/chat/{instance.chat_id}">{instance.agent_setting}</a>
						</div>
					</div>
					<!-- <div class="prev-instance-divider"></div> -->
				{/each}
			</div>

			<div class="right-container">
				<div class="chat-messages">
					{#each messages as message, index}
						{#if message.sender == 'user'}
							<div
								class="text text-user"
								on:click={() => selectMessage(index)}
								on:keydown={(e) => {
									if (e.key === 'Enter') selectMessage(index);
								}}
								tabindex="0"
								role="button"
							>
								{index}: {message.message}
							</div>
						{:else}
							<div
								class="text text-agent"
								on:click={() => selectMessage(index)}
								on:keydown={(e) => {
									if (e.key === 'Enter') selectMessage(index);
								}}
								tabindex="0"
								role="button"
							>
								{index}: {message.message}
							</div>
						{/if}
					{/each}
				</div>
				<div class="chat-input">
					<textarea bind:value={currentMessage} placeholder="Type a message..."></textarea>
					<button class="send-button text-white font-bold py-2 px-4 rounded" on:click={sendMessage}
						>Send</button
					>
				</div>
			</div>
		</div>
		{#if selectedMessageIndex !== null}
			<div class="modal">
				<div>
					<h2>Message explainer</h2>
					<div class="sentence-container mt-2">
						{#if splitMessage}
							<p>Words of the message:</p>
							<div class="words-container">
								{#each splitMessage as word}
									<button class="word" on:click={() => (selectedWord = word)}>{word}</button>
								{/each}
							</div>
						{:else}
							<p>Message:</p>
							<div class="word mt-3">{messages[selectedMessageIndex].message}</div>
						{/if}
					</div>
					{#if selectedWord}
						<p class="selected-word mt-6">{selectedWord}</p>
						{#if incorrectWord}
							<div class="mt-2">
								<p>This word is already in the Wordbank</p>
								<div class="flex flex-row gap-5 justify-center">
									<button
										class="text-white font-bold py-2 px-4 rounded mt-3"
										on:click|preventDefault={() => ((selectedWord = null), (incorrectWord = false))}
										>Return</button
									>
								</div>
							</div>
						{:else if successfulAdd}
							<div class="mt-2">
								<p>Word sucessfully added</p>
								<div class="flex flex-row gap-5 justify-center">
									<button
										class="text-white font-bold py-2 px-4 rounded mt-3"
										on:click|preventDefault={() => ((selectedWord = null), (successfulAdd = false))}
										>Return</button
									>
								</div>
							</div>
						{:else}
							<div class="mt-2">
								<p>Are you sure you want to add this word?</p>
								<div class="flex flex-row gap-5 justify-center">
									<button
										class="text-white font-bold py-2 px-4 rounded mt-3"
										on:click|preventDefault={handleAddWord}>Yes, add word</button
									>
									<button
										class="text-white font-bold py-2 px-4 rounded mt-3"
										on:click|preventDefault={() => (selectedWord = null)}>No, return</button
									>
								</div>
							</div>
						{/if}
					{:else}
						<p class="mt-8">
							Here you can translate, explain using Ai or even split words to Wordbank
						</p>
						<div class="flex flex-row justify-center gap-8 mt-1">
							{#if !grammarExplain}
								<button
									class="text-white font-bold py-2 px-4 rounded mt-3"
									on:click={handleGrammarExplain}>Explain</button
								>
							{/if}
							{#if !translation}
								<button class="text-white font-bold py-2 px-4 rounded mt-3" on:click={handleTranslation}>Translate</button>
							{/if}
							{#if splitMessage}
								<button
									class="text-white font-bold py-2 px-4 rounded mt-3"
									on:click={() => (splitMessage = null)}>Reverse split</button
								>
							{:else}
								<button
									class="text-white font-bold py-2 px-4 rounded mt-3"
									on:click={splitAndCleanWord}>Add to wordbank</button
								>
							{/if}
						</div>
						{#if grammarExplain || grammarIsLoading}
							{#if grammarIsLoading}
								<p class="mt-6">Explanation loading...</p>
							{:else}
								<div class="mt-6 text-center flex flex-col justify-center items-center">
									<p>Explanation:</p>
									<div class="mt-2 word">{grammarExplain}</div>
								</div>
							{/if}
						{/if}
						{#if translation || translationIsLoading}
							{#if translationIsLoading}
								<p class="mt-6">Translation loading...</p>
							{:else}
								<div class="mt-6 text-center flex flex-col justify-center items-center">
									<p>Translation:</p>
									<div class="mt-2 word text-center">{translation}</div>
								</div>
							{/if}
						{/if}
					{/if}
					<button
						class="mt-10 text-white font-bold py-2 px-4 rounded"
						on:click={() => (
							(selectedMessageIndex = null),
							(splitMessage = null),
							(selectedWord = null),
							(incorrectWord = false),
							(grammarExplain = null),
							(translation = null)
						)}>Close modal</button
					>
				</div>
			</div>
		{/if}
	</main>
{:else}
	<p>You are not signed in.</p>
	<button class="text-white font-bold" on:click={() => goto('/login')}>Go to Login</button>
{/if}

<style>
	.words-container {
		margin-top: 1rem;
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
		justify-content: center;
		width: 100%;
		gap: 1rem;
		overflow-y: scroll;
	}

	.sentence-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		max-width: 80%;
	}

	.word {
		border: 4px solid rgba(255, 255, 255, 0.25);
		color: white;
		background-color: black;
		padding: 8px;
		border-radius: 0.5rem;
		width: fit-content;
	}

	h2 {
		font-family: 'OffBitBold', sans-serif;
		font-size: 4rem;
	}

	.selected-word {
		font-family: 'OffBitBold', sans-serif;
		font-size: 2rem;
	}

	.modal {
		background: rgba(5, 1, 36, 0.5);
		position: fixed;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		z-index: 1;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.modal > div {
		min-width: 55%;
		max-width: 55%;
		max-height: 80%;
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
		overflow-y: scroll;
	}

	main {
		height: calc(100vh - 85px);
		font-family: 'GeistMedium', sans-serif;
	}

	.chat-container {
		display: flex;
		height: calc(100vh - 85px);
		min-height: 100%;
		width: 100%;
	}

	/* Left side */
	.prev-chats {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 20%;
		height: 100%;
		overflow-y: auto;
		border-right: 4px solid rgba(255, 255, 255, 0.25);
	}

	.new-chat {
		width: 100%;
		height: 100px;
		font-family: 'OffBitBold', sans-serif;
		font-size: x-large;
	}

	.send-button {
		font-family: 'OffBitBold', sans-serif;
		font-size: x-large;
	}

	/* .prev-title-container {
		display: flex;
		align-items: center;
		height: 100px;
		min-height: 0;
		flex-shrink: 0; 
	}

	.prev-instance-divider {
		height: 5px;
		width: 100%;
		background-color: black;
		min-height: 0;
		flex-shrink: 0; 
	} */

	.prev-instance-container {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100px;
		min-height: 0; /* Add this line */
		flex-shrink: 0; /* Add this line */
		border-bottom: 4px solid rgba(255, 255, 255, 0.25);
		transition:
			background-color 0.3s ease,
			border-bottom-color 0.3s ease,
			color 0.3s ease;
	}

	.prev-instance-container:hover {
		border-bottom: 4px solid rgba(255, 255, 255, 0.5);
		background-color: rgba(31, 31, 221, 0.8);
	}

	.prev-instance-container div {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		width: 250px; /* Adjust as needed */
		text-align: center;
	}

	/* Right side */
	.right-container {
		display: flex;
		flex-direction: column;
		width: 80%;
		/* height: 100%; */
		flex-grow: 1; /* Ensure it takes available space */
		/* background-color: lightblue; */
	}

	.chat-messages {
		width: 100%;
		height: calc(100vh - 85px - 120px);
		flex-grow: 1; /* Allow it to grow and take available space */
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		align-items: center;
	}

	.text {
		width: 45%;
		padding: 20px;
		margin: 15px 30px 15px 30px;
		border: 4px solid rgba(255, 255, 255, 0.25);
		transition: all 0.3s ease;
	}

	.text:hover {
		background-color: rgba(31, 31, 221, 0.8);
	}

	.text-user {
		align-self: self-end;
		border-radius: 1rem 0rem 0rem 1rem;
		text-align: end;
	}

	.text-agent {
		align-self: self-start;
		border-radius: 0rem 1rem 1rem 0rem;
	}

	.chat-input {
		height: 120px;
		position: fixed;
		bottom: 0;
		width: 100%;
		/* background-color: lightcoral; */
		display: flex;
		/* padding: 25px; */
		background-color: black;
	}

	.chat-input button {
		width: 10vw;
	}

	textarea {
		width: calc(100vw - 20vw - 10vw);
		overflow-y: auto; /* Make the textarea scrollable */
		resize: none; /* Remove the resizing feature */
		background-color: black;
		border-top: 4px solid rgba(255, 255, 255, 0.25);
		color: white;
		padding: 8px;
		padding-left: 12px;
	}

	button {
		background-color: rgba(255, 166, 0, 0.5);
		transition: all 0.3s ease;
	}

	button:hover {
		background-color: rgba(255, 166, 0, 0.8);
	}

	/* button {
		background-color: rgba(255, 166, 0, 0.5);
		transition: all 0.3s ease;
		font-family: 'OffBitBold', sans-serif;
		font-size: x-large;
	}

	button:hover {
		background-color: rgba(255, 166, 0, 0.8);
	} */

	.active {
		background-color: rgba(31, 31, 221, 0.8);
	}
</style>
