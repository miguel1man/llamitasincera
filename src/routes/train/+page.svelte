<script lang="ts">
	import { FileDropzone } from '@skeletonlabs/skeleton'
	import { uploadFiles } from '../../services/fileUploadService'
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton'
	import type { TableSource } from '@skeletonlabs/skeleton'
		
	let files: FileList | null = null
	let uploadResponse: any[] = []
	let tableSource: TableSource = {
		head: ['File', 'Uploaded'],
		body: []
	}

	async function onChangeHandler(event: Event) {
		const input = event.target as HTMLInputElement
		if (input.files) {
			files = input.files
			uploadResponse = await uploadFiles(files)
			tableSource = {
				head: ['File', 'Uploaded'],
				body: tableMapperValues(uploadResponse, ["file", "uploaded"])
			}
		}
	}
</script>

<div class="container h-full mx-auto flex justify-center items-center py-16">
	<div class="space-y-10 text-center flex flex-col items-center">

			<h1 class="h1">
				<span class="bg-gradient-to-br from-yellow-500 to-orange-500 bg-clip-text text-transparent box-decoration-clone">Train the AI with your data</span>
			</h1>

				<FileDropzone name="files" on:change={onChangeHandler} multiple>
					<svelte:fragment slot="message">Drag and drop your files</svelte:fragment>
					<svelte:fragment slot="meta">Supported files: pdf, word, md and txt.</svelte:fragment>
				</FileDropzone>

			{#if uploadResponse.length > 0}
				<div class="flex justify-center space-x-2">
					<Table source={tableSource} />
				</div>
			{/if}
	</div>
</div>
