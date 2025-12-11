/**
 * 学生点评相关API
 */
import request from './request'

// 学生点评接口类型定义
export interface StudentComment {
  id: string
  teacher_id: string
  student_id: string
  content: string
  score?: number
  tags?: string
  is_public: string
  created_at: string
  updated_at: string
  teacher_name?: string
  student_name?: string
}

export interface StudentCommentListResponse {
  items: StudentComment[]
  total: number
  page: number
  page_size: number
}

export interface StudentCommentCreate {
  student_id: string
  content: string
  score?: number
  tags?: string
  is_public?: string
}

export interface StudentCommentUpdate {
  content?: string
  score?: number
  tags?: string
  is_public?: string
}

// 获取学生点评列表
export const getStudentComments = async (params?: {
  page?: number
  page_size?: number
  student_id?: string
}): Promise<StudentCommentListResponse> => {
  return request.get('/student-comments', { params })
}

// 获取学生点评详情
export const getStudentComment = async (id: string): Promise<StudentComment> => {
  return request.get(`/student-comments/${id}`)
}

// 创建学生点评
export const createStudentComment = async (data: StudentCommentCreate): Promise<StudentComment> => {
  return request.post('/student-comments', data)
}

// 更新学生点评
export const updateStudentComment = async (id: string, data: StudentCommentUpdate): Promise<StudentComment> => {
  return request.put(`/student-comments/${id}`, data)
}

// 删除学生点评
export const deleteStudentComment = async (id: string): Promise<void> => {
  return request.delete(`/student-comments/${id}`)
}



