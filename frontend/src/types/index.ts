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
  // 旧字段（保留兼容性）
  job_type?: string
  industry?: string
  salary_expect?: number
  work_location?: string
  // 新字段
  job_type_list?: string  // JSON字符串
  industry_list?: string  // JSON字符串
  work_location_list?: string  // JSON字符串
  job_nature?: string  // FULL_TIME | PART_TIME
  salary_min?: number  // 单位：千元/月
  salary_max?: number  // 单位：千元/月
  part_time_days?: string
  work_time_slot?: string
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



