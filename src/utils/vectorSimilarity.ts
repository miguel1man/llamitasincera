const vectorSimilarity = (score: number) => {
  if (score > 50) {
    score = 50
  }
  const similarity = Number((100 - score * 2).toFixed(0))
  return similarity
}

export default vectorSimilarity
