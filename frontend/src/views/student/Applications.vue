<template>
  <div class="student-applications max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-5xl font-display font-bold text-gray-900 mb-10 bg-gradient-primary bg-clip-text text-transparent animate-fade-in-up">我的申请</h1>

    <!-- 筛选条件 -->
    <div class="card-elevated rounded-2xl p-6 mb-8 border border-gray-100/50 animate-fade-in-up" style="animation-delay: 0.1s;">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-semibold text-gray-700 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          状态筛选：
        </label>
        <select
          v-model="statusFilter"
          @change="loadApplications"
          class="px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
        >
          <option value="">全部</option>
          <option value="PENDING">待审核</option>
          <option value="REVIEWING">审核中</option>
          <option value="ACCEPTED">已通过</option>
          <option value="REJECTED">已拒绝</option>
        </select>
      </div>
    </div>

    <!-- 申请列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="applications.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无申请记录</p>
        <p class="text-gray-400 text-sm mt-2">快去申请心仪的职位吧！</p>
      </div>
      <div
        v-for="app in applications"
        :key="app.id"
        class="card-elevated rounded-2xl p-6 border-2 border-gray-200 hover:border-primary-300 hover:bg-gradient-to-br hover:from-primary-50/30 hover:to-transparent transition-all duration-300"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-display font-semibold text-gray-900">{{ app.job?.title || '职位' }}</h3>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                申请时间：{{ formatDate(app.created_at) }}
              </span>
              <span v-if="app.updated_at !== app.created_at" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                更新时间：{{ formatDate(app.updated_at) }}
              </span>
            </div>
            <p v-if="app.message" class="text-gray-700 mb-3 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ app.message }}
            </p>
          </div>
          <div class="ml-6 flex flex-col items-end space-y-3">
            <span
              :class="getStatusClass(app.status)"
              class="px-4 py-1.5 rounded-full text-sm font-medium"
            >
              {{ getStatusText(app.status) }}
            </span>
            <button
              @click="viewJobDetail(app.job_id)"
              class="px-5 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              查看职位
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <Pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      @change="handlePaginationChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getApplications, type JobApplication } from '@/api/applications'
import { getJob, type Job } from '@/api/jobs'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 申请列表
const applications = ref<(JobApplication & { job?: Job })[]>([])
const loading = ref(false)
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)


// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
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

// 加载申请列表
const loadApplications = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }

    const response = await getApplications(params)
    applications.value = response.items
    total.value = response.total

    // 加载职位信息
    for (const app of applications.value) {
      try {
        app.job = await getJob(app.job_id)
      } catch (error) {
        console.error(`加载职位 ${app.job_id} 失败:`, error)
      }
    }
  } catch (error) {
    console.error('加载申请列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadApplications()
}

// 查看职位详情
const viewJobDetail = (jobId: string) => {
  router.push(`/student/jobs/${jobId}`)
}

onMounted(() => {
  loadApplications()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>


