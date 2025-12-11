<template>
  <div class="enterprise-statistics">
    <h1 class="text-3xl font-bold mb-6">数据统计</h1>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">发布职位</div>
        <div class="text-3xl font-bold text-blue-600">{{ statistics.total_jobs }}</div>
        <div class="text-sm text-gray-500 mt-1">已发布：{{ statistics.published_jobs }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">收到申请</div>
        <div class="text-3xl font-bold text-green-600">{{ statistics.total_applications }}</div>
        <div class="text-sm text-gray-500 mt-1">已通过：{{ statistics.accepted_applications }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">面试安排</div>
        <div class="text-3xl font-bold text-orange-600">{{ statistics.total_interviews }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">已发Offer</div>
        <div class="text-3xl font-bold text-purple-600">{{ statistics.total_offers }}</div>
        <div class="text-sm text-gray-500 mt-1">已接受：{{ statistics.accepted_offers }}</div>
      </div>
    </div>

    <!-- 更多统计 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">收藏简历</div>
        <div class="text-3xl font-bold text-pink-600">{{ statistics.total_favorites }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">宣讲会</div>
        <div class="text-3xl font-bold text-indigo-600">{{ statistics.total_info_sessions }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">触达人才</div>
        <div class="text-3xl font-bold text-teal-600">{{ statistics.total_talents }}</div>
      </div>
    </div>

    <!-- 按职位统计申请 -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">按职位统计申请数</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else-if="statistics.applications_by_job?.length === 0" class="text-center py-8 text-gray-500">
          暂无统计数据
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="item in statistics.applications_by_job"
            :key="item.job_id"
            class="border rounded-lg p-4"
          >
            <div class="flex justify-between items-center">
              <div>
                <h3 class="font-semibold">职位ID：{{ item.job_id }}</h3>
                <p class="text-gray-600 text-sm mt-1">申请数：{{ item.count }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getEnterprisePersonalStatistics } from '@/api/statistics'

const statistics = ref({
  total_jobs: 0,
  published_jobs: 0,
  total_applications: 0,
  accepted_applications: 0,
  total_interviews: 0,
  total_offers: 0,
  accepted_offers: 0,
  total_favorites: 0,
  total_info_sessions: 0,
  total_job_fair_registrations: 0,
  total_chat_sessions: 0,
  total_talents: 0,
  applications_by_job: [] as Array<{ job_id: string; count: number }>
})
const loading = ref(false)

// 加载统计数据
const loadStatistics = async () => {
  loading.value = true
  try {
    const response = await getEnterprisePersonalStatistics()
    statistics.value = response
  } catch (error: any) {
    console.error('加载统计数据失败:', error)
    alert('加载统计数据失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.enterprise-statistics {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

