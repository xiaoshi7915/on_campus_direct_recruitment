<template>
  <div class="enterprise-info-sessions">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">宣讲会管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        创建宣讲会
      </button>
    </div>

    <!-- 宣讲会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="infoSessions.length === 0" class="text-center py-12 text-gray-500">
        暂无宣讲会信息
      </div>
      <div
        v-for="session in infoSessions"
        :key="session.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ session.title }}</h3>
              <span
                :class="getStatusClass(session.status)"
                class="px-2 py-1 rounded text-xs"
              >
                {{ getStatusText(session.status) }}
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3">
              <p>时间：{{ formatDateTime(session.start_time) }} - {{ formatDateTime(session.end_time) }}</p>
              <p v-if="session.location">地点：{{ session.location }}</p>
              <p>类型：{{ getSessionTypeText(session.session_type) }}</p>
              <p v-if="session.max_students">最大人数：{{ session.max_students }}</p>
              <p>已报名：{{ session.check_in_count }}</p>
            </div>
            <p v-if="session.description" class="text-gray-700 line-clamp-2">
              {{ session.description }}
            </p>
            <div v-if="session.live_url" class="mt-3">
              <a
                :href="session.live_url"
                target="_blank"
                class="text-blue-600 hover:text-blue-800"
              >
                直播链接 →
              </a>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editInfoSession(session)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="viewRegistrations(session.id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              查看报名
            </button>
            <button
              @click="showInviteModal(session.id)"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              邀请学生
            </button>
            <button
              @click="handleDeleteInfoSession(session.id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建模态框 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">创建宣讲会</h2>
        <form @submit.prevent="saveCreate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">标题 *</label>
              <input v-model="createForm.title" type="text" required class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">描述</label>
              <textarea v-model="createForm.description" rows="3" class="w-full px-3 py-2 border rounded-lg"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium mb-2">开始时间 *</label>
                <input v-model="createForm.start_time" type="datetime-local" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-2">结束时间 *</label>
                <input v-model="createForm.end_time" type="datetime-local" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">地点</label>
              <input v-model="createForm.location" type="text" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">类型 *</label>
              <select v-model="createForm.session_type" required class="w-full px-3 py-2 border rounded-lg">
                <option value="OFFLINE">线下</option>
                <option value="ONLINE">线上</option>
                <option value="HYBRID">混合</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">直播链接</label>
              <input v-model="createForm.live_url" type="url" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">最大人数</label>
              <input v-model.number="createForm.max_students" type="number" min="1" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">宣讲会资料</label>
              <div class="space-y-2">
                <div v-for="(material, index) in createForm.materials" :key="index" class="flex items-center space-x-2">
                  <a :href="material" target="_blank" class="text-blue-600 hover:text-blue-800 flex-1 truncate">{{ material }}</a>
                  <button type="button" @click="createForm.materials.splice(index, 1)" class="text-red-600 hover:text-red-800">删除</button>
                </div>
                <input
                  type="file"
                  ref="createFileInput"
                  @change="handleCreateFileSelect"
                  accept=".pdf,.doc,.docx,.ppt,.pptx"
                  class="hidden"
                />
                <button
                  type="button"
                  @click="createFileInput?.click()"
                  class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  上传资料
                </button>
              </div>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="showCreateModal = false" class="px-4 py-2 border rounded-lg">取消</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">创建</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 编辑模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">编辑宣讲会</h2>
        <form @submit.prevent="saveEdit">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">标题</label>
              <input v-model="editForm.title" type="text" required class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">描述</label>
              <textarea v-model="editForm.description" rows="3" class="w-full px-3 py-2 border rounded-lg"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium mb-2">开始时间</label>
                <input v-model="editForm.start_time" type="datetime-local" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-2">结束时间</label>
                <input v-model="editForm.end_time" type="datetime-local" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">地点</label>
              <input v-model="editForm.location" type="text" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">类型</label>
              <select v-model="editForm.session_type" class="w-full px-3 py-2 border rounded-lg">
                <option value="OFFLINE">线下</option>
                <option value="ONLINE">线上</option>
                <option value="HYBRID">混合</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">直播链接</label>
              <input v-model="editForm.live_url" type="url" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">最大人数</label>
              <input v-model.number="editForm.max_students" type="number" min="1" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">状态</label>
              <select v-model="editForm.status" class="w-full px-3 py-2 border rounded-lg">
                <option value="DRAFT">草稿</option>
                <option value="PUBLISHED">已发布</option>
                <option value="ONGOING">进行中</option>
                <option value="ENDED">已结束</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">宣讲会资料</label>
              <div class="space-y-2">
                <div v-for="(material, index) in editForm.materials" :key="index" class="flex items-center space-x-2">
                  <a :href="material" target="_blank" class="text-blue-600 hover:text-blue-800 flex-1 truncate">{{ material }}</a>
                  <button type="button" @click="editForm.materials.splice(index, 1)" class="text-red-600 hover:text-red-800">删除</button>
                </div>
                <input
                  type="file"
                  ref="editFileInput"
                  @change="handleEditFileSelect"
                  accept=".pdf,.doc,.docx,.ppt,.pptx"
                  class="hidden"
                />
                <button
                  type="button"
                  @click="editFileInput?.click()"
                  class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  上传资料
                </button>
              </div>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="showEditModal = false" class="px-4 py-2 border rounded-lg">取消</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">保存</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 邀请学生模态框 -->
    <div v-if="showInviteStudentModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-3xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">邀请学生参加宣讲会</h2>
        
        <!-- 搜索和筛选 -->
        <div class="mb-4 space-y-3">
          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="block text-sm font-medium mb-2">搜索学生（姓名/学号）</label>
              <input v-model="searchKeyword" type="text" @input="handleSearchStudents" class="w-full px-3 py-2 border rounded-lg" placeholder="输入姓名或学号" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">院系</label>
              <select v-model="searchDepartmentId" @change="handleSearchStudents" class="w-full px-3 py-2 border rounded-lg">
                <option value="">全部</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">年级</label>
              <select v-model="searchGrade" @change="handleSearchStudents" class="w-full px-3 py-2 border rounded-lg">
                <option value="">全部</option>
                <option value="2021">2021级</option>
                <option value="2022">2022级</option>
                <option value="2023">2023级</option>
                <option value="2024">2024级</option>
                <option value="2025">2025级</option>
              </select>
            </div>
          </div>
          <button @click="handleSearchStudents" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">搜索</button>
        </div>
        
        <!-- 学生列表 -->
        <div class="mb-4 border rounded-lg max-h-96 overflow-y-auto">
          <div v-if="searchingStudents" class="text-center py-8 text-gray-500">搜索中...</div>
          <div v-else-if="searchStudentsList.length === 0" class="text-center py-8 text-gray-500">暂无学生</div>
          <div v-else class="divide-y">
            <div v-for="student in searchStudentsList" :key="student.id" class="p-3 hover:bg-gray-50 flex items-center justify-between">
              <div class="flex-1">
                <div class="font-medium">{{ student.real_name }}</div>
                <div class="text-sm text-gray-500">学号: {{ student.student_id }} | 年级: {{ student.grade || '-' }} | 专业: {{ student.major || '-' }}</div>
              </div>
              <input
                type="checkbox"
                :value="student.id"
                v-model="selectedStudentIds"
                class="ml-4"
              />
            </div>
          </div>
        </div>
        
        <div class="mb-4 text-sm text-gray-600">
          已选择 {{ selectedStudentIds.length }} 名学生
        </div>
        
        <div class="mt-6 flex justify-end space-x-3">
          <button type="button" @click="closeInviteModal" class="px-4 py-2 border rounded-lg">取消</button>
          <button type="button" @click="handleInviteStudentsBatch" :disabled="selectedStudentIds.length === 0" class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed">
            批量邀请 ({{ selectedStudentIds.length }})
          </button>
        </div>
      </div>
    </div>

    <!-- 报名列表模态框 -->
    <div v-if="showRegistrationsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">报名列表</h2>
        <div v-if="registrations.length === 0" class="text-center py-8 text-gray-500">
          暂无报名信息
        </div>
        <div v-else class="space-y-2">
          <div v-for="reg in registrations" :key="reg.id" class="border rounded-lg p-4">
            <div class="flex justify-between items-center">
              <div>
                <p class="font-medium">学生ID: {{ reg.student_id }}</p>
                <p class="text-sm text-gray-600">状态: {{ reg.status }}</p>
                <p v-if="reg.check_in_time" class="text-sm text-gray-600">签到时间: {{ new Date(reg.check_in_time).toLocaleString() }}</p>
              </div>
              <span :class="{
                'bg-yellow-100 text-yellow-800': reg.status === 'PENDING',
                'bg-green-100 text-green-800': reg.status === 'CONFIRMED',
                'bg-red-100 text-red-800': reg.status === 'CANCELLED',
                'bg-blue-100 text-blue-800': reg.status === 'CHECKED_IN'
              }" class="px-2 py-1 rounded text-xs">
                {{ reg.status }}
              </span>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="showRegistrationsModal = false" class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600">关闭</button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <Pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      @change="handlePaginationChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getInfoSessions, createInfoSession, updateInfoSession, deleteInfoSession, getInfoSessionRegistrations, inviteStudentToInfoSession, searchStudents, inviteStudentsBatch, type InfoSession, type InfoSessionRegistration, type StudentSearchItem } from '@/api/infoSessions'
