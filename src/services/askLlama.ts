export async function fetchData(question: string) {
  try {
    const response = await fetch(
        `http://localhost:5000/api/llamacpp?question=${encodeURIComponent(question)}`
    );

    if (!response.body) {
      console.log("no body")
      return
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    const readChunk = async () => {
      const { done, value } = await reader.read();

      if (done) {
        console.log("Stream completo");
        return;
      }

      const chunkText = decoder.decode(value);
      console.log("chunkText:", chunkText);

      await readChunk();
    };

    await readChunk();
  } catch (error) {
      console.error("Error fetching data:", error);
  }
}
