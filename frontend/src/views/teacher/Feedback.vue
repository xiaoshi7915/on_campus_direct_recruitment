<template>
  <div class="teacher-feedback max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">意见反馈</h1>
      <button
        @click="showForm = true"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        提交反馈
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-semibold text-gray-700 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          状态筛选：
        </label>
        <select
          v-model="statusFilter"
          @change="loadFeedbacks"
          class="px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
        >
          <option value="">全部</option>
          <option value="PENDING">待处理</option>
          <option value="PROCESSING">处理中</option>
          <option value="RESOLVED">已解决</option>
          <option value="REJECTED">已拒绝</option>
        </select>
      </div>
    </div>

    <!-- 反馈列表 -->
    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>

    <div v-else-if="feedbacks.length === 0" class="text-center py-16">
      <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-gray-500 text-lg">暂无反馈记录</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="feedback in feedbacks"
        :key="feedback.id"
        class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ feedback.title }}</h3>
            <p class="text-gray-600 text-sm mb-3">{{ feedback.content }}</p>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>{{ formatDate(feedback.created_at) }}</span>
              <span
                class="px-3 py-1 rounded-full text-xs font-semibold"
                :class="getStatusClass(feedback.status)"
              >
                {{ getStatusText(feedback.status) }}
              </span>
            </div>
          </div>
        </div>
        <div v-if="feedback.reply" class="mt-4 pt-4 border-t border-gray-200 bg-gray-50 rounded-lg p-4">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-blue-600 mr-2 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <div class="flex-1">
              <p class="text-sm font-semibold text-gray-700 mb-1">管理员回复：</p>
              <p class="text-gray-600 text-sm">{{ feedback.reply }}</p>
              <p v-if="feedback.replied_at" class="text-xs text-gray-500 mt-2">
                {{ formatDate(feedback.replied_at) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 提交反馈表单弹窗 -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 class="text-2xl font-bold text-gray-900">提交反馈</h2>
          <button
            @click="showForm = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="submitFeedback" class="p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">标题</label>
              <input
                v-model="formData.title"
                type="text"
                required
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="请输入反馈标题"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">内容</label>
              <textarea
                v-model="formData.content"
                required
                rows="6"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="请详细描述您的问题或建议"
              ></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-4">
            <button
              type="button"
              @click="showForm = false"
              class="px-6 py-2.5 border border-gray-300 rounded-xl text-gray-700 hover:bg-gray-50 transition-all duration-200"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all duration-200 font-semibold"
            >
              提交
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getFeedbacks, createFeedback } from '@/api/feedbacks'
import type { FeedbackResponse } from '@/types/index'

const feedbacks = ref<FeedbackResponse[]>([])
const loading = ref(false)
const statusFilter = ref('')
const showForm = ref(false)
const formData = ref({
  title: '',
  content: '',
  images: ''
})

const loadFeedbacks = async () => {
  loading.value = true
  try {
    const res = await getFeedbacks({
      status: statusFilter.value || undefined
    })
    feedbacks.value = res.items
  } catch (error) {
    console.error('加载反馈失败:', error)
    alert('加载反馈失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const submitFeedback = async () => {
  try {
    await createFeedback({
      title: formData.value.title,
      content: formData.value.content,
      images: formData.value.images || undefined
    })
    alert('提交成功，我们会尽快处理')
    showForm.value = false
    formData.value = {
      title: '',
      content: '',
      images: ''
    }
    loadFeedbacks()
  } catch (error: any) {
    alert(error.response?.data?.detail || '提交失败，请稍后重试')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    PROCESSING: 'bg-blue-100 text-blue-800',
    RESOLVED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    PENDING: '待处理',
    PROCESSING: '处理中',
    RESOLVED: '已解决',
    REJECTED: '已拒绝'
  }
  return texts[status] || status
}

onMounted(() => {
  loadFeedbacks()
})
</script>

<style scoped>
.teacher-feedback {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

