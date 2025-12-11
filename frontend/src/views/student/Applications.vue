<template>
  <div class="student-applications">
    <h1 class="text-3xl font-bold mb-6">我的申请</h1>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="statusFilter"
          @change="loadApplications"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
            <h3 class="text-xl font-semibold mb-2">{{ app.job?.title || '职位' }}</h3>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3">
              <span>申请时间：{{ formatDate(app.created_at) }}</span>
              <span v-if="app.updated_at !== app.created_at">
                更新时间：{{ formatDate(app.updated_at) }}
              </span>
            </div>
            <p v-if="app.message" class="text-gray-700 mb-3">{{ app.message }}</p>
          </div>
          <div class="ml-6 flex flex-col items-end space-y-2">
            <span
              :class="getStatusClass(app.status)"
              class="px-3 py-1 rounded-full text-sm"
            >
              {{ getStatusText(app.status) }}
            </span>
            <button
              @click="viewJobDetail(app.job_id)"
              class="px-4 py-2 text-blue-600 hover:text-blue-800"
            >
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
.student-applications {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


