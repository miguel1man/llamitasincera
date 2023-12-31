async function getSimilarEmbeddings(question: string, id: string) {
	const url = `http://localhost:5000/api/similar-embeddings`
	const body = {
		question,
		id
	}
	// console.log("body:", body)

	try {
		const response = await fetch(url, {
			method: 'POST',
			body: JSON.stringify(body),
			headers: {
				'Content-Type': 'application/json'
			}
		})
		// console.log('Response Api embeddings:', response)

		if (response.ok) {
			const responseData = await response.json()
			return responseData
		} else {
			throw new Error(`Request failed with status: ${response.status}`)
		}
	} catch (error) {
		console.error('Error sending question to API:', error)
		throw error
	}
}

export default getSimilarEmbeddings
