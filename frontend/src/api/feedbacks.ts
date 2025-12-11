/**
 * 反馈建议相关API
 */
import request from './request'
import type { FeedbackResponse, FeedbackListResponse } from '../types/index'

/**
 * 获取反馈列表
 */
export function getFeedbacks(params?: {
  page?: number
  page_size?: number
  status?: string
}) {
  return request.get<FeedbackListResponse>('/feedbacks', { params })
}

/**
 * 获取反馈详情
 */
export function getFeedback(feedbackId: string) {
  return request.get<FeedbackResponse>(`/feedbacks/${feedbackId}`)
}

/**
 * 创建反馈
 */
export function createFeedback(data: {
  title: string
  content: string
  images?: string
}) {
  return request.post<FeedbackResponse>('/feedbacks', data)
}

