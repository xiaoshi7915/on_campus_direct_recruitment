<template>
  <div class="enterprise-system-messages max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">系统消息</h1>
      <button
        v-if="unreadCount > 0"
        @click="markAllRead"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        全部标记为已读
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-semibold text-gray-700 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          状态筛选：
        </label>
        <select
          v-model="readFilter"
          @change="loadMessages"
          class="px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
        >
          <option :value="null">全部</option>
          <option :value="false">未读</option>
          <option :value="true">已读</option>
        </select>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="messages.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <p class="text-gray-500 text-lg">暂无系统消息</p>
        <p class="text-gray-400 text-sm mt-2">系统消息将在这里显示</p>
      </div>
      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border',
          !message.is_read ? 'border-l-4 border-l-blue-500 border-gray-200' : 'border-gray-200'
        ]"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div v-if="!message.is_read" class="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
              <div class="flex items-center text-sm text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ formatDate(message.created_at) }}
              </div>
            </div>
            <div class="text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-xl border border-gray-200">{{ message.content }}</div>
          </div>
          <div class="ml-6">
            <button
              v-if="!message.is_read"
              @click="markRead(message.id)"
              class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 text-sm font-medium flex items-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              标记已读
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="mt-8">
      <Pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        @change="handlePaginationChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getSystemMessages, markMessageRead, markAllMessagesRead, type SystemMessage } from '@/api/systemMessages'
import Pagination from '@/components/Pagination.vue'

const messages = ref<SystemMessage[]>([])
const loading = ref(false)
const readFilter = ref<boolean | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const unreadCount = computed(() => messages.value.filter(m => !m.is_read).length)

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadMessages = async () => {
  loading.value = true
  try {
    const res = await getSystemMessages({
      page: currentPage.value,
      page_size: pageSize.value,
      is_read: readFilter.value ?? undefined
    })
    messages.value = res.items
    total.value = res.total
  } catch (error: any) {
    console.error('加载系统消息失败:', error)
    alert('加载系统消息失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadMessages()
}

const markRead = async (messageId: string) => {
  try {
    await markMessageRead(messageId)
    await loadMessages()
  } catch (error: any) {
    console.error('标记已读失败:', error)
    alert('标记已读失败: ' + (error.response?.data?.detail || error.message))
  }
}

const markAllRead = async () => {
  try {
    await markAllMessagesRead()
    await loadMessages()
  } catch (error: any) {
    console.error('全部标记已读失败:', error)
    alert('全部标记已读失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadMessages()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

