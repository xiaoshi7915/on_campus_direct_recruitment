/**
 * 学生管理相关API（教师端）
 */
import request from './request'

// 学生接口类型定义
export interface Student {
  id: string
  user_id: string
  real_name: string
  student_id?: string
  grade?: string
  major?: string
  school_id?: string
  department_id?: string
  resume_count: number
  application_count: number
  created_at: string
  updated_at: string
}

export interface StudentListResponse {
  items: Student[]
  total: number
  page: number
  page_size: number
}

// 获取学生列表
export const getStudents = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
  grade?: string
  major?: string
  department_id?: string
}): Promise<StudentListResponse> => {
  return request.get('/students', { params })
}

// 获取学生详情
export const getStudent = async (id: string): Promise<Student> => {
  return request.get(`/students/${id}`)
}

// 移除学生（从管辖范围内移除）
export const removeStudent = async (id: string): Promise<void> => {
  return request.delete(`/students/${id}`)
}


