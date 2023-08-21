<script lang="ts">
	import { TreeView, TreeViewItem } from '@skeletonlabs/skeleton'
	import { Ratings } from '@skeletonlabs/skeleton'
	import vectorSimilarity from '../utils/vectorSimilarity'
	import type { ResponseData } from '../types/index'

	export let responseData: ResponseData
</script>

<TreeView>
	{#each responseData.content as item (item.metadata.file)}
		<TreeViewItem open={true}>
			<h6>{item.metadata.file}</h6>
			<svelte:fragment slot="children">
				<article class="mt-2 mb-4 space-y-2 p-4 rounded-[0.5em]">
					<section class="w-full flex flex-direction-row items-center gap-[1em]">
						<p>Score:</p>
						<Ratings
							max={5}
							value={vectorSimilarity(item.score)}
							justify="left"
							spacing="space-x-[0.1em]"
						>
							<svelte:fragment slot="empty">
								<svg
									class="h-5 w-5 text-transparent"
									opacity="0.1"
									fill="white"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="1"
										d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
									/>
								</svg>
							</svelte:fragment>
							<svelte:fragment slot="full">
								<svg
									class="h-5 w-5 text-transparent"
									opacity="0.9"
									fill="white"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="1"
										d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
									/>
								</svg>
							</svelte:fragment>
						</Ratings>
					</section>
					{#if item.metadata.header}
						<p class="font-bold">{item.metadata.header}</p>
					{/if}
					<p>{item.text}</p>
				</article>
			</svelte:fragment>
		</TreeViewItem>
	{/each}
</TreeView>
