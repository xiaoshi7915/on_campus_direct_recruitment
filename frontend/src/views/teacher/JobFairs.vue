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
              <button
                v-if="jobFair.status === 'PENDING'"
                @click="showApprovalModal(jobFair)"
                class="ml-2 px-2 py-1 bg-yellow-500 text-white rounded text-xs hover:bg-yellow-600"
              >
                审批
              </button>
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
      <div class="bg-white rounded-lg p-6 max-w-5xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold">报名列表</h2>
          <button
            v-if="registrations.length > 0"
            @click="exportJobFairRegistrations"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            导出清单
          </button>
        </div>
        <div v-if="registrations.length === 0" class="text-center py-8 text-gray-500">
          暂无报名信息
        </div>
        <div v-else>
          <table class="w-full border-collapse">
            <thead>
              <tr class="bg-gray-50">
                <th class="border px-4 py-2 text-left">企业名称</th>
                <th class="border px-4 py-2 text-left">报名时间</th>
                <th class="border px-4 py-2 text-left">状态</th>
                <th class="border px-4 py-2 text-left">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="reg in registrations" :key="reg.id" class="hover:bg-gray-50">
                <td class="border px-4 py-2">{{ reg.enterprise_name || reg.enterprise_id }}</td>
                <td class="border px-4 py-2">{{ new Date(reg.created_at).toLocaleString('zh-CN') }}</td>
                <td class="border px-4 py-2">
                  <span :class="{
                    'bg-yellow-100 text-yellow-800': reg.status === 'PENDING',
                    'bg-green-100 text-green-800': reg.status === 'APPROVED',
                    'bg-red-100 text-red-800': reg.status === 'REJECTED',
                    'bg-blue-100 text-blue-800': reg.status === 'CHECKED_IN'
                  }" class="px-2 py-1 rounded text-xs">
                    {{ reg.status }}
                  </span>
                </td>
                <td class="border px-4 py-2">
                  <button
                    @click="viewEnterpriseDetail(reg)"
                    class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
                  >
                    查看详情
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="showRegistrationsModal = false" class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600">关闭</button>
        </div>
      </div>
    </div>

    <!-- 企业详情模态框 -->
    <div v-if="showEnterpriseDetailModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">企业详情</h2>
        <div v-if="selectedEnterpriseDetail" class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700">企业名称</label>
            <p class="mt-1 text-gray-900">{{ selectedEnterpriseDetail.company_name }}</p>
          </div>
          <div v-if="selectedEnterpriseDetail.industry">
            <label class="block text-sm font-medium text-gray-700">行业</label>
            <p class="mt-1 text-gray-900">{{ selectedEnterpriseDetail.industry }}</p>
          </div>
          <div v-if="selectedEnterpriseDetail.scale">
            <label class="block text-sm font-medium text-gray-700">规模</label>
            <p class="mt-1 text-gray-900">{{ selectedEnterpriseDetail.scale }}</p>
          </div>
          <div v-if="selectedEnterpriseDetail.address">
            <label class="block text-sm font-medium text-gray-700">地址</label>
            <p class="mt-1 text-gray-900">{{ selectedEnterpriseDetail.address }}</p>
          </div>
          <div v-if="selectedEnterpriseDetail.website">
            <label class="block text-sm font-medium text-gray-700">网站</label>
            <p class="mt-1 text-gray-900">
              <a :href="selectedEnterpriseDetail.website" target="_blank" class="text-blue-500 hover:underline">
                {{ selectedEnterpriseDetail.website }}
              </a>
            </p>
          </div>
          <div v-if="selectedEnterpriseDetail.description">
            <label class="block text-sm font-medium text-gray-700">描述</label>
            <p class="mt-1 text-gray-900">{{ selectedEnterpriseDetail.description }}</p>
          </div>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="showEnterpriseDetailModal = false; selectedEnterpriseDetail = null" class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600">关闭</button>
        </div>
      </div>
    </div>

    <!-- 邀请企业模态框 -->
    <div v-if="showInviteModalVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-4">邀请企业</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">选择企业 *</label>
            <select v-model="inviteEnterpriseId" required class="w-full px-3 py-2 border rounded-lg">
              <option value="">请选择企业</option>
              <option v-for="enterprise in enterpriseList" :key="enterprise.id" :value="enterprise.id">
                {{ enterprise.company_name }}
              </option>
            </select>
          </div>
        </div>
        <div class="mt-6 flex justify-end space-x-3">
          <button type="button" @click="showInviteModalVisible = false; inviteEnterpriseId = ''; currentJobFair = null" class="px-4 py-2 border rounded-lg">取消</button>
          <button type="button" @click="handleInviteEnterprise" class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600">邀请</button>
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
import { approveJobFair, type ApprovalRequest } from '@/api/approvals'
import { getEnterprises, type EnterpriseProfile } from '@/api/enterprises'
import Pagination from '@/components/Pagination.vue'

