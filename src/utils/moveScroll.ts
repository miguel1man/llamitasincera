export default function moveScroll(container: HTMLDivElement) {
  container.scrollTo({
    top: container.scrollHeight,
    behavior: 'smooth',
  })
}
