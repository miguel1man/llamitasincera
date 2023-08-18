<script lang="ts">
	import type { Chunk, Message, ResponseData } from '../types/index'
	import { SlideToggle } from '@skeletonlabs/skeleton'
	import { TreeView, TreeViewItem } from '@skeletonlabs/skeleton'
	import { ProgressRadial } from '@skeletonlabs/skeleton'
	import { handleChatQuestion } from '../services/apiChatLlama'
	import { apiVectorDB } from '../services/apiVectorDB'
	import vectorSimilarity from '../lib/vectorSimilarity'

	let currentMessage = ''
	let chunks: Chunk[] = []
	let messages: Message[] = [
		/* {
			content: "test question 1",
			isQuestion: true
		},
		{
			content: "test answer 1",
			isQuestion: false
		} */
	]
	let isShowSourcesMode = false
	let isShowConfig = false
  let responseData: ResponseData | null = null
		/* {
			content: [
				{
					metadata: {
						file: "file name 001.txt",
						header: "header text 01"
					},
					score: 19.82347,
					text: "lorem ipsum lorem ipsum lorem ipsum lorem ipsum"
				},
				{
					metadata: {
						file: "file test 002.pdf"
					},
					score: 5.82347,
					text: "lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum"
				}
			],
			id: 'id_1'
		} */

	function showConfig() {
		isShowConfig = !isShowConfig
	}

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
			// console.log("responseData:", responseData)
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

<main class="my-2 mx-auto flex flex-col justify-center items-center space-y-20">
	<section class="max-w-screen-lg md:max-w-screen-xl xl:max-w-[100em] grid gap-4 {isShowConfig ? 'lg:grid-cols-2' : 'lg:grid-cols-1'}">
		
		{#if isShowConfig}
		<section class="card rounded-[0.75em] bg-tertiary-500 bg-opacity-10 space-y-2 p-2 w-full mt-4 lg:mt-0">
			<SlideToggle name="slider-sources" checked={isShowSourcesMode} background="bg-secondary-800" active="bg-primary-500" on:click={toggleSourceMode}>
				{#if isShowSourcesMode}
					Show Sources
				{:else}
					Quick Chat
				{/if}
			</SlideToggle>
			{#if responseData}
			<section>
				{#each responseData.content as item (item.metadata.file)}
				<TreeView>
					<TreeViewItem open={true}>
					<h6>{item.metadata.file}</h6>
					<svelte:fragment slot="children">
						<article class="mt-2 mb-4 space-y-2 p-4 rounded-[0.5em]">
							<div class="w-full flex flex-direction-row items-center gap-2">
								Score:
								<ProgressRadial width="w-9" font={180} value={vectorSimilarity(item.score)}>{vectorSimilarity(item.score)}%</ProgressRadial>
							</div>
							{#if item.metadata.header}
								<p class={"font-bold"}>{item.metadata.header}</p>
							{/if}
							<p>{item.text}</p>
						</article>
					</svelte:fragment>
					</TreeViewItem>
				</TreeView>
				{/each}
			</section>
			{/if}
		</section>
		{/if}
		
		<div class="card rounded-[0.75em] xl:w-[40em] bg-tertiary-500 bg-opacity-10 space-y-2 p-2">
			<div class="h-[calc(100vh-10em)] flex flex-col space-y-2 overflow-y-auto">
				{#each messages as message (message.content)}
				<div class="card p-4 max-w-[95%] rounded-[0.75em] {message.isQuestion 
					? 'variant-soft-tertiary rounded-tr-none ml-auto justify-end' 
					: 'variant-soft-secondary rounded-tl-none mr-auto justify-start'}">
					<p>{message.content}</p>
				</div>
				{/each}
			</div>

			<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-[0.5em] gap-4">
				<button class="input-group-shim" on:click={showConfig}>
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
				<button class="variant-filled-primary" on:click={sendMessage}>
					Send
				</button>
			</div>
		</div>
	</section>
</main>

<style>
	:global(summary) {
		background-color: rgb(var(--color-secondary-900));
		margin-bottom: 0.5em;
	}

	:global(summary):hover {
		background-color: rgb(var(--color-secondary-800)) !important;
	}

	:global(summary.rounded-container-token) {
		border-radius: 0.5em;
	}

	:global(.tree-item article) {
		background-color: rgb(var(--color-secondary-700) / var(--tw-bg-opacity));
	}
	
</style>