<template>
  <div class="enterprise-dashboard">
    <h1 class="text-3xl font-bold mb-6">企业工作台</h1>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">发布职位</div>
        <div class="text-3xl font-bold text-blue-600">{{ jobCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">收到申请</div>
        <div class="text-3xl font-bold text-green-600">{{ applicationCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">待处理面试</div>
        <div class="text-3xl font-bold text-orange-600">{{ interviewCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">已发Offer</div>
        <div class="text-3xl font-bold text-purple-600">{{ offerCount }}</div>
      </div>
    </div>

    <!-- 最近申请 -->
    <div class="bg-white rounded-lg shadow mb-6">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">最近申请</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else-if="recentApplications.length === 0" class="text-center py-8 text-gray-500">
          暂无申请记录
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="app in recentApplications"
            :key="app.id"
            class="border rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-semibold text-lg">{{ app.job?.title || '职位' }}</h3>
                <p class="text-gray-600 text-sm mt-1">
                  申请时间：{{ formatDate(app.created_at) }}
                </p>
                <p v-if="app.message" class="text-gray-700 mt-2">{{ app.message }}</p>
              </div>
              <div class="ml-4 flex flex-col items-end space-y-2">
                <span
                  :class="getStatusClass(app.status)"
                  class="px-3 py-1 rounded-full text-sm"
                >
                  {{ getStatusText(app.status) }}
                </span>
                <button
                  @click="viewApplication(app.id)"
                  class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
                >
                  查看详情
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门职位 -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">热门职位</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else-if="popularJobs.length === 0" class="text-center py-8 text-gray-500">
          暂无职位信息
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="job in popularJobs"
            :key="job.id"
            class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
            @click="goToJobDetail(job.id)"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-semibold text-lg">{{ job.title }}</h3>
                <p class="text-gray-600 text-sm mt-1">
                  {{ job.work_location }} | {{ job.job_type }} | 
                  {{ job.salary_min }}-{{ job.salary_max }}元
                </p>
                <p class="text-gray-500 text-sm mt-2">
                  查看：{{ job.view_count }} | 申请：{{ job.apply_count }}
                </p>
              </div>
              <button
                @click.stop="goToJobDetail(job.id)"
                class="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                管理
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getApplications, type JobApplication } from '@/api/applications'
import { getJobs, type Job } from '@/api/jobs'
import { getInterviews } from '@/api/interviews'

const router = useRouter()

// 统计数据
const jobCount = ref(0)
const applicationCount = ref(0)
const interviewCount = ref(0)
const offerCount = ref(0)

// 最近申请
const recentApplications = ref<(JobApplication & { job?: Job })[]>([])
const popularJobs = ref<Job[]>([])
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

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载统计数据
    const [jobsRes, applicationsRes, interviewsRes] = await Promise.all([
      getJobs({ page_size: 1 }),
      getApplications({ page_size: 5 }),
      getInterviews({ page_size: 1 }),
    ])

    jobCount.value = jobsRes.total
    applicationCount.value = applicationsRes.total
    interviewCount.value = interviewsRes.total
    offerCount.value = 0 // TODO: 获取Offer数量
    recentApplications.value = applicationsRes.items
    
    // 加载热门职位（按申请数排序）
    const popularJobsRes = await getJobs({ page_size: 5, status: 'PUBLISHED' })
    popularJobs.value = popularJobsRes.items.sort((a, b) => b.apply_count - a.apply_count)
    
    // 加载申请对应的职位信息
    for (const app of recentApplications.value) {
      try {
        const job = await import('@/api/jobs').then(m => m.getJob(app.job_id))
        app.job = job
      } catch (error) {
        console.error(`加载职位 ${app.job_id} 失败:`, error)
      }
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 跳转到职位详情
const goToJobDetail = (jobId: string) => {
  router.push(`/enterprise/jobs/${jobId}`)
}

// 查看申请详情
const viewApplication = (applicationId: string) => {
  router.push(`/enterprise/applications/${applicationId}`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.enterprise-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

