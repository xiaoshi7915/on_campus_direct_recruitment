<template>
  <div class="enterprise-application-detail max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    <div v-else-if="!application" class="text-center py-16">
      <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-gray-500 text-lg">申请不存在</p>
    </div>
    <div v-else>
      <!-- 返回按钮 -->
      <button
        @click="$router.back()"
        class="mb-6 px-4 py-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-xl transition-all duration-200 font-medium flex items-center"
      >
        <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        返回
      </button>

      <!-- 申请详情 -->
      <div class="bg-white rounded-xl shadow-md p-8 mb-6 border border-gray-200">
        <div class="flex justify-between items-start mb-6">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-4">
              <div class="p-2 bg-green-50 rounded-lg">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h1 class="text-3xl font-bold text-gray-900">职位申请详情</h1>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                申请时间：{{ formatDate(application.created_at) }}
              </span>
              <span
                :class="getStatusClass(application.status)"
                class="px-3 py-1 rounded-full text-sm font-medium"
              >
                {{ getStatusText(application.status) }}
              </span>
            </div>
          </div>
          <div class="flex flex-col space-y-2">
            <button
              v-if="application.status === 'PENDING'"
              @click="handleAccept"
              class="px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              接受申请
            </button>
            <button
              v-if="application.status === 'PENDING'"
              @click="handleReject"
              class="px-6 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              拒绝申请
            </button>
          </div>
        </div>

        <div class="border-t border-gray-200 pt-6">
          <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            申请信息
          </h2>
          <div class="space-y-3 ml-7">
            <div class="flex items-start">
              <span class="font-semibold text-gray-700 w-24">职位：</span>
              <span class="text-gray-900">{{ application.job_title || '未知' }}</span>
            </div>
            <div class="flex items-start">
              <span class="font-semibold text-gray-700 w-24">申请人：</span>
              <span class="text-gray-900">{{ application.student_name || '未知' }}</span>
            </div>
            <div class="flex items-start">
              <span class="font-semibold text-gray-700 w-24">申请留言：</span>
              <span class="text-gray-900 flex-1 bg-gray-50 p-3 rounded-lg border border-gray-200">{{ application.message || '无' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 简历信息 -->
      <div v-if="resume" class="bg-white rounded-xl shadow-md p-8 border border-gray-200">
        <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          简历信息
        </h2>
        <div class="space-y-4">
          <div>
            <h3 class="font-semibold text-gray-900 mb-3">基本信息</h3>
            <div class="text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-xl border border-gray-200">{{ resume.content }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getApplication, updateApplication } from '@/api/applications'
import { getResume } from '@/api/resumes'

const route = useRoute()
const router = useRouter()

const application = ref<any>(null)
const resume = ref<any>(null)
const loading = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    PENDING: '待审核',
    REVIEWING: '审核中',
    ACCEPTED: '已通过',
    REJECTED: '已拒绝',
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    REVIEWING: 'bg-blue-100 text-blue-800',
    ACCEPTED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800',
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// 加载申请详情
const loadApplicationDetail = async () => {
  loading.value = true
  try {
    const applicationId = route.params.id as string
    application.value = await getApplication(applicationId)
    
    // 加载简历信息
    if (application.value?.resume_id) {
      try {
        resume.value = await getResume(application.value.resume_id)
      } catch (error) {
        console.error('加载简历失败:', error)
      }
    }
  } catch (error) {
    console.error('加载申请详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 接受申请
const handleAccept = async () => {
  if (!application.value) return
  
  try {
    await updateApplication(application.value.id, { status: 'ACCEPTED' })
    alert('已接受申请！')
    await loadApplicationDetail()
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

// 拒绝申请
const handleReject = async () => {
  if (!application.value) return
  
  if (!confirm('确定要拒绝这个申请吗？')) {
    return
  }
  
  try {
    await updateApplication(application.value.id, { status: 'REJECTED' })
    alert('已拒绝申请！')
    await loadApplicationDetail()
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

onMounted(() => {
  loadApplicationDetail()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>


