<template>
  <div class="enterprise-job-detail max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    <div v-else-if="!job" class="text-center py-16">
      <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-gray-500 text-lg">职位不存在</p>
    </div>
    <div v-else>
      <!-- 返回按钮 -->
      <button
        @click="$router.back()"
        class="mb-6 text-blue-600 hover:text-blue-700 font-medium flex items-center transition-colors"
      >
        <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        返回
      </button>

      <!-- 职位详情 -->
      <div class="bg-white rounded-xl shadow-md p-8 mb-6 border border-gray-200">
        <div class="flex flex-col lg:flex-row lg:justify-between lg:items-start mb-6">
          <div class="flex-1 mb-4 lg:mb-0">
            <div class="flex items-center space-x-3 mb-4">
              <span
                :class="getStatusClass(job.status)"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ getStatusText(job.status) }}
              </span>
            </div>
            <h1 class="text-4xl font-extrabold text-gray-900 mb-4">{{ job.title }}</h1>
            <div class="flex flex-wrap gap-4 text-gray-600 mb-4">
              <span class="flex items-center">
                <svg class="w-5 h-5 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ job.work_location }}
              </span>
              <span class="flex items-center">
                <svg class="w-5 h-5 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ job.job_type }}
              </span>
              <span v-if="job.salary_min && job.salary_max" class="flex items-center text-blue-600 font-bold">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ job.salary_min }}-{{ job.salary_max }}元
              </span>
              <span class="flex items-center">
                <svg class="w-5 h-5 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
                </svg>
                {{ job.education || '不限' }}
              </span>
            </div>
          </div>
          <div class="flex flex-col space-y-3 lg:ml-6">
            <button
              @click="handleEdit"
              class="px-8 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center justify-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              编辑职位
            </button>
            <button
              @click="handleDelete"
              class="px-8 py-3 bg-red-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-red-700 transition-all duration-200 flex items-center justify-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              删除职位
            </button>
          </div>
        </div>

        <div v-if="job.tags" class="mb-6 flex flex-wrap gap-2">
          <span
            v-for="tag in job.tags.split(',')"
            :key="tag"
            class="px-3 py-1.5 bg-blue-100 text-blue-800 text-sm rounded-md font-medium"
          >
            {{ tag }}
          </span>
        </div>

        <div class="border-t border-gray-200 pt-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            职位描述
          </h2>
          <div class="text-gray-700 whitespace-pre-wrap leading-relaxed bg-gray-50 p-6 rounded-xl border border-gray-200">{{ job.description }}</div>
        </div>

        <div v-if="job.requirements" class="border-t border-gray-200 pt-6 mt-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            职位要求
          </h2>
          <div class="text-gray-700 whitespace-pre-wrap leading-relaxed bg-gray-50 p-6 rounded-xl border border-gray-200">{{ job.requirements }}</div>
        </div>

        <div class="border-t border-gray-200 pt-6 mt-6">
          <div class="flex flex-wrap gap-6 text-sm text-gray-600">
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              查看次数：{{ job.view_count }}
            </span>
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              申请次数：{{ job.apply_count }}
            </span>
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              发布时间：{{ formatDate(job.created_at) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 申请列表 -->
      <div class="bg-white rounded-xl shadow-md p-8 border border-gray-200">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          职位申请列表
        </h2>
        <div v-if="applications.length === 0" class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-gray-500 text-lg">暂无申请</p>
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="application in applications"
            :key="application.id"
            class="border border-gray-200 rounded-xl p-5 hover:shadow-md hover:border-blue-200 transition-all duration-200 bg-white"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-semibold text-lg text-gray-900 mb-2">{{ application.student_name || '学生' }}</h3>
                <div class="flex flex-wrap gap-4 text-sm text-gray-600 mb-2">
                  <span class="flex items-center">
                    <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    申请时间：{{ formatDate(application.created_at) }}
                  </span>
                </div>
                <span
                  :class="getStatusClass(application.status)"
                  class="px-3 py-1 rounded-full text-sm font-medium inline-block"
                >
                  {{ getStatusText(application.status) }}
                </span>
              </div>
              <button
                @click="viewApplication(application.id)"
                class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center ml-4"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                查看详情
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
import { useRoute, useRouter } from 'vue-router'
import { getJob, type Job, deleteJob } from '@/api/jobs'
import { getApplications } from '@/api/applications'

const route = useRoute()
const router = useRouter()

const job = ref<Job | null>(null)
const applications = ref<any[]>([])
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
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    CLOSED: '已关闭',
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
    DRAFT: 'bg-gray-100 text-gray-800',
    PUBLISHED: 'bg-green-100 text-green-800',
    CLOSED: 'bg-red-100 text-red-800',
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// 加载职位详情
const loadJobDetail = async () => {
  loading.value = true
  try {
    const jobId = route.params.id as string
    job.value = await getJob(jobId)
    
    // 加载申请列表
    if (job.value) {
      const result = await getApplications({ job_id: jobId })
      applications.value = result.items || []
    }
  } catch (error) {
    console.error('加载职位详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 编辑职位
const handleEdit = () => {
  if (job.value) {
    router.push(`/enterprise/jobs/${job.value.id}/edit`)
  }
}

// 删除职位
const handleDelete = async () => {
  if (!job.value) return
  
  if (!confirm('确定要删除这个职位吗？')) {
    return
  }
  
  try {
    await deleteJob(job.value.id)
    alert('删除成功！')
    router.push('/enterprise/jobs')
  } catch (error: any) {
    alert(error.response?.data?.detail || '删除失败，请稍后重试')
  }
}

// 查看申请详情
const viewApplication = (applicationId: string) => {
  router.push(`/enterprise/applications/${applicationId}`)
}

onMounted(() => {
  loadJobDetail()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>


