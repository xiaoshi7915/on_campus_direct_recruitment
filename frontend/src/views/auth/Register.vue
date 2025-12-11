<template>
  <div class="register-container">
    <div class="register-box">
      <h2 class="text-2xl font-bold mb-6">用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
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
        <div class="form-group">
          <label for="password">密码</label>
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
        <div class="form-group">
          <label for="phone">手机号（可选）</label>
          <input
            id="phone"
            v-model="formData.phone"
            type="tel"
            class="form-input"
            placeholder="请输入手机号"
          />
        </div>
        <div class="form-group">
          <label for="email">邮箱（可选）</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            class="form-input"
            placeholder="请输入邮箱"
          />
        </div>
        <div class="form-group">
          <label for="user_type">用户类型</label>
          <select
            id="user_type"
            v-model="formData.user_type"
            required
            class="form-input"
          >
            <option value="">请选择用户类型</option>
            <option value="STUDENT">学生</option>
            <option value="TEACHER">教师</option>
            <option value="ENTERPRISE">企业</option>
            <option value="ADMIN">管理员</option>
          </select>
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <div class="mt-4 text-center">
        <router-link to="/login" class="text-blue-500">已有账号？立即登录</router-link>
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
  @apply flex items-center justify-center min-h-screen bg-gray-100;
}

.register-box {
  @apply bg-white p-8 rounded-lg shadow-md w-full max-w-md;
}

.register-box h2 {
  @apply text-gray-900;
}

.register-box h2 {
  @apply text-gray-900;
}

.form-group {
  @apply mb-4;
}

.form-group label {
  @apply block mb-2 text-gray-700 font-medium;
}

.form-input {
  @apply w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white;
}

.form-input::placeholder {
  @apply text-gray-400;
}

.form-input option {
  @apply text-gray-900 bg-white;
}

.btn-submit {
  @apply w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed;
}
</style>


