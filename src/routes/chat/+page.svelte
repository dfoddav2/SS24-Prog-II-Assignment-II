<script>
	// import { onMount } from 'svelte';
	import { user } from '../../lib/userStore.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let messages = []; // Array to hold the messages
	// let chatInstances = [
	// 	{ id: 1, title: 'A german police officer...' },
	// 	{ id: 2, title: 'A cashier at Lidl. Going through a checkout...' }
	// ]; // Array to hold the chat instances
	let currentMessage = ''; // Variable to hold the current message
	let chatInstances = [];

	async function handleNewChat() {
		if (currentMessage) {
			const response = await fetch('http://localhost:7890/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${$user.access_token}`
				},
				body: JSON.stringify({ agent_setting: currentMessage })
			});
			if (response.ok) {
				const data = await response.json();
				goto(`/chat/${data.chat_id}`);
			} else {
				console.error('Failed to start chat:', response.status, response.statusText);
			}
		}
	}

	onMount(async () => {
		// let solution = 'xxxxx';
		if ($user && $user.access_token) {
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
				let data = await response.json();
				chatInstances = data['chat_preview'];
				console.log(chatInstances);
			} else {
				console.error('Failed to fetch chat previews:', response.status, response.statusText);
			}
		}
	});

	// Function to navigate to the chat (this is to circumvent the issue with the anchor tag)
	function navigateToChat(chat_id) {
		goto(`/chat/${chat_id}`);
	}
</script>

{#if $user && $user.access_token}
	<main>
		<div class="chat-container">
			<div class="prev-chats">
				<button
					id="button-active"
					class="new-chat bg-blue-400 hover:bg-blue-500 text-white font-bold"
					on:click={() => goto('/chat')}>Start new chat</button
				>
				<!-- <div class="prev-title-container">
					<p>Previous chats:</p>
				</div> -->
				<!-- <div class="prev-instance-divider"></div> -->
				{#each chatInstances as instance (instance.chat_id)}
					<div
						class="prev-instance-container"
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
					<h2>Start a new chat here</h2>
					<p class="text-center">Or choose from a previous one on the left side</p>
					<p class="text-center">
						You can start a new chat by describing the scenario in the textarea and then pressing
						start
					</p>
					<p class="text-center">
						Example description: "You are a swimmer who has just won the gold medal. I am
						interviewing you."
					</p>
					<p>(For now you must initiate the conversaation)</p>
					<!-- {#each messages as message (message.id)}
						<div>{message.text}</div>
					{/each} -->
				</div>
				<div class="chat-input">
					<textarea bind:value={currentMessage} placeholder="Type a message..."></textarea>
					<button
						class="bg-blue-400 hover:bg-blue-500 text-white font-bold"
						on:click={handleNewChat}>Start</button
					>
				</div>
			</div>
		</div>
	</main>
{:else}
	<p>You are not signed in.</p>
	<button class="bg-blue-400 hover:bg-blue-500 text-white font-bold" on:click={() => goto('/login')}
		>Go to Login</button
	>
{/if}

<style>
	/* Setting up view */
	/* @font-face {
		font-family: 'OffBitBold';
		src: url('OffBitBold.otf') format('opentype');
		font-weight: normal;
		font-style: normal;
	}

	@font-face {
		font-family: 'GeistMedium';
		src: url('Geist-Medium.ttf') format('truetype');
		font-weight: normal;
		font-style: normal;
	} */

	main {
		height: calc(100vh - 85px);
		font-family: 'GeistMedium', sans-serif;
	}

	h2 {
		font-family: 'OffBitBold', sans-serif;
		font-size: xx-large;
	}

	p {
		font-size: large;
	}

	p:last-of-type {
		margin-bottom: 20px;
	}

	.chat-container {
		display: flex;
		height: 100%;
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
		/* background-color: cadetblue; */
		border-right: 4px solid rgba(255, 255, 255, 0.25);
	}

	.new-chat {
		width: 100%;
		height: 100px;
	}

	/* .prev-title-container {
		display: flex;
		align-items: center;
		height: 100px;
		min-height: 0;
		flex-shrink: 0; 
		border-bottom: 3px solid black;
	} */

	/* .prev-instance-divider {
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
		height: 100%;
		/* background-color: lightblue; */
	}

	.chat-messages {
		width: 100%;
		height: calc(100vh - 85px - 120px);
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		align-items: center;
	}

	.chat-input {
		height: 120px;
		position: fixed;
		bottom: 0;
		width: 100%;
		/* background-color: lightcoral; */
		display: flex;
		/* padding: 25px; */
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
		/* background-color: rgba(255, 166, 0, 0.8); */
		background-color: rgba(255, 166, 0, 0.5);
		transition: all 0.3s ease;
		font-family: 'OffBitBold', sans-serif;
		font-size: x-large;
	}

	button:hover {
		background-color: rgba(255, 166, 0, 0.8);
	}

	#button-active {
		background-color: rgba(255, 166, 0, 0.8);
	}
</style>
