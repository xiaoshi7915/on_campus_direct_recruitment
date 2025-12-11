<template>
  <div class="student-favorites">
    <h1 class="text-3xl font-bold mb-6">我的收藏</h1>

    <!-- 筛选 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">收藏类型：</label>
        <select
          v-model="targetType"
          @change="handleSearch"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">全部</option>
          <option value="JOB">职位</option>
          <option value="COMPANY">企业</option>
        </select>
      </div>
    </div>

    <!-- 收藏列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="favorites.length === 0" class="text-center py-12 text-gray-500">
        暂无收藏
      </div>
      <div
        v-for="favorite in favorites"
        :key="favorite.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                {{ getTargetTypeName(favorite.target_type) }}
              </span>
              <h3 class="text-xl font-semibold">{{ getTargetName(favorite) }}</h3>
            </div>
            <p class="text-gray-600 text-sm mb-3">
              收藏时间：{{ formatDate(favorite.created_at) }}
            </p>
            <div v-if="favorite.target_type === 'JOB'" class="text-gray-700">
              <div v-if="favorite.job">
                <p v-if="favorite.job.work_location"><strong>工作地点：</strong>{{ favorite.job.work_location }}</p>
                <p v-if="favorite.job.job_type"><strong>工作类型：</strong>{{ favorite.job.job_type }}</p>
                <p v-if="favorite.job.salary_min && favorite.job.salary_max">
                  <strong>薪资：</strong>{{ favorite.job.salary_min }}-{{ favorite.job.salary_max }}元
                </p>
                <p v-if="favorite.job.education"><strong>学历要求：</strong>{{ favorite.job.education }}</p>
                <p v-if="favorite.job.description" class="mt-2 text-sm line-clamp-2">
                  <strong>职位描述：</strong>{{ favorite.job.description }}
                </p>
              </div>
              <div v-else class="text-gray-400 text-sm">
                职位信息加载中...
              </div>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              v-if="favorite.target_type === 'JOB'"
              @click="goToJobDetail(favorite.target_id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看详情
            </button>
            <button
              @click="handleRemoveFavorite(favorite.target_type, favorite.target_id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
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
import { ref, onMounted, computed } from 'vue'
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

// 计算总页数
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

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
.student-favorites {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

