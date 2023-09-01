export async function uploadFiles(files: FileList | null): Promise<any[]> {
	if (!files) {
		console.error('No files provided.')
		return []
	}

	const formData = new FormData()
	for (let i = 0; i < files.length; i++) {
		formData.append('files', files[i])
	}

	try {
		const response = await fetch('http://localhost:5000/api/upload-files', {
			method: 'POST',
			body: formData
		})

		if (!response.ok) {
			throw new Error(`Upload failed with status ${response.status}`)
		}

		const uploadResponse = await response.json()
		return uploadResponse
	} catch (error) {
		console.error('Error uploading files:', error)
		return []
	}
}
