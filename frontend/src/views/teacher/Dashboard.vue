<template>
  <div class="teacher-dashboard">
    <h1 class="text-3xl font-bold mb-6">教师工作台</h1>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">管辖学生</div>
        <div class="text-3xl font-bold text-blue-600">{{ studentCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">活跃学生</div>
        <div class="text-3xl font-bold text-green-600">{{ activeStudentCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">双选会</div>
        <div class="text-3xl font-bold text-orange-600">{{ jobFairCount }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">宣讲会</div>
        <div class="text-3xl font-bold text-purple-600">{{ infoSessionCount }}</div>
      </div>
    </div>

    <!-- 学生活跃度统计 -->
    <div class="bg-white rounded-lg shadow mb-6">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">学生活跃度统计</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <div class="text-gray-600 text-sm">学生总数</div>
            <div class="text-2xl font-bold text-blue-600">{{ statistics.total_students }}</div>
          </div>
          <div>
            <div class="text-gray-600 text-sm">活跃学生</div>
            <div class="text-2xl font-bold text-green-600">{{ statistics.active_students }}</div>
          </div>
          <div>
            <div class="text-gray-600 text-sm">简历数量</div>
            <div class="text-2xl font-bold text-purple-600">{{ statistics.resume_count }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">最近活动</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else-if="recentActivities.length === 0" class="text-center py-8 text-gray-500">
          暂无活动记录
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="activity in recentActivities"
            :key="activity.id"
            class="border rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <h3 class="font-semibold text-lg">{{ activity.title }}</h3>
            <p class="text-gray-600 text-sm mt-1">
              {{ activity.description }}
            </p>
            <p class="text-gray-500 text-xs mt-2">
              {{ formatDate(activity.created_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getInfoSessions } from '@/api/infoSessions'
import { getJobFairs } from '@/api/jobFairs'

// 统计数据
const studentCount = ref(0)
const activeStudentCount = ref(0)
const jobFairCount = ref(0)
const infoSessionCount = ref(0)
const statistics = ref({
  total_students: 0,
  active_students: 0,
  resume_count: 0,
  application_count: 0,
})
const recentActivities = ref<any[]>([])
const loading = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载统计数据
    const [jobFairsRes, infoSessionsRes] = await Promise.all([
      getJobFairs({ page_size: 1 }),
      getInfoSessions({ page_size: 1 }),
    ])

    jobFairCount.value = jobFairsRes.total
    infoSessionCount.value = infoSessionsRes.total
    
    // TODO: 加载学生统计数据和活动数据
    // const statsRes = await getStudentActivityStatistics()
    // statistics.value = statsRes
    // studentCount.value = statsRes.total_students
    // activeStudentCount.value = statsRes.active_students
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.teacher-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

