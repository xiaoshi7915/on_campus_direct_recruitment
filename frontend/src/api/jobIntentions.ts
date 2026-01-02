/**
 * 求职意向相关API
 */
import request from './request'
import type { JobIntentionResponse, JobIntentionListResponse } from '../types/index'

/**
 * 获取求职意向列表
 */
export function getJobIntentions(params?: {
  page?: number
  page_size?: number
}) {
  return request.get<JobIntentionListResponse>('/job-intentions', { params })
}

/**
 * 获取求职意向详情
 */
export function getJobIntention(intentionId: string) {
  return request.get<JobIntentionResponse>(`/job-intentions/${intentionId}`)
}

/**
 * 创建求职意向
 */
export function createJobIntention(data: {
  // 旧字段（保留兼容性）
  job_type?: string
  industry?: string
  salary_expect?: number
  work_location?: string
  // 新字段
  job_type_list?: string[]
  industry_list?: string[]
  work_location_list?: string[]
  job_nature?: 'FULL_TIME' | 'PART_TIME'
  salary_min?: number  // 单位：千元/月
  salary_max?: number  // 单位：千元/月
  part_time_days?: string
  work_time_slot?: string
}) {
  return request.post<JobIntentionResponse>('/job-intentions', data)
}

/**
 * 更新求职意向
 */
export function updateJobIntention(intentionId: string, data: {
  // 旧字段（保留兼容性）
  job_type?: string
  industry?: string
  salary_expect?: number
  work_location?: string
  // 新字段
  job_type_list?: string[]
  industry_list?: string[]
  work_location_list?: string[]
  job_nature?: 'FULL_TIME' | 'PART_TIME'
  salary_min?: number  // 单位：千元/月
  salary_max?: number  // 单位：千元/月
  part_time_days?: string
  work_time_slot?: string
}) {
  return request.put<JobIntentionResponse>(`/job-intentions/${intentionId}`, data)
}

/**
 * 删除求职意向
 */
export function deleteJobIntention(intentionId: string) {
  return request.delete(`/job-intentions/${intentionId}`)
}

