<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
      <div class="mb-6">
        <button
          @click="$router.back()"
          class="text-blue-600 hover:text-blue-800 mb-4"
        >
          ← 返回
        </button>
        <h2 class="text-2xl font-bold">安排面试</h2>
      </div>

      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="!application" class="text-center py-12 text-gray-500">申请不存在</div>
      <form v-else @submit.prevent="handleSubmit" class="space-y-6">
        <!-- 申请信息 -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-semibold mb-2">申请信息</h3>
          <div class="text-sm text-gray-600 space-y-1">
            <p><strong>职位：</strong>{{ application.job_title || '未知' }}</p>
            <p><strong>申请人：</strong>{{ application.student_name || '未知' }}</p>
            <p><strong>申请时间：</strong>{{ formatDate(application.created_at) }}</p>
          </div>
        </div>

        <!-- 面试类型 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">面试类型 *</label>
          <select
            v-model="form.interview_type"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请选择</option>
            <option value="PHONE">电话面试</option>
            <option value="VIDEO">视频面试</option>
            <option value="ONSITE">现场面试</option>
          </select>
        </div>

        <!-- 面试时间 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">面试时间 *</label>
          <input
            v-model="form.scheduled_time"
            type="datetime-local"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- 面试时长 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">面试时长（分钟）</label>
          <input
            v-model.number="form.duration"
            type="number"
            min="15"
            step="15"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="例如：30"
          />
        </div>

        <!-- 面试地点（现场面试时显示） -->
        <div v-if="form.interview_type === 'ONSITE'">
          <label class="block text-sm font-medium text-gray-700 mb-2">面试地点 *</label>
          <input
            v-model="form.location"
            type="text"
            :required="form.interview_type === 'ONSITE'"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入面试地点"
          />
        </div>

        <!-- 会议链接（视频面试时显示） -->
        <div v-if="form.interview_type === 'VIDEO'">
          <label class="block text-sm font-medium text-gray-700 mb-2">会议链接 *</label>
          <input
            v-model="form.meeting_url"
            type="url"
            :required="form.interview_type === 'VIDEO'"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="https://..."
          />
        </div>

        <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>

        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="$router.back()"
            class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="submitting"
            class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {{ submitting ? '提交中...' : '创建面试' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getApplication } from '@/api/applications'
import { createInterview } from '@/api/interviews'

const route = useRoute()
const router = useRouter()

const application = ref<any>(null)
const loading = ref(false)
const submitting = ref(false)
const error = ref('')

const form = ref({
  interview_type: '',
  scheduled_time: '',
  duration: 30,
  location: '',
  meeting_url: ''
})

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 加载申请详情
const loadApplication = async () => {
  loading.value = true
  error.value = ''
  try {
    const applicationId = route.query.application_id as string
    if (!applicationId) {
      error.value = '缺少申请ID'
      return
    }
    application.value = await getApplication(applicationId)
  } catch (err: any) {
    console.error('加载申请详情失败:', err)
    error.value = err.response?.data?.detail || err.message || '加载申请详情失败'
  } finally {
    loading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  error.value = ''
  
  // 验证必填字段
  if (!form.value.interview_type) {
    error.value = '请选择面试类型'
    return
  }
  if (!form.value.scheduled_time) {
    error.value = '请选择面试时间'
    return
  }
  if (form.value.interview_type === 'ONSITE' && !form.value.location) {
    error.value = '请填写面试地点'
    return
  }
  if (form.value.interview_type === 'VIDEO' && !form.value.meeting_url) {
    error.value = '请填写会议链接'
    return
  }
  
  submitting.value = true
  try {
    const applicationId = route.query.application_id as string
    await createInterview({
      application_id: applicationId,
      interview_type: form.value.interview_type,
      scheduled_time: new Date(form.value.scheduled_time).toISOString(),
      duration: form.value.duration || undefined,
      location: form.value.location || undefined,
      meeting_url: form.value.meeting_url || undefined,
    })
    alert('面试安排成功！')
    router.push('/enterprise/applications')
  } catch (err: any) {
    console.error('创建面试失败:', err)
    error.value = err.response?.data?.detail || err.message || '创建面试失败'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadApplication()
})
</script>