import { getDepartments, type Department } from '@/api/departments'
import { uploadDocument } from '@/api/upload'
import Pagination from '@/components/Pagination.vue'

// 宣讲会列表
const infoSessions = ref<InfoSession[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showRegistrationsModal = ref(false)
const showInviteStudentModal = ref(false)
const currentSession = ref<InfoSession | null>(null)
const currentInviteSessionId = ref<string | null>(null)
const inviteStudentId = ref('')
const registrations = ref<InfoSessionRegistration[]>([])
const searchKeyword = ref('')
const searchDepartmentId = ref('')
const searchGrade = ref('')
const searchStudentsList = ref<StudentSearchItem[]>([])
const selectedStudentIds = ref<string[]>([])
const searchingStudents = ref(false)
const departments = ref<Department[]>([])
const createFileInput = ref<HTMLInputElement | null>(null)
const editFileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

const createForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  session_type: 'OFFLINE',
  live_url: '',
  max_students: 0,
  materials: [] as string[],
})
const editForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  session_type: 'OFFLINE',
  live_url: '',
  max_students: 0,
  status: 'DRAFT',
  materials: [] as string[],
})

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 获取宣讲会类型文本
const getSessionTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    OFFLINE: '线下',
    ONLINE: '线上',
    HYBRID: '混合',
  }
  return typeMap[type] || type
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    ONGOING: '进行中',
    ENDED: '已结束',
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    DRAFT: 'bg-gray-100 text-gray-800',
    PUBLISHED: 'bg-green-100 text-green-800',
    ONGOING: 'bg-blue-100 text-blue-800',
    ENDED: 'bg-gray-100 text-gray-500',
  }
  return classMap[status] || ''
}

