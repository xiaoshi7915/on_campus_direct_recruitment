<template>
  <div class="student-job-fairs">
    <h1 class="text-3xl font-bold mb-6">双选会</h1>

    <!-- 双选会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="jobFairs.length === 0" class="text-center py-12 text-gray-500">
        暂无双选会信息
      </div>
      <div
        v-for="jobFair in jobFairs"
        :key="jobFair.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ jobFair.title }}</h3>
            <div class="text-gray-600 text-sm mb-3">
              <p>时间：{{ formatDateTime(jobFair.start_time) }} - {{ formatDateTime(jobFair.end_time) }}</p>
              <p v-if="jobFair.location">地点：{{ jobFair.location }}</p>
              <p v-if="jobFair.max_enterprises">最大企业数：{{ jobFair.max_enterprises }}</p>
            </div>
            <p v-if="jobFair.description" class="text-gray-700 line-clamp-2">
              {{ jobFair.description }}
            </p>
            <p class="text-gray-500 text-sm mt-3">
              状态：<span :class="getStatusClass(jobFair.status)">
                {{ getStatusText(jobFair.status) }}
              </span>
            </p>
          </div>
          <div class="ml-6">
            <button
              @click="handleRegister(jobFair.id)"
              :disabled="jobFair.status !== 'PUBLISHED'"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
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
    DRAFT: 'text-gray-600',
    PUBLISHED: 'text-green-600',
    ONGOING: 'text-blue-600',
    ENDED: 'text-gray-500',
  }
  return classMap[status] || ''
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
.student-job-fairs {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


