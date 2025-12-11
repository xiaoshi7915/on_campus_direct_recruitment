/**
 * 教师管理相关API
 */
import request from './request'

// 教师接口类型定义
export interface Teacher {
  id: string
  user_id: string
  real_name: string
  username?: string
  phone?: string
  email?: string
  school_id?: string
  department_id?: string
  title?: string
  position?: string
  is_main_account: boolean
  main_account_id?: string
  status?: string
  created_at: string
}

export interface TeacherListResponse {
  items: Teacher[]
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
  title?: string
  position?: string
}

export interface TeacherApprovalRequest {
  action: string  // APPROVE 或 REJECT
  comment?: string
}

export interface PermissionTransferRequest {
  target_teacher_id: string
  transfer_students?: string[]
}

export interface ClassTransferRequest {
  target_teacher_id: string
  class_ids: string[]
}

// 获取子账号列表
export const getSubAccounts = async (params?: {
  page?: number
  page_size?: number
}): Promise<TeacherListResponse> => {
  return request.get('/teacher-management/sub-accounts', { params })
}

// 创建子账号
export const createSubAccount = async (data: SubAccountCreate): Promise<Teacher> => {
  return request.post('/teacher-management/sub-accounts', data)
}

// 删除子账号
export const deleteSubAccount = async (subAccountId: string): Promise<void> => {
  return request.delete(`/teacher-management/sub-accounts/${subAccountId}`)
}

// 获取待审批教师列表（管理员）
export const getPendingTeacherApprovals = async (params?: {
  page?: number
  page_size?: number
}): Promise<TeacherListResponse> => {
  return request.get('/teacher-management/pending-approvals', { params })
}

// 审批教师注册（管理员）
export const approveTeacherRegistration = async (teacherId: string, data: TeacherApprovalRequest): Promise<{ success: boolean; message: string }> => {
  return request.post(`/teacher-management/${teacherId}/approve`, data)
}

// 权限移交
export const transferPermission = async (data: PermissionTransferRequest): Promise<{ success: boolean; message: string }> => {
  return request.post('/teacher-management/permission-transfer', data)
}

// 班级移交
export const transferClass = async (data: ClassTransferRequest): Promise<{ success: boolean; message: string }> => {
  return request.post('/teacher-management/class-transfer', data)
}



