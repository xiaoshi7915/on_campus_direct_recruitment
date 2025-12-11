<template>
  <div class="student-notifications">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">系统消息</h1>
      <div class="flex items-center space-x-4">
        <span class="text-sm text-gray-600">
          未读消息：<span class="font-bold text-red-500">{{ unreadCount }}</span>
        </span>
        <button
          @click="markAllAsRead"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          全部标记为已读
        </button>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="readFilter"
          @change="loadNotifications"
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
      <div v-else-if="notifications.length === 0" class="text-center py-12 text-gray-500">
        暂无消息
      </div>
      <div
        v-for="msg in notifications"
        :key="msg.id"
        :class="['bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow', !msg.is_read && 'border-l-4 border-blue-500']"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-2 mb-2">
              <h3 class="text-lg font-semibold">{{ msg.content }}</h3>
              <span v-if="!msg.is_read" class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                未读
              </span>
            </div>
            <div class="text-sm text-gray-500">
              {{ formatDate(msg.created_at) }}
            </div>
          </div>
          <button
            v-if="!msg.is_read"
            @click="markAsRead(msg.id)"
            class="ml-4 px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 text-sm"
          >
            标记已读
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getNotifications, markAsRead as markRead, getUnreadCount } from '@/api/notifications'

const notifications = ref<any[]>([])
const loading = ref(false)
const readFilter = ref<boolean | null>(null)
const unreadCount = ref(0)

const loadNotifications = async () => {
  loading.value = true
  try {
    const res = await getNotifications({
      is_read: readFilter.value ?? undefined
    })
    notifications.value = res.data.items
    loadUnreadCount()
  } catch (error) {
    console.error('加载消息失败:', error)
  } finally {
    loading.value = false
  }
}

const loadUnreadCount = async () => {
  try {
    const res = await getUnreadCount()
    unreadCount.value = res.data.count
  } catch (error) {
    console.error('加载未读数量失败:', error)
  }
}

const markAsRead = async (messageId: string) => {
  try {
    await markRead(messageId)
    loadNotifications()
  } catch (error) {
    alert('标记失败')
  }
}

const markAllAsRead = async () => {
  if (!confirm('确定要标记所有消息为已读吗？')) return
  try {
    for (const msg of notifications.value) {
      if (!msg.is_read) {
        await markRead(msg.id)
      }
    }
    loadNotifications()
  } catch (error) {
    alert('标记失败')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(() => {
  loadNotifications()
})
</script>

