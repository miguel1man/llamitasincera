import type { Chunk } from '../types/index'

async function handleChatQuestion(
	question: string,
	model_name: string,
	chunks: Chunk[]
): Promise<string> {
	let chunkText = ''
	// console.log("model_name:", model_name)
	try {
		const response = await fetch(
			`http://localhost:5000/api/chat-llama?question=${encodeURIComponent(
				question
			)}&model_name=${model_name}`
		)

		if (!response.body) {
			console.log('No API response.')
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
		console.error('Error handling question:', e)
		return ''
	}
}

export { handleChatQuestion }
