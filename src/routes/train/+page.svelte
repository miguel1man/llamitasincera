<script lang="ts">
	import { FileDropzone } from '@skeletonlabs/skeleton'
	import { uploadFiles } from '../../services/apiUploadFile'
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton'
	import type { TableSource } from '@skeletonlabs/skeleton'
	import { mockFiles } from '../../utils/mockData'

	let files: FileList | null = null
	let uploadResponse: any[] = mockFiles
	let tableSource: TableSource = {
		head: ['File', 'Uploaded'],
		body: tableMapperValues(uploadResponse, ['file', 'uploaded'])
	}

	async function onChangeHandler(event: Event) {
		const input = event.target as HTMLInputElement
		if (input.files) {
			files = input.files
			uploadResponse = await uploadFiles(files)
			tableSource = {
				head: ['File', 'Uploaded'],
				body: tableMapperValues(uploadResponse, ['file', 'uploaded'])
			}
		}
	}
</script>

<main
	class="h-full w-full mx-auto flex justify-center items-center bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-cyan-500 via-sky-700 to-slate-900"
>
	<section
		class="space-y-[2em] w-[48em] m-[1em] p-[2em] rounded-[1em] flex flex-col items-center bg-gradient-to-b from-black/90 to-black/70 backdrop-blur border-[1px] border-solid border-white border-opacity-10"
	>
		<h1 class="h1">
			<span class="text-white text-center">Drag and drop your files</span>
		</h1>

		<FileDropzone name="files" on:change={onChangeHandler} multiple>
			<svelte:fragment slot="message">Supported types</svelte:fragment>
			<svelte:fragment slot="meta">pdf, doc, txt and md.</svelte:fragment>
		</FileDropzone>

		{#if uploadResponse.length > 0}
			<div class="w-full">
				<Table source={tableSource} />
			</div>
		{/if}
	</section>
</main>
