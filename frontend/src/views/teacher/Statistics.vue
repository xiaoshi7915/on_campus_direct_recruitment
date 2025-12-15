<template>
  <div class="teacher-statistics max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
          <div class="text-gray-600 text-sm font-semibold">学生总数</div>
          <div class="p-2 bg-blue-50 rounded-lg">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-blue-600">{{ statistics.total_students }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">活跃学生</div>
          <div class="p-2 bg-green-50 rounded-lg">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-green-600">{{ statistics.active_students }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">简历数量</div>
          <div class="p-2 bg-orange-50 rounded-lg">
            <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-orange-600">{{ statistics.resume_count }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-200">
        <div class="flex items-center justify-between mb-2">
          <div class="text-gray-600 text-sm font-semibold">申请数量</div>
          <div class="p-2 bg-purple-50 rounded-lg">
            <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
        </div>
        <div class="text-3xl font-bold text-purple-600">{{ statistics.application_count }}</div>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md border border-gray-100 p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">开始日期</label>
          <input
            v-model="startDate"
            type="date"
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @change="loadStatistics"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">结束日期</label>
          <input
            v-model="endDate"
            type="date"
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @change="loadStatistics"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">院系</label>
          <input
            v-model="departmentId"
            type="text"
            placeholder="院系ID（可选）"
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @change="loadStatistics"
          />
        </div>
      </div>
    </div>

    <!-- 按部门统计 -->
    <div class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div class="p-6 border-b border-gray-200 bg-gray-50">
        <h2 class="text-xl font-semibold text-gray-900 flex items-center">
          <svg class="w-5 h-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          按部门统计
        </h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-3 text-gray-600">加载中...</p>
        </div>
        <div v-else-if="byDepartment.length === 0" class="text-center py-12 text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p>暂无统计数据</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="dept in byDepartment"
            :key="dept.department_id"
            class="border border-gray-200 rounded-xl p-4 hover:bg-gray-50 transition-colors duration-200"
          >
            <div class="flex justify-between items-center">
              <div>
                <h3 class="font-semibold text-gray-900">部门ID：{{ dept.department_id }}</h3>
                <p class="text-gray-600 text-sm mt-1">学生数：{{ dept.count }}</p>
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
import request from '@/api/request'

// 统计数据
const statistics = ref({
  total_students: 0,
  active_students: 0,
  resume_count: 0,
  application_count: 0,
  by_department: [] as Array<{ department_id: string; count: number }>,
})
const byDepartment = ref<Array<{ department_id: string; count: number }>>([])
const loading = ref(false)
const startDate = ref('')
const endDate = ref('')
const departmentId = ref('')

// 加载统计数据
const loadStatistics = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (startDate.value) {
      params.start_date = startDate.value
    }
    if (endDate.value) {
      params.end_date = endDate.value
    }
    if (departmentId.value) {
      params.department_id = departmentId.value
    }

    const response = await request.get('/statistics/students/activity', { params })
    statistics.value = response
    byDepartment.value = response.by_department || []
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

