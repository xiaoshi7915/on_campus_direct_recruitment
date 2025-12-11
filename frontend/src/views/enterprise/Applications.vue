<template>
  <div class="enterprise-applications">
    <h1 class="text-3xl font-bold mb-6">申请管理</h1>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">状态筛选</label>
          <select
            v-model="statusFilter"
            @change="loadApplications"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">全部</option>
            <option value="PENDING">待审核</option>
            <option value="REVIEWING">审核中</option>
            <option value="ACCEPTED">已通过</option>
            <option value="REJECTED">已拒绝</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">职位筛选</label>
          <select
            v-model="jobFilter"
            @change="loadApplications"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">全部职位</option>
            <option v-for="job in jobs" :key="job.id" :value="job.id">
              {{ job.title }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索申请人..."
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="loadApplications"
          />
        </div>
      </div>
    </div>

    <!-- 申请列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="applications.length === 0" class="text-center py-12 text-gray-500">
        暂无申请记录
      </div>
      <div
        v-for="app in applications"
        :key="app.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ app.job?.title || '职位' }}</h3>
              <span
                :class="getStatusClass(app.status)"
                class="px-3 py-1 rounded-full text-sm"
              >
                {{ getStatusText(app.status) }}
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3">
              <p>申请人ID：{{ app.student_id }}</p>
              <p>申请时间：{{ formatDate(app.created_at) }}</p>
            </div>
            <p v-if="app.message" class="text-gray-700 mb-3">{{ app.message }}</p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewResume(app.resume_id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看简历
            </button>
            <button
              v-if="app.status === 'PENDING' || app.status === 'REVIEWING'"
              @click="handleAccept(app.id)"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              通过
            </button>
            <button
              v-if="app.status === 'PENDING' || app.status === 'REVIEWING'"
              @click="handleReject(app.id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              拒绝
            </button>
            <button
              @click="scheduleInterview(app)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
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
.enterprise-applications {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

