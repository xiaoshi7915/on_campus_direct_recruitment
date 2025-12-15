<template>
  <div class="enterprise-jobs max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">职位管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        发布职位
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-semibold text-gray-700 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          状态筛选：
        </label>
        <select
          v-model="statusFilter"
          @change="loadJobs"
          class="px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
        >
          <option value="">全部</option>
          <option value="DRAFT">草稿</option>
          <option value="PUBLISHED">已发布</option>
          <option value="CLOSED">已关闭</option>
        </select>
      </div>
    </div>

    <!-- 职位列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="jobs.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无职位信息</p>
        <p class="text-gray-400 text-sm mt-2">点击上方按钮发布第一个职位</p>
      </div>
      <div
        v-for="job in jobs"
        :key="job.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ job.title }}</h3>
              <span
                :class="getStatusClass(job.status)"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ getStatusText(job.status) }}
              </span>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ job.work_location }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ job.job_type }}
              </span>
              <span v-if="job.salary_min && job.salary_max" class="flex items-center text-blue-600 font-semibold">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ job.salary_min }}-{{ job.salary_max }}元
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
                </svg>
                {{ job.education || '不限' }}
              </span>
            </div>
            <p class="text-gray-700 line-clamp-2 mb-3 ml-11">{{ job.description }}</p>
            <div class="flex items-center space-x-6 text-sm text-gray-500 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                查看：{{ job.view_count }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                申请：{{ job.apply_count }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                发布时间：{{ formatDate(job.created_at) }}
              </span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editJob(job)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              编辑
            </button>
            <button
              @click="viewApplications(job.id)"
              class="px-5 py-2.5 border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              查看申请
            </button>
            <button
              @click="handleDeleteJob(job.id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              删除
            </button>
          </div>
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

    <!-- 创建/编辑职位模态框 -->
    <div
      v-if="showCreateModal || editingJob"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-gray-100 w-full max-w-4xl max-h-[95vh] flex flex-col overflow-hidden">
        <!-- 固定头部 -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200 flex-shrink-0">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {{ editingJob ? '编辑职位' : '发布职位' }}
          </h2>
          <button
            @click="closeModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <!-- 可滚动内容区域 -->
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">职位标题 *</label>
              <input
                v-model="jobForm.title"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="例如：Java开发工程师"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">部门</label>
              <input
                v-model="jobForm.department"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="例如：技术部"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">职位类型</label>
              <select
                v-model="jobForm.job_type"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              >
                <option value="FULL_TIME">全职</option>
                <option value="PART_TIME">兼职</option>
                <option value="INTERN">实习</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">工作地点</label>
              <input
                v-model="jobForm.work_location"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="例如：北京"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">最低薪资</label>
              <input
                v-model.number="jobForm.salary_min"
                type="number"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="例如：10000"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">最高薪资</label>
              <input
                v-model.number="jobForm.salary_max"
                type="number"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="例如：20000"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">工作经验</label>
              <input
                v-model="jobForm.experience"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="例如：1-3年"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">学历要求</label>
              <select
                v-model="jobForm.education"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              >
                <option value="不限">不限</option>
                <option value="本科">本科</option>
                <option value="硕士">硕士</option>
                <option value="博士">博士</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">职位描述 *</label>
            <textarea
              v-model="jobForm.description"
              required
              rows="6"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
              placeholder="请输入职位描述..."
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">职位要求</label>
            <textarea
              v-model="jobForm.requirements"
              rows="4"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
              placeholder="请输入职位要求..."
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">标签（用逗号分隔）</label>
            <input
              v-model="jobForm.tags"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              placeholder="例如：高薪,五险一金,带薪年假"
            />
          </div>
          <div v-if="editingJob">
            <label class="block text-sm font-semibold text-gray-700 mb-2">状态</label>
            <select
              v-model="jobForm.status"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            >
              <option value="DRAFT">草稿</option>
              <option value="PUBLISHED">已发布</option>
              <option value="CLOSED">已关闭</option>
            </select>
          </div>
          </div>
        </div>
        <!-- 固定底部按钮 -->
        <div class="flex justify-end space-x-4 p-6 border-t border-gray-200 bg-gray-50 flex-shrink-0">
          <button
            type="button"
            @click="closeModal"
            class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
          >
            取消
          </button>
          <button
            type="button"
            @click="saveJob"
            class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getJobs, createJob, updateJob, deleteJob, type Job } from '@/api/jobs'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 职位列表
const jobs = ref<Job[]>([])
const loading = ref(false)
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const showCreateModal = ref(false)
const editingJob = ref<Job | null>(null)

// 表单数据
const jobForm = ref({
  title: '',
  department: '',
  job_type: 'FULL_TIME',
  work_location: '',
  salary_min: undefined as number | undefined,
  salary_max: undefined as number | undefined,
  experience: '',
  education: '不限',
  description: '',
  requirements: '',
  tags: '',
  status: 'PUBLISHED',
})


// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    CLOSED: '已关闭',
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    DRAFT: 'bg-gray-100 text-gray-800',
    PUBLISHED: 'bg-green-100 text-green-800',
    CLOSED: 'bg-red-100 text-red-800',
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// 加载职位列表
const loadJobs = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }

    const response = await getJobs(params)
    jobs.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载职位列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadJobs()
}

// 编辑职位
const editJob = (job: Job) => {
  editingJob.value = job
  jobForm.value = {
    title: job.title,
    department: job.department || '',
    job_type: job.job_type || 'FULL_TIME',
    work_location: job.work_location || '',
    salary_min: job.salary_min,
    salary_max: job.salary_max,
    experience: job.experience || '',
    education: job.education || '不限',
    description: job.description,
    requirements: job.requirements || '',
    tags: job.tags || '',
    status: job.status,
  }
}

// 保存职位
const saveJob = async () => {
  try {
    if (editingJob.value) {
      await updateJob(editingJob.value.id, jobForm.value)
    } else {
      await createJob(jobForm.value)
    }
    closeModal()
    loadJobs()
  } catch (error: any) {
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  }
}

// 删除职位
const handleDeleteJob = async (jobId: string) => {
  if (!confirm('确定要删除这个职位吗？')) {
    return
  }
  try {
    await deleteJob(jobId)
    loadJobs()
  } catch (error: any) {
    alert(error.response?.data?.detail || '删除失败，请稍后重试')
  }
}

// 查看申请
const viewApplications = (jobId: string) => {
  router.push(`/enterprise/applications?job_id=${jobId}`)
}

// 关闭模态框
const closeModal = () => {
  showCreateModal.value = false
  editingJob.value = null
  jobForm.value = {
    title: '',
    department: '',
    job_type: 'FULL_TIME',
    work_location: '',
    salary_min: undefined,
    salary_max: undefined,
    experience: '',
    education: '不限',
    description: '',
    requirements: '',
    tags: '',
    status: 'PUBLISHED',
  }
}

onMounted(() => {
  loadJobs()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

