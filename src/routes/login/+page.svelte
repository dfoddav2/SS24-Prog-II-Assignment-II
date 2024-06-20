<script>
	import { user } from '../../lib/userStore.js';
	import { fade } from 'svelte/transition';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let name = '';
	let isRegistering = false;
	let errorMessage = '';

	function toggleRegistering() {
		isRegistering = !isRegistering;
	}

	async function handleSubmit() {
		if (isRegistering) {
			// register();
			const response = await fetch('http://localhost:7890/user/register', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password, name })
			});

			if (response.ok) {
				const { access_token, email, password, name } = await response.json();
				user.set({ email, access_token, password, name });
				goto('/user');
			} else {
				// handle error
				errorMessage = 'Email already in use';
			}
		} else {
			// login();
			const response = await fetch('http://localhost:7890/user/login', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			if (response.ok) {
				const { access_token, email, password, name } = await response.json();
				user.set({ email, access_token, password, name });
				goto('/user');
			} else {
				// handle error
				errorMessage = 'Invalid email or password';
			}
		}
	}

	function onLogout() {
		user.reset();
	}
</script>

<main class="flex flex-col items-center justify-center">
	{#if $user && $user.access_token}
		<div class="mx-auto p-8 rounded-lg login_card px-12">
			<h1 class="text-3xl font-bold mb-4">You are already logged in</h1>
			<p class="mb-4">
				You can <a href="/user" class="text-blue-500 hover:underline">view your profile</a> or
			</p>
			<button
				type="submit"
				class="mb-3 mt-4 bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded"
				on:click={onLogout}
			>
				Log out
			</button>
		</div>
	{:else}
		<div class="max-w-md mx-auto p-8 login_card">
			<h1 class="login-title text-3xl font-bold mb-6">{isRegistering ? 'Register' : 'Log in'}</h1>
			<form on:submit|preventDefault={handleSubmit}>
				<div class="mb-4">
					<label for="email" class="block mb-2">Email</label>
					<input
						id="email"
						type="email"
						bind:value={email}
						class="w-full px-3 py-2 border rounded text-black"
						required
					/>
				</div>
				<div class="mb-4">
					<label for="password" class="block mb-2">Password</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						class="w-full px-3 py-2 border rounded text-black"
						required
					/>
				</div>
				{#if isRegistering}
					<div class="mb-6" in:fade={{ duration: 400 }} out:fade={{ duration: 200 }}>
						<label for="name" class="block mb-2">Name</label>
						<input
							id="name"
							type="text"
							bind:value={name}
							class="w-full px-3 py-2 border rounded text-black"
							required
						/>
					</div>
				{:else}
					<input type="hidden" id="name" bind:value={name} />
				{/if}
				<div class="flex justify-center">
					<button
						type="submit"
						class="mt-4 mb-1 bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded"
					>
						{isRegistering ? 'Register' : 'Log in'}
					</button>
				</div>
			</form>
			{#if errorMessage}
				<div class="mt-4">
					<p class="text-red-300">{errorMessage}</p>
				</div>
			{/if}
		</div>
		<p class="mt-4">
			{isRegistering ? 'Already registered?' : 'No account yet?'}
			<a href="/" on:click|preventDefault={toggleRegistering} class="text-blue-500 hover:underline">
				{isRegistering ? 'Log in here' : 'Register here'}
			</a>
		</p>
	{/if}
</main>

<style>
	/* @font-face {
		font-family: 'GeistMedium';
		src: url('Geist-Medium.ttf') format('truetype');
		font-weight: normal;
		font-style: normal;
	}

	@font-face {
		font-family: 'GeistBlack';
		src: url('Geist-Black.ttf') format('truetype');
		font-weight: normal;
		font-style: normal;
	} */

	main {
		height: calc(100vh - 85px);
		font-family: 'GeistMedium', sans-serif;
	}

	.login_card {
		transition: all 0.5s ease-in-out;
		/* max-height: calc(100vh - 85px); */
		border: 4px solid rgba(255, 255, 255, 0.25);
		border-radius: 1rem;
		text-align: center;
		transition: background-color 0.3s ease;
	}

	.login_card:hover {
		background-color: rgba(31, 31, 221, 0.6);

	}

	.login-title {
		font-family: 'GeistBlack', sans-serif;
	}
	
	button {
		background-color: rgba(255, 166, 0, 0.5);
		transition: all 0.3s ease;
	}

	button:hover {
		background-color: rgba(255, 166, 0, 0.8);
	}
</style>
