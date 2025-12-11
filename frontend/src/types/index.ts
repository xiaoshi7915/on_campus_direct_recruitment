/**
 * 类型定义
 */

// Offer相关类型
export interface OfferResponse {
  id: string
  application_id: string
  enterprise_id: string
  student_id: string
  job_title: string
  salary?: number
  start_date?: string
  content: string
  status: string
  expires_at?: string
  created_at: string
  updated_at: string
}

export interface OfferListResponse {
  items: OfferResponse[]
  total: number
  page: number
  page_size: number
}

// 求职意向相关类型
export interface JobIntentionResponse {
  id: string
  student_id: string
  job_type?: string
  industry?: string
  salary_expect?: number
  work_location?: string
  created_at: string
  updated_at: string
}

export interface JobIntentionListResponse {
  items: JobIntentionResponse[]
  total: number
  page: number
  page_size: number
}

// 反馈相关类型
export interface FeedbackResponse {
  id: string
  user_id: string
  user_type: string
  title: string
  content: string
  images?: string
  status: string
  reply?: string
  replied_at?: string
  created_at: string
  updated_at: string
}

export interface FeedbackListResponse {
  items: FeedbackResponse[]
  total: number
  page: number
  page_size: number
}


