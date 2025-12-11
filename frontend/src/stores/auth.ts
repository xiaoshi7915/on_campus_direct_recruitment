/**
 * 认证状态管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, type LoginRequest } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const userInfo = ref<any>(null)

  // 登录
  const userLogin = async (loginData: LoginRequest) => {
    try {
      const response = await login(loginData)
      token.value = response.access_token
      refreshToken.value = response.refresh_token
      
      // 保存到localStorage
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      
      // 获取用户信息
      await fetchUserInfo()
      
      return response
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const { getCurrentUser } = await import('@/api/users')
      userInfo.value = await getCurrentUser()
    } catch (error) {
      console.error('获取用户信息失败:', error)
      userInfo.value = null
    }
  }

  // 登出
  const userLogout = () => {
    token.value = null
    refreshToken.value = null
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  // 检查是否已登录
  const isAuthenticated = () => {
    return !!token.value
  }

  return {
    token,
    refreshToken,
    userInfo,
    userLogin,
    userLogout,
    isAuthenticated,
    fetchUserInfo,
  }
})


