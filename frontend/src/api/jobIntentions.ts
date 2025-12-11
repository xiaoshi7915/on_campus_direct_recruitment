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
  job_type?: string
  industry?: string
  salary_expect?: number
  work_location?: string
}) {
  return request.post<JobIntentionResponse>('/job-intentions', data)
}

/**
 * 更新求职意向
 */
export function updateJobIntention(intentionId: string, data: {
  job_type?: string
  industry?: string
  salary_expect?: number
  work_location?: string
}) {
  return request.put<JobIntentionResponse>(`/job-intentions/${intentionId}`, data)
}

/**
 * 删除求职意向
 */
export function deleteJobIntention(intentionId: string) {
  return request.delete(`/job-intentions/${intentionId}`)
}

