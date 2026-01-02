<template>
  <div class="admin-statistics w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8 flex items-center">
      <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      数据统计
    </h1>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 flex items-center space-x-4 hover:shadow-lg transition-all duration-200">
        <div class="p-3 bg-blue-50 rounded-lg">
          <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
        <div>
          <div class="text-gray-600 text-sm mb-1">用户总数</div>
          <div class="text-3xl font-bold text-blue-600">{{ statistics.total_users }}</div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 flex items-center space-x-4 hover:shadow-lg transition-all duration-200">
        <div class="p-3 bg-green-50 rounded-lg">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
        <div>
          <div class="text-gray-600 text-sm mb-1">学生数</div>
          <div class="text-3xl font-bold text-green-600">{{ statistics.total_students }}</div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 flex items-center space-x-4 hover:shadow-lg transition-all duration-200">
        <div class="p-3 bg-orange-50 rounded-lg">
          <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div>
          <div class="text-gray-600 text-sm mb-1">职位数</div>
          <div class="text-3xl font-bold text-orange-600">{{ statistics.total_jobs }}</div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 flex items-center space-x-4 hover:shadow-lg transition-all duration-200">
        <div class="p-3 bg-purple-50 rounded-lg">
          <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div>
          <div class="text-gray-600 text-sm mb-1">申请数</div>
          <div class="text-3xl font-bold text-purple-600">{{ statistics.total_applications }}</div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 flex items-center space-x-4 hover:shadow-lg transition-all duration-200">
        <div class="p-3 bg-blue-50 rounded-lg">
          <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <div class="text-gray-600 text-sm mb-1">双选会数</div>
          <div class="text-3xl font-bold text-blue-600">{{ statistics.total_job_fairs }}</div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 flex items-center space-x-4 hover:shadow-lg transition-all duration-200">
        <div class="p-3 bg-green-50 rounded-lg">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <div class="text-gray-600 text-sm mb-1">宣讲会数</div>
          <div class="text-3xl font-bold text-green-600">{{ statistics.total_info_sessions }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/api/request'

// 统计数据
const statistics = ref({
  total_users: 0,
  total_students: 0,
  total_jobs: 0,
  total_applications: 0,
  total_job_fairs: 0,
  total_info_sessions: 0,
})
const loading = ref(false)

// 加载统计数据
const loadStatistics = async () => {
  loading.value = true
  try {
    const response = await request.get('/statistics/platform/overview')
    statistics.value = response
  } catch (error) {
    console.error('加载统计数据失败:', error)
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

