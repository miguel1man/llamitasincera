<script lang="ts">
	import { FileDropzone } from '@skeletonlabs/skeleton'
	import { uploadFiles } from '../../services/apiUploadFile'
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton'
	import type { TableSource } from '@skeletonlabs/skeleton'
	// import { mockFiles } from '../../utils/mockData'

	let files: FileList | null = null
	let uploadResponse: any[] = []
	let tableSource: TableSource = {
		head: ['File', 'Uploaded'],
		body: tableMapperValues(uploadResponse, ["file", "uploaded"])
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
	<div class="space-y-10 max-w-[36em] text-center flex flex-col items-center">

			<h1 class="h1">
				<span class="bg-gradient-to-br from-yellow-500 to-orange-500 bg-clip-text text-transparent box-decoration-clone">Drag and drop your files</span>
			</h1>

				<FileDropzone name="files" on:change={onChangeHandler} multiple>
					<svelte:fragment slot="message">Supported types</svelte:fragment>
					<svelte:fragment slot="meta">pdf, doc, txt and md.</svelte:fragment>
				</FileDropzone>

			{#if uploadResponse.length > 0}
				<div class="space-x-2 w-full">
					<Table source={tableSource} />
				</div>
			{/if}
	</div>
</div>
