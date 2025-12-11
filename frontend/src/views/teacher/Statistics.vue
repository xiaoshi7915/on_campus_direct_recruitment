<template>
  <div class="teacher-statistics">
    <h1 class="text-3xl font-bold mb-6">数据统计</h1>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">学生总数</div>
        <div class="text-3xl font-bold text-blue-600">{{ statistics.total_students }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">活跃学生</div>
        <div class="text-3xl font-bold text-green-600">{{ statistics.active_students }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">简历数量</div>
        <div class="text-3xl font-bold text-orange-600">{{ statistics.resume_count }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">申请数量</div>
        <div class="text-3xl font-bold text-purple-600">{{ statistics.application_count }}</div>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">开始日期</label>
          <input
            v-model="startDate"
            type="date"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="loadStatistics"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
          <input
            v-model="endDate"
            type="date"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="loadStatistics"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">院系</label>
          <input
            v-model="departmentId"
            type="text"
            placeholder="院系ID（可选）"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="loadStatistics"
          />
        </div>
      </div>
    </div>

    <!-- 按部门统计 -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">按部门统计</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else-if="byDepartment.length === 0" class="text-center py-8 text-gray-500">
          暂无统计数据
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="dept in byDepartment"
            :key="dept.department_id"
            class="border rounded-lg p-4"
          >
            <div class="flex justify-between items-center">
              <div>
                <h3 class="font-semibold">部门ID：{{ dept.department_id }}</h3>
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
.teacher-statistics {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

