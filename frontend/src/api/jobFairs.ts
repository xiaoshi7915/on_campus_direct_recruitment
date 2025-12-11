/**
 * 双选会相关API
 */
import request from './request'

// 双选会接口类型定义
export interface JobFair {
  id: string
  school_id?: string
  title: string
  description?: string
  start_time: string
  end_time: string
  location?: string
  status: string
  max_enterprises?: number
  created_at: string
  updated_at: string
}

export interface JobFairListResponse {
  items: JobFair[]
  total: number
  page: number
  page_size: number
}

export interface JobFairCreateRequest {
  school_id?: string
  title: string
  description?: string
  start_time: string
  end_time: string
  location?: string
  max_enterprises?: number
}

// 获取双选会列表
export const getJobFairs = async (params?: {
  page?: number
  page_size?: number
  school_id?: string
  status?: string
}): Promise<JobFairListResponse> => {
  return request.get('/job-fairs', { params })
}

// 创建双选会
export const createJobFair = async (data: JobFairCreateRequest): Promise<JobFair> => {
  return request.post('/job-fairs', data)
}

// 获取双选会详情
export const getJobFair = async (id: string): Promise<JobFair> => {
  return request.get(`/job-fairs/${id}`)
}

// 报名双选会
export const registerJobFair = async (jobFairId: string): Promise<void> => {
  return request.post(`/job-fairs/${jobFairId}/register`)
}

// 更新双选会
export const updateJobFair = async (id: string, data: Partial<JobFairCreateRequest>): Promise<JobFair> => {
  return request.put(`/job-fairs/${id}`, data)
}

// 删除双选会
export const deleteJobFair = async (id: string): Promise<void> => {
  return request.delete(`/job-fairs/${id}`)
}

// 获取双选会报名列表
export interface JobFairRegistration {
  id: string
  job_fair_id: string
  enterprise_id: string
  enterprise_name?: string
  enterprise_detail?: {
    id?: string
    company_name?: string
    industry?: string
    scale?: string
    address?: string
    website?: string
    description?: string
  }
  status: string
  check_in_time?: string
  created_at: string
}

export const getJobFairRegistrations = async (jobFairId: string): Promise<JobFairRegistration[]> => {
  return request.get(`/job-fairs/${jobFairId}/registrations`)
}

// 企业双选会签到
export const checkInJobFair = async (jobFairId: string): Promise<JobFairRegistration> => {
  return request.post(`/job-fairs/${jobFairId}/check-in`)
}

// 获取企业报名的双选会列表
export const getMyJobFairRegistrations = async (params?: {
  page?: number
  page_size?: number
}): Promise<JobFairListResponse> => {
  return request.get('/job-fairs/my-registrations', { params })
}

// 邀请企业参加双选会
export const inviteEnterpriseToJobFair = async (jobFairId: string, enterpriseId: string): Promise<JobFairRegistration> => {
  return request.post(`/job-fairs/${jobFairId}/invite?enterprise_id=${enterpriseId}`)
}

