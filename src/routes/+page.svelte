<script lang="ts">
	import { SlideToggle } from '@skeletonlabs/skeleton';

	let currentMessage = ''
	let chunks: any = []
	let messages: { content: string; isQuestion: boolean }[] = []
	let isShowSourcesMode = false;

  function toggleMode() {
    isShowSourcesMode = !isShowSourcesMode;
  }

	async function handleChatQuestion(question: string) {
		try {
			const newQuestion: { content: string; isQuestion: boolean } = {
        content: question,
        isQuestion: true,
      }

      messages = [...messages, newQuestion]

			const response = await fetch(
				`http://localhost:5001/api/chat-llama?question=${encodeURIComponent(question)}`
			)

			if (!response.body) {
				console.log("No API response.")
				return
			}
			const reader = response.body.getReader()
			const decoder = new TextDecoder()

			const readChunk = async () => {
				const { done, value } = await reader.read()

				if (done) {
					console.log("Completed stream")
					return
				}

				const chunkText = decoder.decode(value)
				console.log("chunkText:", chunkText)
				
				const newAnswer: { content: string; isQuestion: boolean } = {
          content: chunkText,
          isQuestion: false,
        }

        messages = [...messages, newAnswer]
				
				chunks = [...chunks, chunkText]


				await readChunk()
			}

			await readChunk()
		} catch (e) {
			console.error("Error handling question:", e)
		}
	}
	
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center space-y-20">
	<div class="min-w-[50em] max-w-lg mx-auto">
		<div class="flex flex-col justify-end space-y-2">
			{#each messages as message (message.content)}
        <div
          class="flex justify-{message.isQuestion ? 'end' : 'start'} space-x-2"
        >
          <div
            class="card p-4 rounded-{message.isQuestion ? 'tr' : 'tl'}-none space-y-2 {message.isQuestion ? 'variant-primary' : 'variant-soft-secondary'}"
          >
            <p>{message.content}</p>
          </div>
        </div>
      {/each}
		</div>

		<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token my-2">
			<button class="input-group-shim">+</button>
			<textarea
				bind:value={currentMessage}
				class="bg-transparent border-0 ring-0"
				name="prompt"
				id="prompt"
				placeholder="Write a message..."
				rows="1"
			/>
			<button class="variant-filled-primary" on:click={() => {
					handleChatQuestion(currentMessage)
					currentMessage = ''
				}}
			>
				Send
			</button>
		</div>

		<div class="flex justify-center">
			<SlideToggle name="slider-label" checked={isShowSourcesMode} active="bg-primary-500" on:click={toggleMode}>
				{#if isShowSourcesMode}
					Show Sources
				{:else}
					Quick Chat
				{/if}
			</SlideToggle>
		</div>
	</div>
</div>