<template>
  <div class="enterprise-chat" style="height: calc(100vh - 120px);">
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
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-semibold">{{ getOtherUserName(currentSession) }}</h3>
              <!-- 快捷操作按钮 -->
              <div class="flex space-x-2">
                <!-- 学生相关快捷操作 -->
                <template v-if="otherUserType === 'STUDENT'">
                  <button
                    @click="viewStudentResume"
                    class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                    title="查看简历"
                  >
                    查看简历
                  </button>
                  <button
                    @click="markResume"
                    class="px-3 py-1 text-sm bg-yellow-500 text-white rounded hover:bg-yellow-600"
                    title="标记简历"
                  >
                    标记简历
                  </button>
                  <button
                    @click="toggleResumeFavorite"
                    :class="isResumeFavorited ? 'bg-red-500 hover:bg-red-600' : 'bg-gray-500 hover:bg-gray-600'"
                    class="px-3 py-1 text-sm text-white rounded"
                    :title="isResumeFavorited ? '取消收藏' : '收藏简历'"
                  >
                    {{ isResumeFavorited ? '已收藏' : '收藏简历' }}
                  </button>
                  <button
                    @click="downloadResume"
                    class="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
                    title="下载简历"
                  >
                    下载简历
                  </button>
                  <button
                    @click="inviteToInfoSession"
                    class="px-3 py-1 text-sm bg-purple-500 text-white rounded hover:bg-purple-600"
                    title="宣讲会邀请"
                  >
                    宣讲会邀请
                  </button>
                  <button
                    @click="inviteToInterview"
                    class="px-3 py-1 text-sm bg-indigo-500 text-white rounded hover:bg-indigo-600"
                    title="面试邀请"
                  >
                    面试邀请
                  </button>
                </template>
                <!-- 教师相关快捷操作（学校） -->
                <template v-else-if="otherUserType === 'TEACHER' && teacherSchoolId">
                  <button
                    @click="viewSchoolDetail"
                    class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                    title="查看学校主页"
                  >
                    查看学校
                  </button>
                  <button
                    @click="markSchool"
                    class="px-3 py-1 text-sm bg-yellow-500 text-white rounded hover:bg-yellow-600"
                    title="标记学校"
                  >
                    标记学校
                  </button>
                  <button
                    @click="toggleSchoolFavorite"
                    :class="isSchoolFavorited ? 'bg-red-500 hover:bg-red-600' : 'bg-gray-500 hover:bg-gray-600'"
                    class="px-3 py-1 text-sm text-white rounded"
                    :title="isSchoolFavorited ? '取消收藏' : '收藏学校'"
                  >
                    {{ isSchoolFavorited ? '已收藏' : '收藏学校' }}
                  </button>
                  <button
                    @click="shareSchool"
                    class="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
                    title="分享学校"
                  >
                    分享学校
                  </button>
                  <button
                    @click="requestOfflineInfoSession"
                    class="px-3 py-1 text-sm bg-purple-500 text-white rounded hover:bg-purple-600"
                    title="申请线下宣讲会"
                  >
                    申请宣讲会
                  </button>
                </template>
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

    <!-- 标记简历模态框 -->
    <div v-if="showMarkResumeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-4">标记简历</h2>
        <form @submit.prevent="saveResumeMark" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">备注</label>
            <textarea
              v-model="markForm.note"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">标记颜色</label>
            <select
              v-model="markForm.color"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="blue">蓝色</option>
              <option value="red">红色</option>
              <option value="green">绿色</option>
              <option value="yellow">黄色</option>
            </select>
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showMarkResumeModal = false"
              class="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              保存
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 标记学校模态框 -->
    <div v-if="showMarkSchoolModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-4">标记学校</h2>
        <form @submit.prevent="saveSchoolMark" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">备注</label>
            <textarea
              v-model="markForm.note"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">标记颜色</label>
            <select
              v-model="markForm.color"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="blue">蓝色</option>
              <option value="red">红色</option>
              <option value="green">绿色</option>
              <option value="yellow">黄色</option>
            </select>
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showMarkSchoolModal = false"
              class="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              保存
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 宣讲会邀请模态框 -->
    <div v-if="showInviteInfoSessionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-96 overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">选择宣讲会</h2>
        <div v-if="infoSessions.length === 0" class="text-center py-8 text-gray-500">
          暂无可邀请的宣讲会
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="session in infoSessions"
            :key="session.id"
            class="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
            @click="submitInfoSessionInvite(session.id)"
          >
            <h3 class="font-semibold">{{ session.title }}</h3>
            <p class="text-sm text-gray-600">{{ new Date(session.start_time).toLocaleString('zh-CN') }}</p>
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <button
            @click="showInviteInfoSessionModal = false"
            class="px-4 py-2 border rounded-lg hover:bg-gray-50"
          >
            取消
          </button>
        </div>
      </div>
    </div>

    <!-- 面试邀请模态框 -->
    <div v-if="showInviteInterviewModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-96 overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">选择申请</h2>
        <div v-if="applications.length === 0" class="text-center py-8 text-gray-500">
          暂无可邀请的申请
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="app in applications"
            :key="app.id"
            class="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
            @click="submitInterviewInvite(app.id)"
          >
            <h3 class="font-semibold">{{ app.job_title || '职位' }}</h3>
            <p class="text-sm text-gray-600">申请时间：{{ new Date(app.created_at).toLocaleString('zh-CN') }}</p>
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <button
            @click="showInviteInterviewModal = false"
            class="px-4 py-2 border rounded-lg hover:bg-gray-50"
          >
            取消
          </button>
        </div>
      </div>
    </div>

    <!-- 申请线下宣讲会模态框 -->
    <div v-if="showRequestInfoSessionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-96 overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">申请线下宣讲会</h2>
        <form @submit.prevent="submitRequestInfoSession" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">宣讲会标题 *</label>
            <input
              v-model="requestForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
            <textarea
              v-model="requestForm.description"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">建议开始时间 *</label>
            <input
              v-model="requestForm.proposed_start_time"
              type="datetime-local"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">建议结束时间 *</label>
            <input
              v-model="requestForm.proposed_end_time"
              type="datetime-local"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">建议地点</label>
            <input
              v-model="requestForm.proposed_location"
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">最大学生数</label>
            <input
              v-model.number="requestForm.max_students"
              type="number"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">联系人</label>
            <input
              v-model="requestForm.contact_person"
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">联系电话</label>
            <input
              v-model="requestForm.contact_phone"
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">联系邮箱</label>
            <input
              v-model="requestForm.contact_email"
              type="email"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">申请留言</label>
            <textarea
              v-model="requestForm.message"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showRequestInfoSessionModal = false"
              class="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              提交申请
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCurrentUser, type User } from '@/api/users'
import {
  getChatSessions,
  getSessionMessages,
  type ChatSession,
  type Message,
} from '@/api/chat'
import { getStudentProfile, type StudentProfile } from '@/api/profile'
import { getTeacherProfile, type TeacherProfile } from '@/api/profile'
import { getResumes, type Resume } from '@/api/resumes'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'
import { getMark, createMark, updateMark, deleteMark, type Mark, type MarkCreateRequest } from '@/api/marks'
import { getSchool, getSchoolShareLink, requestOfflineInfoSession as requestOfflineInfoSessionAPI, type School, type OfflineInfoSessionRequest } from '@/api/schools'
import { downloadResume as downloadResumeAPI } from '@/api/resumes'
import { inviteStudentToInfoSession, searchStudents } from '@/api/infoSessions'
import { createInterview, type InterviewCreateRequest } from '@/api/interviews'
import { getInfoSessions } from '@/api/infoSessions'
import { getApplications } from '@/api/applications'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

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

