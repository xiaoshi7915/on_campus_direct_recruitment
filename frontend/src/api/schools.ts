/**
 * 学校管理相关API
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
}

export interface SchoolVerificationRequest {
  verification_documents?: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
}

// 获取当前教师所属的学校信息
export const getMySchool = async (): Promise<School> => {
  return request.get('/schools/my-school')
}

// 申请学校实名认证
export const requestSchoolVerification = async (data: SchoolVerificationRequest): Promise<School> => {
  return request.post('/schools/my-school/verify', data)
}




