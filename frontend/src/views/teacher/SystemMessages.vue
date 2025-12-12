<template>
  <div class="teacher-system-messages">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">系统消息</h1>
      <button
        v-if="unreadCount > 0"
        @click="markAllRead"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        全部标记为已读
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="readFilter"
          @change="loadMessages"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="null">全部</option>
          <option :value="false">未读</option>
          <option :value="true">已读</option>
        </select>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="messages.length === 0" class="text-center py-12 text-gray-500">
        暂无系统消息
      </div>
      <div
        v-for="message in messages"
        :key="message.id"
        :class="['bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow', !message.is_read && 'border-l-4 border-blue-500']"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-2 mb-2">
              <span v-if="!message.is_read" class="w-2 h-2 bg-blue-500 rounded-full"></span>
              <span class="text-sm text-gray-500">{{ formatDate(message.created_at) }}</span>
            </div>
            <div class="text-gray-700 whitespace-pre-wrap">{{ message.content }}</div>
          </div>
          <div class="ml-6">
            <button
              v-if="!message.is_read"
              @click="markRead(message.id)"
              class="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200"
            >
              标记已读
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="mt-6 flex justify-center">
      <div class="flex space-x-2">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 border rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          上一页
        </button>
        <span class="px-4 py-2">
          第 {{ currentPage }} / {{ totalPages }} 页
        </span>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 border rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { getSystemMessages, markMessageRead, markAllMessagesRead, type SystemMessage } from '@/api/systemMessages'

const messages = ref<SystemMessage[]>([])
const loading = ref(false)
const readFilter = ref<boolean | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const unreadCount = computed(() => messages.value.filter(m => !m.is_read).length)
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

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
  } catch (error) {
    console.error('加载系统消息失败:', error)
    alert('加载系统消息失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const markRead = async (messageId: string) => {
  try {
    await markMessageRead(messageId)
    loadMessages()
  } catch (error: any) {
    alert(error.response?.data?.detail || '标记失败，请稍后重试')
  }
}

const markAllRead = async () => {
  try {
    await markAllMessagesRead()
    loadMessages()
  } catch (error: any) {
    alert(error.response?.data?.detail || '标记失败，请稍后重试')
  }
}

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadMessages()
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadMessages()
})
</script>

<style scoped>
.teacher-system-messages {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

