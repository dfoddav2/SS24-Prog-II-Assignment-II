<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { user } from '/src/lib/userStore.js';

	let leaderboard = [];
	let isLoading = true;

	onMount(async () => {
		const response = await fetch('http://localhost:7890/play/wortle/leaderboard');

		if (response.ok) {
			leaderboard = await response.json();
		} else {
			// handle error
		}

		isLoading = false;
	});
</script>

<main class="flex flex-col items-center justify-center">
	<div class="upper-decor decor">
		<div class="horizontal-scrolling-items">
			<div class="horizontal-scrolling-items__item">
				Wortle - Wortle - Wortle - Wortle&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wortle - Wortle - Wortle - Wortle&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wortle - Wortle - Wortle - Wortle&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wortle - Wortle - Wortle - Wortle -&nbsp
			</div>
		</div>
	</div>
	<div class="card">
		<div class="flex flex-col items-center justify-center gap-5">
			<h2>Wortle</h2>
			<div class="flex gap-5">
				<button
					class="text-white font-bold py-3 px-5 rounded"
					on:click={() => goto('/play/wortle/single')}>Singleplayer</button
				>
				<button
					class="text-white font-bold py-3 px-5 rounded"
					on:click={() => goto('/play/wortle/multi')}>Multiplayer</button
				>
			</div>
		</div>
		<div class="flex flex-col items-center mt-10 gap-5">
			<h2 class="hall">Hall of fame</h2>
			{#if isLoading}
				<p>Loading...</p>
			{:else}
				<table class="w-full text-left border-collapse">
					<thead>
						<tr>
							<th
								class="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light"
								>Email</th
							>
							<th
								class="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light"
								>Singleplayer Score</th
							>
							<th
								class="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light"
								>Multiplayer Score</th
							>
						</tr>
					</thead>
					<tbody>
						{#if $user && $user.email}
							{#each leaderboard as { email, singleplayer_score, multiplayer_score }, i}
								{#if $user.email == email}
									<tr key={i} class="own-score">
										<td class="py-4 px-6 border-b border-grey-light">{email}</td>
										<td class="py-4 px-6 border-b border-grey-light">{singleplayer_score}</td>
										<td class="py-4 px-6 border-b border-grey-light">{multiplayer_score}</td>
									</tr>
								{:else}
									<tr key={i}>
										<td class="py-4 px-6 border-b border-grey-light">{email}</td>
										<td class="py-4 px-6 border-b border-grey-light">{singleplayer_score}</td>
										<td class="py-4 px-6 border-b border-grey-light">{multiplayer_score}</td>
									</tr>
								{/if}
							{/each}
						{:else}
							{#each leaderboard as { email, singleplayer_score, multiplayer_score }, i}
								<tr key={i}>
									<td class="py-4 px-6 border-b border-grey-light">{email}</td>
									<td class="py-4 px-6 border-b border-grey-light">{singleplayer_score}</td>
									<td class="py-4 px-6 border-b border-grey-light">{multiplayer_score}</td>
								</tr>
							{/each}
						{/if}
					</tbody>
				</table>
			{/if}
		</div>
	</div>
	<div class="lower-decor decor">
		<div class="horizontal-scrolling-items-right">
			<div class="horizontal-scrolling-items__item">
				Wortle - Wortle - Wortle - Wortle&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wortle - Wortle - Wortle - Wortle&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wortle - Wortle - Wortle - Wortle&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Wortle - Wortle - Wortle - Wortle -&nbsp
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

	.hall {
		font-size: 3rem;
	}

	.card {
		/* transition: all 0.5s ease-in-out; */
		max-height: 90%;
		padding: 50px;
		z-index: 1;
		border: 4px solid rgba(255, 255, 255, 0.25);
		border-radius: 1rem;
		transition: background-color 0.3s ease;
		backdrop-filter: blur(10px); /* Apply the blur effect */
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

	.own-score {
		background-color: rgba(255, 166, 0, 0.5);
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
</style>
