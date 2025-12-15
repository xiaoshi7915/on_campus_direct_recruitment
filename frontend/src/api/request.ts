/**
 * Axios请求封装
 * 包含请求重试机制和统一错误处理
 */
import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import { handleApiError } from '@/utils/errorHandler'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 发送表单数据请求（用于OAuth2登录等需要表单格式的接口）
 */
export const requestForm = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
})

// 为表单请求添加请求拦截器（添加token）
requestForm.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 为表单请求添加响应拦截器（统一错误处理）
requestForm.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error) => {
    handleApiError(error)
    return Promise.reject(error)
  }
)

// 请求重试配置
const MAX_RETRIES = 3
const RETRY_DELAY = 1000 // 1秒

/**
 * 判断是否应该重试请求
 */
function shouldRetry(error: AxiosError): boolean {
  // 网络错误或超时错误才重试
  if (!error.response) {
    return true
  }
  
  // 5xx服务器错误也重试
  const status = error.response.status
  return status >= 500 && status < 600
}

/**
 * 延迟函数
 */
function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * 请求重试拦截器
 */
service.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const config = error.config as InternalAxiosRequestConfig & { __retryCount?: number }
    
    // 初始化重试次数
    if (!config.__retryCount) {
      config.__retryCount = 0
    }
    
    // 判断是否应该重试
    if (config.__retryCount < MAX_RETRIES && shouldRetry(error)) {
      config.__retryCount += 1
      
      // 延迟后重试
      await delay(RETRY_DELAY * config.__retryCount) // 指数退避
      
      return service(config)
    }
    
    // 不再重试，返回错误
    return Promise.reject(error)
  }
)

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 从localStorage获取token并添加到请求头
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 如果响应成功，直接返回数据
    return response.data
  },
  (error) => {
    // 使用统一的错误处理
    handleApiError(error)
    return Promise.reject(error)
  }
)

export default service

