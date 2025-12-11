<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="text-2xl font-bold mb-6">用户登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名/手机号/邮箱</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
            class="form-input"
            placeholder="请输入用户名、手机号或邮箱"
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
            class="form-input"
            placeholder="请输入密码"
          />
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <div class="mt-4 text-center">
        <router-link to="/register" class="text-blue-500">还没有账号？立即注册</router-link>
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
  @apply flex items-center justify-center min-h-screen bg-gray-100;
}

.login-box {
  @apply bg-white p-8 rounded-lg shadow-md w-full max-w-md;
}

.form-group {
  @apply mb-4;
}

.form-group label {
  @apply block mb-2 text-gray-700;
}

.form-input {
  @apply w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white;
}

.form-input::placeholder {
  @apply text-gray-400;
}

.login-box h2 {
  @apply text-gray-900;
}

.btn-submit {
  @apply w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed;
}
</style>


