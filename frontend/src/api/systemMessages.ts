/**
 * 系统消息相关API
 */
import request from './request'

export interface SystemMessage {
  id: string
  content: string
  is_read: boolean
  created_at: string
}

export interface SystemMessageListResponse {
  items: SystemMessage[]
  total: number
  page: number
  page_size: number
}

/**
 * 获取系统消息列表
 */
export function getSystemMessages(params?: {
  page?: number
  page_size?: number
  is_read?: boolean
}) {
  return request.get<SystemMessageListResponse>('/system-messages', { params })
}

/**
 * 标记消息为已读
 */
export function markMessageRead(messageId: string) {
  return request.post(`/system-messages/${messageId}/read`)
}

/**
 * 标记所有消息为已读
 */
export function markAllMessagesRead() {
  return request.post('/system-messages/read-all')
}

