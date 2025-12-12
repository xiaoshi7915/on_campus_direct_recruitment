/**
 * 认证相关API
 */
import request from './request'

// 企业认证接口类型定义
export interface EnterpriseVerification {
  id: string
  enterprise_id: string
  status: string
  business_license_url?: string
  legal_person_id_front_url?: string
  legal_person_id_back_url?: string
  authorization_letter_url?: string
  other_documents?: string[]
  reviewer_id?: string
  review_comment?: string
  reviewed_at?: string
  created_at: string
  updated_at: string
}

export interface EnterpriseVerificationCreateRequest {
  business_license_url?: string
  legal_person_id_front_url?: string
  legal_person_id_back_url?: string
  authorization_letter_url?: string
  other_documents?: string[]
}

export interface EnterpriseVerificationUpdateRequest {
  status: string
  review_comment?: string
}

export interface EnterpriseVerificationListResponse {
  items: EnterpriseVerification[]
  total: number
  page: number
  page_size: number
}

// 个人身份认证接口类型定义
export interface PersonalVerification {
  id: string
  user_id: string
  user_type: string
  status: string
  id_card_front_url?: string
  id_card_back_url?: string
  real_name?: string
  id_card_number?: string
  other_documents?: string[]
  reviewer_id?: string
  review_comment?: string
  reviewed_at?: string
  created_at: string
  updated_at: string
}

export interface PersonalVerificationCreateRequest {
  id_card_front_url?: string
  id_card_back_url?: string
  real_name?: string
  id_card_number?: string
  other_documents?: string[]
}

export interface PersonalVerificationUpdateRequest {
  status: string
  review_comment?: string
}

export interface PersonalVerificationListResponse {
  items: PersonalVerification[]
  total: number
  page: number
  page_size: number
}

// 企业认证API
export const createEnterpriseVerification = async (data: EnterpriseVerificationCreateRequest): Promise<EnterpriseVerification> => {
  return request.post('/verifications/enterprise', data)
}

export const getEnterpriseVerifications = async (params?: {
  page?: number
  page_size?: number
  status?: string
}): Promise<EnterpriseVerificationListResponse> => {
  return request.get('/verifications/enterprise', { params })
}

export const getEnterpriseVerification = async (id: string): Promise<EnterpriseVerification> => {
  return request.get(`/verifications/enterprise/${id}`)
}

export const updateEnterpriseVerification = async (id: string, data: EnterpriseVerificationUpdateRequest): Promise<EnterpriseVerification> => {
  return request.put(`/verifications/enterprise/${id}`, data)
}

// 个人身份认证API
export const createPersonalVerification = async (data: PersonalVerificationCreateRequest): Promise<PersonalVerification> => {
  return request.post('/verifications/personal', data)
}

export const getPersonalVerifications = async (params?: {
  page?: number
  page_size?: number
  status?: string
}): Promise<PersonalVerificationListResponse> => {
  return request.get('/verifications/personal', { params })
}

export const updatePersonalVerification = async (id: string, data: PersonalVerificationUpdateRequest): Promise<PersonalVerification> => {
  return request.put(`/verifications/personal/${id}`, data)
}

