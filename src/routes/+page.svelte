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

  function toggleSourceMode() {
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

<div class="my-2 mx-auto flex flex-col justify-center items-center space-y-20">
	<div class="max-w-screen-lg md:max-w-screen-xl xl:max-w-[100em] mx-auto grid gap-4 lg:grid-cols-2">
		<div class="card rounded-4 xl:w-[40em] bg-tertiary-500 bg-opacity-10 space-y-2 p-2">
			<div class="h-[calc(100vh-10em)] flex flex-col space-y-2 overflow-y-auto">
				{#each messages as message (message.content)}
					<div class="card p-4 max-w-[95%] {message.isQuestion ? 'variant-primary rounded-tr-none ml-auto justify-end' : 'variant-soft-secondary rounded-tl-none mr-auto justify-start'}">
						<p>{message.content}</p>
					</div>
				{/each}
			</div>

			<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token gap-4">
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
		</div>

		<div class="card rounded-4 bg-tertiary-500 bg-opacity-10 space-y-2 p-2 w-full mt-4 lg:mt-0">
			<SlideToggle name="slider-sources" checked={isShowSourcesMode} active="bg-primary-500" on:click={toggleSourceMode}>
				{#if isShowSourcesMode}
					Show Sources
				{:else}
					Quick Chat
				{/if}
			</SlideToggle>
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
</div>