<template>
  <div class="student-job-detail w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
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
      <div class="mb-6 flex justify-end">
        <button
          @click="$router.back()"
          class="text-blue-600 hover:text-blue-700 font-medium flex items-center transition-colors"
        >
          <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回
        </button>
      </div>

      <!-- 职位详情 -->
      <div class="bg-white rounded-xl shadow-md p-8 mb-6 border border-gray-200">
        <div class="flex flex-col lg:flex-row lg:justify-between lg:items-start mb-6">
          <div class="flex-1 mb-4 lg:mb-0">
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
              @click="handleApply"
              class="btn btn-primary btn-lg"
            >
              <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              立即申请
            </button>
            <button
              @click="handleFavorite"
              class="btn btn-outline-primary btn-lg"
            >
              <svg v-if="isFavorited" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              {{ isFavorited ? '已收藏' : '收藏' }}
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getJob, type Job } from '@/api/jobs'
import { createApplication } from '@/api/applications'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'

const route = useRoute()
const router = useRouter()

const job = ref<Job | null>(null)
const loading = ref(false)
const isFavorited = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 加载职位详情
const loadJobDetail = async () => {
  loading.value = true
  try {
    const jobId = route.params.id as string
    job.value = await getJob(jobId)
    
    // 检查收藏状态
    if (job.value) {
      isFavorited.value = await checkFavorite('JOB', job.value.id)
    }
  } catch (error) {
    console.error('加载职位详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 申请职位
const handleApply = async () => {
  if (!job.value) return
  
  try {
    await createApplication({ job_id: job.value.id })
    alert('申请成功！')
    router.push('/student/applications')
  } catch (error: any) {
    alert(error.response?.data?.detail || '申请失败，请稍后重试')
  }
}

// 收藏/取消收藏
const handleFavorite = async () => {
  if (!job.value) return
  
  try {
    if (isFavorited.value) {
      await removeFavorite('JOB', job.value.id)
      isFavorited.value = false
    } else {
      await addFavorite('JOB', job.value.id)
      isFavorited.value = true
    }
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

onMounted(() => {
  loadJobDetail()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>


