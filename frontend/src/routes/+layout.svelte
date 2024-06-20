<script>
	import '../app.css';
	import { user } from '../lib/userStore.js';
	import { goto } from '$app/navigation';

	function onLogout() {
		user.reset();
		goto('/login');
	}
</script>

<div class="wrapper text-gray-100 min-h-screen">
	<header class="text-white px-6">
		<nav>
			<h1 class="font-bold"><a href="/" class="hover:underline">Assignment 2</a></h1>
			<ul class="flex space-x-6">
				{#if $user && $user.access_token}
					<li><a href="/user" class="hover:underline">Profile</a></li>
					<li><a href="/chat" class="hover:underline">Chat</a></li>
					<li><a href="/play" class="hover:underline">Play</a></li>
					<li><a href="/wordbank" class="hover:underline">Wordbank</a></li>
					<li><a href="/" on:click|preventDefault={onLogout} class="hover:underline">Logout</a></li>
				{:else}
					<li><a href="/login" class="hover:underline">Login</a></li>
				{/if}
				<li><a href="/about" class="hover:underline">About</a></li>
			</ul>
		</nav>
	</header>
	<slot />
</div>

<style>
	.wrapper {
		background-color: black;
	}

	header {
		display: flex;
		align-items: center;
		height: 85px;
		border-bottom: 3px solid rgba(255, 255, 255, 0.25);
		font-size: large;
		color: rgba(221, 255, 244, 0.5);
		transition: background-color 0.3s ease, border-bottom-color 0.3s ease, color 0.3s ease;
	}

	header:hover {
		background-color: rgba(31, 31, 221, 0.8);
		border-bottom-color: rgba(255, 255, 255, 1);
		color: rgba(221, 255, 244, 1);
	}

	nav {
		width: 100%;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	ul {
		justify-content: end;
	}

	@font-face {
		font-family: 'OffBitBold';
		src: url('OffBitBold.otf') format('opentype');
		font-weight: normal;
		font-style: normal;
	}

	h1 {
		font-family: 'OffBitBold',  sans-serif;
		font-size: xx-large;
	}

	li {
		font-family: 'OffBitBold',  sans-serif;
		font-size: 25px;
	}
</style>