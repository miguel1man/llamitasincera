const vectorSimilarity = (score: number): number => {
  const fib = [1, 6, 12, 18, 24, 30]
  const stars = [5, 4, 3, 2, 1, 0]

  for (let i = 0; i < fib.length; i++) {
    if (score < fib[i]) {
      return stars[i]
    }
  }

  return 0
}

export default vectorSimilarity
