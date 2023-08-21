import { toastStore } from '@skeletonlabs/skeleton'
	import type { ToastSettings } from '@skeletonlabs/skeleton'

export default function toastChat(foo: number): void {
  const t: ToastSettings = {
    message: 'Reading sources to elaborate an answer: ' + foo ,
    timeout: 10000
  }
  toastStore.trigger(t)
}