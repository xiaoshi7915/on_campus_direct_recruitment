<template>
  <div class="student-jobs max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 标题和搜索栏 -->
    <div class="mb-10 animate-fade-in-up">
      <h1 class="text-5xl font-display font-bold text-gray-900 mb-6">职位搜索</h1>
      <div class="card-elevated rounded-2xl p-6 border border-gray-100/50">
        <div class="flex flex-col sm:flex-row gap-4">
          <div class="flex-1 relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索职位名称、公司名称..."
              class="w-full pl-10 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
              @keyup.enter="handleSearch"
            />
          </div>
          <button
            @click="handleSearch"
            class="px-8 py-3.5 bg-gradient-primary text-white rounded-xl font-semibold shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center transform hover:scale-105"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="card-elevated rounded-2xl p-6 mb-8 border border-gray-100/50">
      <h2 class="text-xl font-display font-semibold text-gray-900 mb-6 flex items-center">
        <div class="w-1 h-6 bg-gradient-primary rounded-full mr-3"></div>
        <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        筛选条件
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
            <svg class="w-4 h-4 mr-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            工作地点
          </label>
          <select
            v-model="filters.location"
            class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
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
          <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
            <svg class="w-4 h-4 mr-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            职位类型
          </label>
          <select
            v-model="filters.job_type"
            class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
            @change="handleSearch"
          >
            <option value="">全部</option>
            <option value="FULL_TIME">全职</option>
            <option value="PART_TIME">兼职</option>
            <option value="INTERN">实习</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
            <svg class="w-4 h-4 mr-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            薪资范围
          </label>
          <select
            v-model="filters.salary"
            class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
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
          <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
            <svg class="w-4 h-4 mr-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
            </svg>
            学历要求
          </label>
          <select
            v-model="filters.education"
            class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
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
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="jobs.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无职位信息</p>
        <p class="text-gray-400 text-sm mt-2">请尝试调整筛选条件</p>
      </div>
      <div
        v-for="job in jobs"
        :key="job.id"
        class="card-elevated rounded-2xl p-6 border-2 border-gray-200 hover:border-primary-300 hover:bg-gradient-to-br hover:from-primary-50/50 hover:to-transparent transition-all duration-300 cursor-pointer group"
        @click="goToJobDetail(job.id)"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-start justify-between mb-3">
              <h3 class="text-xl font-display font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                {{ job.title }}
              </h3>
              <span v-if="job.salary_min && job.salary_max" class="bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent font-display font-bold text-lg ml-4 whitespace-nowrap">
                {{ job.salary_min }}-{{ job.salary_max }}元
              </span>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3">
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
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
                </svg>
                {{ job.education || '不限' }}
              </span>
            </div>
            <p class="text-gray-700 line-clamp-2 mb-3">{{ job.description }}</p>
            <div v-if="job.tags" class="flex flex-wrap gap-2">
              <span
                v-for="tag in job.tags.split(',')"
                :key="tag"
                class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-md font-medium"
              >
                {{ tag }}
              </span>
            </div>
          </div>
          <div class="ml-6 flex flex-col items-end space-y-2">
            <button
              @click.stop="handleApply(job.id)"
              class="px-6 py-3 bg-gradient-primary text-white rounded-xl hover:shadow-lg transition-all duration-300 font-semibold whitespace-nowrap transform hover:scale-105 shadow-md"
            >
              立即申请
            </button>
            <button
              @click.stop="handleFavorite(job.id)"
              class="px-6 py-3 border-2 border-gray-300 rounded-xl hover:border-primary-500 hover:text-primary-600 hover:bg-primary-50 transition-all duration-300 font-medium whitespace-nowrap"
            >
              <span v-if="isFavorite(job.id)" class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
                已收藏
              </span>
              <span v-else class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                收藏
              </span>
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
import { ref, onMounted } from 'vue'
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
/* 样式已内联到模板中 */
</style>


