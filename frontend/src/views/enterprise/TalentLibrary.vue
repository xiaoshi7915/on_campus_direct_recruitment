<template>
  <div class="talent-library-page">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">人才库</h1>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="statusFilter"
          @change="loadTalents"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">全部</option>
          <option value="ALL">全部</option>
          <option value="FAVORITED">已收藏</option>
          <option value="COMMUNICATING">沟通中</option>
          <option value="INTERVIEWED">已约面</option>
          <option value="HIRED">已录用</option>
        </select>
        <input
          v-model="keyword"
          type="text"
          placeholder="搜索姓名、手机号、邮箱"
          class="flex-1 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          @input="handleSearch"
        />
        <button
          @click="loadTalents"
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          搜索
        </button>
      </div>
    </div>

    <!-- 人才列表 -->
    <div class="bg-white rounded-lg shadow">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="talents.length === 0" class="text-center py-12 text-gray-500">
        暂无人才记录
      </div>
      <div v-else>
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">姓名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">联系方式</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">简历</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">最后联系时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="talent in talents" :key="talent.student_id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ talent.student_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>{{ talent.student_phone || '-' }}</div>
                <div class="text-xs text-gray-400">{{ talent.student_email || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div v-if="talent.resume_title">{{ talent.resume_title }}</div>
                <div v-else class="text-gray-400">-</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="getStatusClass(talent.status)"
                  class="px-2 py-1 rounded text-xs font-medium"
                >
                  {{ getStatusText(talent.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ talent.last_contact_time ? formatDate(talent.last_contact_time) : '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2">
                  <button
                    v-if="talent.resume_id"
                    @click="viewResume(talent.resume_id)"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    查看简历
                  </button>
                  <button
                    v-if="talent.resume_id"
                    @click="downloadResumeFile(talent.resume_id)"
                    class="text-green-600 hover:text-green-900"
                  >
                    下载简历
                  </button>
                  <button
                    v-if="talent.application_id"
                    @click="viewApplication(talent.application_id)"
                    class="text-purple-600 hover:text-purple-900"
                  >
                    查看申请
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分页 -->
        <div class="p-4 border-t">
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
    month: 'long',
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
  router.push(`/teacher/resumes/${resumeId}`)
}

// 下载简历
const downloadResumeFile = async (resumeId: string) => {
  try {
    await downloadResume(resumeId)
  } catch (error: any) {
    // 错误信息已经在downloadResume中处理并显示，这里不需要再次alert
    // 但如果需要，可以在这里添加额外的处理逻辑
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
  max-width: 1200px;
  margin: 0 auto;
}
</style>

