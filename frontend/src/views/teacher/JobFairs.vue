<template>
  <div class="teacher-job-fairs">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">双选会管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        创建双选会
      </button>
    </div>

    <!-- 双选会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="jobFairs.length === 0" class="text-center py-12 text-gray-500">
        暂无双选会信息
      </div>
      <div
        v-for="jobFair in jobFairs"
        :key="jobFair.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ jobFair.title }}</h3>
              <span
                :class="getStatusClass(jobFair.status)"
                class="px-2 py-1 rounded text-xs"
              >
                {{ getStatusText(jobFair.status) }}
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3">
              <p>时间：{{ formatDateTime(jobFair.start_time) }} - {{ formatDateTime(jobFair.end_time) }}</p>
              <p v-if="jobFair.location">地点：{{ jobFair.location }}</p>
              <p v-if="jobFair.max_enterprises">最大企业数：{{ jobFair.max_enterprises }}</p>
            </div>
            <p v-if="jobFair.description" class="text-gray-700 line-clamp-2">
              {{ jobFair.description }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editJobFair(jobFair)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="viewRegistrations(jobFair.id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              查看报名
            </button>
            <button
              @click="showInviteModal(jobFair)"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              邀请企业
            </button>
            <button
              @click="handleDeleteJobFair(jobFair.id)"
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
        <h2 class="text-2xl font-bold mb-4">创建双选会</h2>
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
              <label class="block text-sm font-medium mb-2">最大企业数</label>
              <input v-model.number="createForm.max_enterprises" type="number" min="1" class="w-full px-3 py-2 border rounded-lg" />
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
        <h2 class="text-2xl font-bold mb-4">编辑双选会</h2>
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
              <label class="block text-sm font-medium mb-2">最大企业数</label>
              <input v-model.number="editForm.max_enterprises" type="number" min="1" class="w-full px-3 py-2 border rounded-lg" />
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
                <p class="font-medium">企业ID: {{ reg.enterprise_id }}</p>
                <p class="text-sm text-gray-600">状态: {{ reg.status }}</p>
                <p v-if="reg.check_in_time" class="text-sm text-gray-600">签到时间: {{ new Date(reg.check_in_time).toLocaleString() }}</p>
              </div>
              <span :class="{
                'bg-yellow-100 text-yellow-800': reg.status === 'PENDING',
                'bg-green-100 text-green-800': reg.status === 'APPROVED',
                'bg-red-100 text-red-800': reg.status === 'REJECTED',
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
import { getJobFairs, createJobFair, updateJobFair, deleteJobFair, getJobFairRegistrations, inviteEnterpriseToJobFair, type JobFair, type JobFairRegistration } from '@/api/jobFairs'
import Pagination from '@/components/Pagination.vue'

// 双选会列表
const jobFairs = ref<JobFair[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showRegistrationsModal = ref(false)
const showInviteModalVisible = ref(false)
const currentJobFair = ref<JobFair | null>(null)
const registrations = ref<JobFairRegistration[]>([])
const inviteEnterpriseId = ref('')
const createForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  max_enterprises: 0,
})
const editForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  max_enterprises: 0,
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

// 加载双选会列表
const loadJobFairs = async () => {
  loading.value = true
  try {
    const response = await getJobFairs({ 
      page: currentPage.value,
      page_size: pageSize.value,
      status: undefined 
    })
    jobFairs.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载双选会列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadJobFairs()
}

// 保存创建
const saveCreate = async () => {
  try {
    await createJobFair({
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
      max_enterprises: 0,
    }
    loadJobFairs()
  } catch (error: any) {
    alert('创建失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 编辑双选会
const editJobFair = (jobFair: JobFair) => {
  currentJobFair.value = jobFair
  editForm.value = {
    title: jobFair.title,
    description: jobFair.description || '',
    start_time: jobFair.start_time ? new Date(jobFair.start_time).toISOString().slice(0, 16) : '',
    end_time: jobFair.end_time ? new Date(jobFair.end_time).toISOString().slice(0, 16) : '',
    location: jobFair.location || '',
    max_enterprises: jobFair.max_enterprises || 0,
    status: jobFair.status
  }
  showEditModal.value = true
}

// 保存编辑
const saveEdit = async () => {
  if (!currentJobFair.value) return
  
  try {
    await updateJobFair(currentJobFair.value.id, {
      ...editForm.value,
      start_time: new Date(editForm.value.start_time).toISOString(),
      end_time: new Date(editForm.value.end_time).toISOString(),
    })
    alert('更新成功！')
    showEditModal.value = false
    loadJobFairs()
  } catch (error: any) {
    alert('更新失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 查看报名
const viewRegistrations = async (jobFairId: string) => {
  try {
    registrations.value = await getJobFairRegistrations(jobFairId)
    showRegistrationsModal.value = true
  } catch (error: any) {
    alert('加载报名信息失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 显示邀请模态框
const showInviteModal = (jobFair: JobFair) => {
  currentJobFair.value = jobFair
  inviteEnterpriseId.value = ''
  showInviteModalVisible.value = true
}

// 邀请企业
const handleInviteEnterprise = async () => {
  if (!currentJobFair.value || !inviteEnterpriseId.value.trim()) {
    alert('请输入企业ID')
    return
  }
  
  try {
    await inviteEnterpriseToJobFair(currentJobFair.value.id, inviteEnterpriseId.value.trim())
    alert('邀请成功！')
    showInviteModalVisible.value = false
    inviteEnterpriseId.value = ''
    currentJobFair.value = null
    // 如果当前正在查看报名，刷新报名列表
    if (showRegistrationsModal.value && currentJobFair.value) {
      viewRegistrations(currentJobFair.value.id)
    }
  } catch (error: any) {
    alert('邀请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 删除双选会
const handleDeleteJobFair = async (jobFairId: string) => {
  if (!confirm('确定要删除这个双选会吗？')) {
    return
  }
  try {
    await deleteJobFair(jobFairId)
    alert('删除成功！')
    loadJobFairs()
  } catch (error: any) {
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadJobFairs()
})
</script>

<style scoped>
.teacher-job-fairs {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

