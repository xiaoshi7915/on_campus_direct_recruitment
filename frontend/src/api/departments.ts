/**
 * 院系管理相关API
 */
import request from './request'

// 院系接口类型定义
export interface Department {
  id: string
  school_id: string
  name: string
  code?: string
  description?: string
  honors?: string
  created_at: string
  updated_at: string
}

export interface DepartmentListResponse {
  items: Department[]
  total: number
  page: number
  page_size: number
}

export interface DepartmentCreate {
  name: string
  code?: string
  description?: string
  honors?: string
}

export interface DepartmentUpdate {
  name?: string
  code?: string
  description?: string
  honors?: string
}

// 获取院系列表
export const getDepartments = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
  school_id?: string
}): Promise<DepartmentListResponse> => {
  return request.get('/departments', { params })
}

// 获取院系详情
export const getDepartment = async (id: string): Promise<Department> => {
  return request.get(`/departments/${id}`)
}

// 创建院系
export const createDepartment = async (data: DepartmentCreate): Promise<Department> => {
  return request.post('/departments', data)
}

// 更新院系
export const updateDepartment = async (id: string, data: DepartmentUpdate): Promise<Department> => {
  return request.put(`/departments/${id}`, data)
}

// 删除院系
export const deleteDepartment = async (id: string): Promise<void> => {
  return request.delete(`/departments/${id}`)
}



