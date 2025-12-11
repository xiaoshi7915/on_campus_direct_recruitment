/**
 * 系统消息相关API
 */
import request from './request'

/**
 * 获取系统消息列表
 */
export function getNotifications(params?: {
  page?: number
  page_size?: number
  is_read?: boolean
}) {
  return request.get('/api/v1/notifications', { params })
}

/**
 * 标记消息为已读
 */
export function markAsRead(messageId: string) {
  return request.post(`/api/v1/notifications/${messageId}/read`)
}

/**
 * 获取未读消息数量
 */
export function getUnreadCount() {
  return request.get('/api/v1/notifications/unread-count')
}

