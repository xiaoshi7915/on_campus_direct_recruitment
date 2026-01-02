<template>
  <div class="student-notifications w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">系统消息</h1>
      <div class="flex items-center space-x-4">
        <div class="px-4 py-2 bg-red-50 border-2 border-red-200 rounded-xl">
          <span class="text-sm text-gray-700">
            未读消息：<span class="font-bold text-red-600">{{ unreadCount }}</span>
          </span>
        </div>
        <button
          v-if="unreadCount > 0"
          @click="markAllAsRead"
          class="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          全部标记为已读
        </button>
      </div>
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
          @change="loadNotifications"
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
      <div v-else-if="notifications.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <p class="text-gray-500 text-lg">暂无消息</p>
        <p class="text-gray-400 text-sm mt-2">系统消息将在这里显示</p>
      </div>
      <div
        v-for="msg in notifications"
        :key="msg.id"
        :class="[
          'bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border',
          !msg.is_read ? 'border-l-4 border-l-blue-500 border-gray-200' : 'border-gray-200'
        ]"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div v-if="!msg.is_read" class="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">{{ msg.content }}</h3>
              <span v-if="!msg.is_read" class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                未读
              </span>
            </div>
            <div class="text-sm text-gray-500 ml-11 flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ formatDate(msg.created_at) }}
            </div>
          </div>
          <button
            v-if="!msg.is_read"
            @click="markAsRead(msg.id)"
            class="ml-6 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 text-sm font-medium flex items-center"
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

