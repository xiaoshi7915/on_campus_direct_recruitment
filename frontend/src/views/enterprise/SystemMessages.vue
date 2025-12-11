<template>
  <div class="enterprise-system-messages">
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
    <div v-if="total > 0" class="mt-6">
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
.enterprise-system-messages {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

