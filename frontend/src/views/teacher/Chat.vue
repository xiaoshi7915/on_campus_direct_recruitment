<template>
  <div class="teacher-chat" style="height: calc(100vh - 120px);">
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
          <div class="p-4 border-b bg-white flex-shrink-0">
            <div class="flex justify-between items-center flex-wrap gap-2">
              <h3 class="text-lg font-semibold">{{ getOtherUserName(currentSession) }}</h3>
              <!-- 快捷操作按钮 -->
              <div class="flex flex-wrap gap-2">
                <!-- 企业相关快捷操作 -->
                <template v-if="otherUserType === 'ENTERPRISE'">
                  <button
                    @click="viewEnterpriseProfile"
                    class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                    title="查看企业信息"
                  >
                    查看企业
                  </button>
                  <button
                    @click="viewEnterpriseJobs"
                    class="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
                    title="查看职位信息"
                  >
                    查看职位
                  </button>
                  <button
                    @click="viewEnterpriseInfoSessions"
                    class="px-3 py-1 text-sm bg-purple-500 text-white rounded hover:bg-purple-600"
                    title="查看宣讲会"
                  >
                    查看宣讲会
                  </button>
                  <button
                    @click="viewEnterpriseJobFairs"
                    class="px-3 py-1 text-sm bg-indigo-500 text-white rounded hover:bg-indigo-600"
                    title="查看双选会"
                  >
                    查看双选会
                  </button>
                </template>
                <!-- 学生相关快捷操作 -->
                <template v-else-if="otherUserType === 'STUDENT'">
                  <button
                    @click="viewStudentProfile"
                    class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                    title="查看学生信息"
                  >
                    查看学生
                  </button>
                  <button
                    @click="viewStudentResumes"
                    class="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
                    title="查看简历"
                  >
                    查看简历
                  </button>
                  <button
                    @click="recommendToEnterprise"
                    class="px-3 py-1 text-sm bg-purple-500 text-white rounded hover:bg-purple-600"
                    title="推荐给企业"
                  >
                    推荐给企业
                  </button>
                </template>
                <!-- 调试信息（开发时可见） -->
                <div v-if="!otherUserType || otherUserType === 'UNKNOWN'" class="text-xs text-gray-500">
                  用户类型: {{ otherUserType || '未设置' }}
                </div>
              </div>
            </div>
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
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser } from '@/api/users'
import {
  getChatSessions,
  getSessionMessages,
  sendMessage,
  type ChatSession,
  type Message,
} from '@/api/chat'

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
const studentUserId = ref<string | null>(null)
const studentId = ref<string | null>(null)

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
  // 如果是与学校聊天，显示学校名称
  if (session.school_id && session.school_name) {
    return session.school_name
  }
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
  if (!currentSession.value) return

  try {
    // 如果是与学校聊天
    if (currentSession.value.school_id) {
      otherUserType.value = 'SCHOOL'
    } else {
      // 从会话信息中获取对方用户类型
      const otherUserTypeFromSession = currentSession.value.user1_id === currentUserId.value
        ? currentSession.value.user2_type
        : currentSession.value.user1_type
      
      otherUserType.value = otherUserTypeFromSession || 'UNKNOWN'
      
      // 如果是企业，获取企业ID
      if (otherUserType.value === 'ENTERPRISE') {
        const otherUserId = getOtherUserId.value
        if (otherUserId) {
          try {
            const { getEnterpriseProfile } = await import('@/api/profile')
            const enterpriseProfile = await getEnterpriseProfile(otherUserId)
            enterpriseId.value = enterpriseProfile.id
          } catch (error) {
            console.error('获取企业信息失败:', error)
          }
        }
      }
      
      // 如果是学生，获取学生ID
      if (otherUserType.value === 'STUDENT') {
        const otherUserId = getOtherUserId.value
        if (otherUserId) {
          studentUserId.value = otherUserId
          try {
            const { getStudentProfile } = await import('@/api/profile')
            const studentProfile = await getStudentProfile(otherUserId)
            studentId.value = studentProfile.id
          } catch (error) {
            console.error('获取学生信息失败:', error)
          }
        }
      }
    }
  } catch (error) {
    console.error('加载对方用户信息失败:', error)
  }
}

// 选择会话
const selectSession = async (session: ChatSession) => {
  currentSession.value = session
  currentSessionId.value = session.id
  await loadMessages(session.id)
  await loadOtherUserInfo()
}

// 加载消息
const loadMessages = async (sessionId: string) => {
  messagesLoading.value = true
  try {
    const response = await getSessionMessages(sessionId, {
      page: 1,
      page_size: 50,
    })
    messages.value = response.items.reverse()
    
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
    const receiverId = currentSession.value.user1_id === currentUserId.value
      ? currentSession.value.user2_id
      : currentSession.value.user1_id
    
    if (!receiverId) {
      alert('无法获取接收者信息')
      return
    }
    
    const newMessage = await sendMessage(currentSession.value.id, {
      receiver_id: receiverId,
      content: messageContent.value,
    })
    messages.value.push(newMessage)
    messageContent.value = ''
    
    await nextTick()
    scrollToBottom()
    
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

// ==================== 企业相关快捷操作 ====================

// 查看企业信息
const viewEnterpriseProfile = () => {
  if (enterpriseId.value) {
    router.push(`/teacher/enterprises/${enterpriseId.value}`)
  } else {
    alert('无法获取企业信息')
  }
}

// 查看企业职位
const viewEnterpriseJobs = () => {
  if (enterpriseId.value) {
    router.push(`/teacher/jobs?enterprise_id=${enterpriseId.value}`)
  } else {
    alert('无法获取企业信息')
  }
}

// 查看企业宣讲会
const viewEnterpriseInfoSessions = () => {
  if (enterpriseId.value) {
    router.push(`/teacher/info-sessions?enterprise_id=${enterpriseId.value}`)
  } else {
    alert('无法获取企业信息')
  }
}

// 查看企业双选会
const viewEnterpriseJobFairs = () => {
  router.push('/teacher/job-fairs')
}

// ==================== 学生相关快捷操作 ====================

// 查看学生信息
const viewStudentProfile = () => {
  if (studentId.value) {
    router.push(`/teacher/students/${studentId.value}`)
  } else {
    alert('无法获取学生信息')
  }
}

// 查看学生简历
const viewStudentResumes = () => {
  if (studentUserId.value) {
    router.push(`/teacher/resumes?user_id=${studentUserId.value}`)
  } else {
    router.push('/teacher/resumes')
  }
}

// 推荐给企业
const recommendToEnterprise = () => {
  if (studentId.value) {
    router.push(`/teacher/talent-recommendations?student_id=${studentId.value}`)
  } else {
    router.push('/teacher/talent-recommendations')
  }
}

onMounted(async () => {
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
.teacher-chat {
  display: flex;
  flex-direction: column;
}
</style>

