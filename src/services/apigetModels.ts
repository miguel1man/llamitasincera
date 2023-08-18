type ModelFileName = string;

export async function fetchModelFiles(): Promise<ModelFileName[]> {
  const response = await fetch('http://localhost:6757/api/get-models')
  let modelFiles: string[] = []

  if (response.ok) {
    modelFiles = await response.json()
    return modelFiles
  } else {
    return []
  }
}
