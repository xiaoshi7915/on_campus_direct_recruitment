/**
 * 职位相关API
 */
import request from './request'

// 职位接口类型定义
export interface Job {
  id: string
  enterprise_id: string
  enterprise_name?: string  // 企业名称
  enterprise_logo?: string  // 企业Logo
  enterprise_industry?: string  // 企业行业
  enterprise_scale?: string  // 企业规模
  title: string
  department?: string
  job_type?: string
  salary_min?: number
  salary_max?: number
  work_location?: string
  experience?: string  // 工作经验要求
  education?: string
  description: string
  requirements?: string
  status: string
  view_count: number
  apply_count: number
  tags?: string
  created_at: string
  updated_at: string
}

export interface JobListResponse {
  items: Job[]
  total: number
  page: number
  page_size: number
}

export interface JobCreateRequest {
  title: string
  department?: string
  job_type?: string
  salary_min?: number
  salary_max?: number
  work_location?: string
  experience?: string
  education?: string
  description: string
  requirements?: string
  tags?: string
}

export interface JobUpdateRequest extends Partial<JobCreateRequest> {
  status?: string
}

// 获取职位列表
export const getJobs = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
  location?: string
  job_type?: string
  status?: string
}): Promise<JobListResponse> => {
  return request.get('/jobs', { params })
}

// 获取职位详情
export const getJob = async (id: string): Promise<Job> => {
  return request.get(`/jobs/${id}`)
}

// 创建职位（企业）
export const createJob = async (data: JobCreateRequest): Promise<Job> => {
  return request.post('/jobs', data)
}

// 更新职位（企业）
export const updateJob = async (id: string, data: JobUpdateRequest): Promise<Job> => {
  return request.put(`/jobs/${id}`, data)
}

// 删除职位（企业）
export const deleteJob = async (id: string): Promise<void> => {
  return request.delete(`/jobs/${id}`)
}

