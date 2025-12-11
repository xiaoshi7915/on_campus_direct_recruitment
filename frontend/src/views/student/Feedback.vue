<template>
  <div class="student-feedback">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">意见反馈</h1>
      <button
        @click="showForm = true"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        提交反馈
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="statusFilter"
          @change="loadFeedbacks"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="feedbacks.length === 0" class="text-center py-12 text-gray-500">
        暂无反馈记录
      </div>
      <div
        v-for="feedback in feedbacks"
        :key="feedback.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start mb-3">
          <h3 class="text-xl font-semibold">{{ feedback.title }}</h3>
          <span
            :class="getStatusClass(feedback.status)"
            class="px-3 py-1 rounded-full text-sm"
          >
            {{ getStatusText(feedback.status) }}
          </span>
        </div>
        <div class="text-gray-700 mb-3 whitespace-pre-wrap">{{ feedback.content }}</div>
        <div v-if="feedback.images" class="mb-3">
          <div class="flex flex-wrap gap-2">
            <img
              v-for="(img, index) in feedback.images.split(',')"
              :key="index"
              :src="img"
              alt="反馈图片"
              class="w-24 h-24 object-cover rounded"
            />
          </div>
        </div>
        <div v-if="feedback.reply" class="mt-3 p-3 bg-gray-50 rounded">
          <div class="text-sm font-medium text-gray-700 mb-1">管理员回复：</div>
          <div class="text-gray-600 whitespace-pre-wrap">{{ feedback.reply }}</div>
          <div v-if="feedback.replied_at" class="text-xs text-gray-500 mt-2">
            回复时间：{{ formatDate(feedback.replied_at) }}
          </div>
        </div>
        <div class="text-sm text-gray-500 mt-3">
          提交时间：{{ formatDate(feedback.created_at) }}
        </div>
      </div>
    </div>

    <!-- 提交反馈表单弹窗 -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">提交反馈</h2>
        <form @submit.prevent="submitFeedback">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">标题 *</label>
              <input
                v-model="formData.title"
                type="text"
                required
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入反馈标题"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">内容 *</label>
              <textarea
                v-model="formData.content"
                required
                rows="6"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请详细描述您的问题或建议"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">图片（可选）</label>
              <input
                type="text"
                v-model="formData.images"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="图片URL，多个用逗号分隔"
              />
              <p class="text-xs text-gray-500 mt-1">提示：可以先上传图片到文件上传接口，然后粘贴URL</p>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-2">
            <button
              type="button"
              @click="showForm = false"
              class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
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

