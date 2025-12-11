<template>
  <div class="student-dashboard">
    <h1 class="text-3xl font-bold mb-6">学生工作台</h1>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">我的简历</div>
        <div class="text-3xl font-bold text-blue-600">{{ resumeCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">我的申请</div>
        <div class="text-3xl font-bold text-green-600">{{ applicationCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">待面试</div>
        <div class="text-3xl font-bold text-orange-600">{{ interviewCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">收藏职位</div>
        <div class="text-3xl font-bold text-purple-600">{{ favoriteCount }}</div>
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
              <div>
                <h3 class="font-semibold text-lg">{{ app.job?.title || '职位' }}</h3>
                <p class="text-gray-600 text-sm mt-1">
                  申请时间：{{ formatDate(app.created_at) }}
                </p>
              </div>
              <span
                :class="getStatusClass(app.status)"
                class="px-3 py-1 rounded-full text-sm"
              >
                {{ getStatusText(app.status) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐职位 -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">推荐职位</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else-if="recommendedJobs.length === 0" class="text-center py-8 text-gray-500">
          暂无推荐职位
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="job in recommendedJobs"
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
              </div>
              <button
                @click.stop="handleApply(job.id)"
                class="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                立即申请
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
import { getResumes } from '@/api/resumes'
import { getFavorites } from '@/api/favorites'
import { getInterviews } from '@/api/interviews'
import { createApplication } from '@/api/applications'

const router = useRouter()

// 统计数据
const resumeCount = ref(0)
const applicationCount = ref(0)
const interviewCount = ref(0)
const favoriteCount = ref(0)

// 最近申请
const recentApplications = ref<JobApplication[]>([])
const recommendedJobs = ref<Job[]>([])
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
    const [resumesRes, applicationsRes, interviewsRes, favoritesRes, jobsRes] = await Promise.all([
      getResumes({ page_size: 1 }),
      getApplications({ page_size: 5 }),
      getInterviews({ status: 'SCHEDULED', page_size: 1 }),
      getFavorites({ target_type: 'JOB', page_size: 1 }),
      getJobs({ page_size: 5, status: 'PUBLISHED' }),
    ])

    resumeCount.value = resumesRes.total
    applicationCount.value = applicationsRes.total
    interviewCount.value = interviewsRes.total
    favoriteCount.value = favoritesRes.total
    recentApplications.value = applicationsRes.items
    recommendedJobs.value = jobsRes.items
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 跳转到职位详情
const goToJobDetail = (jobId: string) => {
  router.push(`/student/jobs/${jobId}`)
}

// 申请职位
const handleApply = async (jobId: string) => {
  try {
    await createApplication({ job_id: jobId })
    alert('申请成功！')
    loadData()
  } catch (error: any) {
    alert(error.response?.data?.detail || '申请失败，请稍后重试')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.student-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


