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
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="showEditModal = false" class="px-4 py-2 border rounded-lg">取消</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">保存</button>
          </div>
        </form>
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
import { getInfoSessions, createInfoSession, updateInfoSession, deleteInfoSession, getInfoSessionRegistrations, type InfoSession, type InfoSessionRegistration } from '@/api/infoSessions'
import Pagination from '@/components/Pagination.vue'

// 宣讲会列表
const infoSessions = ref<InfoSession[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showRegistrationsModal = ref(false)
const currentSession = ref<InfoSession | null>(null)
const registrations = ref<InfoSessionRegistration[]>([])
const createForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  session_type: 'OFFLINE',
  live_url: '',
  max_students: 0,
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
  status: 'DRAFT'
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
    await createInfoSession({
      ...createForm.value,
      start_time: new Date(createForm.value.start_time).toISOString(),
      end_time: new Date(createForm.value.end_time).toISOString(),
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
    }
    loadInfoSessions()
  } catch (error: any) {
    alert('创建失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 编辑宣讲会
const editInfoSession = (session: InfoSession) => {
  currentSession.value = session
  editForm.value = {
    title: session.title,
    description: session.description || '',
    start_time: session.start_time ? new Date(session.start_time).toISOString().slice(0, 16) : '',
    end_time: session.end_time ? new Date(session.end_time).toISOString().slice(0, 16) : '',
    location: session.location || '',
    session_type: session.session_type,
    live_url: session.live_url || '',
    max_students: session.max_students || 0,
    status: session.status
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