// 双选会列表
const jobFairs = ref<JobFair[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showRegistrationsModal = ref(false)
const showInviteModalVisible = ref(false)
const showApprovalModalVisible = ref(false)
const showEnterpriseDetailModal = ref(false)
const currentJobFair = ref<JobFair | null>(null)
const registrations = ref<JobFairRegistration[]>([])
const inviteEnterpriseId = ref('')
const enterpriseList = ref<EnterpriseProfile[]>([])
const selectedEnterpriseDetail = ref<any>(null)
const approvalAction = ref<'APPROVE' | 'REJECT'>('APPROVE')
const approvalComment = ref('')
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
    PENDING: '待审批',
    PUBLISHED: '已发布',
    REJECTED: '已拒绝',
    ONGOING: '进行中',
    ENDED: '已结束',
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    DRAFT: 'bg-gray-100 text-gray-800',
    PENDING: 'bg-yellow-100 text-yellow-800',
    PUBLISHED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800',
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

// 加载企业列表
const loadEnterprises = async () => {
  try {
    const response = await getEnterprises({ page_size: 100 })
    enterpriseList.value = response.items
  } catch (error) {
    console.error('加载企业列表失败:', error)
  }
}

// 显示邀请模态框
const showInviteModal = (jobFair: JobFair) => {
  currentJobFair.value = jobFair
  inviteEnterpriseId.value = ''
  loadEnterprises()
  showInviteModalVisible.value = true
}

// 查看企业详情
const viewEnterpriseDetail = (reg: JobFairRegistration) => {
  if (reg.enterprise_detail) {
    selectedEnterpriseDetail.value = reg.enterprise_detail
    showEnterpriseDetailModal.value = true
  } else {
    alert('企业详情不可用')
  }
}

// 导出双选会报名列表
const exportJobFairRegistrations = () => {
  if (registrations.value.length === 0) {
    alert('没有可导出的数据')
    return
  }
  
  // 准备CSV数据
  const headers = ['企业名称', '报名时间', '状态', '签到时间']
  const rows = registrations.value.map(reg => [
    reg.enterprise_name || reg.enterprise_id,
    new Date(reg.created_at).toLocaleString('zh-CN'),
    reg.status,
    reg.check_in_time ? new Date(reg.check_in_time).toLocaleString('zh-CN') : ''
  ])
  
  // 转换为CSV格式
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')
  
  // 添加BOM以支持中文
  const BOM = '\uFEFF'
  const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `双选会报名列表_${currentJobFair.value?.title || '未命名'}_${new Date().toISOString().slice(0, 10)}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
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
    const invitedJobFairId = currentJobFair.value?.id
    inviteEnterpriseId.value = ''
    currentJobFair.value = null
    // 如果当前正在查看报名，刷新报名列表
    if (showRegistrationsModal.value && invitedJobFairId) {
      viewRegistrations(invitedJobFairId)
    }
  } catch (error: any) {
    alert('邀请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 显示审批模态框
const showApprovalModal = (jobFair: JobFair) => {
  currentJobFair.value = jobFair
  approvalAction.value = 'APPROVE'
  approvalComment.value = ''
  showApprovalModalVisible.value = true
}

// 审批双选会
const handleApproveJobFair = async () => {
  if (!currentJobFair.value) return
  
  try {
    await approveJobFair(currentJobFair.value.id, {
      action: approvalAction.value,
      comment: approvalComment.value || undefined
    })
    alert(approvalAction.value === 'APPROVE' ? '审批通过！' : '审批拒绝！')
    showApprovalModalVisible.value = false
    currentJobFair.value = null
    approvalAction.value = 'APPROVE'
    approvalComment.value = ''
    loadJobFairs()
  } catch (error: any) {
    alert('审批失败: ' + (error.response?.data?.detail || error.message))
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
  loadEnterprises()
})
</script>

<style scoped>
.teacher-job-fairs {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

