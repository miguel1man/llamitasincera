import type { Chunk } from '../types/index'

async function handleChatSources(
	question: string,
	model_name: string,
	chunks: Chunk[]
): Promise<string> {
	let chunkText = ''

	try {
		const response = await fetch(
			`http://localhost:6757/api/chat-sources?question=${encodeURIComponent(
				question
			)}&model_name=${model_name}`
		)

		if (!response.body) {
			console.log('No response on: API chat sources.')
			return ''
		}

		const reader = response.body.getReader()
		const decoder = new TextDecoder()

		const readChunk = async (): Promise<void> => {
			const { done, value } = await reader.read()

			if (done) {
				console.log('Completed stream')
				return
			}

			chunkText = decoder.decode(value)

			chunks = [...chunks, chunkText]

			await readChunk()
		}

		await readChunk()

		return chunkText
	} catch (e) {
		console.error('Error handling chat with sources:', e)
		return ''
	}
}

export { handleChatSources }
