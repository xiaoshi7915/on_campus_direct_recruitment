<template>
  <div class="student-info-sessions">
    <h1 class="text-3xl font-bold mb-6">宣讲会</h1>

    <!-- 宣讲会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="infoSessions.length === 0" class="text-center py-12 text-gray-500">
        暂无宣讲会信息
      </div>
      <div
        v-for="session in infoSessions"
        :key="session.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ session.title }}</h3>
            <div class="text-gray-600 text-sm mb-3">
              <p>时间：{{ formatDateTime(session.start_time) }} - {{ formatDateTime(session.end_time) }}</p>
              <p v-if="session.location">地点：{{ session.location }}</p>
              <p>类型：{{ getSessionTypeText(session.session_type) }}</p>
              <p v-if="session.max_students">最大人数：{{ session.max_students }}</p>
              <p>已报名：{{ session.check_in_count }}</p>
            </div>
            <p v-if="session.description" class="text-gray-700 line-clamp-2">
              {{ session.description }}
            </p>
            <div v-if="session.live_url" class="mt-3">
              <a
                :href="session.live_url"
                target="_blank"
                class="text-blue-600 hover:text-blue-800"
              >
                观看直播 →
              </a>
            </div>
            <p class="text-gray-500 text-sm mt-3">
              状态：<span :class="getStatusClass(session.status)">
                {{ getStatusText(session.status) }}
              </span>
            </p>
          </div>
          <div class="ml-6">
            <button
              @click="handleRegister(session.id)"
              :disabled="session.status !== 'PUBLISHED'"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
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
    DRAFT: 'text-gray-600',
    PUBLISHED: 'text-green-600',
    ONGOING: 'text-blue-600',
    ENDED: 'text-gray-500',
  }
  return classMap[status] || ''
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
.student-info-sessions {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