// 对方用户信息
const otherUser = ref<User | null>(null)
const otherUserType = ref<string>('')
const otherStudentProfile = ref<StudentProfile | null>(null)
const otherTeacherProfile = ref<TeacherProfile | null>(null)
const teacherSchoolId = ref<string | null>(null)
const studentResumes = ref<Resume[]>([])
const defaultResume = ref<Resume | null>(null)
const isResumeFavorited = ref(false)
const isSchoolFavorited = ref(false)
const currentResumeMark = ref<Mark | null>(null)
const currentSchoolMark = ref<Mark | null>(null)

// 模态框状态
const showMarkResumeModal = ref(false)
const showMarkSchoolModal = ref(false)
const showInviteInfoSessionModal = ref(false)
const showInviteInterviewModal = ref(false)
const showRequestInfoSessionModal = ref(false)
const markForm = ref({ note: '', color: 'blue' })
const infoSessions = ref<any[]>([])
const applications = ref<any[]>([])
const currentInviteUserId = ref<string | null>(null)  // 当前邀请的用户ID
const requestForm = ref<OfflineInfoSessionRequest>({
  school_id: '',
  title: '',
  description: '',
  proposed_start_time: '',
  proposed_end_time: '',
  proposed_location: '',
  max_students: undefined,
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  message: ''
})

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
  const otherUserId = getOtherUserId.value
  if (!otherUserId || !currentSession.value) return

  try {
    // 从会话信息中获取对方用户类型
    const otherUserTypeFromSession = currentSession.value.user1_id === currentUserId.value
      ? currentSession.value.user2_type
      : currentSession.value.user1_type
    
    otherUserType.value = otherUserTypeFromSession || 'UNKNOWN'
    
    // 根据用户类型加载相应的信息
    if (otherUserType.value === 'STUDENT') {
      // 对于学生，通过简历API获取学生信息
      // 企业用户可以查看所有简历，我们可以通过user_id查找对应的简历
      try {
        // 先获取所有简历，然后通过user_id匹配找到对应的student_id
        // 注意：这需要后端API支持，或者我们需要通过其他方式获取student_id
        // 暂时先尝试获取简历列表，然后通过其他方式匹配
        const resumesResponse = await getResumes({ page_size: 100 })
        
        // 由于无法直接通过user_id查询，我们需要通过其他方式
        // 暂时先不加载详细信息，但允许用户使用快捷操作（会提示需要学生信息）
      } catch (error: any) {
        console.log('无法获取学生详细信息（权限限制）:', error)
      }
    } else if (otherUserType.value === 'TEACHER') {
      // 对于教师，暂时无法获取学校ID（需要权限）
      // 快捷操作中的学校相关功能可能无法使用
      console.log('教师用户，学校相关快捷操作需要学校ID，但无法获取（权限限制）')
    }
  } catch (error) {
    console.error('加载对方用户信息失败:', error)
  }
}

