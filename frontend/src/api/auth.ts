/**
 * 认证相关API
 */
import request, { requestForm } from './request'

// 注册接口
export interface RegisterRequest {
  username: string
  password: string
  phone?: string
  email?: string
  user_type: 'STUDENT' | 'TEACHER' | 'ENTERPRISE' | 'ADMIN'
}

// 登录接口
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

/**
 * 用户注册
 */
export const register = (data: RegisterRequest) => {
  return request.post('/auth/register', data)
}

/**
 * 用户登录
 * OAuth2登录需要使用表单数据格式
 */
export const login = (data: LoginRequest) => {
  // OAuth2登录接口需要表单数据格式
  const formData = new URLSearchParams()
  formData.append('username', data.username)
  formData.append('password', data.password)
  
  // 使用统一的表单请求封装
  return requestForm.post('/auth/login', formData.toString())
}

/**
 * 刷新令牌
 */
export const refreshToken = (refreshToken: string) => {
  return request.post('/auth/refresh', { refresh_token: refreshToken })
}

// 忘记密码请求
export interface ForgotPasswordRequest {
  phone?: string
  email?: string
  username?: string
}

// 重置密码请求
export interface ResetPasswordRequest {
  phone?: string
  email?: string
  username?: string
  verification_code: string
  new_password: string
}

// 修改密码请求
export interface ChangePasswordRequest {
  old_password: string
  new_password: string
}

/**
 * 忘记密码 - 发送验证码
 */
export const forgotPassword = (data: ForgotPasswordRequest) => {
  return request.post('/auth/forgot-password', data)
}

/**
 * 重置密码
 */
export const resetPassword = (data: ResetPasswordRequest) => {
  return request.post('/auth/reset-password', data)
}

/**
 * 修改密码（需要登录）
 */
export const changePassword = (data: ChangePasswordRequest) => {
  return request.post('/auth/change-password', data)
}

