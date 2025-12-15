<template>
  <div class="enterprise-applications max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">申请管理</h1>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        筛选条件
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">状态筛选</label>
          <select
            v-model="statusFilter"
            @change="loadApplications"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
          >
            <option value="">全部</option>
            <option value="PENDING">待审核</option>
            <option value="REVIEWING">审核中</option>
            <option value="ACCEPTED">已通过</option>
            <option value="REJECTED">已拒绝</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">职位筛选</label>
          <select
            v-model="jobFilter"
            @change="loadApplications"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
          >
            <option value="">全部职位</option>
            <option v-for="job in jobs" :key="job.id" :value="job.id">
              {{ job.title }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">搜索申请人</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索申请人..."
              class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @keyup.enter="loadApplications"
            />
          </div>
        </div>
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
        <p class="text-gray-400 text-sm mt-2">等待学生申请您的职位</p>
      </div>
      <div
        v-for="app in applications"
        :key="app.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ app.job?.title || '职位' }}</h3>
              <span
                :class="getStatusClass(app.status)"
                class="px-4 py-1.5 rounded-full text-sm font-medium"
              >
                {{ getStatusText(app.status) }}
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3 ml-11 space-y-1">
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                申请人：{{ app.student_name || app.student_id || '未知' }}
              </p>
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                申请时间：{{ formatDate(app.created_at) }}
              </p>
            </div>
            <p v-if="app.message" class="text-gray-700 mb-3 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ app.message }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewResume(app.resume_id)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              查看简历
            </button>
            <button
              v-if="app.status === 'PENDING' || app.status === 'REVIEWING'"
              @click="handleAccept(app.id)"
              class="px-5 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              通过
            </button>
            <button
              v-if="app.status === 'PENDING' || app.status === 'REVIEWING'"
              @click="handleReject(app.id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              拒绝
            </button>
            <button
              @click="scheduleInterview(app)"
              class="px-5 py-2.5 border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              安排面试
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getApplications, updateApplication, type JobApplication } from '@/api/applications'
import { getJobs, type Job } from '@/api/jobs'
import Pagination from '@/components/Pagination.vue'

const route = useRoute()
const router = useRouter()

// 申请列表
const applications = ref<(JobApplication & { job?: Job })[]>([])
const jobs = ref<Job[]>([])
const loading = ref(false)
const statusFilter = ref('')
const jobFilter = ref(route.query.job_id as string || '')
const searchKeyword = ref('')
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

// 加载职位列表（用于筛选）
const loadJobs = async () => {
  try {
    const response = await getJobs({ page_size: 100 })
    jobs.value = response.items
  } catch (error) {
    console.error('加载职位列表失败:', error)
  }
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
    if (jobFilter.value) {
      params.job_id = jobFilter.value
    }

    const response = await getApplications(params)
    applications.value = response.items
    total.value = response.total

    // 加载职位信息
    for (const app of applications.value) {
      try {
        const job = await import('@/api/jobs').then(m => m.getJob(app.job_id))
        app.job = job
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

// 查看简历
const viewResume = (resumeId: string) => {
  // 跳转到简历详情页面
  window.open(`/teacher/resumes/${resumeId}`, '_blank')
}

// 通过申请
const handleAccept = async (applicationId: string) => {
  try {
    await updateApplication(applicationId, { status: 'ACCEPTED' })
    alert('已通过申请')
    loadApplications()
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

// 拒绝申请
const handleReject = async (applicationId: string) => {
  if (!confirm('确定要拒绝这个申请吗？')) {
    return
  }
  try {
    await updateApplication(applicationId, { status: 'REJECTED' })
    alert('已拒绝申请')
    loadApplications()
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

// 安排面试
const scheduleInterview = (application: JobApplication) => {
  router.push(`/enterprise/interviews/create?application_id=${application.id}`)
}

onMounted(() => {
  loadJobs()
  loadApplications()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

