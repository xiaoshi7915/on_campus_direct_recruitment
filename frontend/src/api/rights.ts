/**
 * 权益管理相关API（管理员端）
 */
import request from './request'

// 权益接口类型定义
export interface Right {
  id: string
  name: string
  code: string
  description?: string
  type: string
  value?: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface RightsListResponse {
  items: Right[]
  total: number
  page: number
  page_size: number
}

export interface RightsCreateRequest {
  name: string
  code: string
  description?: string
  type: string
  value?: number
  is_active?: boolean
}

export interface RightsUpdateRequest {
  name?: string
  description?: string
  type?: string
  value?: number
  is_active?: boolean
}

// 权益套餐接口类型定义
export interface RightsPackageItem {
  id: string
  package_id: string
  rights_id: string
  quantity: number
  created_at: string
}

export interface RightsPackage {
  id: string
  name: string
  description?: string
  price: number
  duration_days?: number
  is_active: boolean
  created_at: string
  updated_at: string
  items: RightsPackageItem[]
}

export interface RightsPackageListResponse {
  items: RightsPackage[]
  total: number
  page: number
  page_size: number
}

export interface RightsPackageItemCreate {
  rights_id: string
  quantity: number
}

export interface RightsPackageCreateRequest {
  name: string
  description?: string
  price: number
  duration_days?: number
  is_active?: boolean
  items: RightsPackageItemCreate[]
}

export interface RightsPackageUpdateRequest {
  name?: string
  description?: string
  price?: number
  duration_days?: number
  is_active?: boolean
}

// 获取权益列表
export const getRights = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
  type?: string
}): Promise<RightsListResponse> => {
  return request.get('/rights', { params })
}

// 创建权益
export const createRight = async (data: RightsCreateRequest): Promise<Right> => {
  return request.post('/rights', data)
}

// 更新权益
export const updateRight = async (id: string, data: RightsUpdateRequest): Promise<Right> => {
  return request.put(`/rights/${id}`, data)
}

// 删除权益
export const deleteRight = async (id: string): Promise<void> => {
  return request.delete(`/rights/${id}`)
}

// 获取权益套餐列表
export const getRightsPackages = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
}): Promise<RightsPackageListResponse> => {
  return request.get('/rights/packages', { params })
}

// 创建权益套餐
export const createRightsPackage = async (data: RightsPackageCreateRequest): Promise<RightsPackage> => {
  return request.post('/rights/packages', data)
}

// 更新权益套餐
export const updateRightsPackage = async (id: string, data: RightsPackageUpdateRequest): Promise<RightsPackage> => {
  return request.put(`/rights/packages/${id}`, data)
}

// 删除权益套餐
export const deleteRightsPackage = async (id: string): Promise<void> => {
  return request.delete(`/rights/packages/${id}`)
}


