/**
 * 标记相关API
 */
import request from './request'

// 标记接口类型定义
export interface Mark {
  id: string
  user_id: string
  target_type: string
  target_id: string
  note?: string
  color?: string
  created_at: string
  updated_at: string
}

export interface MarkListResponse {
  items: Mark[]
  total: number
  page: number
  page_size: number
}

export interface MarkCreateRequest {
  target_type: string
  target_id: string
  note?: string
  color?: string
}

export interface MarkUpdateRequest {
  note?: string
  color?: string
}

// 获取标记列表
export const getMarks = async (params?: {
  page?: number
  page_size?: number
  target_type?: string
}): Promise<MarkListResponse> => {
  return request.get('/marks', { params })
}

// 获取特定目标的标记
export const getMark = async (targetType: string, targetId: string): Promise<Mark> => {
  return request.get(`/marks/${targetType}/${targetId}`)
}

// 创建标记
export const createMark = async (data: MarkCreateRequest): Promise<Mark> => {
  return request.post('/marks', data)
}

// 更新标记
export const updateMark = async (id: string, data: MarkUpdateRequest): Promise<Mark> => {
  return request.put(`/marks/${id}`, data)
}

// 删除标记
export const deleteMark = async (id: string): Promise<void> => {
  return request.delete(`/marks/${id}`)
}



