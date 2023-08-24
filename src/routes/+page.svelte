<script lang="ts">
	import type { Chunk, Message, ResponseData } from '../types/index'
	import { onMount, tick } from 'svelte'
	import { SlideToggle } from '@skeletonlabs/skeleton'
	import { Toast, toastStore } from '@skeletonlabs/skeleton'
	import type { ToastSettings } from '@skeletonlabs/skeleton'
	import { fetchModelFiles } from '../services/apiGetModels'
	import { addAnswer, addQuestion } from '../services/addChats'
	import SourcesTree from '../components/SourcesTree.svelte'
	import moveScroll from '../utils/moveScroll'
	import getSimilarEmbeddings from '../services/apiSimilarEmbeddings'
	// import { mockMessages, mockSources } from '../utils/mockData'

	let chunks: Chunk[] = []
	let currentMessage = ''
	let isShowConfig = false
	let isShowSourcesMode = false
	let messageCounter = 1
	let messages: Message[] = []
	let modelFiles: string[] = []
	let newQuestionId = `id_${messageCounter}`
	let responseData: ResponseData | null = null
	let scrollContainer: any
	let selectedModel: string
	let updatedChunks: string

	function showConfig() {
		isShowConfig = !isShowConfig
	}

	function toggleSourceMode() {
		isShowSourcesMode = !isShowSourcesMode
	}

	function changeModel(event: Event) {
		selectedModel = (event.target as HTMLSelectElement).value
	}

	const handleSendChat = async () => {
		const newQuestion = await addQuestion(currentMessage, messageCounter, messages, newQuestionId)
		messages = [...newQuestion]
		const userMessage = currentMessage
		currentMessage = ''
		await tick()
		moveScroll(scrollContainer)

		if (isShowSourcesMode) {
			responseData = await getSimilarEmbeddings(currentMessage, newQuestionId)
		}

		const newAnswer = await addAnswer(
			chunks,
			userMessage,
			isShowSourcesMode,
			messageCounter,
			messages,
			newQuestionId,
			responseData,
			selectedModel,
			updatedChunks
		)
		messages = [...newAnswer]
		currentMessage = ''
		await tick()
		moveScroll(scrollContainer)
	}

	onMount(async () => {
		modelFiles = await fetchModelFiles()
		if (modelFiles.length === 0) {
			const t: ToastSettings = {
				message: 'No LLM detected',
				action: {
					label: 'Reload page',
					response: () => location.reload()
				},
				autohide: false
			}
			toastStore.trigger(t)
		}
		selectedModel = modelFiles[0]
	})
</script>

<main
	class="w-full h-full py-[1em] flex flex-col justify-center items-center bg-gradient-to-br from-black via-red-900 to-orange-600"
>
	<div
		class="grid ml-[0.5em] mr-[1.5em] {isShowConfig
			? 'lg:grid-cols-2 gap-[1em]'
			: 'lg:grid-cols-1 space-y-[1em]'}"
	>
		<section
			class="section w-full mx-[0.5em] p-[1em] rounded-[0.75em] space-y-[1em] bg-gradient-to-b from-black/90 to-black/70 backdrop-blur border-[1px] border-solid border-white border-opacity-10
				{isShowConfig ? 'md:w-full' : 'md:max-w-[100%] w-[100%]'}
				lg:order-2 w-full max-w-[48em] xl:max-w-[64em]"
		>
			<div
				class="h-[calc(100vh-11.75em)] flex flex-col space-y-2 overflow-y-auto"
				bind:this={scrollContainer}
			>
				{#each messages as message, index (index)}
					<div
						class="p-[1em] max-w-[95%] border-[1px] border-solid border-white border-opacity-10 rounded-[1em]
					{message.isQuestion
							? 'bg-white/[5%] rounded-br-none ml-auto justify-end'
							: 'bg-white/[15%]  rounded-bl-none mr-auto justify-start'}"
					>
						<p>{message.content}</p>
					</div>
				{/each}
			</div>

			<section
				class="input-group input-group-divider focus:outline-color-blue grid-cols-[auto_1fr_auto] rounded-[0.5em] gap-0 md:min-w-[30em] lg:min-w-[28em]"
			>
				<button
					class="input-group-shim font-bold text-[1em] bg-red-700"
					on:click={showConfig}
					style="color: rgb(var(--color-white));"
				>
					{#if isShowConfig}
						-
					{:else}
						+
					{/if}
				</button>
				<textarea
					bind:value={currentMessage}
					class="bg-black/[50%] border-0 ring-0"
					name="prompt"
					id="prompt"
					placeholder="Write a question..."
					rows="1"
				/>
				<button class="bg-red-700" on:click={handleSendChat}>Send</button>
			</section>
			<Toast position="t" background="bg-red-700" />
		</section>

		{#if isShowConfig}
			<section
				class="section w-full mx-[0.5em] p-[1em] rounded-[0.75em] space-y-[1em] bg-gradient-to-b from-black/90 to-black/70 backdrop-blur border-[1px] border-solid border-white border-opacity-10 {isShowConfig
					? 'mt-0'
					: 'mt-[1em]'} lg:order-1"
			>
				<section on:change={changeModel} class="flex flex-row items-center gap-[1em]">
					<p class="font-bold">LLM:</p>
					<select class="select max-w-[20em]">
						{#each modelFiles as model, index (index)}
							<option value={model}>{model}</option>
						{/each}
					</select>
					<button
						type="button"
						class="btn-icon"
						on:click={() => {
							fetchModelFiles()
						}}
					>
						<svg
							class="h-8 w-8 text-gray-300"
							width="24"
							height="24"
							viewBox="0 0 24 24"
							stroke-width="2"
							stroke="currentColor"
							fill="none"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path stroke="none" d="M0 0h24v24H0z" />
							<path d="M4 12v-3a3 3 0 0 1 3 -3h13m-3 -3l3 3l-3 3" />
							<path d="M20 12v3a3 3 0 0 1 -3 3h-13m3 3l-3-3l3-3" />
						</svg>
					</button>
				</section>

				<section class="flex flex-row items-center gap-[1em]">
					<p class="font-bold">Chat mode:</p>
					<SlideToggle
						name="slider-sources"
						checked={isShowSourcesMode}
						background="bg-red-900"
						active="bg-red-600"
						on:click={toggleSourceMode}
					>
						{#if isShowSourcesMode}
							<p>Show sources</p>
						{:else}
							<p>Quick chat</p>
						{/if}
					</SlideToggle>
				</section>

				{#if isShowSourcesMode && !responseData}
					<div
						class="m-[1em] p-[2em] mx-auto max-w-[24em] text-center border-[1px] border-solid border-white border-opacity-10 rounded-[1em] bg-white/[5%]"
					>
						The app will provide the sources it used to answer your questions here.
					</div>
				{/if}

				{#if responseData}
					<section class="h-[calc(100vh-15em)] overflow-y-auto">
						<SourcesTree {responseData} />
					</section>
				{/if}
			</section>
		{/if}
	</div>
</main>
