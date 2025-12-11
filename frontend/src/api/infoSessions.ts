/**
 * 宣讲会相关API
 */
import request from './request'

// 宣讲会接口类型定义
export interface InfoSession {
  id: string
  enterprise_id: string
  school_id?: string
  title: string
  description?: string
  start_time: string
  end_time: string
  location?: string
  session_type: string
  live_url?: string
  status: string
  max_students?: number
  check_in_count: number
  created_at: string
  updated_at: string
}

export interface InfoSessionListResponse {
  items: InfoSession[]
  total: number
  page: number
  page_size: number
}

// 获取宣讲会列表
export const getInfoSessions = async (params?: {
  page?: number
  page_size?: number
  enterprise_id?: string
  school_id?: string
  status?: string
}): Promise<InfoSessionListResponse> => {
  return request.get('/info-sessions', { params })
}

// 创建宣讲会
export interface InfoSessionCreateRequest {
  school_id?: string
  title: string
  description?: string
  start_time: string
  end_time: string
  location?: string
  session_type: string
  live_url?: string
  max_students?: number
}

export const createInfoSession = async (data: InfoSessionCreateRequest): Promise<InfoSession> => {
  return request.post('/info-sessions', data)
}

// 获取宣讲会详情
export const getInfoSession = async (id: string): Promise<InfoSession> => {
  return request.get(`/info-sessions/${id}`)
}

// 报名宣讲会
export const registerInfoSession = async (sessionId: string): Promise<void> => {
  return request.post(`/info-sessions/${sessionId}/register`)
}

// 更新宣讲会
export const updateInfoSession = async (id: string, data: Partial<InfoSession>): Promise<InfoSession> => {
  return request.put(`/info-sessions/${id}`, data)
}

// 删除宣讲会
export const deleteInfoSession = async (id: string): Promise<void> => {
  return request.delete(`/info-sessions/${id}`)
}

// 获取宣讲会报名列表
export interface InfoSessionRegistration {
  id: string
  session_id: string
  student_id: string
  student_name?: string
  student_detail?: {
    id?: string
    name?: string
    student_id?: string
    major?: string
    grade?: string
  }
  status: string
  check_in_time?: string
  created_at: string
}

export const getInfoSessionRegistrations = async (sessionId: string): Promise<InfoSessionRegistration[]> => {
  return request.get(`/info-sessions/${sessionId}/registrations`)
}

