/**
 * 行业职位类型维表相关API
 */
import request from './request'

export interface IndustryCategory {
  id: string
  name: string
  code?: string
  sort_order: number
}

export interface SubIndustry {
  id: string
  category_id: string
  name: string
  code?: string
  sort_order: number
}

export interface JobType {
  id: string
  category_id?: string
  sub_industry_id?: string
  name: string
  code?: string
  description?: string
  sort_order: number
}

export interface IndustryCategoryListResponse {
  items: IndustryCategory[]
  total: number
  page: number
  page_size: number
}

export interface SubIndustryListResponse {
  items: SubIndustry[]
  total: number
  page: number
  page_size: number
}

export interface JobTypeListResponse {
  items: JobType[]
  total: number
  page: number
  page_size: number
}

/**
 * 获取所有行业分类（一级行业）
 */
export function getIndustryCategories(params?: {
  page?: number
  page_size?: number
}) {
  return request.get<IndustryCategory[]>('/industry-job-types/industry-categories', { params })
}

/**
 * 获取细分行业（二级行业）
 */
export function getSubIndustries(params?: {
  category_id?: string
  page?: number
  page_size?: number
}) {
  return request.get<SubIndustry[]>('/industry-job-types/sub-industries', { params })
}

/**
 * 获取职位类型
 */
export function getJobTypes(params?: {
  category_id?: string
  sub_industry_id?: string
  page?: number
  page_size?: number
}) {
  return request.get<JobType[]>('/industry-job-types/job-types', { params })
}

