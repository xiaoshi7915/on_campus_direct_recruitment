/**
 * 认证相关API
 */
import request from './request'
import axios from 'axios'

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
  
  // 使用axios直接发送，因为request封装默认使用JSON
  return axios.post('/api/v1/auth/login', formData.toString(), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  }).then(response => response.data)
}

/**
 * 刷新令牌
 */
export const refreshToken = (refreshToken: string) => {
  return request.post('/auth/refresh', { refresh_token: refreshToken })
}


