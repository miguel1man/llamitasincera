import type { Chunk, Message, ResponseData } from '../types/index'
import { handleChatQuestion } from './apiChatLlama'
import { handleChatSources } from './apiChatSources'
import getSimilarEmbeddings from './apiSimilarEmbeddings'

export const addAnswer = async (
  chunks: Chunk[],
  currentMessage: string,
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
		responseData = await getSimilarEmbeddings(currentMessage, newQuestionId)
		updatedChunks = await handleChatSources(currentMessage, selectedModel, chunks)
	} else {
		updatedChunks = await handleChatQuestion(currentMessage, selectedModel, chunks)
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
