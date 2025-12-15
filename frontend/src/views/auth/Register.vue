<template>
  <div class="register-container min-h-screen flex items-center justify-center py-12 px-4">
    <div class="register-box w-full max-w-md">
      <!-- Logo和标题 -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl mb-4 shadow-lg">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-gray-900 mb-2">创建账户</h2>
        <p class="text-gray-600">注册新账户以开始使用</p>
      </div>

      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister" class="space-y-5">
        <div class="form-group">
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
            用户名 <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              minlength="3"
              class="form-input"
              placeholder="请输入用户名（至少3个字符）"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            密码 <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              minlength="6"
              class="form-input"
              placeholder="请输入密码（至少6个字符）"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
            手机号（可选）
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
            <input
              id="phone"
              v-model="formData.phone"
              type="tel"
              class="form-input"
              placeholder="请输入手机号"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            邮箱（可选）
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="form-input"
              placeholder="请输入邮箱"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="user_type" class="block text-sm font-medium text-gray-700 mb-2">
            用户类型 <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <select
              id="user_type"
              v-model="formData.user_type"
              required
              class="form-input pl-10 appearance-none"
            >
              <option value="">请选择用户类型</option>
              <option value="STUDENT">学生</option>
              <option value="TEACHER">教师</option>
              <option value="ENTERPRISE">企业</option>
              <option value="ADMIN">管理员</option>
            </select>
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>

        <button
          type="submit"
          class="btn-submit w-full"
          :disabled="loading"
        >
          <span v-if="loading" class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            注册中...
          </span>
          <span v-else class="flex items-center justify-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            注册
          </span>
        </button>
      </form>

      <!-- 登录链接 -->
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          已有账号？
          <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-semibold">
            立即登录
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register, type RegisterRequest } from '@/api/auth'

const router = useRouter()

// 表单数据
const formData = ref<RegisterRequest>({
  username: '',
  password: '',
  phone: '',
  email: '',
  user_type: 'STUDENT',
})

// 加载状态
const loading = ref(false)

// 处理注册
const handleRegister = async () => {
  loading.value = true
  try {
    // 清理空字符串，转换为undefined（可选字段）
    const submitData = {
      username: formData.value.username,
      password: formData.value.password,
      user_type: formData.value.user_type,
      phone: formData.value.phone?.trim() || undefined,
      email: formData.value.email?.trim() || undefined,
    }
    
    await register(submitData)
    alert('注册成功，请登录')
    router.push('/login')
  } catch (error: any) {
    console.error('注册失败:', error)
    
    // 处理错误信息显示
    let errorMessage = '注册失败，请重试'
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData === 'string') {
        errorMessage = errorData
      } else if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Pydantic验证错误
          errorMessage = errorData.detail.map((err: any) => {
            const field = err.loc?.join('.') || '字段'
            return `${field}: ${err.msg}`
          }).join('\n')
        } else {
          errorMessage = errorData.detail
        }
      } else if (errorData.message) {
        errorMessage = errorData.message
      }
    } else if (error.message) {
      errorMessage = error.message
    }
    
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  background: linear-gradient(135deg, #f9fafb 0%, #e5e7eb 100%);
}

.register-box {
  @apply bg-white p-8 rounded-2xl border border-gray-100;
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.15);
}

.form-input {
  @apply w-full py-3 pr-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200;
  padding-left: 3.75rem; /* 60px - 确保图标和文字不重合 */
}

.form-input::placeholder {
  @apply text-gray-400;
}

.form-input option {
  @apply text-gray-900 bg-white;
}

.btn-submit {
  background-color: #2563eb;
  color: white;
  border-radius: 0.75rem;
  font-weight: 600;
  padding: 0.875rem 1.5rem;
  min-height: 3rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background-color: #1d4ed8;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>


