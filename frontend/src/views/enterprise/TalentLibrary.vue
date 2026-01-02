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
                  <div class="flex space-x-2">
                    <button
                      v-if="talent.resume_id"
                      @click="viewResume(talent.resume_id)"
                      class="px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 text-xs font-medium"
                      title="查看简历"
                    >
                      查看简历
                    </button>
                    <button
                      v-if="talent.resume_id"
                      @click="downloadResumeFile(talent.resume_id)"
                      class="px-3 py-1.5 bg-green-600 text-white rounded-lg hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 text-xs font-medium"
                      title="下载简历"
                    >
                      下载
                    </button>
                    <button
                      v-if="talent.application_id"
                      @click="viewApplication(talent.application_id)"
                      class="px-3 py-1.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 shadow-sm hover:shadow-md transition-all duration-200 text-xs font-medium"
                      title="查看申请"
                    >
                      申请
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTalents, type TalentItem } from '@/api/enterpriseManagement'
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

onMounted(() => {
  loadTalents()
})
</script>

<style scoped>
.talent-library-page {
  min-height: calc(100vh - 120px);
}
</style>
