<template>
  <div class="student-feedback w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
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
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="feedbacks.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无反馈记录</p>
        <p class="text-gray-400 text-sm mt-2">点击上方按钮提交您的反馈</p>
      </div>
      <div
        v-for="feedback in feedbacks"
        :key="feedback.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-orange-50 rounded-lg">
              <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900">{{ feedback.title }}</h3>
          </div>
          <span
            :class="getStatusClass(feedback.status)"
            class="px-4 py-1.5 rounded-full text-sm font-medium"
          >
            {{ getStatusText(feedback.status) }}
          </span>
        </div>
        <div class="text-gray-700 mb-4 ml-11 bg-gray-50 p-4 rounded-xl border border-gray-200 whitespace-pre-wrap">{{ feedback.content }}</div>
        <div v-if="feedback.images" class="mb-4 ml-11">
          <div class="flex flex-wrap gap-3">
            <img
              v-for="(img, index) in feedback.images.split(',')"
              :key="index"
              :src="img"
              alt="反馈图片"
              class="w-32 h-32 object-cover rounded-xl border-2 border-gray-200 hover:border-blue-300 transition-all duration-200 cursor-pointer"
              @click="window.open(img, '_blank')"
            />
          </div>
        </div>
        <div v-if="feedback.reply" class="mt-4 ml-11 p-4 bg-green-50 border-2 border-green-200 rounded-xl">
          <div class="text-sm font-semibold text-green-800 mb-2 flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            管理员回复：
          </div>
          <div class="text-gray-700 whitespace-pre-wrap">{{ feedback.reply }}</div>
          <div v-if="feedback.replied_at" class="text-xs text-gray-500 mt-2 flex items-center">
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            回复时间：{{ formatDate(feedback.replied_at) }}
          </div>
        </div>
        <div class="text-sm text-gray-500 mt-4 ml-11 flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          提交时间：{{ formatDate(feedback.created_at) }}
        </div>
      </div>
    </div>

    <!-- 提交反馈表单弹窗 -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-2xl max-h-[90vh] overflow-y-auto border border-gray-100">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            提交反馈
          </h2>
          <button
            @click="showForm = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="submitFeedback" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">标题 *</label>
            <input
              v-model="formData.title"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              placeholder="请输入反馈标题"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">内容 *</label>
            <textarea
              v-model="formData.content"
              required
              rows="6"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
              placeholder="请详细描述您的问题或建议"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">图片（可选）</label>
            <input
              type="text"
              v-model="formData.images"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              placeholder="图片URL，多个用逗号分隔"
            />
            <p class="text-xs text-gray-500 mt-2 flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              提示：可以先上传图片到文件上传接口，然后粘贴URL
            </p>
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showForm = false"
              class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
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

