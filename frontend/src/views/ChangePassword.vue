<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">修改密码</h2>
      
      <form @submit.prevent="handleChangePassword" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">旧密码</label>
          <input
            v-model="form.old_password"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入旧密码"
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
        
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {{ loading ? '修改中...' : '修改密码' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { changePassword } from '@/api/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const handleChangePassword = async () => {
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
    await changePassword({
      old_password: form.value.old_password,
      new_password: form.value.new_password
    })
    success.value = '密码修改成功！'
    // 3秒后跳转到登录页
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || '修改密码失败'
  } finally {
    loading.value = false
  }
}
</script>


