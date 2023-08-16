<script lang="ts">
	import type { Chunk, Message, ResponseData } from '../types/index'
	import { SlideToggle } from '@skeletonlabs/skeleton'
	import { handleChatQuestion } from '../services/apiChatLlama'
	import { apiVectorDB } from '../services/apiVectorDB'

	let currentMessage = ''
	let chunks: Chunk[] = []
	let messages: Message[] = []
	let isShowSourcesMode = false
  let responseData: ResponseData | null = null

  function toggleMode() {
    isShowSourcesMode = !isShowSourcesMode
  }

	async function sendMessage() {
		const newQuestion: Message = {
			content: currentMessage,
			isQuestion: true,
		}
    messages = [...messages, newQuestion]
		
		if (isShowSourcesMode) {
			responseData = await apiVectorDB(currentMessage, "id_1")
			console.log("response data:", responseData)
		}

		const updatedChunks = await handleChatQuestion(currentMessage, chunks)
		const newAnswer: Message = {
			content: updatedChunks,
			isQuestion: false,
		}

    messages = [...messages, newAnswer]
		currentMessage = ''
	}
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center space-y-20">
	<div class="min-w-[50em] max-w-lg mx-auto">
		<div class="flex flex-col justify-end space-y-2">
			{#each messages as message (message.content)}
        <div class="flex justify-{message.isQuestion ? 'end' : 'start'} space-x-2">
          <div class="card p-4 rounded-{message.isQuestion ? 'tr' : 'tl'}-none space-y-2 {message.isQuestion ? 'variant-primary' : 'variant-soft-secondary'}">
            <p>{message.content}</p>
          </div>
        </div>
      {/each}
		</div>

		<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token my-3">
			<button class="input-group-shim">+</button>
			<textarea
				bind:value={currentMessage}
				class="bg-transparent border-0 ring-0"
				name="prompt"
				id="prompt"
				placeholder="Write a message..."
				rows="1"
			/>
			<button class="variant-filled-primary" on:click={sendMessage}>
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

		{#if responseData}
			<div>
				<h2>Response Data:</h2>
				{#each responseData.content as contentItem (contentItem.metadata.file)}
					<p>File: {contentItem.metadata.file}</p>
					<p>Header: {contentItem.metadata.header}</p>
					<p>Score: {contentItem.score}</p>
					<p>Text: {contentItem.text}</p>
				{/each}
			</div>
		{/if}

	</div>
</div>