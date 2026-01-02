<template>
  <div class="student-chat w-full max-w-full px-4 sm:px-6 lg:px-8" style="height: calc(100vh - 120px); padding-top: 2rem; padding-bottom: 2rem;">
    <div class="flex h-full bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <!-- 会话列表 -->
      <div class="w-1/3 border-r border-gray-200 bg-gray-50 flex flex-col">
        <div class="p-6 border-b border-gray-200 bg-white">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            聊天
          </h2>
        </div>
        <div class="flex-1 overflow-y-auto">
          <div v-if="loading" class="p-8 text-center">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-3 text-gray-600">加载中...</p>
          </div>
          <div v-else-if="sessions.length === 0" class="p-8 text-center text-gray-500">
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <p class="text-sm">暂无聊天记录</p>
          </div>
          <div
            v-for="session in sessions"
            :key="session.id"
            @click="selectSession(session)"
            :class="[
              'p-4 border-b border-gray-200 cursor-pointer transition-all duration-200',
              currentSessionId === session.id ? 'bg-blue-50 border-l-4 border-l-blue-500' : 'hover:bg-gray-100'
            ]"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-gray-900 truncate">{{ getOtherUserName(session) }}</p>
                <p class="text-sm text-gray-500 truncate mt-1">
                  {{ session.last_message_at ? formatDate(session.last_message_at) : '暂无消息' }}
                </p>
              </div>
              <span
                v-if="getUnreadCount(session) > 0"
                class="ml-2 bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-[20px] text-center flex-shrink-0"
              >
                {{ getUnreadCount(session) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天窗口 -->
      <div class="flex-1 flex flex-col min-h-0 bg-white">
        <div v-if="!currentSession" class="flex-1 flex items-center justify-center text-gray-500 bg-gray-50">
          <div class="text-center">
            <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <p class="text-lg">请选择一个会话</p>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col min-h-0 overflow-hidden">
          <!-- 聊天头部 -->
          <div class="p-6 border-b border-gray-200 bg-white flex-shrink-0">
            <div class="flex justify-between items-center flex-wrap gap-3">
              <h3 class="text-xl font-bold text-gray-900">{{ getOtherUserName(currentSession) }}</h3>
              <!-- 快捷操作按钮 -->
              <div class="flex flex-wrap gap-2">
                <!-- 企业相关快捷操作 -->
                <template v-if="otherUserType === 'ENTERPRISE'">
                  <button
                    @click="viewEnterpriseProfile"
                    class="btn btn-primary btn-sm"
                    title="查看企业信息"
                  >
                    查看企业
                  </button>
                  <button
                    @click="viewEnterpriseJobs"
                    class="btn btn-success btn-sm"
                    title="查看职位信息"
                  >
                    查看职位
                  </button>
                  <button
                    @click="viewEnterpriseInfoSessions"
                    class="btn btn-primary btn-sm"
                    title="查看宣讲会"
                  >
                    查看宣讲会
                  </button>
                  <button
                    @click="viewEnterpriseJobFairs"
                    class="btn btn-primary btn-sm"
                    title="查看双选会"
                  >
                    查看双选会
                  </button>
                </template>
                <!-- 教师相关快捷操作 -->
                <template v-else-if="otherUserType === 'TEACHER'">
                  <button
                    @click="viewMyProfile"
                    class="btn btn-primary btn-sm"
                    title="查看我的信息"
                  >
                    我的信息
                  </button>
                  <button
                    @click="viewMyResumes"
                    class="btn btn-success btn-sm"
                    title="查看我的简历"
                  >
                    我的简历
                  </button>
                  <button
                    @click="recommendToEnterprise"
                    class="btn btn-primary btn-sm"
                    title="推荐给企业"
                  >
                    推荐给企业
                  </button>
                </template>
                <!-- 调试信息（开发时可见） -->
                <div v-if="!otherUserType || otherUserType === 'UNKNOWN'" class="text-xs text-gray-500 px-3 py-2 bg-gray-100 rounded-xl">
                  用户类型: {{ otherUserType || '未设置' }}
                </div>
              </div>
            </div>
          </div>

          <!-- 消息列表 -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 bg-gray-50 min-h-0">
            <div v-if="messagesLoading" class="text-center py-8">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p class="mt-3 text-gray-600">加载中...</p>
            </div>
            <div v-else-if="messages.length === 0" class="text-center py-12 text-gray-500">
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p>暂无消息</p>
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
                    'max-w-xs lg:max-w-md px-4 py-3 rounded-xl shadow-sm',
                    message.sender_id === currentUserId
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-800 border border-gray-200'
                  ]"
                >
                  <p class="break-words">{{ message.content }}</p>
                  <p
                    :class="[
                      'text-xs mt-2',
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
          <div class="p-6 border-t border-gray-200 bg-white flex-shrink-0">
            <form @submit.prevent="handleSendMessage" class="flex space-x-3">
              <input
                v-model="messageContent"
                type="text"
                placeholder="输入消息..."
                class="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
              <button
                type="submit"
                class="btn btn-primary btn-md"
              >
                <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
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
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCurrentUser } from '@/api/users'
import {
  getChatSessions,
  getSessionMessages,
  type ChatSession,
  type Message,
} from '@/api/chat'

