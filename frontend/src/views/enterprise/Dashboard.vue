<template>
  <div class="enterprise-dashboard">
    <!-- 页面标题 -->
    <div class="mb-10 animate-fade-in-up">
      <h1 class="text-5xl font-display font-bold text-gray-900 mb-3 bg-gradient-primary bg-clip-text text-transparent">企业工作台</h1>
      <p class="text-gray-600 text-lg">管理您的招聘业务，查看数据统计</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.1s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">发布职位</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">{{ jobCount }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
      
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.2s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">收到申请</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-secondary-600 to-secondary-400 bg-clip-text text-transparent">{{ applicationCount }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-secondary-100 to-secondary-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>
      </div>
      
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.3s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">待处理面试</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-accent-600 to-accent-400 bg-clip-text text-transparent">{{ interviewCount }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-accent-100 to-accent-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
      
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.4s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">已发Offer</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-warm-600 to-warm-400 bg-clip-text text-transparent">{{ offerCount }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-warm-100 to-warm-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-warm-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近申请 -->
    <div class="card-elevated rounded-2xl mb-8 border border-gray-100/50">
      <div class="p-6 border-b border-gray-100/50">
        <h2 class="text-2xl font-display font-semibold text-gray-900 flex items-center">
          <div class="w-1 h-6 bg-gradient-primary rounded-full mr-3"></div>
          最近申请
        </h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-4 text-gray-500">加载中...</p>
        </div>
        <div v-else-if="recentApplications.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="mt-4 text-gray-500">暂无申请记录</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="app in recentApplications"
            :key="app.id"
            class="border border-gray-200 rounded-xl p-5 hover:shadow-lg hover:border-blue-200 transition-all duration-200 bg-white"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-semibold text-lg text-gray-900 mb-2">{{ app.job?.title || '职位' }}</h3>
                <div class="flex items-center text-sm text-gray-600 mb-2">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  申请时间：{{ formatDate(app.created_at) }}
                </div>
                <p v-if="app.message" class="text-gray-700 text-sm bg-gray-50 rounded-lg p-2 mt-2">{{ app.message }}</p>
              </div>
              <div class="ml-4 flex flex-col items-end space-y-2">
                <span
                  :class="getStatusClass(app.status)"
                  class="px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap"
                >
                  {{ getStatusText(app.status) }}
                </span>
                <button
                  @click="viewApplication(app.id)"
                  class="btn btn-primary btn-sm"
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
    <div class="card-elevated rounded-2xl border border-gray-100/50">
      <div class="p-6 border-b border-gray-100/50">
        <h2 class="text-2xl font-display font-semibold text-gray-900 flex items-center">
          <div class="w-1 h-6 bg-gradient-primary rounded-full mr-3"></div>
          热门职位
        </h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-4 text-gray-500">加载中...</p>
        </div>
        <div v-else-if="popularJobs.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <p class="mt-4 text-gray-500">暂无职位信息</p>
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="job in popularJobs"
            :key="job.id"
            class="border-2 border-gray-200 rounded-2xl p-6 hover:shadow-xl hover:border-primary-300 hover:bg-gradient-to-br hover:from-primary-50/50 hover:to-transparent transition-all duration-300 bg-white/80 backdrop-blur-sm cursor-pointer group"
            @click="goToJobDetail(job.id)"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-semibold text-lg text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                  {{ job.title }}
                </h3>
                <div class="flex flex-wrap items-center gap-3 text-sm text-gray-600 mb-2">
                  <span class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {{ job.work_location }}
                  </span>
                  <span class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {{ job.job_type }}
                  </span>
                  <span class="flex items-center font-semibold text-blue-600">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {{ job.salary_min }}-{{ job.salary_max }}元
                  </span>
                </div>
                <div class="flex items-center gap-4 text-xs text-gray-500">
                  <span class="flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    查看：{{ job.view_count }}
                  </span>
                  <span class="flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    申请：{{ job.apply_count }}
                  </span>
                </div>
              </div>
              <button
                @click.stop="goToJobDetail(job.id)"
                class="btn btn-primary btn-md ml-4 whitespace-nowrap"
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
  width: 100%;
  max-width: 100%;
  padding: 0 1rem;
}
</style>

