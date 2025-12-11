/**
 * 企业管理相关API
 */
import request from './request'

// 子账号接口类型定义
export interface EnterpriseSubAccount {
  id: string
  user_id: string
  company_name: string
  username?: string
  phone?: string
  email?: string
  is_main_account: boolean
  main_account_id?: string
  status?: string
  created_at: string
}

export interface EnterpriseSubAccountListResponse {
  items: EnterpriseSubAccount[]
  total: number
  page: number
  page_size: number
}

export interface SubAccountCreate {
  username: string
  password: string
  real_name: string
  phone?: string
  email?: string
  position?: string
}

// 人才库项类型定义
export interface TalentItem {
  student_id: string
  student_name: string
  student_phone?: string
  student_email?: string
  resume_id?: string
  resume_title?: string
  status: string  // ALL, FAVORITED, COMMUNICATING, INTERVIEWED, HIRED
  last_contact_time?: string
  application_id?: string
  interview_id?: string
  offer_id?: string
}

export interface TalentListResponse {
  items: TalentItem[]
  total: number
  page: number
  page_size: number
}

// 获取子账号列表
export const getSubAccounts = async (params?: {
  page?: number
  page_size?: number
}): Promise<EnterpriseSubAccountListResponse> => {
  return request.get('/enterprise-management/sub-accounts', { params })
}

// 创建子账号
export const createSubAccount = async (data: SubAccountCreate): Promise<EnterpriseSubAccount> => {
  return request.post('/enterprise-management/sub-accounts', data)
}

// 删除子账号
export const deleteSubAccount = async (subAccountId: string): Promise<void> => {
  return request.delete(`/enterprise-management/sub-accounts/${subAccountId}`)
}

// 获取人才库列表
export const getTalents = async (params?: {
  page?: number
  page_size?: number
  status_filter?: string
  keyword?: string
}): Promise<TalentListResponse> => {
  return request.get('/enterprise-management/talents', { params })
}

