/**
 * 职位申请相关API
 */
import request from './request'

// 职位申请接口类型定义
export interface JobApplication {
  id: string
  job_id: string
  student_id: string
  enterprise_id: string
  resume_id?: string
  status: string
  message?: string
  created_at: string
  updated_at: string
  job_title?: string
  student_name?: string
}

export interface ApplicationListResponse {
  items: JobApplication[]
  total: number
  page: number
  page_size: number
}

export interface ApplicationCreateRequest {
  job_id: string
  resume_id?: string
  message?: string
}

export interface ApplicationUpdateRequest {
  status?: string
}

// 获取申请列表
export const getApplications = async (params?: {
  page?: number
  page_size?: number
  job_id?: string
  student_id?: string
  user_id?: string
  status?: string
}): Promise<ApplicationListResponse> => {
  return request.get('/applications', { params })
}

// 获取申请详情
export const getApplication = async (id: string): Promise<JobApplication> => {
  return request.get(`/applications/${id}`)
}

// 创建申请
export const createApplication = async (data: ApplicationCreateRequest): Promise<JobApplication> => {
  return request.post('/applications', data)
}

// 更新申请状态
export const updateApplication = async (id: string, data: ApplicationUpdateRequest): Promise<JobApplication> => {
  // 后端API使用Query参数传递status，而不是body
  // 验证status参数是否存在
  if (!data.status) {
    throw new Error('状态参数不能为空')
  }
  return request.put(`/applications/${id}?status=${encodeURIComponent(data.status)}`)
}

