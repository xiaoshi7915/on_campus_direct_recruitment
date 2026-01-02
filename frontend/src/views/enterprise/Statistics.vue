<template>
  <div class="enterprise-statistics w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8 flex items-center">
      <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      数据统计
    </h1>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">发布职位</div>
          <div class="p-2 bg-blue-50 rounded-lg">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-blue-600">{{ statistics.total_jobs }}</div>
        <div class="text-sm text-gray-500 mt-1">已发布：{{ statistics.published_jobs }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">收到申请</div>
          <div class="p-2 bg-green-50 rounded-lg">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-green-600">{{ statistics.total_applications }}</div>
        <div class="text-sm text-gray-500 mt-1">已通过：{{ statistics.accepted_applications }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">面试安排</div>
          <div class="p-2 bg-orange-50 rounded-lg">
            <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-orange-600">{{ statistics.total_interviews }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">已发Offer</div>
          <div class="p-2 bg-purple-50 rounded-lg">
            <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-purple-600">{{ statistics.total_offers }}</div>
        <div class="text-sm text-gray-500 mt-1">已接受：{{ statistics.accepted_offers }}</div>
      </div>
    </div>

    <!-- 更多统计 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">收藏简历</div>
          <div class="p-2 bg-pink-50 rounded-lg">
            <svg class="w-5 h-5 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-pink-600">{{ statistics.total_favorites }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">宣讲会</div>
          <div class="p-2 bg-indigo-50 rounded-lg">
            <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-indigo-600">{{ statistics.total_info_sessions }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">触达人才</div>
          <div class="p-2 bg-teal-50 rounded-lg">
            <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-teal-600">{{ statistics.total_talents }}</div>
      </div>
    </div>

    <!-- 按职位统计申请 -->
    <div class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div class="p-6 border-b border-gray-200 bg-gray-50">
        <h2 class="text-xl font-semibold text-gray-900 flex items-center">
          <svg class="w-5 h-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          按职位统计申请数
        </h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-3 text-gray-600">加载中...</p>
        </div>
        <div v-else-if="statistics.applications_by_job?.length === 0" class="text-center py-12 text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p>暂无统计数据</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="item in statistics.applications_by_job"
            :key="item.job_id"
            class="border border-gray-200 rounded-xl p-4 hover:bg-gray-50 transition-colors duration-200"
          >
            <div class="flex justify-between items-center">
              <div>
                <h3 class="font-semibold text-gray-900">职位ID：{{ item.job_id }}</h3>
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
/* 样式已内联到模板中 */
</style>

