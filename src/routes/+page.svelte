<script>
	// Script here
</script>

<main class="flex items-center justify-center">
	<div class="upper-decor decor">
		<div class="horizontal-scrolling-items">
			<div class="horizontal-scrolling-items__item">
				Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2 -&nbsp
			</div>
		</div>
	</div>
	<div class="card max-w-3xl mx-auto p-12">
		<h1 class="text-4xl font-bold mb-4">Language Learning App</h1>
		<p class="text-center">Improve your conversation skills with AI simulation</p>
		<p class="mb-8 text-center">+ a Wordle style networking game</p>
		<div class="flex justify-center">
			<a href="/login" alt="To the login page">
				<button class="text-white font-bold py-2 px-4 rounded"> Get Started </button>
			</a>
		</div>
	</div>
	<div class="lower-decor decor">
		<div class="horizontal-scrolling-items-right">
			<div class="horizontal-scrolling-items__item">
				Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2&nbsp
			</div>
			<div class="horizontal-scrolling-items__item">
				- Assignment 2 - Assignment 2 - Assignment 2 - Assignment 2 -&nbsp
			</div>
		</div>
	</div>
</main>

<style>
	/* Add your custom styles here */
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

	.card {
		/* transition: all 0.5s ease-in-out; */
		z-index: 1;
		border: 4px solid rgba(255, 255, 255, 0.25);
		border-radius: 1rem;
		transition: background-color 0.3s ease;
		backdrop-filter: blur(10px); /* Apply the blur effect */
	}

	.card:hover {
		background-color: rgba(31, 31, 221, 0.6);
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
</style>
