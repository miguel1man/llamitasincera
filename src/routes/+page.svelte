<script lang="ts">
	let currentMessage = '';
	let chunks: any = []
	
	async function fetchData(question: string) {
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
				chunks = [...chunks, chunkText]

				await readChunk();
			};

			await readChunk();
		} catch (e) {
			console.error("Error fetching data:", e);
		}
	}
	
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center space-y-20">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Chat with a llama</h2>
	</div>

	<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token">
		<button class="input-group-shim">+</button>
		<textarea
			bind:value={currentMessage}
			class="bg-transparent border-0 ring-0"
			name="prompt"
			id="prompt"
			placeholder="Write a message..."
			rows="1"
		/>
		<button class="variant-filled-primary" on:click={() => fetchData(currentMessage)}>Send</button>
	</div>
	<pre>
    {#each chunks as chunk}
      {chunk}
    {/each}
  </pre>
</div>