// 加载学生简历（通过user_id查找）
const loadStudentResumes = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) return
  
  try {
    // 通过user_id获取简历（后端API已支持）
    const response = await getResumes({ user_id: otherUserId, page_size: 10 })
    studentResumes.value = response.items
    defaultResume.value = response.items.find(r => r.is_default) || response.items[0] || null
    
    // 检查默认简历的收藏状态
    if (defaultResume.value) {
      try {
        isResumeFavorited.value = await checkFavorite('RESUME', defaultResume.value.id)
      } catch {
        isResumeFavorited.value = false
      }
      
      // 检查默认简历的标记
      try {
        currentResumeMark.value = await getMark('RESUME', defaultResume.value.id)
        if (currentResumeMark.value) {
          markForm.value.note = currentResumeMark.value.note || ''
          markForm.value.color = currentResumeMark.value.color || 'blue'
        }
      } catch {
        currentResumeMark.value = null
      }
    }
  } catch (error) {
    console.error('加载学生简历失败:', error)
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

watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

// ==================== 学生相关快捷操作 ====================

// 查看学生简历
const viewStudentResume = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  // 先加载简历
  if (studentResumes.value.length === 0) {
    await loadStudentResumes()
  }
  
  if (defaultResume.value) {
    // 打开新窗口查看简历
    window.open(`/enterprise/resumes/${defaultResume.value.id}`, '_blank')
  } else {
    alert('该学生暂无简历')
  }
}

