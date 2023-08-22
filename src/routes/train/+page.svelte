<script lang="ts">
	import type { TableSource } from '@skeletonlabs/skeleton'
	import type { ToastSettings } from '@skeletonlabs/skeleton'
	import { FileDropzone } from '@skeletonlabs/skeleton'
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton'
	import { Toast, toastStore } from '@skeletonlabs/skeleton'
	import { ProgressRadial } from '@skeletonlabs/skeleton'
	import { uploadFiles } from '../../services/apiUploadFile'
	// import { mockFiles } from '../../utils/mockData'

	let uploadResponse: any[] = []
	let loadingSources = false

	let tableSource: TableSource = {
		head: ['Files trained'],
		body: tableMapperValues(uploadResponse, ['file'])
	}

	function showFileAlert(text: string) {
		const t: ToastSettings = {
			message: text,
			timeout: 5000
		}
		toastStore.trigger(t)
	}

	async function onChangeHandler(event: Event) {
		loadingSources = true
		const input = event.target as HTMLInputElement
		if (input.files) {
			const allowedFileTypes = ['.pdf', '.md']
			const files = input.files

			const validFiles: any = []
			const invalidFiles: any = []

			Array.from(files).forEach((file) => {
				const fileExtension = file.name.substring(file.name.lastIndexOf('.'))
				if (allowedFileTypes.includes(fileExtension)) {
					validFiles.push(file)
				} else {
					invalidFiles.push(file)
				}
			})

			const validFileList = new DataTransfer()
			validFiles.forEach((file: any) => {
				validFileList.items.add(file)
			})

			if (validFiles.length > 0) {
				uploadResponse = await uploadFiles(validFileList.files)
				// console.log('uploadRespsonse:', uploadResponse)

				const uploadedSuccess = uploadResponse.filter((item) => item.uploaded === true)
				const uploadedFailed = uploadResponse.filter((item) => item.uploaded === false)

				tableSource = {
					head: ['Files trained'],
					body: tableMapperValues(uploadedSuccess, ['file'])
				}
				if (invalidFiles.length > 0 || uploadedFailed.length > 0) {
					showFileAlert('File not supported.')
					// invalidFiles.forEach((file: any) => {
					// 	console.log(`File "${file.name}" is not a valid PDF or MD file.`)
					// })
				}
			} else {
				showFileAlert('No valid files to upload.')
			}
			loadingSources = false
		}
	}
</script>

<main
	class="h-full w-full mx-auto flex justify-center items-center bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-cyan-500 via-sky-700 to-slate-900"
>
	<section
		class="space-y-[2em] text-center w-[36em] m-[1em] p-[2em] rounded-[2em] flex flex-col items-center bg-gradient-to-b from-black/90 to-black/70 backdrop-blur border-[1px] border-solid border-white border-opacity-10"
	>
		<h1 class="text-xl">
			<span class="text-white text-center"
				>Drag and drop your files to train the AI with your data</span
			>
		</h1>

		<FileDropzone name="files" on:change={onChangeHandler} multiple>
			<svelte:fragment slot="message">Supported types</svelte:fragment>
			<svelte:fragment slot="meta">pdf, doc, txt and md.</svelte:fragment>
		</FileDropzone>

		{#if loadingSources}
			<ProgressRadial width="w-[4em]" />
		{/if}

		{#if uploadResponse.length > 0}
			<div class="w-full">
				<Table source={tableSource} />
			</div>
		{/if}
	</section>
	<Toast />
</main>