const authStore = useAuthStore()
const router = useRouter()

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

// 对方用户类型和相关信息
const otherUserType = ref<string>('')
const enterpriseId = ref<string | null>(null)
const teacherUserId = ref<string | null>(null)

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

// 获取对方用户ID
const getOtherUserId = computed(() => {
  if (!currentSession.value) return null
  return currentSession.value.user1_id === currentUserId.value
    ? currentSession.value.user2_id
    : currentSession.value.user1_id
})

// 加载对方用户信息
const loadOtherUserInfo = async () => {
  if (!currentSession.value || !currentUserId.value) {
    return
  }

  try {
    // 从会话信息中获取对方用户类型
    const otherUserTypeFromSession = currentSession.value.user1_id === currentUserId.value
      ? currentSession.value.user2_type
      : currentSession.value.user1_type
    
    // 处理用户类型格式：后端可能返回 'UserType.ENTERPRISE' 或 'ENTERPRISE'
    // 需要提取实际的类型值
    let userTypeValue = otherUserTypeFromSession || 'UNKNOWN'
    if (userTypeValue.includes('.')) {
      // 如果包含点号，提取点号后的部分（如 'UserType.ENTERPRISE' -> 'ENTERPRISE'）
      userTypeValue = userTypeValue.split('.').pop() || 'UNKNOWN'
    }
    // 确保用户类型是大写格式
    otherUserType.value = userTypeValue.toUpperCase()
    
    // 如果是企业，获取企业ID
    if (otherUserType.value === 'ENTERPRISE') {
      const otherUserId = getOtherUserId.value
      if (otherUserId) {
        try {
          // 通过user_id获取企业档案，从而获取enterprise_id
          const { getEnterpriseProfile } = await import('@/api/profile')
          const enterpriseProfile = await getEnterpriseProfile(otherUserId)
          enterpriseId.value = enterpriseProfile.id
        } catch (error) {
          // 静默处理错误，不影响聊天功能
        }
      }
    }
  } catch (error) {
    // 静默处理错误，不影响聊天功能
  }
}

// 选择会话
const selectSession = async (session: ChatSession) => {
  currentSession.value = session
  currentSessionId.value = session.id
  await loadMessages(session.id)
  // 确保currentUserId已设置后再加载用户信息
  if (currentUserId.value) {
    await loadOtherUserInfo()
  } else {
    // 延迟一下再尝试加载
    setTimeout(async () => {
      if (currentUserId.value) {
        await loadOtherUserInfo()
      }
    }, 100)
  }
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

// 监听会话变化，自动加载用户信息
watch(currentSession, async (newSession) => {
  if (newSession && currentUserId.value) {
    await loadOtherUserInfo()
  }
}, { immediate: true })

// 监听currentUserId变化，如果会话已选择，重新加载用户信息
watch(currentUserId, async (newUserId) => {
  if (newUserId && currentSession.value) {
    await loadOtherUserInfo()
  }
})

// ==================== 企业相关快捷操作 ====================

// 查看企业信息
const viewEnterpriseProfile = () => {
  if (enterpriseId.value) {
    router.push(`/student/enterprises/${enterpriseId.value}`)
  } else {
    alert('无法获取企业信息')
  }
}

// 查看企业职位
const viewEnterpriseJobs = () => {
  if (enterpriseId.value) {
    router.push(`/student/jobs?enterprise_id=${enterpriseId.value}`)
  } else {
    alert('无法获取企业信息')
  }
}

// 查看企业宣讲会
const viewEnterpriseInfoSessions = () => {
  if (enterpriseId.value) {
    router.push(`/student/info-sessions?enterprise_id=${enterpriseId.value}`)
  } else {
    alert('无法获取企业信息')
  }
}

// 查看企业双选会
const viewEnterpriseJobFairs = () => {
  // 双选会是学校组织的，不是企业组织的，所以这里可以跳转到双选会列表
  router.push('/student/job-fairs')
}

// ==================== 教师相关快捷操作 ====================

// 查看我的信息
const viewMyProfile = () => {
  router.push('/student/profile')
}

// 查看我的简历
const viewMyResumes = () => {
  router.push('/student/resumes')
}

// 推荐给企业
const recommendToEnterprise = () => {
  // 跳转到推荐页面，可以选择企业进行推荐
  router.push('/student/recommendations')
}

onMounted(async () => {
  // 获取当前用户ID
  try {
    const user = await getCurrentUser()
    currentUserId.value = user.id
  } catch (error) {
    // 静默处理错误
  }
  
  await loadSessions()
  
  // 如果有默认会话，自动选择并加载用户信息
  if (sessions.value.length > 0 && !currentSession.value) {
    await selectSession(sessions.value[0])
  }
})
</script>

<style scoped>
.student-chat {
  display: flex;
  flex-direction: column;
}
</style>


