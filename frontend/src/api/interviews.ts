/**
 * 面试相关API
 */
import request from './request'

// 面试接口类型定义
export interface Interview {
  id: string
  application_id: string
  enterprise_id: string
  student_id: string
  interview_type: string
  scheduled_time: string
  duration?: number
  location?: string
  meeting_url?: string
  status: string
  feedback?: string
  created_at: string
  updated_at: string
}

export interface InterviewListResponse {
  items: Interview[]
  total: number
  page: number
  page_size: number
}

export interface InterviewCreateRequest {
  application_id: string
  interview_type: string
  scheduled_time: string
  duration?: number
  location?: string
  meeting_url?: string
}

export interface InterviewUpdateRequest {
  interview_type?: string
  scheduled_time?: string
  duration?: number
  location?: string
  meeting_url?: string
  status?: string
  feedback?: string
}

// 获取面试列表
export const getInterviews = async (params?: {
  page?: number
  page_size?: number
  enterprise_id?: string
  student_id?: string
  status?: string
}): Promise<InterviewListResponse> => {
  return request.get('/interviews', { params })
}

// 获取面试详情
export const getInterview = async (id: string): Promise<Interview> => {
  return request.get(`/interviews/${id}`)
}

// 创建面试
export const createInterview = async (data: InterviewCreateRequest): Promise<Interview> => {
  return request.post('/interviews', data)
}

// 更新面试
export const updateInterview = async (id: string, data: InterviewUpdateRequest): Promise<Interview> => {
  return request.put(`/interviews/${id}`, data)
}

// 取消面试
export const cancelInterview = async (id: string): Promise<void> => {
  return request.delete(`/interviews/${id}`)
}


