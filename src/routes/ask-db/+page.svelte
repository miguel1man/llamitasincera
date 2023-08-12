<script lang="ts">
	import { askVectorDB } from '../../services/askVectorDB';
	let currentMessage = '';
	let vectorDBResponse: any;
	const id: string = "qwerty"
	let answerContent: any

	async function onClickHandler(question: string, id: string) {
		console.log("currentMessage:", currentMessage)
  	vectorDBResponse = await askVectorDB(question, id);
		console.log("vectorDBResponse:", vectorDBResponse)
		
		const answerId: string = vectorDBResponse.id
		console.log("answerId:", answerId)
		answerContent = vectorDBResponse.content
		console.log("answerContent:", answerContent)
	}

</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center space-y-20">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Chat with your data</h2>
	</div>

	<div class="space-y-8 flex flex-col justify-center items-center">
		<div class="input-group input-group-divider rounded-container-token">
			<textarea
				bind:value={currentMessage}
				class="textarea bg-transparent border-0 ring-0 flex-grow w-full"
				name="prompt"
				id="prompt"
				placeholder="Write a message..."
				rows="1"
			/>
		</div>
		<button class="btn variant-filled-primary max-w-[5em]" on:click={() => onClickHandler(currentMessage, id)}>Send</button>
	</div>
	<div class="space-y-8">
		{#if answerContent}
			{#each answerContent as answerItem}
				<div class="card">
					<header class="card-header">{answerItem.metadata.file}</header>
					<div class="p-4 space-y-4">
						<h6 class="h6">{answerItem.metadata.header}</h6>
						<article>
							<p>
								{answerItem.text}
							</p>
						</article>
					</div>
				</div>
			{/each}
		{/if}
	</div>
</div>