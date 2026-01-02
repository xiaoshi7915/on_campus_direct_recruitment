<template>
  <div class="student-job-fairs w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">双选会</h1>

    <!-- 双选会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="jobFairs.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无双选会信息</p>
        <p class="text-gray-400 text-sm mt-2">等待发布新的双选会</p>
      </div>
      <div
        v-for="jobFair in jobFairs"
        :key="jobFair.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ jobFair.title }}</h3>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                时间：{{ formatDateTime(jobFair.start_time) }} - {{ formatDateTime(jobFair.end_time) }}
              </span>
              <span v-if="jobFair.location" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                地点：{{ jobFair.location }}
              </span>
              <span v-if="jobFair.max_enterprises" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                最大企业数：{{ jobFair.max_enterprises }}
              </span>
            </div>
            <p v-if="jobFair.description" class="text-gray-700 line-clamp-2 ml-11 mb-3 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ jobFair.description }}
            </p>
            <div class="ml-11">
              <span
                :class="getStatusClass(jobFair.status)"
                class="px-3 py-1 rounded-full text-sm font-medium"
              >
                {{ getStatusText(jobFair.status) }}
              </span>
            </div>
          </div>
          <div class="ml-6">
            <button
              @click="handleRegister(jobFair.id)"
              :disabled="jobFair.status !== 'PUBLISHED'"
              :class="[
                'px-6 py-3 rounded-xl font-semibold shadow-md hover:shadow-lg transition-all duration-200 flex items-center',
                isRegistered(jobFair.id)
                  ? 'bg-green-600 text-white hover:bg-green-700'
                  : jobFair.status === 'PUBLISHED'
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
            >
              <svg v-if="isRegistered(jobFair.id)" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ isRegistered(jobFair.id) ? '已报名' : '报名' }}
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
import { getJobFairs, registerJobFair, type JobFair } from '@/api/jobFairs'
import Pagination from '@/components/Pagination.vue'

// 双选会列表
const jobFairs = ref<JobFair[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const registeredIds = ref<Set<string>>(new Set())

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
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
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    ONGOING: '进行中',
    ENDED: '已结束',
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    DRAFT: 'bg-gray-100 text-gray-800',
    PUBLISHED: 'bg-green-100 text-green-800',
    ONGOING: 'bg-blue-100 text-blue-800',
    ENDED: 'bg-gray-100 text-gray-500',
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// 检查是否已报名
const isRegistered = (jobFairId: string) => {
  return registeredIds.value.has(jobFairId)
}

// 加载双选会列表
const loadJobFairs = async () => {
  loading.value = true
  try {
    const response = await getJobFairs({
      page: currentPage.value,
      page_size: pageSize.value,
    })
    jobFairs.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载双选会列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadJobFairs()
}

// 报名双选会
const handleRegister = async (jobFairId: string) => {
  try {
    await registerJobFair(jobFairId)
    registeredIds.value.add(jobFairId)
    alert('报名成功！')
  } catch (error: any) {
    alert(error.response?.data?.detail || '报名失败，请稍后重试')
  }
}

onMounted(() => {
  loadJobFairs()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>


