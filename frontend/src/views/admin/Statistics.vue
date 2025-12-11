<template>
  <div class="admin-statistics">
    <h1 class="text-3xl font-bold mb-6">数据统计</h1>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">用户总数</div>
        <div class="text-3xl font-bold text-blue-600">{{ statistics.total_users }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">学生数</div>
        <div class="text-3xl font-bold text-green-600">{{ statistics.total_students }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">职位数</div>
        <div class="text-3xl font-bold text-orange-600">{{ statistics.total_jobs }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">申请数</div>
        <div class="text-3xl font-bold text-purple-600">{{ statistics.total_applications }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">双选会数</div>
        <div class="text-3xl font-bold text-blue-600">{{ statistics.total_job_fairs }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">宣讲会数</div>
        <div class="text-3xl font-bold text-green-600">{{ statistics.total_info_sessions }}</div>
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
.admin-statistics {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

