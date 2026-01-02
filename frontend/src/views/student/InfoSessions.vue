<template>
  <div class="student-info-sessions w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">宣讲会</h1>

    <!-- 宣讲会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="infoSessions.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无宣讲会信息</p>
        <p class="text-gray-400 text-sm mt-2">等待发布新的宣讲会</p>
      </div>
      <div
        v-for="session in infoSessions"
        :key="session.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-purple-50 rounded-lg">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ session.title }}</h3>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                时间：{{ formatDateTime(session.start_time) }} - {{ formatDateTime(session.end_time) }}
              </span>
              <span v-if="session.location" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                地点：{{ session.location }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                类型：{{ getSessionTypeText(session.session_type) }}
              </span>
              <span v-if="session.max_students" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                最大人数：{{ session.max_students }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                已报名：{{ session.check_in_count }}
              </span>
            </div>
            <p v-if="session.description" class="text-gray-700 line-clamp-2 ml-11 mb-3 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ session.description }}
            </p>
            <div v-if="session.live_url" class="ml-11 mb-3">
              <a
                :href="session.live_url"
                target="_blank"
                class="btn btn-danger btn-sm"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                观看直播
              </a>
            </div>
            <div class="ml-11">
              <span
                :class="getStatusClass(session.status)"
                class="px-3 py-1 rounded-full text-sm font-medium"
              >
                {{ getStatusText(session.status) }}
              </span>
            </div>
          </div>
          <div class="ml-6">
            <button
              @click="handleRegister(session.id)"
              :disabled="session.status !== 'PUBLISHED'"
              :class="[
                'btn btn-md',
                isRegistered(session.id)
                  ? 'btn-success'
                  : session.status === 'PUBLISHED'
                  ? 'btn-primary'
                  : 'btn-secondary'
              ]"
            >
              <svg v-if="isRegistered(session.id)" class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ isRegistered(session.id) ? '已报名' : '报名' }}
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
import { getInfoSessions, registerInfoSession, type InfoSession } from '@/api/infoSessions'
import Pagination from '@/components/Pagination.vue'

// 宣讲会列表
const infoSessions = ref<InfoSession[]>([])
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

// 获取宣讲会类型文本
const getSessionTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    OFFLINE: '线下',
    ONLINE: '线上',
    HYBRID: '混合',
  }
  return typeMap[type] || type
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
const isRegistered = (sessionId: string) => {
  return registeredIds.value.has(sessionId)
}

// 加载宣讲会列表
const loadInfoSessions = async () => {
  loading.value = true
  try {
    const response = await getInfoSessions({
      page: currentPage.value,
      page_size: pageSize.value,
    })
    infoSessions.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载宣讲会列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadInfoSessions()
}

// 报名宣讲会
const handleRegister = async (sessionId: string) => {
  try {
    await registerInfoSession(sessionId)
    registeredIds.value.add(sessionId)
    alert('报名成功！')
  } catch (error: any) {
    alert(error.response?.data?.detail || '报名失败，请稍后重试')
  }
}

onMounted(() => {
  loadInfoSessions()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>


