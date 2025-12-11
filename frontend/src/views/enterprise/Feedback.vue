<template>
  <div class="enterprise-feedback">
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
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4 text-gray-900">提交反馈</h2>
          <form @submit.prevent="submitFeedback">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  标题 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="feedbackForm.title"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入反馈标题"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  内容 <span class="text-red-500">*</span>
                </label>
                <textarea
                  v-model="feedbackForm.content"
                  required
                  rows="6"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入反馈内容"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">图片（可选）</label>
                <input
                  type="text"
                  v-model="feedbackForm.images"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="图片URL，多个用逗号分隔"
                />
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-4">
              <button
                type="button"
                @click="showForm = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                提交
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="mt-6">
      <Pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        @change="handlePaginationChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getFeedbacks, createFeedback, type FeedbackResponse } from '@/api/feedbacks'
import Pagination from '@/components/Pagination.vue'

const feedbacks = ref<FeedbackResponse[]>([])
const loading = ref(false)
const showForm = ref(false)
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const feedbackForm = ref({
  title: '',
  content: '',
  images: ''
})

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    PENDING: '待处理',
    PROCESSING: '处理中',
    RESOLVED: '已解决',
    REJECTED: '已拒绝'
  }
  return statusMap[status] || status
}

const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    PROCESSING: 'bg-blue-100 text-blue-800',
    RESOLVED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadFeedbacks = async () => {
  loading.value = true
  try {
    const res = await getFeedbacks({
      page: currentPage.value,
      page_size: pageSize.value,
      status: statusFilter.value || undefined
    })
    feedbacks.value = res.items
    total.value = res.total
  } catch (error: any) {
    console.error('加载反馈列表失败:', error)
    alert('加载反馈列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadFeedbacks()
}

const submitFeedback = async () => {
  try {
    await createFeedback({
      title: feedbackForm.value.title,
      content: feedbackForm.value.content,
      images: feedbackForm.value.images || undefined
    })
    alert('提交成功！')
    showForm.value = false
    feedbackForm.value = {
      title: '',
      content: '',
      images: ''
    }
    loadFeedbacks()
  } catch (error: any) {
    console.error('提交反馈失败:', error)
    alert('提交失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadFeedbacks()
})
</script>

<style scoped>
.enterprise-feedback {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

