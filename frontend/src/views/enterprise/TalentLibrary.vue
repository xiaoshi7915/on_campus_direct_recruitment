<template>
  <div class="talent-library-page w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
        <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        人才库
      </h1>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        筛选条件
      </h2>
      <div class="flex flex-wrap items-center gap-4">
        <div class="flex items-center space-x-2">
          <label class="text-sm font-semibold text-gray-700 whitespace-nowrap">状态筛选：</label>
          <select
            v-model="statusFilter"
            @change="loadTalents"
            class="select-base min-w-[150px]"
          >
            <option value="">全部</option>
            <option value="FAVORITED">已收藏</option>
            <option value="COMMUNICATING">沟通中</option>
            <option value="INTERVIEWED">已约面</option>
            <option value="HIRED">已录用</option>
          </select>
        </div>
        <div class="flex-1 min-w-[200px]">
          <input
            v-model="keyword"
            type="text"
            placeholder="搜索姓名、手机号、邮箱..."
            class="input-base"
            @input="handleSearch"
          />
        </div>
        <button
          @click="loadTalents"
          class="btn btn-primary btn-md"
        >
          <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          搜索
        </button>
      </div>
    </div>

    <!-- 人才列表 -->
    <div class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="talents.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p class="text-lg">暂无人才记录</p>
      </div>
      <div v-else>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">姓名</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">联系方式</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">简历</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">状态</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">最后联系时间</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="talent in talents" :key="talent.student_id" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                      <span class="text-blue-600 font-semibold">{{ talent.student_name?.charAt(0) || 'T' }}</span>
                    </div>
                    <span class="text-sm font-semibold text-gray-900">{{ talent.student_name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ talent.student_phone || '-' }}</div>
                  <div class="text-xs text-gray-500">{{ talent.student_email || '-' }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div v-if="talent.resume_title" class="text-sm text-gray-900 max-w-xs truncate">{{ talent.resume_title }}</div>
                  <div v-else class="text-sm text-gray-400">-</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="getStatusClass(talent.status)"
                    class="px-3 py-1 rounded-full text-xs font-semibold"
                  >
                    {{ getStatusText(talent.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {{ talent.last_contact_time ? formatDate(talent.last_contact_time) : '-' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-if="talent.resume_id"
                      @click="viewResume(talent.resume_id)"
                      class="btn btn-primary btn-sm"
                      title="查看简历"
                    >
                      <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      查看简历
                    </button>
                    <button
                      v-if="talent.resume_id"
                      @click="downloadResumeFile(talent.resume_id)"
                      class="btn btn-success btn-sm"
                      title="下载简历"
                    >
                      <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      下载
                    </button>
                    <button
                      v-if="talent.application_id"
                      @click="viewApplication(talent.application_id)"
                      class="btn btn-secondary btn-sm"
                      title="查看申请"
                    >
                      <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      申请
                    </button>
                    <button
                      v-if="talent.interview_id"
                      @click="viewInterview(talent.interview_id)"
                      class="btn btn-secondary btn-sm"
                      title="查看面试"
                    >
                      <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      面试
                    </button>
                    <button
                      v-if="talent.offer_id"
                      @click="viewOffer(talent.offer_id)"
                      class="btn btn-success btn-sm"
                      title="查看Offer"
                    >
                      <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Offer
                    </button>
                    <button
                      @click="editTalent(talent)"
                      class="btn btn-outline-primary btn-sm"
                      title="编辑备注/标签"
                    >
                      <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      编辑
                    </button>
                    <button
                      @click="updateStatus(talent)"
                      class="btn btn-outline-secondary btn-sm"
                      title="更新状态"
                    >
                      <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      状态
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 分页 -->
        <div class="p-6 border-t border-gray-200 bg-gray-50">
          <Pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            @change="handlePaginationChange"
          />
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showEditModal = false"
    >
      <div class="bg-white rounded-2xl p-8 w-full max-w-md shadow-2xl border border-gray-100">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            编辑人才信息
          </h2>
          <button
            @click="showEditModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveEdit" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">备注</label>
            <textarea
              v-model="editForm.notes"
              rows="4"
              class="textarea-base"
              placeholder="请输入备注信息"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">标签（逗号分隔）</label>
            <input
              v-model="editForm.tags"
              type="text"
              class="input-base"
              placeholder="如：优秀、技术强、沟通好"
            />
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showEditModal = false"
              class="btn btn-secondary btn-md"
            >
              取消
            </button>
            <button
              type="submit"
              class="btn btn-primary btn-md"
            >
              <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              保存
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTalents, updateTalent, type TalentItem } from '@/api/enterpriseManagement'
import { downloadResume } from '@/api/resumes'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 数据
const talents = ref<TalentItem[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const statusFilter = ref('')
const keyword = ref('')

// 编辑弹窗
const showEditModal = ref(false)
const editingTalent = ref<TalentItem | null>(null)
const editForm = ref({
  notes: '',
  tags: ''
})

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    ALL: '全部',
    FAVORITED: '已收藏',
    COMMUNICATING: '沟通中',
    INTERVIEWED: '已约面',
    HIRED: '已录用'
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    ALL: 'bg-gray-100 text-gray-800',
    FAVORITED: 'bg-yellow-100 text-yellow-800',
    COMMUNICATING: 'bg-blue-100 text-blue-800',
    INTERVIEWED: 'bg-purple-100 text-purple-800',
    HIRED: 'bg-green-100 text-green-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载人才库列表
const loadTalents = async () => {
  loading.value = true
  try {
    const response = await getTalents({
      page: currentPage.value,
      page_size: pageSize.value,
      status_filter: statusFilter.value || undefined,
      keyword: keyword.value || undefined
    })
    talents.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('加载人才库失败:', error)
    // 如果是企业信息不存在的错误，直接跳转到企业中心页面，不显示错误提示
    if (error.response?.status === 404 && (error.response?.data?.detail?.includes('企业信息不存在') || error.response?.data?.detail?.includes('企业档案不存在'))) {
      // 直接跳转，不显示错误提示（全局错误处理已经跳过显示）
      router.push('/enterprise/profile')
      return
    }
    // 其他错误才显示提示
    alert('加载人才库失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  loadTalents()
}

// 分页变化
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadTalents()
}

// 查看简历
const viewResume = (resumeId: string) => {
  router.push(`/enterprise/resumes/${resumeId}`)
}

// 下载简历
const downloadResumeFile = async (resumeId: string) => {
  try {
    await downloadResume(resumeId)
  } catch (error: any) {
    console.error('下载简历失败:', error)
  }
}

// 查看申请
const viewApplication = (applicationId: string) => {
  router.push(`/enterprise/applications/${applicationId}`)
}

// 查看面试
const viewInterview = (interviewId: string) => {
  router.push(`/enterprise/schedules?type=INTERVIEW&interview_id=${interviewId}`)
}

// 查看Offer
const viewOffer = (offerId: string) => {
  router.push(`/enterprise/schedules?type=INTERVIEW&offer_id=${offerId}`)
}

// 编辑人才信息
const editTalent = (talent: TalentItem) => {
  editingTalent.value = talent
  editForm.value = {
    notes: '',
    tags: ''
  }
  showEditModal.value = true
}

// 保存编辑
const saveEdit = async () => {
  if (!editingTalent.value) return
  
  try {
    await updateTalent(editingTalent.value.student_id, {
      notes: editForm.value.notes || undefined,
      tags: editForm.value.tags || undefined
    })
    alert('保存成功')
    showEditModal.value = false
    editingTalent.value = null
    loadTalents()
  } catch (error: any) {
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 更新状态
const updateStatus = async (talent: TalentItem) => {
  const statusOptions = ['ALL', 'FAVORITED', 'COMMUNICATING', 'INTERVIEWED', 'HIRED']
  const statusTexts = ['全部', '已收藏', '沟通中', '已约面', '已录用']
  
  const currentIndex = statusOptions.indexOf(talent.status)
  const nextIndex = (currentIndex + 1) % statusOptions.length
  const newStatus = statusOptions[nextIndex]
  
  if (!confirm(`确定将状态更新为"${statusTexts[nextIndex]}"吗？`)) return
  
  try {
    await updateTalent(talent.student_id, {
      status: newStatus
    })
    alert('状态更新成功')
    loadTalents()
  } catch (error: any) {
    alert('状态更新失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadTalents()
})
</script>

<style scoped>
.talent-library-page {
  min-height: calc(100vh - 120px);
}
</style>
