// [chatId]/+page.js
export async function load({ params }) {
	const chatId = params.chatId;

	return { chatId };
}