// 分页相关
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 加载宣讲会列表
const loadInfoSessions = async () => {
  loading.value = true
  try {
    const response = await getInfoSessions({ 
      page: currentPage.value,
      page_size: pageSize.value,
      status: undefined 
    })
    infoSessions.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载宣讲会列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadInfoSessions()
}

// 保存创建
const saveCreate = async () => {
  try {
    const response = await createInfoSession({
      ...createForm.value,
      start_time: new Date(createForm.value.start_time).toISOString(),
      end_time: new Date(createForm.value.end_time).toISOString(),
      materials: createForm.value.materials.length > 0 ? createForm.value.materials : undefined,
    })
    alert('创建成功！')
    showCreateModal.value = false
    createForm.value = {
      title: '',
      description: '',
      start_time: '',
      end_time: '',
      location: '',
      session_type: 'OFFLINE',
      live_url: '',
      max_students: 0,
      materials: [],
    }
    // 刷新列表
    await loadInfoSessions()
  } catch (error: any) {
    alert('创建失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 处理创建时的文件选择
const handleCreateFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  
  uploading.value = true
  try {
    const response = await uploadDocument(file, 'info_session')
    createForm.value.materials.push(response.url)
    alert('文件上传成功！')
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploading.value = false
    if (createFileInput.value) {
      createFileInput.value.value = ''
    }
  }
}

// 处理编辑时的文件选择
const handleEditFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  
  uploading.value = true
  try {
    const response = await uploadDocument(file, 'info_session')
    editForm.value.materials.push(response.url)
    alert('文件上传成功！')
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploading.value = false
    if (editFileInput.value) {
      editFileInput.value.value = ''
    }
  }
}

// 编辑宣讲会
const editInfoSession = (session: InfoSession) => {
  currentSession.value = session
  // 解析materials字段（可能是JSON字符串或数组）
  let materials: string[] = []
  if (session.materials) {
    if (typeof session.materials === 'string') {
      try {
        materials = JSON.parse(session.materials)
      } catch {
        materials = [session.materials]
      }
    } else if (Array.isArray(session.materials)) {
      materials = session.materials
    }
  }
  
  editForm.value = {
    title: session.title,
    description: session.description || '',
    start_time: session.start_time ? new Date(session.start_time).toISOString().slice(0, 16) : '',
    end_time: session.end_time ? new Date(session.end_time).toISOString().slice(0, 16) : '',
    location: session.location || '',
    session_type: session.session_type,
    live_url: session.live_url || '',
    max_students: session.max_students || 0,
    status: session.status,
    materials: materials
  }
  showEditModal.value = true
}

// 保存编辑
const saveEdit = async () => {
  if (!currentSession.value) return
  
  try {
    await updateInfoSession(currentSession.value.id, {
      ...editForm.value,
      start_time: new Date(editForm.value.start_time).toISOString(),
      end_time: new Date(editForm.value.end_time).toISOString(),
      materials: editForm.value.materials.length > 0 ? editForm.value.materials : undefined,
    })
    alert('更新成功！')
    showEditModal.value = false
    loadInfoSessions()
  } catch (error: any) {
    alert('更新失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 查看报名
const viewRegistrations = async (sessionId: string) => {
  try {
    registrations.value = await getInfoSessionRegistrations(sessionId)
    showRegistrationsModal.value = true
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || error.message
    if (error.response?.status === 403) {
      alert('权限不足：只能查看自己创建的宣讲会的报名信息。')
    } else {
      alert('加载报名信息失败: ' + errorMessage)
    }
  }
}

// 加载院系列表
const loadDepartments = async () => {
  try {
    const response = await getDepartments({ page_size: 100 })
    departments.value = response.items
  } catch (error) {
    console.error('加载院系列表失败:', error)
  }
}

// 显示邀请模态框
const showInviteModal = (sessionId: string) => {
  currentInviteSessionId.value = sessionId
  searchKeyword.value = ''
  searchDepartmentId.value = ''
  searchGrade.value = ''
  searchStudentsList.value = []
  selectedStudentIds.value = []
  showInviteStudentModal.value = true
  loadDepartments()
  handleSearchStudents()
}

// 关闭邀请模态框
const closeInviteModal = () => {
  showInviteStudentModal.value = false
  searchKeyword.value = ''
  searchDepartmentId.value = ''
  searchGrade.value = ''
  searchStudentsList.value = []
  selectedStudentIds.value = []
  currentInviteSessionId.value = null
}

// 搜索学生
const handleSearchStudents = async () => {
  // 搜索学生不需要session_id，可以独立搜索
  searchingStudents.value = true
  try {
    const response = await searchStudents({
      keyword: searchKeyword.value || undefined,
      department_id: searchDepartmentId.value || undefined,
      grade: searchGrade.value || undefined,
      page: 1,
      page_size: 100
    })
    searchStudentsList.value = response.items
  } catch (error: any) {
    console.error('搜索学生失败:', error)
    alert('搜索学生失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    searchingStudents.value = false
  }
}

// 批量邀请学生
const handleInviteStudentsBatch = async () => {
  if (!currentInviteSessionId.value || selectedStudentIds.value.length === 0) {
    alert('请选择要邀请的学生')
    return
  }
  
  try {
    const result = await inviteStudentsBatch(currentInviteSessionId.value, selectedStudentIds.value)
    alert(`邀请完成！成功: ${result.success_count}，失败: ${result.failed_count}`)
    if (result.failed_reasons.length > 0) {
      console.log('失败原因:', result.failed_reasons)
    }
    closeInviteModal()
    // 刷新报名列表
    if (showRegistrationsModal.value && currentInviteSessionId.value) {
      await viewRegistrations(currentInviteSessionId.value)
    }
  } catch (error: any) {
    alert('批量邀请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 删除宣讲会
const handleDeleteInfoSession = async (sessionId: string) => {
  if (!confirm('确定要删除这个宣讲会吗？')) {
    return
  }
  try {
    await deleteInfoSession(sessionId)
    alert('删除成功！')
    loadInfoSessions()
  } catch (error: any) {
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadInfoSessions()
})
</script>

<style scoped>
.enterprise-info-sessions {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

