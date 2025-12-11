<template>
  <div class="student-system-messages">
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getSystemMessages, markMessageRead, markAllMessagesRead, type SystemMessage } from '@/api/systemMessages'

const messages = ref<SystemMessage[]>([])
const loading = ref(false)
const readFilter = ref<boolean | null>(null)

const unreadCount = computed(() => messages.value.filter(m => !m.is_read).length)

const loadMessages = async () => {
  loading.value = true
  try {
    const res = await getSystemMessages({
      is_read: readFilter.value ?? undefined
    })
    messages.value = res.items
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
    alert('已全部标记为已读')
    loadMessages()
  } catch (error: any) {
    alert(error.response?.data?.detail || '标记失败，请稍后重试')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(() => {
  loadMessages()
})
</script>

