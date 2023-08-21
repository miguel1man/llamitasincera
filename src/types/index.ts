type Chunk = string

interface Content {
  metadata: Metadata
  score: number
  text: string
}

interface Message {
  id: string
  isQuestion: boolean
  content: string
}

interface Metadata {
  file: string
  header?: string
}

interface ResponseData {
  content: Content[]
  id: string
}

export type { Chunk, Content, Message, Metadata, ResponseData }