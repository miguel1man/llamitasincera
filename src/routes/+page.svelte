<script lang="ts">
	import type { Chunk, Message, ResponseData } from '../types/index'
	import { onMount } from 'svelte'
	import { SlideToggle } from '@skeletonlabs/skeleton'
	import { handleChatQuestion } from '../services/apiChatLlama'
	import { apiVectorDB } from '../services/apiVectorDB'
	import TreeViewSource from '../components/TreeViewSource.svelte'
	import { fetchModelFiles } from '../services/apigetModels'
	// import { mockMessages, mockSources } from '../utils/mockData'

	let currentMessage = ''
	let chunks: Chunk[] = []
	let messageContainer:any
	let isShowSourcesMode = false
	let isShowConfig = false
	let messages: Message[] = []
  let responseData: ResponseData | null = null
	let modelFiles: string[] = []
	let modelName: string

	function showConfig() {
		isShowConfig = !isShowConfig
	}

  function toggleSourceMode() {
    isShowSourcesMode = !isShowSourcesMode
  }

	function changeModel(event: Event) {
		modelName = (event.target as HTMLSelectElement).value
	}

	async function sendMessage() {
		if (currentMessage.length === 0) return

		const newQuestion: Message = {
			content: currentMessage,
			isQuestion: true,
		}
    messages = [...messages, newQuestion]
		
		if (isShowSourcesMode) {
			responseData = await apiVectorDB(currentMessage, "id_001")
		}

		const updatedChunks = await handleChatQuestion(currentMessage, modelName, chunks)
		const newAnswer: Message = {
			content: updatedChunks,
			isQuestion: false,
		}

    messages = [...messages, newAnswer]
		currentMessage = ''
		messageContainer.scrollTop = messageContainer.scrollHeight
	}

  onMount(async () => {
    modelFiles = await fetchModelFiles()
		modelName = modelFiles[0]
  })
</script>

<main class="my-2 mx-auto flex flex-col justify-center items-center space-y-20">
	<section class="max-w-screen-lg md:max-w-screen-xl xl:max-w-[100em] grid gap-4 {isShowConfig ? 'lg:grid-cols-2' : 'lg:grid-cols-1'}">
		
		{#if isShowConfig}
			<section class="card rounded-[0.75em] bg-tertiary-500 bg-opacity-10 space-y-[1em] p-[1em] w-full mt-4 lg:mt-0">
				
				<section on:change={changeModel} class="flex flex-row items-center gap-[1em]">
					<p class="font-bold">LLM:</p>
					<select class="select max-w-[20em]">
						{#each modelFiles as model}
							<option value={model}>{model}</option>
						{/each}
					</select>
				</section>

				<section class="flex flex-row items-center gap-[1em]">
					<p class="font-bold">Chat mode:</p>
					<SlideToggle name="slider-sources" checked={isShowSourcesMode} background="bg-secondary-800" active="bg-primary-500" on:click={toggleSourceMode}>
						{#if isShowSourcesMode}
							<p>Show sources</p>
						{:else}
							<p>Quick chat</p>
						{/if}
					</SlideToggle>
				</section>

				{#if responseData}
					<section class="h-[calc(100vh-10em)] overflow-y-auto">
						<TreeViewSource responseData={responseData}/>
					</section>
				{/if}

			</section>
		{/if}
		
		<div class="card rounded-[0.75em] xl:w-[40em] bg-tertiary-500 bg-opacity-10 space-y-2 p-2">
			<div class="h-[calc(100vh-10em)] flex flex-col space-y-2 overflow-y-auto" bind:this={messageContainer}>
				{#each messages as message (message.content)}
				<div class="card p-4 max-w-[95%] rounded-[0.75em] {message.isQuestion 
					? 'variant-soft-tertiary rounded-tr-none ml-auto justify-end' 
					: 'variant-soft-secondary rounded-tl-none mr-auto justify-start'}">
					<p>{message.content}</p>
				</div>
				{/each}
			</div>

			<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-[0.5em] gap-4">
				<button class="input-group-shim" on:click={showConfig} style="color: rgb(var(--color-secondary-500));">
					{#if isShowConfig}
						-
					{:else}
						+
					{/if}
				</button>
				<textarea
					bind:value={currentMessage}
					class="bg-transparent border-0 ring-0"
					name="prompt"
					id="prompt"
					placeholder="Write a question..."
					rows="1"
				/>
				<button class="bg-secondary-800" on:click={sendMessage}>
					Send
				</button>
			</div>
		</div>

	</section>
</main>
