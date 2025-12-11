<template>
  <div class="enterprise-jobs">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">职位管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        发布职位
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="statusFilter"
          @change="loadJobs"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="jobs.length === 0" class="text-center py-12 text-gray-500">
        暂无职位信息
      </div>
      <div
        v-for="job in jobs"
        :key="job.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ job.title }}</h3>
              <span
                :class="getStatusClass(job.status)"
                class="px-2 py-1 rounded text-xs"
              >
                {{ getStatusText(job.status) }}
              </span>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3">
              <span>{{ job.work_location }}</span>
              <span>{{ job.job_type }}</span>
              <span v-if="job.salary_min && job.salary_max">
                {{ job.salary_min }}-{{ job.salary_max }}元
              </span>
              <span>{{ job.education || '不限' }}</span>
            </div>
            <p class="text-gray-700 line-clamp-2 mb-3">{{ job.description }}</p>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>查看：{{ job.view_count }}</span>
              <span>申请：{{ job.apply_count }}</span>
              <span>发布时间：{{ formatDate(job.created_at) }}</span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editJob(job)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="viewApplications(job.id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              查看申请
            </button>
            <button
              @click="handleDeleteJob(job.id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
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
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">
          {{ editingJob ? '编辑职位' : '发布职位' }}
        </h2>
        <form @submit.prevent="saveJob">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">职位标题 *</label>
              <input
                v-model="jobForm.title"
                type="text"
                required
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例如：Java开发工程师"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">部门</label>
              <input
                v-model="jobForm.department"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例如：技术部"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">职位类型</label>
              <select
                v-model="jobForm.job_type"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="FULL_TIME">全职</option>
                <option value="PART_TIME">兼职</option>
                <option value="INTERN">实习</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">工作地点</label>
              <input
                v-model="jobForm.work_location"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例如：北京"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">最低薪资</label>
              <input
                v-model.number="jobForm.salary_min"
                type="number"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例如：10000"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">最高薪资</label>
              <input
                v-model.number="jobForm.salary_max"
                type="number"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例如：20000"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">工作经验</label>
              <input
                v-model="jobForm.experience"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例如：1-3年"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">学历要求</label>
              <select
                v-model="jobForm.education"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="不限">不限</option>
                <option value="本科">本科</option>
                <option value="硕士">硕士</option>
                <option value="博士">博士</option>
              </select>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">职位描述 *</label>
            <textarea
              v-model="jobForm.description"
              required
              rows="6"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入职位描述..."
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">职位要求</label>
            <textarea
              v-model="jobForm.requirements"
              rows="4"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入职位要求..."
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">标签（用逗号分隔）</label>
            <input
              v-model="jobForm.tags"
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：高薪,五险一金,带薪年假"
            />
          </div>
          <div v-if="editingJob" class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
            <select
              v-model="jobForm.status"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="DRAFT">草稿</option>
              <option value="PUBLISHED">已发布</option>
              <option value="CLOSED">已关闭</option>
            </select>
          </div>
          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="closeModal"
              class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              保存
            </button>
          </div>
        </form>
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
.enterprise-jobs {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

