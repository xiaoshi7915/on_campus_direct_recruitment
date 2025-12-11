<template>
  <div class="student-jobs">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">职位搜索</h1>
      <div class="flex items-center space-x-4">
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="搜索职位..."
          class="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          @keyup.enter="handleSearch"
        />
        <button
          @click="handleSearch"
          class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          搜索
        </button>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">工作地点</label>
          <select
            v-model="filters.location"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          >
            <option value="">全部</option>
            <option value="北京">北京</option>
            <option value="上海">上海</option>
            <option value="广州">广州</option>
            <option value="深圳">深圳</option>
            <option value="杭州">杭州</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">职位类型</label>
          <select
            v-model="filters.job_type"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          >
            <option value="">全部</option>
            <option value="FULL_TIME">全职</option>
            <option value="PART_TIME">兼职</option>
            <option value="INTERN">实习</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">薪资范围</label>
          <select
            v-model="filters.salary"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          >
            <option value="">全部</option>
            <option value="0-5000">5K以下</option>
            <option value="5000-10000">5K-10K</option>
            <option value="10000-20000">10K-20K</option>
            <option value="20000-">20K以上</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">学历要求</label>
          <select
            v-model="filters.education"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          >
            <option value="">全部</option>
            <option value="不限">不限</option>
            <option value="本科">本科</option>
            <option value="硕士">硕士</option>
            <option value="博士">博士</option>
          </select>
        </div>
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
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer"
        @click="goToJobDetail(job.id)"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ job.title }}</h3>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3">
              <span>{{ job.work_location }}</span>
              <span>{{ job.job_type }}</span>
              <span v-if="job.salary_min && job.salary_max">
                {{ job.salary_min }}-{{ job.salary_max }}元
              </span>
              <span>{{ job.education || '不限' }}</span>
            </div>
            <p class="text-gray-700 line-clamp-2">{{ job.description }}</p>
            <div v-if="job.tags" class="mt-3 flex flex-wrap gap-2">
              <span
                v-for="tag in job.tags.split(',')"
                :key="tag"
                class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
              >
                {{ tag }}
              </span>
            </div>
          </div>
          <div class="ml-6 flex flex-col items-end space-y-2">
            <button
              @click.stop="handleApply(job.id)"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              立即申请
            </button>
            <button
              @click.stop="handleFavorite(job.id)"
              class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              {{ isFavorite(job.id) ? '已收藏' : '收藏' }}
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getJobs, type Job } from '@/api/jobs'
import { createApplication } from '@/api/applications'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 搜索关键词
const searchKeyword = ref('')

// 筛选条件
const filters = ref({
  location: '',
  job_type: '',
  salary: '',
  education: '',
})

// 职位列表
const jobs = ref<Job[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 收藏状态
const favoriteIds = ref<Set<string>>(new Set())

// 计算总页数
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

// 检查是否已收藏
const isFavorite = (jobId: string) => favoriteIds.value.has(jobId)

// 搜索职位
const handleSearch = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
      status: 'PUBLISHED',
    }

    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    if (filters.value.location) {
      params.location = filters.value.location
    }
    if (filters.value.job_type) {
      params.job_type = filters.value.job_type
    }
    if (filters.value.education) {
      params.education = filters.value.education
    }

    const response = await getJobs(params)
    jobs.value = response.items
    total.value = response.total

    // 检查收藏状态
    for (const job of jobs.value) {
      const favorited = await checkFavorite('JOB', job.id)
      if (favorited) {
        favoriteIds.value.add(job.id)
      }
    }
  } catch (error) {
    console.error('搜索职位失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  handleSearch()
}

// 跳转到职位详情
const goToJobDetail = (jobId: string) => {
  router.push(`/student/jobs/${jobId}`)
}

// 申请职位
const handleApply = async (jobId: string) => {
  try {
    await createApplication({ job_id: jobId })
    alert('申请成功！')
  } catch (error: any) {
    alert(error.response?.data?.detail || '申请失败，请稍后重试')
  }
}

// 收藏/取消收藏
const handleFavorite = async (jobId: string) => {
  try {
    if (isFavorite(jobId)) {
      await removeFavorite('JOB', jobId)
      favoriteIds.value.delete(jobId)
    } else {
      await addFavorite('JOB', jobId)
      favoriteIds.value.add(jobId)
    }
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.student-jobs {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


