<script lang="ts">
	let currentMessage = '';
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center space-y-20">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Chat with a llama</h2>
	</div>

	<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token">
		<button class="input-group-shim">+</button>
		<textarea
			bind:value={currentMessage}
			class="bg-transparent border-0 ring-0"
			name="prompt"
			id="prompt"
			placeholder="Write a message..."
			rows="1"
		/>
		<button class="variant-filled-primary">Send</button>
	</div>			
</div>