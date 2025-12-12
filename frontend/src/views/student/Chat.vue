<template>
  <div class="student-chat" style="height: calc(100vh - 120px);">
    <div class="flex h-full">
      <!-- 会话列表 -->
      <div class="w-1/3 border-r bg-white">
        <div class="p-4 border-b">
          <h2 class="text-xl font-semibold">聊天</h2>
        </div>
        <div class="overflow-y-auto h-full">
          <div v-if="loading" class="p-4 text-center">加载中...</div>
          <div v-else-if="sessions.length === 0" class="p-4 text-center text-gray-500">
            暂无聊天记录
          </div>
          <div
            v-for="session in sessions"
            :key="session.id"
            @click="selectSession(session)"
            :class="[
              'p-4 border-b cursor-pointer hover:bg-gray-50',
              currentSessionId === session.id ? 'bg-blue-50' : ''
            ]"
          >
            <div class="flex justify-between items-start">
              <div>
                <p class="font-semibold">{{ getOtherUserName(session) }}</p>
                <p class="text-sm text-gray-600 truncate">
                  {{ session.last_message_at ? formatDate(session.last_message_at) : '暂无消息' }}
                </p>
              </div>
              <span
                v-if="getUnreadCount(session) > 0"
                class="bg-red-500 text-white text-xs rounded-full px-2 py-1"
              >
                {{ getUnreadCount(session) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天窗口 -->
      <div class="flex-1 flex flex-col min-h-0">
        <div v-if="!currentSession" class="flex-1 flex items-center justify-center text-gray-500">
          请选择一个会话
        </div>
        <div v-else class="flex-1 flex flex-col min-h-0 overflow-hidden">
          <!-- 聊天头部 -->
          <div class="p-4 border-b bg-white">
            <h3 class="text-lg font-semibold">{{ getOtherUserName(currentSession) }}</h3>
          </div>

          <!-- 消息列表 -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 bg-gray-50 min-h-0">
            <div v-if="messagesLoading" class="text-center py-4">加载中...</div>
            <div v-else-if="messages.length === 0" class="text-center py-8 text-gray-500">
              暂无消息
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="message in messages"
                :key="message.id"
                :class="[
                  'flex',
                  message.sender_id === currentUserId ? 'justify-end' : 'justify-start'
                ]"
              >
                <div
                  :class="[
                    'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
                    message.sender_id === currentUserId
                      ? 'bg-blue-500 text-white'
                      : 'bg-white text-gray-800'
                  ]"
                >
                  <p>{{ message.content }}</p>
                  <p
                    :class="[
                      'text-xs mt-1',
                      message.sender_id === currentUserId ? 'text-blue-100' : 'text-gray-500'
                    ]"
                  >
                    {{ formatDateTime(message.created_at) }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入框 -->
          <div class="p-4 border-t bg-white flex-shrink-0">
            <form @submit.prevent="handleSendMessage" class="flex space-x-2">
              <input
                v-model="messageContent"
                type="text"
                placeholder="输入消息..."
                class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="submit"
                class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                发送
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getCurrentUser } from '@/api/users'
import {
  getChatSessions,
  getSessionMessages,
  type ChatSession,
  type Message,
} from '@/api/chat'

const authStore = useAuthStore()

// 会话列表
const sessions = ref<ChatSession[]>([])
const currentSession = ref<ChatSession | null>(null)
const currentSessionId = ref<string | null>(null)
const currentUserId = ref<string>('')
const loading = ref(false)
const messagesLoading = ref(false)

// 消息列表
const messages = ref<Message[]>([])
const messageContent = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 获取对方用户名
const getOtherUserName = (session: ChatSession) => {
  // 优先使用会话中的用户名
  if (session.user1_id === currentUserId.value) {
    return session.user2_name || session.user2_id
  } else {
    return session.user1_name || session.user1_id
  }
}

// 获取未读消息数
const getUnreadCount = (session: ChatSession) => {
  return session.user1_id === currentUserId.value
    ? session.unread_count_user1
    : session.unread_count_user2
}

// 加载会话列表
const loadSessions = async () => {
  loading.value = true
  try {
    const response = await getChatSessions()
    sessions.value = response.items
  } catch (error) {
    console.error('加载会话列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 选择会话
const selectSession = async (session: ChatSession) => {
  currentSession.value = session
  currentSessionId.value = session.id
  await loadMessages(session.id)
}

// 加载消息
const loadMessages = async (sessionId: string) => {
  messagesLoading.value = true
  try {
    const response = await getSessionMessages(sessionId, {
      page: 1,
      page_size: 50,
    })
    messages.value = response.items.reverse() // 反转以显示最新消息在底部
    
    // 滚动到底部
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('加载消息失败:', error)
  } finally {
    messagesLoading.value = false
  }
}

// 发送消息
const handleSendMessage = async () => {
  if (!messageContent.value.trim() || !currentSession.value) return

  try {
    const { sendMessage: sendMessageAPI } = await import('@/api/chat')
    const newMessage = await sendMessageAPI(currentSession.value.id, {
      receiver_id:
        currentSession.value.user1_id === currentUserId.value
          ? currentSession.value.user2_id
          : currentSession.value.user1_id,
      content: messageContent.value,
    })
    messages.value.push(newMessage)
    messageContent.value = ''
    
    // 滚动到底部
    await nextTick()
    scrollToBottom()
    
    // 刷新会话列表
    loadSessions()
  } catch (error: any) {
    alert(error.response?.data?.detail || '发送失败，请稍后重试')
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 监听消息变化，自动滚动
watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

onMounted(async () => {
  // 获取当前用户ID
  try {
    const user = await getCurrentUser()
    currentUserId.value = user.id
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
  
  await loadSessions()
})
</script>

<style scoped>
.student-chat {
  display: flex;
  flex-direction: column;
}
</style>


