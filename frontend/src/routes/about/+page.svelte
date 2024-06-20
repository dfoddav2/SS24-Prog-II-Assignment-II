<script>
	import FaGithub from 'virtual:icons/fa6-brands/github';
	import FaLinkedin from 'virtual:icons/fa6-brands/linkedin';

	const links = [
		{ name: 'GitHub', icon: FaGithub, url: 'https://github.com/your-username' },
		{ name: 'LinkedIn', icon: FaLinkedin, url: 'https://linkedin.com/in/your-username' }
		// { name: 'Email', icon: 'mail', url: 'mailto:your-email@example.com' }
	];
</script>

<main class="flex flex-col items-center justify-center h-screen gap-y-2.5">
	<h1 class="!text-3xl text-center mb-3">This is a project for Assignment II. of the SS2024 course of Programming II.</h1>
	<p class="mt-3">Tokens don't grow on trees, so please go easy on the calls made to ChatGPT.</p>
	<h2 class="font-bold mb-4 pt-6 love">Made with ❤️ by David Fodor</h2>
	<ul class="flex space-x-4">
		{#each links as link}
			<li>
				<a
					href={link.url}
					target="_blank"
					rel="noopener noreferrer"
					class="flex items-center space-x-2 text-blue-500 hover:text-blue-700"
				>
					<svelte:component this={link.icon} class="w-6 h-6" />
					<span>{link.name}</span>
				</a>
			</li>
		{/each}
	</ul>
</main>

<style>
	@import 'tailwindcss/base';

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

	.love {
		font-family: 'OffBitBold',  sans-serif;
		font-size: 2rem;
	}
</style>
