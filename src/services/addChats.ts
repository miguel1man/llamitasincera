import type { Chunk, Message, ResponseData } from '../types/index'
import { handleChatQuestion } from './apiChatLlama'
import { handleChatSources } from './apiChatSources'
import getSimilarEmbeddings from './apiSimilarEmbeddings'

export const addAnswer = async (
  chunks: Chunk[],
  userMessage: string,
  isShowSourcesMode: boolean,
  messageCounter: number,
  messages: Message[],
  newQuestionId: string,
  responseData: ResponseData | null,
  selectedModel: string,
  updatedChunks: string
): Promise<Message[]> => {
	messageCounter++

	if (isShowSourcesMode) {
		responseData = await getSimilarEmbeddings(userMessage, newQuestionId)
		updatedChunks = await handleChatSources(userMessage, selectedModel, chunks)
	} else {
		updatedChunks = await handleChatQuestion(userMessage, selectedModel, chunks)
	}

	const newAnswer: Message = {
		content: updatedChunks,
		isQuestion: false,
		id: newQuestionId
	}
	
	messages = [...messages, newAnswer]
	return messages
}

export const addQuestion = async (
  currentMessage: string,
  messageCounter: number,
  messages: Message[],
  newQuestionId: string
): Promise<Message[]> => {
  if (currentMessage.length === 0) return messages
	messageCounter++

	const newQuestion: Message = {
		content: currentMessage,
		isQuestion: true,
		id: newQuestionId
	}

	messages = [...messages, newQuestion]
	return messages
}
