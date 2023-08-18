<script lang="ts">
  import { TreeView, TreeViewItem } from '@skeletonlabs/skeleton'
	import { ProgressRadial } from '@skeletonlabs/skeleton'
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
          <div class="w-full flex flex-direction-row items-center gap-2">
            Score:
            <ProgressRadial width="w-9" font={180} value={vectorSimilarity(item.score)}>{vectorSimilarity(item.score)}%</ProgressRadial>
          </div>
          {#if item.metadata.header}
            <p class="font-bold">{item.metadata.header}</p>
          {/if}
          <p>{item.text}</p>
        </article>
      </svelte:fragment>
    </TreeViewItem>
  {/each}
</TreeView>
