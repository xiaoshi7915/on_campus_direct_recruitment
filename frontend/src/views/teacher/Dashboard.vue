<template>
  <div class="teacher-dashboard">
    <h1 class="text-3xl font-bold mb-6">教师工作台</h1>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">管辖学生</div>
        <div class="text-3xl font-bold text-blue-600">{{ statistics.total_students }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">活跃学生</div>
        <div class="text-3xl font-bold text-green-600">{{ statistics.active_students }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">双选会</div>
        <div class="text-3xl font-bold text-orange-600">{{ jobFairAnalysis.total_job_fairs }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <div class="text-gray-600 text-sm mb-2">宣讲会</div>
        <div class="text-3xl font-bold text-purple-600">{{ infoSessionAnalysis.total_info_sessions }}</div>
      </div>
    </div>

    <!-- 学生活跃度统计 -->
    <div class="bg-white rounded-lg shadow mb-6">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">学生活跃度统计</h2>
      </div>
      <div class="p-6">
        <!-- 筛选条件 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">开始日期</label>
            <input
              v-model="studentFilter.start_date"
              type="date"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadStudentStatistics"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
            <input
              v-model="studentFilter.end_date"
              type="date"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadStudentStatistics"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">院系ID</label>
            <input
              v-model="studentFilter.department_id"
              type="text"
              placeholder="院系ID（可选）"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadStudentStatistics"
            />
          </div>
        </div>
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6">
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
          <div>
            <div class="text-gray-600 text-sm">申请数量</div>
            <div class="text-2xl font-bold text-orange-600">{{ statistics.application_count }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 双选会统计分析 -->
    <div class="bg-white rounded-lg shadow mb-6">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">双选会统计分析</h2>
      </div>
      <div class="p-6">
        <!-- 筛选条件 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">开始日期</label>
            <input
              v-model="jobFairFilter.start_date"
              type="date"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadJobFairAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
            <input
              v-model="jobFairFilter.end_date"
              type="date"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadJobFairAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">学校ID</label>
            <input
              v-model="jobFairFilter.school_id"
              type="text"
              placeholder="学校ID（可选）"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadJobFairAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
            <select
              v-model="jobFairFilter.status"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadJobFairAnalysis"
            >
              <option value="">全部</option>
              <option value="DRAFT">草稿</option>
              <option value="PUBLISHED">已发布</option>
              <option value="ONGOING">进行中</option>
              <option value="ENDED">已结束</option>
              <option value="CANCELLED">已取消</option>
            </select>
          </div>
        </div>
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <div class="text-gray-600 text-sm">双选会总数</div>
            <div class="text-2xl font-bold text-blue-600">{{ jobFairAnalysis.total_job_fairs }}</div>
          </div>
          <div>
            <div class="text-gray-600 text-sm">报名企业数</div>
            <div class="text-2xl font-bold text-green-600">{{ jobFairAnalysis.registered_enterprises }}</div>
          </div>
          <div>
            <div class="text-gray-600 text-sm">报名学生数</div>
            <div class="text-2xl font-bold text-purple-600">{{ jobFairAnalysis.registered_students }}</div>
          </div>
        </div>
        <!-- 按状态统计 -->
        <div v-if="jobFairAnalysis.by_status && jobFairAnalysis.by_status.length > 0" class="mt-6">
          <h3 class="text-lg font-semibold mb-3">按状态统计</h3>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div
              v-for="item in jobFairAnalysis.by_status"
              :key="item.status"
              class="border rounded-lg p-3"
            >
              <div class="text-sm text-gray-600">{{ getStatusName(item.status) }}</div>
              <div class="text-xl font-bold">{{ item.count }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 宣讲会统计分析 -->
    <div class="bg-white rounded-lg shadow mb-6">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">宣讲会统计分析</h2>
      </div>
      <div class="p-6">
        <!-- 筛选条件 -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">开始日期</label>
            <input
              v-model="infoSessionFilter.start_date"
              type="date"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
            <input
              v-model="infoSessionFilter.end_date"
              type="date"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">学校ID</label>
            <input
              v-model="infoSessionFilter.school_id"
              type="text"
              placeholder="学校ID（可选）"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">企业ID</label>
            <input
              v-model="infoSessionFilter.enterprise_id"
              type="text"
              placeholder="企业ID（可选）"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
            <select
              v-model="infoSessionFilter.status"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              @change="loadInfoSessionAnalysis"
            >
              <option value="">全部</option>
              <option value="DRAFT">草稿</option>
              <option value="PUBLISHED">已发布</option>
              <option value="ONGOING">进行中</option>
              <option value="ENDED">已结束</option>
              <option value="CANCELLED">已取消</option>
            </select>
          </div>
        </div>
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div class="text-gray-600 text-sm">宣讲会总数</div>
            <div class="text-2xl font-bold text-blue-600">{{ infoSessionAnalysis.total_info_sessions }}</div>
          </div>
          <div>
            <div class="text-gray-600 text-sm">报名学生数</div>
            <div class="text-2xl font-bold text-green-600">{{ infoSessionAnalysis.registered_students }}</div>
          </div>
        </div>
        <!-- 按状态统计 -->
        <div v-if="infoSessionAnalysis.by_status && infoSessionAnalysis.by_status.length > 0" class="mt-6">
          <h3 class="text-lg font-semibold mb-3">按状态统计</h3>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div
              v-for="item in infoSessionAnalysis.by_status"
              :key="item.status"
              class="border rounded-lg p-3"
            >
              <div class="text-sm text-gray-600">{{ getStatusName(item.status) }}</div>
              <div class="text-xl font-bold">{{ item.count }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 日程管理 -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">日程管理</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">加载中...</div>
        <div v-else-if="schedules.length === 0" class="text-center py-8 text-gray-500">
          暂无日程记录
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="schedule in schedules"
            :key="schedule.id"
            class="border rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="font-semibold text-lg">{{ schedule.title || '未命名日程' }}</h3>
                <p class="text-gray-600 text-sm mt-1">
                  {{ schedule.description || '无描述' }}
                </p>
                <p class="text-gray-500 text-xs mt-2">
                  {{ formatDate(schedule.start_time) }} - {{ formatDate(schedule.end_time) }}
                </p>
                <span class="inline-block mt-2 px-2 py-1 text-xs rounded" :class="getScheduleTypeClass(schedule.schedule_type)">
                  {{ getScheduleTypeName(schedule.schedule_type) }}
                </span>
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
import {
  getStudentActivityStatistics,
  getJobFairAnalysis,
  getInfoSessionAnalysis,
} from '@/api/statistics'
import { getSchedules } from '@/api/schedules'

// 统计数据
const statistics = ref({
  total_students: 0,
  active_students: 0,
  resume_count: 0,
  application_count: 0,
})
const jobFairAnalysis = ref({
  total_job_fairs: 0,
  registered_enterprises: 0,
  registered_students: 0,
  by_status: [] as Array<{ status: string; count: number }>,
  by_school: [] as Array<{ school_id: string; count: number }>,
})
const infoSessionAnalysis = ref({
  total_info_sessions: 0,
  registered_students: 0,
  by_status: [] as Array<{ status: string; count: number }>,
  by_enterprise: [] as Array<{ enterprise_id: string; count: number }>,
})
const schedules = ref<any[]>([])
const loading = ref(false)

// 筛选条件
const studentFilter = ref({
  start_date: '',
  end_date: '',
  department_id: '',
})
const jobFairFilter = ref({
  start_date: '',
  end_date: '',
  school_id: '',
  status: '',
})
const infoSessionFilter = ref({
  start_date: '',
  end_date: '',
  school_id: '',
  enterprise_id: '',
  status: '',
})

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

// 获取状态名称
const getStatusName = (status: string) => {
  const statusMap: Record<string, string> = {
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    ONGOING: '进行中',
    ENDED: '已结束',
    CANCELLED: '已取消',
  }
  return statusMap[status] || status
}

// 获取日程类型名称
const getScheduleTypeName = (type: string) => {
  const typeMap: Record<string, string> = {
    JOB_FAIR: '双选会',
    INFO_SESSION: '宣讲会',
    INTERVIEW: '面试',
    OTHER: '其他',
  }
  return typeMap[type] || type
}

// 获取日程类型样式
const getScheduleTypeClass = (type: string) => {
  const classMap: Record<string, string> = {
    JOB_FAIR: 'bg-orange-100 text-orange-800',
    INFO_SESSION: 'bg-purple-100 text-purple-800',
    INTERVIEW: 'bg-blue-100 text-blue-800',
    OTHER: 'bg-gray-100 text-gray-800',
  }
  return classMap[type] || 'bg-gray-100 text-gray-800'
}

// 加载学生统计数据
const loadStudentStatistics = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (studentFilter.value.start_date) {
      params.start_date = studentFilter.value.start_date
    }
    if (studentFilter.value.end_date) {
      params.end_date = studentFilter.value.end_date
    }
    if (studentFilter.value.department_id) {
      params.department_id = studentFilter.value.department_id
    }
    const response = await getStudentActivityStatistics(params)
    statistics.value = response
  } catch (error) {
    console.error('加载学生统计数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载双选会统计分析
const loadJobFairAnalysis = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (jobFairFilter.value.start_date) {
      params.start_date = jobFairFilter.value.start_date
    }
    if (jobFairFilter.value.end_date) {
      params.end_date = jobFairFilter.value.end_date
    }
    if (jobFairFilter.value.school_id) {
      params.school_id = jobFairFilter.value.school_id
    }
    if (jobFairFilter.value.status) {
      params.status = jobFairFilter.value.status
    }
    const response = await getJobFairAnalysis(params)
    jobFairAnalysis.value = response
  } catch (error) {
    console.error('加载双选会统计分析失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载宣讲会统计分析
const loadInfoSessionAnalysis = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (infoSessionFilter.value.start_date) {
      params.start_date = infoSessionFilter.value.start_date
    }
    if (infoSessionFilter.value.end_date) {
      params.end_date = infoSessionFilter.value.end_date
    }
    if (infoSessionFilter.value.school_id) {
      params.school_id = infoSessionFilter.value.school_id
    }
    if (infoSessionFilter.value.enterprise_id) {
      params.enterprise_id = infoSessionFilter.value.enterprise_id
    }
    if (infoSessionFilter.value.status) {
      params.status = infoSessionFilter.value.status
    }
    const response = await getInfoSessionAnalysis(params)
    infoSessionAnalysis.value = response
  } catch (error) {
    console.error('加载宣讲会统计分析失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载日程
const loadSchedules = async () => {
  loading.value = true
  try {
    // 加载双选会和宣讲会相关的日程
    const [jobFairSchedules, infoSessionSchedules] = await Promise.all([
      getSchedules({ page_size: 5, schedule_type: 'JOB_FAIR' }).catch(() => ({ items: [] })),
      getSchedules({ page_size: 5, schedule_type: 'INFO_SESSION' }).catch(() => ({ items: [] })),
    ])
    schedules.value = [
      ...(jobFairSchedules.items || []),
      ...(infoSessionSchedules.items || []),
    ].slice(0, 10) // 最多显示10条
  } catch (error) {
    console.error('加载日程失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载所有数据
const loadData = async () => {
  await Promise.all([
    loadStudentStatistics(),
    loadJobFairAnalysis(),
    loadInfoSessionAnalysis(),
    loadSchedules(),
  ])
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

