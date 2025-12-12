/**
 * 学校相关API
 */
import request from './request'

// 学校接口类型定义
export interface School {
  id: string
  name: string
  code?: string
  province?: string
  city?: string
  address?: string
  website?: string
  logo_url?: string
  description?: string
  is_verified: boolean
  created_at: string
  updated_at: string
  student_count?: number
  department_count?: number
}

export interface SchoolListResponse {
  items: School[]
  total: number
  page: number
  page_size: number
}

export interface SchoolShareLink {
  school_id: string
  school_name: string
  share_url: string
  share_text: string
  share_image?: string
}

export interface OfflineInfoSessionRequest {
  school_id: string
  title: string
  description?: string
  proposed_start_time: string
  proposed_end_time: string
  proposed_location?: string
  max_students?: number
  contact_person?: string
  contact_phone?: string
  contact_email?: string
  message?: string
}

// 获取学校列表
export const getSchools = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
  province?: string
  city?: string
  is_verified?: boolean
}): Promise<SchoolListResponse> => {
  return request.get('/schools', { params })
}

// 获取学校详情
export const getSchool = async (id: string): Promise<School> => {
  return request.get(`/schools/${id}`)
}

// 获取学校分享链接
export const getSchoolShareLink = async (schoolId: string): Promise<SchoolShareLink> => {
  return request.get(`/schools/${schoolId}/share-link`)
}

// 申请线下宣讲会
export const requestOfflineInfoSession = async (schoolId: string, data: OfflineInfoSessionRequest): Promise<{
  message: string
  info_session_id: string
  status: string
}> => {
  return request.post(`/schools/${schoolId}/request-info-session`, data)
}

// 获取我的学校（仅限教师）
export const getMySchool = async (): Promise<School> => {
  return request.get('/schools/my-school')
}

// 学校实名认证请求
export interface SchoolVerificationRequest {
  verification_documents?: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
}

// 申请学校实名认证（仅限教师）
export const requestSchoolVerification = async (data: SchoolVerificationRequest): Promise<School> => {
  return request.post('/schools/my-school/verify', data)
}