// 标记简历
const markResume = () => {
  if (!defaultResume.value) {
    alert('该学生暂无简历')
    return
  }
  showMarkResumeModal.value = true
}

// 保存简历标记
const saveResumeMark = async () => {
  if (!defaultResume.value) return
  
  try {
    const markData: MarkCreateRequest = {
      target_type: 'RESUME',
      target_id: defaultResume.value.id,
      note: markForm.value.note,
      color: markForm.value.color
    }
    
    if (currentResumeMark.value) {
      await updateMark(currentResumeMark.value.id, {
        note: markForm.value.note,
        color: markForm.value.color
      })
    } else {
      currentResumeMark.value = await createMark(markData)
    }
    
    alert('标记已保存')
    showMarkResumeModal.value = false
  } catch (error: any) {
    alert('保存标记失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 切换简历收藏状态
const toggleResumeFavorite = async () => {
  if (!defaultResume.value) {
    alert('该学生暂无简历')
    return
  }
  
  try {
    if (isResumeFavorited.value) {
      await removeFavorite('RESUME', defaultResume.value.id)
      isResumeFavorited.value = false
      alert('已取消收藏')
    } else {
      await addFavorite('RESUME', defaultResume.value.id)
      isResumeFavorited.value = true
      alert('已收藏')
    }
  } catch (error: any) {
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 下载简历
const downloadResume = async () => {
  if (!defaultResume.value) {
    alert('该学生暂无简历')
    return
  }
  
  try {
    await downloadResumeAPI(defaultResume.value.id)
    alert('简历下载成功')
  } catch (error: any) {
    alert('下载失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 获取学生ID（通过user_id）
const getStudentIdByUserId = async (userId: string): Promise<string | null> => {
  try {
    // 通过简历API获取简历列表，然后找到对应的student_id
    // 注意：这需要后端API支持通过user_id查询，或者我们需要其他方式
    const resumesResponse = await getResumes({ page_size: 100 })
    
    // 由于无法直接通过user_id查询student_id，我们需要通过其他方式
    // 暂时返回null，让用户知道需要学生信息
    // TODO: 需要后端API支持通过user_id查询student_id
    return null
  } catch (error) {
    console.error('获取学生ID失败:', error)
    return null
  }
}

// 宣讲会邀请
const inviteToInfoSession = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  // 加载宣讲会列表
  try {
    const response = await getInfoSessions({ page_size: 100 })
    infoSessions.value = response.items.filter(s => s.status === 'PUBLISHED')
    
    // 存储当前用户ID，用于邀请时查找学生ID
    currentInviteUserId.value = otherUserId
    showInviteInfoSessionModal.value = true
  } catch (error: any) {
    alert('加载宣讲会列表失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 提交宣讲会邀请
const submitInfoSessionInvite = async (sessionId: string) => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  try {
    // 使用user_id邀请（后端API会转换为student_id）
    await inviteStudentToInfoSession(sessionId, undefined, otherUserId)
    alert('邀请成功')
    showInviteInfoSessionModal.value = false
  } catch (error: any) {
    alert('邀请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 面试邀请
const inviteToInterview = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  // 加载申请列表（通过user_id查找）
  try {
    // 通过user_id查找申请（后端API已支持）
    const response = await getApplications({ user_id: otherUserId, page_size: 100 })
    applications.value = response.items.filter(a => a.status === 'ACCEPTED')
    
    if (applications.value.length === 0) {
      alert('该学生暂无已通过的申请，无法安排面试')
      return
    }
    
    showInviteInterviewModal.value = true
  } catch (error: any) {
    alert('加载申请列表失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 提交面试邀请
const submitInterviewInvite = async (applicationId: string) => {
  try {
    router.push(`/enterprise/interviews/create?application_id=${applicationId}`)
    showInviteInterviewModal.value = false
  } catch (error: any) {
    alert('跳转失败: ' + (error.response?.data?.detail || error.message))
  }
}

// ==================== 学校相关快捷操作 ====================

// 查看学校详情
const viewSchoolDetail = () => {
  if (teacherSchoolId.value) {
    router.push(`/enterprise/schools/${teacherSchoolId.value}`)
  } else {
    alert('该教师未关联学校')
  }
}

// 标记学校
const markSchool = () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  showMarkSchoolModal.value = true
}

// 保存学校标记
const saveSchoolMark = async () => {
  if (!teacherSchoolId.value) return
  
  try {
    const markData: MarkCreateRequest = {
      target_type: 'SCHOOL',
      target_id: teacherSchoolId.value,
      note: markForm.value.note,
      color: markForm.value.color
    }
    
    if (currentSchoolMark.value) {
      await updateMark(currentSchoolMark.value.id, {
        note: markForm.value.note,
        color: markForm.value.color
      })
    } else {
      currentSchoolMark.value = await createMark(markData)
    }
    
    alert('标记已保存')
    showMarkSchoolModal.value = false
  } catch (error: any) {
    alert('保存标记失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 切换学校收藏状态
const toggleSchoolFavorite = async () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  
  try {
    if (isSchoolFavorited.value) {
      await removeFavorite('SCHOOL', teacherSchoolId.value)
      isSchoolFavorited.value = false
      alert('已取消收藏')
    } else {
      await addFavorite('SCHOOL', teacherSchoolId.value)
      isSchoolFavorited.value = true
      alert('已收藏')
    }
  } catch (error: any) {
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 分享学校
const shareSchool = async () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  
  try {
    const shareData = await getSchoolShareLink(teacherSchoolId.value)
    
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(shareData.share_url)
      alert('分享链接已复制到剪贴板')
    } else {
      prompt('分享链接（请复制）：', shareData.share_url)
    }
  } catch (error: any) {
    alert('获取分享链接失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 申请线下宣讲会
const requestOfflineInfoSession = () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  
  requestForm.value = {
    school_id: teacherSchoolId.value,
    title: '',
    description: '',
    proposed_start_time: '',
    proposed_end_time: '',
    proposed_location: '',
    max_students: undefined,
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    message: ''
  }
  showRequestInfoSessionModal.value = true
}

// 提交申请线下宣讲会
const submitRequestInfoSession = async () => {
  if (!teacherSchoolId.value) return
  
  try {
    await requestOfflineInfoSessionAPI(teacherSchoolId.value, requestForm.value)
    alert('申请已提交')
    showRequestInfoSessionModal.value = false
  } catch (error: any) {
    alert('申请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 初始化聊天（处理URL参数）
const initChat = async () => {
  try {
    const user = await getCurrentUser()
    currentUserId.value = user.id
    
    // 加载会话列表
    await loadSessions()
    
    // 检查URL参数中是否有user_id或student_id（从人才搜索发起聊天）
    const userIdParam = route.query.user_id as string
    const studentIdParam = route.query.student_id as string
    
    if (userIdParam || studentIdParam) {
      // 创建或获取聊天会话
      try {
        const { createOrGetChatSession } = await import('@/api/chat')
        let session
        
        if (studentIdParam) {
          // 如果提供了student_id，使用student_id创建会话
          // 后端API会将其转换为user_id
          session = await createOrGetChatSession('', studentIdParam)
        } else {
          // 使用user_id创建会话
          session = await createOrGetChatSession(userIdParam)
        }
        
        // 刷新会话列表
        await loadSessions()
        
        // 选择该会话
        await selectSession(session)
        
        // 清除URL参数
        router.replace({ path: route.path, query: {} })
      } catch (error: any) {
        console.error('创建聊天会话失败:', error)
        alert('创建聊天会话失败: ' + (error.response?.data?.detail || error.message))
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

onMounted(() => {
  initChat()
})
</script>

<style scoped>
.enterprise-chat {
  display: flex;
  flex-direction: column;
}
</style>

