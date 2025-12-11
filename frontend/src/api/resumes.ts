/**
 * 简历相关API
 */
import request from './request'

// 简历接口类型定义
export interface Resume {
  id: string
  student_id: string
  title: string
  content: string
  is_default: boolean
  view_count: number
  download_count: number
  created_at: string
  updated_at: string
}

export interface ResumeListResponse {
  items: Resume[]
  total: number
  page: number
  page_size: number
}

export interface ResumeCreateRequest {
  title: string
  content: string
  is_default?: boolean
}

export interface ResumeUpdateRequest {
  title?: string
  content?: string
  is_default?: boolean
}

// 获取简历列表
export const getResumes = async (params?: {
  page?: number
  page_size?: number
  student_id?: string
}): Promise<ResumeListResponse> => {
  return request.get('/resumes', { params })
}

// 获取简历详情
export const getResume = async (id: string): Promise<Resume> => {
  return request.get(`/resumes/${id}`)
}

// 创建简历
export const createResume = async (data: ResumeCreateRequest): Promise<Resume> => {
  return request.post('/resumes', data)
}

// 更新简历
export const updateResume = async (id: string, data: ResumeUpdateRequest): Promise<Resume> => {
  return request.put(`/resumes/${id}`, data)
}

// 删除简历
export const deleteResume = async (id: string): Promise<void> => {
  return request.delete(`/resumes/${id}`)
}

