/**
 * 用户相关API
 */
import request from './request'

// 用户接口类型定义
export interface User {
  id: string
  username: string
  phone?: string
  email?: string
  user_type: string
  status: string
  created_at: string
  updated_at: string
}

// 获取当前用户信息
export const getCurrentUser = async (): Promise<User> => {
  return request.get('/users/me')
}

// 更新用户信息
export const updateUser = async (data: Partial<User>): Promise<User> => {
  return request.put('/users/me', data)
}

// 获取用户列表（管理员）
export interface GetUsersParams {
  page?: number
  page_size?: number
  keyword?: string
  user_type?: string
  status?: string
}

export interface UserListResponse {
  items: User[]
  total: number
  page: number
  page_size: number
}

export const getUsers = async (params?: GetUsersParams): Promise<UserListResponse> => {
  return request.get('/users', { params })
}

