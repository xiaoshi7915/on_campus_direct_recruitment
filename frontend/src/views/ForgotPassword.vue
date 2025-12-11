<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">忘记密码</h2>
      
      <!-- 第一步：输入手机号/邮箱/用户名 -->
      <div v-if="step === 1">
        <form @submit.prevent="handleSendCode" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">手机号/邮箱/用户名</label>
            <input
              v-model="form.identifier"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入手机号、邮箱或用户名"
            />
          </div>
          
          <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
          <div v-if="success" class="text-green-600 text-sm">
            {{ success }}
            <div v-if="verificationCode" class="mt-2 p-2 bg-gray-100 rounded">
              <strong>验证码（开发模式）:</strong> {{ verificationCode }}
            </div>
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {{ loading ? '发送中...' : '发送验证码' }}
          </button>
        </form>
      </div>
      
      <!-- 第二步：输入验证码和新密码 -->
      <div v-if="step === 2">
        <form @submit.prevent="handleResetPassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">验证码</label>
            <input
              v-model="form.verification_code"
              type="text"
              required
              maxlength="6"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入6位验证码"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">新密码</label>
            <input
              v-model="form.new_password"
              type="password"
              required
              minlength="6"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入新密码（至少6位）"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
            <input
              v-model="form.confirm_password"
              type="password"
              required
              minlength="6"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请再次输入新密码"
            />
          </div>
          
          <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
          <div v-if="success" class="text-green-600 text-sm">{{ success }}</div>
          
          <div class="flex space-x-3">
            <button
              type="button"
              @click="step = 1"
              class="flex-1 py-2 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
            >
              返回
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
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


