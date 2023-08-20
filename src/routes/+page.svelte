<script lang="ts">
	import type { Chunk, Message, ResponseData } from '../types/index'
	import { onMount } from 'svelte'
	import { SlideToggle } from '@skeletonlabs/skeleton'
	import { handleChatQuestion } from '../services/apiChatLlama'
	import handleChatSources from '../services/apiChatSources'
	import { getSimilarEmbeddings } from '../services/apiSimilarEmbeddings'
	import SourcesTree from '../components/SourcesTree.svelte'
	import { fetchModelFiles } from '../services/apiGetModels'
	// import { mockMessages, mockSources } from '../utils/mockData'

	let currentMessage = ''
	let chunks: Chunk[] = []
	let messageContainer: HTMLDivElement | null = null
	let isShowSourcesMode = false
	let isShowConfig = false
	let messages: Message[] = []
  let responseData: ResponseData | null = null
	let modelFiles: string[] = []
	let selectedModel: string
	let updatedChunks: string
	let messageCounter = 1

	const newQuestionId = `id_${messageCounter}`

	function showConfig() {
		isShowConfig = !isShowConfig
	}

  function toggleSourceMode() {
    isShowSourcesMode = !isShowSourcesMode
  }

	function changeModel(event: Event) {
		selectedModel = (event.target as HTMLSelectElement).value
	}

	async function sendMessage() {
		if (currentMessage.length === 0) return

		messageCounter++

		const newQuestion: Message = {
			content: currentMessage,
			isQuestion: true,
			id: newQuestionId
		}
    messages = [...messages, newQuestion]
		
		messageCounter++

		console.log('Consumiendo API:', newQuestionId)
		if (isShowSourcesMode) {
			responseData = await getSimilarEmbeddings(currentMessage, newQuestionId)
			console.log('isShowSourcesMode:', responseData)
			updatedChunks = await handleChatSources(currentMessage, selectedModel, chunks)
		} else {
			updatedChunks = await handleChatQuestion(currentMessage, selectedModel, chunks)
			console.log('no sources:', updatedChunks)
		}

		const newAnswer: Message = {
			content: updatedChunks,
			isQuestion: false,
			id: newQuestionId
		}

    messages = [...messages, newAnswer]
		currentMessage = ''
		messageContainer?.scrollTo({
      top: messageContainer.scrollHeight,
      behavior: 'smooth',
    })
	}

  onMount(async () => {
    modelFiles = await fetchModelFiles()
		selectedModel = modelFiles[0]
  })
</script>

<main class="max-w-screen-xl mx-auto m-[1em] flex flex-col justify-center items-center space-y-[1em]">
	<section class="grid gap-[0.5em] {isShowConfig ? 'lg:grid-cols-2' : 'lg:grid-cols-1'}">
		
		<div class="card mx-[0.5em] p-[0.5em] rounded-[0.5em] space-y-[0.5em] md:{isShowConfig ? 'w-full' : 'max-w-[100%] w-[100%]'} lg:order-2 w-full max-w-[48em] xl:max-w-[64em] bg-tertiary-500 bg-opacity-10">
			<div class="h-[calc(100vh-10em)] flex flex-col space-y-2 overflow-y-auto" bind:this={messageContainer}>
				{#each messages as message, index (index)}
				<div class="card p-4 max-w-[95%] rounded-[0.75em] {message.isQuestion 
					? 'variant-soft-tertiary rounded-tr-none ml-auto justify-end' 
					: 'variant-soft-secondary rounded-tl-none mr-auto justify-start'}">
					<p>{message.content}</p>
				</div>
				{/each}
			</div>

			<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-[0.5em] gap-4">
				<button class="input-group-shim font-bold text-[1em]" on:click={showConfig} style="color: rgb(var(--color-secondary-500));">
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

		{#if isShowConfig}
			<section class="card lg:order-1 rounded-[0.75em] bg-tertiary-500 bg-opacity-10 space-y-[1em] p-[1em] w-full mt-4 lg:mt-0">
				
				<section on:change={changeModel} class="flex flex-row items-center gap-[1em]">
					<p class="font-bold">LLM:</p>
					<select class="select max-w-[20em]">
						{#each modelFiles as model}
							<option value={model}>{model}</option>
						{/each}
					</select>
					<button type="button" class="btn-icon" on:click={() => {
						fetchModelFiles()
					}}>
						<svg class="h-8 w-8 text-secondary-500"  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <path d="M4 12v-3a3 3 0 0 1 3 -3h13m-3 -3l3 3l-3 3" />  <path d="M20 12v3a3 3 0 0 1 -3 3h-13m3 3l-3-3l3-3" />
						</svg>
					</button>
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
					<section class="h-[calc(100vh-15em)] overflow-y-auto">
						<SourcesTree responseData={responseData}/>
					</section>
				{/if}

			</section>
		{/if}
		

	</section>
</main>
