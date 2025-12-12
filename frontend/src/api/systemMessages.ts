/**
 * 系统消息相关API
 */
import request from './request'

// 系统消息接口类型定义
export interface SystemMessage {
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

// 系统消息列表响应
export interface SystemMessageListResponse {
  items: SystemMessage[]
  total: number
  page: number
  page_size: number
}

// 未读消息数量响应
export interface UnreadCountResponse {
  unread_count: number
}

// 获取系统消息列表
export const getSystemMessages = async (params?: {
  page?: number
  page_size?: number
  is_read?: boolean
}): Promise<SystemMessageListResponse> => {
  return request.get('/system-messages', { params })
}

// 标记系统消息为已读
export const markMessageRead = async (messageId: string): Promise<{ message: string }> => {
  return request.post(`/system-messages/${messageId}/read`)
}

// 标记所有系统消息为已读
export const markAllMessagesRead = async (): Promise<{ message: string }> => {
  return request.post('/system-messages/read-all')
}

// 获取未读系统消息数量
export const getUnreadCount = async (): Promise<UnreadCountResponse> => {
  return request.get('/system-messages/unread-count')
}

// 创建系统消息（仅管理员）
export const createSystemMessage = async (data: {
  receiver_id: string
  content: string
  title?: string
}): Promise<SystemMessage> => {
  return request.post('/system-messages', {
    params: {
      receiver_id: data.receiver_id,
      content: data.content,
      title: data.title
    }
  })
}
