<script lang="ts">
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { uploadFiles } from '../../services/fileUploadService';
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton';
	import type { TableSource } from '@skeletonlabs/skeleton';
		
	let files: FileList | null = null;
	let uploadResponse: any[] = [];
	let tableSource: TableSource = {
		head: ['File', 'Uploaded'],
		body: []
	}

	async function onChangeHandler(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files) {
			files = input.files;
			uploadResponse = await uploadFiles(files);
			tableSource = {
				head: ['File', 'Uploaded'],
				body: tableMapperValues(uploadResponse, ["file", "uploaded"])
			};
		}
	}
</script>

<div class="container h-full mx-auto flex justify-center items-center py-16">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Upload your data</h2>
			<FileDropzone name="files" on:change={onChangeHandler} multiple>
				<svelte:fragment slot="message">Arrastra tus archivos</svelte:fragment>
				<svelte:fragment slot="meta">pdf, word, md y txt</svelte:fragment>
			</FileDropzone>

		<div class="flex justify-center space-x-2">
			<Table source={tableSource} />
		</div>
	</div>
</div>
