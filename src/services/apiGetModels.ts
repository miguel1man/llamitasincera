type ModelFileName = string

export async function fetchModelFiles(): Promise<ModelFileName[]> {
	// console.log("get models...")
	const response = await fetch('http://localhost:5000/api/get-models')
	let modelFiles: string[] = []

	if (response.ok) {
		modelFiles = await response.json()
		// console.log("modelFiles:", modelFiles)
		return modelFiles
	} else {
		return []
	}
}
