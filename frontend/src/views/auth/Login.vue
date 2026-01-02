<template>
  <div class="login-container min-h-screen flex items-center justify-center py-12 px-4 relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-200/20 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-warm-200/20 rounded-full blur-3xl"></div>
    </div>
    
    <div class="login-box w-full max-w-md relative z-10 animate-fade-in-up">
      <!-- 返回首页按钮 -->
      <div class="mb-6">
        <router-link
          to="/"
          class="inline-flex items-center text-gray-600 hover:text-gray-900 transition-colors font-medium"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回首页
        </router-link>
      </div>
      
      <!-- Logo和标题 -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-primary rounded-3xl mb-6 shadow-xl transform hover:scale-105 transition-transform">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
        <h2 class="text-4xl font-display font-bold text-gray-900 mb-3">校园直聘，欢迎您</h2>
        <p class="text-gray-600 text-lg">登录您的账户以继续</p>
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div class="form-group">
          <label for="username" class="block text-sm font-semibold text-gray-700 mb-3">
            用户名/手机号/邮箱
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              class="form-input"
              placeholder="请输入用户名、手机号或邮箱"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="password" class="block text-sm font-semibold text-gray-700 mb-3">
            密码
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="form-input"
              placeholder="请输入密码"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <router-link to="/forgot-password" class="text-sm text-blue-600 hover:text-blue-700 font-medium">
            忘记密码？
          </router-link>
        </div>

        <button
          type="submit"
          class="btn-submit w-full relative overflow-hidden"
          :disabled="loading"
        >
          <span v-if="loading" class="flex items-center justify-center relative z-10">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            登录中...
          </span>
          <span v-else class="flex items-center justify-center relative z-10">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
            登录
          </span>
        </button>
      </form>

      <!-- 注册链接 -->
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          还没有账号？
          <router-link to="/register" class="text-blue-600 hover:text-blue-700 font-semibold">
            立即注册
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 表单数据
const formData = ref({
  username: '',
  password: '',
})

// 加载状态
const loading = ref(false)

// 处理登录
const handleLogin = async () => {
  loading.value = true
  try {
    await authStore.userLogin(formData.value)
    // 登录成功，根据用户类型跳转
    const userInfo = authStore.userInfo
    if (userInfo) {
      switch (userInfo.user_type) {
        case 'STUDENT':
          router.push('/student')
          break
        case 'ENTERPRISE':
          router.push('/enterprise')
          break
        case 'TEACHER':
          router.push('/teacher')
          break
        case 'ADMIN':
          router.push('/admin')
          break
        default:
          router.push('/')
      }
    } else {
      // 如果获取用户信息失败，跳转到首页
      router.push('/')
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    
    // 处理错误信息显示
    let errorMessage = '登录失败，请检查用户名和密码'
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
.login-container {
  background: var(--gradient-soft);
}

.login-box {
  @apply bg-white/95 backdrop-blur-md p-10 rounded-3xl border border-gray-100/50;
  box-shadow: 
    0 20px 60px -15px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.5);
}

.form-input {
  @apply w-full py-3.5 pr-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300;
  padding-left: 3.5rem;
}

.form-input:hover {
  @apply border-primary-300;
}

.form-input::placeholder {
  @apply text-gray-400;
}

.btn-submit {
  background: var(--gradient-primary);
  color: white;
  border-radius: 1rem;
  font-weight: 600;
  padding: 1rem 1.5rem;
  min-height: 3.5rem;
  box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-submit::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.btn-submit:hover:not(:disabled)::before {
  left: 100%;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px -5px rgba(79, 70, 229, 0.5);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
</style>


