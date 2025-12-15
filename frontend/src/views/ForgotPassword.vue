<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8 flex items-center justify-center">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
          <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
          </svg>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900">忘记密码</h2>
        <p class="mt-2 text-sm text-gray-600">请输入您的账号信息重置密码</p>
      </div>
      
      <!-- 第一步：输入手机号/邮箱/用户名 -->
      <div v-if="step === 1">
        <form @submit.prevent="handleSendCode" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              手机号/邮箱/用户名
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input
                v-model="form.identifier"
                type="text"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="请输入手机号、邮箱或用户名"
              />
            </div>
          </div>
          
          <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ error }}
          </div>
          <div v-if="success" class="p-3 bg-green-50 border border-green-200 rounded-xl text-green-700 text-sm">
            <div class="flex items-center mb-2">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ success }}
            </div>
            <div v-if="verificationCode" class="mt-2 p-2 bg-gray-100 rounded-lg text-xs">
              <strong>验证码（开发模式）:</strong> {{ verificationCode }}
            </div>
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <svg v-if="loading" class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            {{ loading ? '发送中...' : '发送验证码' }}
          </button>
        </form>
      </div>
      
      <!-- 第二步：输入验证码和新密码 -->
      <div v-if="step === 2">
        <form @submit.prevent="handleResetPassword" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              验证码
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                v-model="form.verification_code"
                type="text"
                required
                maxlength="6"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="请输入6位验证码"
              />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              新密码
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                v-model="form.new_password"
                type="password"
                required
                minlength="6"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="请输入新密码（至少6位）"
              />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              确认新密码
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <input
                v-model="form.confirm_password"
                type="password"
                required
                minlength="6"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="请再次输入新密码"
              />
            </div>
          </div>
          
          <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ error }}
          </div>
          <div v-if="success" class="p-3 bg-green-50 border border-green-200 rounded-xl text-green-700 text-sm flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ success }}
          </div>
          
          <div class="flex space-x-3 pt-2">
            <button
              type="button"
              @click="step = 1"
              class="flex-1 py-3 px-4 border-2 border-gray-300 text-gray-700 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              返回
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 py-3 px-4 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
            >
              <svg v-if="loading" class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ loading ? '重置中...' : '重置密码' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { forgotPassword, resetPassword } from '@/api/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

const step = ref(1) // 1: 发送验证码, 2: 重置密码
const form = ref({
  identifier: '', // 手机号/邮箱/用户名
  verification_code: '',
  new_password: '',
  confirm_password: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')
const verificationCode = ref('')
const identifierType = ref<'phone' | 'email' | 'username'>('username')

const handleSendCode = async () => {
  error.value = ''
  success.value = ''
  verificationCode.value = ''
  
  // 判断输入的是手机号、邮箱还是用户名
  const identifier = form.value.identifier.trim()
  let requestData: any = {}
  
  if (/^1[3-9]\d{9}$/.test(identifier)) {
    // 手机号
    identifierType.value = 'phone'
    requestData.phone = identifier
  } else if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identifier)) {
    // 邮箱
    identifierType.value = 'email'
    requestData.email = identifier
  } else {
    // 用户名
    identifierType.value = 'username'
    requestData.username = identifier
  }
  
  loading.value = true
  try {
    const response = await forgotPassword(requestData)
    success.value = response.message || '验证码已发送'
    if (response.code) {
      verificationCode.value = response.code // 开发模式返回验证码
    }
    step.value = 2 // 进入下一步
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || '发送验证码失败'
  } finally {
    loading.value = false
  }
}

const handleResetPassword = async () => {
  error.value = ''
  success.value = ''
  
  // 验证新密码长度
  if (form.value.new_password.length < 6) {
    error.value = '新密码至少需要6位字符'
    return
  }
  
  // 验证两次密码是否一致
  if (form.value.new_password !== form.value.confirm_password) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  loading.value = true
  try {
    const requestData: any = {
      verification_code: form.value.verification_code,
      new_password: form.value.new_password
    }
    
    // 根据类型添加对应的字段
    if (identifierType.value === 'phone') {
      requestData.phone = form.value.identifier.trim()
    } else if (identifierType.value === 'email') {
      requestData.email = form.value.identifier.trim()
    } else {
      requestData.username = form.value.identifier.trim()
    }
    
    await resetPassword(requestData)
    success.value = '密码重置成功！正在跳转到登录页...'
    // 3秒后跳转到登录页
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || '重置密码失败'
  } finally {
    loading.value = false
  }
}
</script>


