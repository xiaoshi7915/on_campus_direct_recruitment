/**
 * 聊天相关API
 */
import request from './request'

// 消息接口类型定义
export interface Message {
  id: string
  session_id: string
  sender_id: string
  receiver_id: string
  content: string
  message_type: string
  file_url?: string
  is_read: boolean
  created_at: string
}

export interface ChatSession {
  id: string
  user1_id: string
  user2_id: string
  last_message_id?: string
  last_message_at?: string
  unread_count_user1: number
  unread_count_user2: number
  created_at: string
  updated_at: string
}

export interface MessageListResponse {
  items: Message[]
  total: number
  page: number
  page_size: number
}

export interface ChatSessionListResponse {
  items: ChatSession[]
  total: number
}

export interface MessageCreateRequest {
  receiver_id: string
  content: string
  message_type?: string
  file_url?: string
}

// 获取聊天会话列表
export const getChatSessions = async (): Promise<ChatSessionListResponse> => {
  return request.get('/chat/sessions')
}

// 创建或获取聊天会话
export const createOrGetChatSession = async (receiverId: string): Promise<ChatSession> => {
  // 使用URL参数传递receiver_id
  return request.post(`/chat/sessions?receiver_id=${encodeURIComponent(receiverId)}`)
}

// 获取会话消息列表
export const getSessionMessages = async (
  sessionId: string,
  params?: {
    page?: number
    page_size?: number
  }
): Promise<MessageListResponse> => {
  return request.get(`/chat/sessions/${sessionId}/messages`, { params })
}

// 发送消息
export const sendMessage = async (
  sessionId: string,
  data: MessageCreateRequest
): Promise<Message> => {
  return request.post(`/chat/sessions/${sessionId}/messages`, data)
}

// 标记消息为已读
export const markMessageAsRead = async (messageId: string): Promise<void> => {
  return request.post(`/chat/messages/${messageId}/read`)
}

