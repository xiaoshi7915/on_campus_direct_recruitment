<template>
  <div class="student-favorites w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">我的收藏</h1>

    <!-- 筛选 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-semibold text-gray-700 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          收藏类型：
        </label>
        <select
          v-model="targetType"
          @change="handleSearch"
          class="px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
        >
          <option value="">全部</option>
          <option value="JOB">职位</option>
          <option value="COMPANY">企业</option>
        </select>
      </div>
    </div>

    <!-- 收藏列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="favorites.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无收藏</p>
        <p class="text-gray-400 text-sm mt-2">快去收藏感兴趣的职位吧！</p>
      </div>
      <div
        v-for="favorite in favorites"
        :key="favorite.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-medium">
                {{ getTargetTypeName(favorite.target_type) }}
              </span>
              <h3 class="text-xl font-semibold text-gray-900">{{ getTargetName(favorite) }}</h3>
            </div>
            <p class="text-gray-600 text-sm mb-3 ml-11 flex items-center">
              <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              收藏时间：{{ formatDate(favorite.created_at) }}
            </p>
            <div v-if="favorite.target_type === 'JOB'" class="ml-11">
              <div v-if="favorite.job" class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-2">
                <div class="flex flex-wrap gap-4 text-gray-700 text-sm">
                  <span v-if="favorite.job.work_location" class="flex items-center">
                    <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <strong class="mr-1">工作地点：</strong>{{ favorite.job.work_location }}
                  </span>
                  <span v-if="favorite.job.job_type" class="flex items-center">
                    <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <strong class="mr-1">工作类型：</strong>{{ favorite.job.job_type }}
                  </span>
                  <span v-if="favorite.job.salary_min && favorite.job.salary_max" class="flex items-center text-blue-600 font-semibold">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <strong class="mr-1">薪资：</strong>{{ favorite.job.salary_min }}-{{ favorite.job.salary_max }}元
                  </span>
                  <span v-if="favorite.job.education" class="flex items-center">
                    <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
                    </svg>
                    <strong class="mr-1">学历要求：</strong>{{ favorite.job.education }}
                  </span>
                </div>
                <p v-if="favorite.job.description" class="mt-3 text-sm text-gray-700 line-clamp-2">
                  <strong>职位描述：</strong>{{ favorite.job.description }}
                </p>
              </div>
              <div v-else class="text-gray-400 text-sm bg-gray-50 p-4 rounded-xl border border-gray-200">
                职位信息加载中...
              </div>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              v-if="favorite.target_type === 'JOB'"
              @click="goToJobDetail(favorite.target_id)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              查看详情
            </button>
            <button
              @click="handleRemoveFavorite(favorite.target_type, favorite.target_id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              取消收藏
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
import { getFavorites, removeFavorite, type Favorite } from '@/api/favorites'
import { getJob, type Job } from '@/api/jobs'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 收藏列表
const favorites = ref<(Favorite & { job?: Job })[]>([])
const loading = ref(false)
const targetType = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 获取收藏类型名称
const getTargetTypeName = (type: string) => {
  const typeMap: Record<string, string> = {
    JOB: '职位',
    COMPANY: '企业',
  }
  return typeMap[type] || type
}

// 获取目标名称
const getTargetName = (favorite: Favorite & { job?: Job }) => {
  if (favorite.target_type === 'JOB' && favorite.job) {
    return favorite.job.title
  }
  return `ID: ${favorite.target_id}`
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 加载收藏列表
const handleSearch = async () => {
  loading.value = true
  try {
    const response = await getFavorites({
      page: currentPage.value,
      page_size: pageSize.value,
      target_type: targetType.value || undefined,
    })
    
    // 加载职位详情（如果是职位收藏）
    const favoritesWithDetails = await Promise.all(
      response.items.map(async (favorite) => {
        if (favorite.target_type === 'JOB') {
          try {
            const job = await getJob(favorite.target_id)
            return { ...favorite, job }
          } catch (error) {
            console.error(`加载职位 ${favorite.target_id} 详情失败:`, error)
            // 即使加载失败，也返回收藏信息，只是没有job详情
            return favorite
          }
        }
        return favorite
      })
    )
    
    favorites.value = favoritesWithDetails
    total.value = response.total
  } catch (error) {
    console.error('加载收藏列表失败:', error)
    alert('加载收藏列表失败: ' + (error as any).message)
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

// 取消收藏
const handleRemoveFavorite = async (targetType: string, targetId: string) => {
  if (!confirm('确定要取消收藏吗？')) {
    return
  }
  
  try {
    await removeFavorite(targetType, targetId)
    alert('取消收藏成功！')
    handleSearch()
  } catch (error: any) {
    alert('取消收藏失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

