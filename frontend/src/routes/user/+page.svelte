<script>
	// import { onMount } from 'svelte';
	import { user } from '../../lib/userStore.js';
	import { goto } from '$app/navigation';

	let profile = null;

	let newName = '';
	async function handleUpdateName() {
		const response = await fetch('http://localhost:7890/user', {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${$user.access_token}`
			},
			body: JSON.stringify({ name: newName })
		});

		if (response.status === 401) {
			user.reset();
			newName = '';
			goto('/login');
		} else if (response.ok) {
			$user.name = newName;
		} else {
			console.error('Failed to update name');
		}
	}
	async function deleteProfile() {
		const response = await fetch('http://localhost:7890/user', {
			method: 'DELETE',
			headers: {
				Authorization: `Bearer ${$user.access_token}`
			}
		});

		if (response.status === 401) {
			user.reset();
			goto('/login');
		} else if (response.ok) {
			user.reset();
			goto('/login');
		} else {
			console.error('Failed to delete profile');
		}
	}
</script>

<div class="container">
	{#if $user && $user.access_token}
		<div class="upper-decor decor">
			<div class="horizontal-scrolling-items">
				<div class="horizontal-scrolling-items__item">
					Welcome - Welcome - Welcome - Welcome&nbsp
				</div>
				<div class="horizontal-scrolling-items__item">
					- Welcome - Welcome - Welcome - Welcome&nbsp
				</div>
				<div class="horizontal-scrolling-items__item">
					- Welcome - Welcome - Welcome - Welcome&nbsp
				</div>
				<div class="horizontal-scrolling-items__item">
					- Welcome - Welcome - Welcome - Welcome -&nbsp
				</div>
			</div>
		</div>
		<!-- {#if profile} -->
		<div class="card max-w-3xl mx-auto p-12">
			<h1 class="text-4xl">Welcome, {$user.name}</h1>
			<p class="text-xl">(Email: {$user.email})</p>
			<!-- ... display other user information ... -->
			<!-- {:else}
			<p>Loading...</p>
		{/if} -->
			<div class="mt-9">
				<p>You may change your name here:</p>
				<form on:submit|preventDefault={handleUpdateName} class="edit_form mt-4">
					<label for="newName">New Name:</label>
					<input id="newName" bind:value={newName} required class="text-black mt-2" />
					<button
						type="submit"
						class="text-white font-bold py-2 px-4 rounded mt-3"
						>Update Name</button
					>
				</form>
				<p class="mt-4">Or you can even delete your profile by clicking here:</p>
				<button
					on:click={deleteProfile}
					class="danger text-white font-bold py-2 px-4 rounded mt-3"
					>Delete user</button
				>
			</div>
		</div>

		<div class="lower-decor decor">
			<div class="horizontal-scrolling-items-right">
				<div class="horizontal-scrolling-items__item">
					{$user.name} - {$user.name} - {$user.name} - {$user.name}&nbsp
				</div>
				<div class="horizontal-scrolling-items__item">
					- {$user.name} - {$user.name} - {$user.name} - {$user.name}&nbsp
				</div>
				<div class="horizontal-scrolling-items__item">
					- {$user.name} - {$user.name} - {$user.name} - {$user.name}&nbsp
				</div>
				<div class="horizontal-scrolling-items__item">
					- {$user.name} - {$user.name} - {$user.name} - {$user.name} -&nbsp
				</div>
			</div>
		</div>
	{:else}
		<p>You are not signed in.</p>
		<button on:click={() => goto('/login')}>Go to Login</button>
	{/if}
</div>

<style>
	.card {
		/* transition: all 0.5s ease-in-out; */
		border: 4px solid rgba(255, 255, 255, 0.25);
		border-radius: 1rem;
		transition: background-color 0.3s ease;
		z-index: 1;
		/* background-color: rgba(0, 0, 0, 0.075); */
		backdrop-filter: blur(10px); /* Apply the blur effect */
	}

	.card:hover {
		background-color: rgba(31, 31, 221, 0.6);
	}

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

	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		height: calc(100vh - 85px);
		width: 100vw !important;
		max-width: 100vw !important;
		font-family: 'GeistMedium', sans-serif;
	}
	.edit_form {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		max-width: 100%;
	}

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

	button {
		background-color: rgba(255, 166, 0, 0.5);
		transition: all 0.3s ease;
	}

	button:hover {
		background-color: rgba(255, 166, 0, 0.8);
	}

	.danger {
		background-color: rgba(255, 0, 0, 0.5);
		transition: all 0.3s ease;
	}

	.danger:hover {
		background-color: rgba(255, 0, 0, 0.8);
	}

	input {
		border: 4px solid rgba(255, 255, 255, 0.25);
		color: white;
		background-color: black;
		padding: 5px;
		border-radius: 0.5rem;
	}
</style>
