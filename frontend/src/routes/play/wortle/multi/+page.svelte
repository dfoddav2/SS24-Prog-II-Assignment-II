<script>
	import { user } from '../../../../lib/userStore.js';
	import { goto } from '$app/navigation';
	import { onMount, onDestroy } from 'svelte';
	import { writable } from 'svelte/store';
	import io from 'socket.io-client';
	import Wortle from '../WortleMulti.svelte';

	let socket;
	let onlineUsers = [];
	let invitations = [];
	let inviteSent = '';
	let disconnect = '';
	let gameState = writable({});

	onMount(() => {
		// Check if JWT is fresh
		async function checkJWT() {
			const response = await fetch('http://localhost:7890/user', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${$user.access_token}`
				}
			});

			if (response.status === 401) {
				user.reset();
				goto('/login');
			}
		}
		checkJWT();

		// Connect to socket
		socket = io('http://localhost:7890');

		// Connect to the multiplayer lobby
		socket.emit('authentication', $user.email);

		// Get the list of online users on every change
		socket.on('users_list', function (users_list) {
			onlineUsers = users_list;
		});

		// Listen for invites
		socket.on('invite', function (inviter) {
			invitations = [...invitations, { inviter: inviter.email, sid: inviter.id }];
			// alert(`You have been invited to play by ${inviter.email} with sid ${inviter.id}`);
		});

		// Listen for declined invite
		socket.on('decline_invite', function () {
			console.log('Invite declined');
			inviteSent = '';
		});

		// Listen for game state changes
		socket.on('game_state', function (newGameState) {
			console.log('New game state received from server:', newGameState);
			gameState.set(newGameState);
		});

		// Listen for opponent disconnect
		socket.on('opponent_disconnect', function (opponent) {
			console.log('Opponent disconnected:', opponent);
			disconnect = opponent;
		});
	});

	function inviteUser(sid, email) {
		socket.emit('invite', sid);
		inviteSent = email;
	}

	function acceptInvite(sid) {
		socket.emit('accept_invite', sid);
		onlineUsers = [];
		invitations = [];
		inviteSent = '';
	}

	function declineInvite(sid) {
		socket.emit('decline_invite', sid);
		invitations = invitations.filter((invite) => invite.sid !== sid);
	}

	// Subscribe to game state
	// gameState.subscribe((newState) => {
	// 	console.log('New game state:', newState);
	// });

	onDestroy(() => {
		if (socket) {
			socket.off('users_list');
			socket.off('invite');
			socket.disconnect();
		}
	});
	// $: console.log(onlineUsers);
</script>

<main class="flex flex-col items-center justify-center">
	<div class="card">
		<h2>Multiplayer Wortle Game</h2>
		{#if $user && $user.access_token}
			{#if Object.keys($gameState).length !== 0}
				<!-- <div>Game started</div> -->
				{#key $gameState}
					<Wortle gameState={$gameState} {socket} />
				{/key}
			{:else}
				{#if disconnect}
					<!-- TODO: Make this a modal later -->
					<p>Opponent {disconnect} disconnected from the server</p>
				{/if}
				<h3>Let's play, {$user.name}</h3>
				<p class="text-center">
					You will find the joined users list below, just click their name to send them an invite.
					If accepted, the game will start.
				</p>
				<div>
					{#if inviteSent}
						<p class="mt-6">Invitation sent to {inviteSent}, waiting for response</p>
					{:else}
						<h3>Online users:</h3>
						<ul>
							{#each Object.entries(onlineUsers) as [sid, email] (sid)}
								{#if email !== $user.email}
									<li>
										<button
											class="text-white font-bold py-2 px-4 rounded"
											on:click={() => inviteUser(sid, email)}>{email}</button
										>
									</li>
								{/if}
							{/each}
						</ul>
					{/if}
					{#each invitations as { inviter, sid } (sid)}
						<div>
							<!-- <p>Invitation received!</p> -->
							<h3>Invited by {inviter}</h3>
							<button class="text-white font-bold py-2 px-4 mx-4 rounded" on:click={acceptInvite(sid)}
								>Accept</button
							>
							<button class="text-white font-bold py-2 px-4 rounded" on:click={declineInvite(sid)}
								>Decline</button
							>
						</div>
					{/each}
				</div>
			{/if}
		{:else}
			<p>You are not signed in. You need to sign in to play this game.</p>
			<button on:click={() => goto('/login')}>Go to Login</button>
		{/if}
	</div>
</main>

<style>
	main {
		height: calc(100vh - 85px);
		font-family: 'GeistMedium', sans-serif;
	}

	h2 {
		font-family: 'OffBitBold', sans-serif;
		font-size: 3.5rem;
		/* margin-bottom: 1rem; */
	}

	h3 {
		font-family: 'OffBitBold', sans-serif;
		font-size: 2rem;
		/* margin-bottom: 1rem; */
		margin-top: 1rem;
	}

	.card {
		/* transition: all 0.5s ease-in-out; */
		z-index: 1;
		border: 4px solid rgba(255, 255, 255, 0.25);
		border-radius: 1rem;
		transition: background-color 0.3s ease;
		/* backdrop-filter: blur(10px); */
		padding: 3rem;
		max-width: 85%;
		text-align: center;
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
