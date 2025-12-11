/**
 * 企业相关API
 */
import request from './request'
import { type EnterpriseProfile } from './profile'

export interface EnterpriseListResponse {
  items: EnterpriseProfile[]
  total: number
  page: number
  page_size: number
}

// 获取企业列表
export const getEnterprises = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
}): Promise<EnterpriseListResponse> => {
  return request.get('/enterprises/list', { params })
}

