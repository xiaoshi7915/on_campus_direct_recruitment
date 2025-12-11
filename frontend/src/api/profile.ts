/**
 * 用户档案相关API
 */
import request from './request'

// 学生档案接口类型定义
export interface StudentProfile {
  id: string
  user_id: string
  real_name: string
  student_id?: string
  school_id?: string
  department_id?: string
  class_id?: string
  grade?: string
  major?: string
  avatar_url?: string
  school_name?: string
  department_name?: string
  phone?: string
  email?: string
  created_at: string
  updated_at: string
}

// 企业档案接口类型定义
export interface EnterpriseProfile {
  id: string
  user_id: string
  company_name: string
  unified_code?: string
  legal_person?: string
  industry?: string
  scale?: string
  address?: string
  website?: string
  logo_url?: string
  description?: string
  is_verified: boolean
  created_at: string
  updated_at: string
}

// 教师档案接口类型定义
export interface TeacherProfile {
  id: string
  user_id: string
  real_name: string
  school_id?: string
  department_id?: string
  title?: string
  position?: string
  teaching_major?: string
  teaching_grade?: string
  avatar_url?: string
  school_name?: string
  department_name?: string
  phone?: string
  email?: string
  created_at: string
  updated_at: string
}

// 获取学生档案
export const getStudentProfile = async (userId?: string): Promise<StudentProfile> => {
  const params = userId ? { user_id: userId } : {}
  return request.get('/profile/student', { params })
}

// 创建学生档案
export const createStudentProfile = async (data: Partial<StudentProfile>): Promise<StudentProfile> => {
  return request.post('/profile/student', data)
}

// 更新学生档案
export const updateStudentProfile = async (data: Partial<StudentProfile>): Promise<StudentProfile> => {
  return request.put('/profile/student', data)
}

// 获取企业档案
export const getEnterpriseProfile = async (userId?: string): Promise<EnterpriseProfile> => {
  const params = userId ? { user_id: userId } : {}
  return request.get('/profile/enterprise', { params })
}

// 创建企业档案
export const createEnterpriseProfile = async (data: Partial<EnterpriseProfile>): Promise<EnterpriseProfile> => {
  return request.post('/profile/enterprise', data)
}

// 更新企业档案
export const updateEnterpriseProfile = async (data: Partial<EnterpriseProfile>): Promise<EnterpriseProfile> => {
  return request.put('/profile/enterprise/me', data)
}

// 获取教师档案
export const getTeacherProfile = async (userId?: string): Promise<TeacherProfile> => {
  const params = userId ? { user_id: userId } : {}
  return request.get('/profile/teacher', { params })
}

// 创建教师档案
export const createTeacherProfile = async (data: Partial<TeacherProfile>): Promise<TeacherProfile> => {
  return request.post('/profile/teacher', data)
}

// 更新教师档案
export const updateTeacherProfile = async (data: Partial<TeacherProfile>): Promise<TeacherProfile> => {
  return request.put('/profile/teacher/me', data)
}


