<template>
  <div class="enterprise-schedules">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">日程管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        新建日程
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">日程类型：</label>
        <select
          v-model="typeFilter"
          @change="loadSchedules"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">全部</option>
          <option value="INTERVIEW">面试</option>
          <option value="JOB_FAIR">双选会</option>
          <option value="INFO_SESSION">宣讲会</option>
          <option value="MANUAL">手动日程</option>
        </select>
        <label class="text-sm font-medium text-gray-700 ml-4">完成状态：</label>
        <select
          v-model="completedFilter"
          @change="loadSchedules"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="null">全部</option>
          <option :value="false">未完成</option>
          <option :value="true">已完成</option>
        </select>
      </div>
    </div>

    <!-- 日程列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="schedules.length === 0" class="text-center py-12 text-gray-500">
        暂无日程
      </div>
      <div
        v-for="schedule in schedules"
        :key="schedule.id"
        :class="['bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow', schedule.is_completed && 'opacity-60']"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-2 mb-2">
              <span
                :class="getTypeClass(schedule.schedule_type)"
                class="px-2 py-1 text-xs font-medium rounded"
              >
                {{ getTypeText(schedule.schedule_type) }}
              </span>
              <span
                v-if="schedule.is_completed"
                class="px-2 py-1 text-xs font-medium rounded bg-green-100 text-green-800"
              >
                已完成
              </span>
              <span class="text-sm text-gray-500">{{ formatDate(schedule.start_time) }}</span>
            </div>
            <h3 class="text-lg font-semibold mb-2">{{ schedule.title }}</h3>
            <p v-if="schedule.content" class="text-gray-700 mb-2">{{ schedule.content }}</p>
            <div class="text-sm text-gray-500">
              <span v-if="schedule.end_time">结束时间：{{ formatDate(schedule.end_time) }}</span>
              <span v-if="schedule.reminder_time" class="ml-4">
                提醒时间：{{ formatDate(schedule.reminder_time) }}
              </span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              v-if="!schedule.is_completed"
              @click="completeSchedule(schedule.id)"
              class="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
            >
              标记完成
            </button>
            <button
              v-else
              @click="uncompleteSchedule(schedule.id)"
              class="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600"
            >
              取消完成
            </button>
            <button
              @click="editSchedule(schedule)"
              class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="deleteScheduleHandler(schedule.id)"
              class="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="mt-6">
      <Pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        @change="handlePaginationChange"
      />
    </div>

    <!-- 创建/编辑日程模态框 -->
    <div
      v-if="showCreateModal || showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-4 text-gray-900">
            {{ showEditModal ? '编辑日程' : '新建日程' }}
          </h2>
          <form @submit.prevent="saveSchedule">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">标题</label>
                <input
                  v-model="scheduleForm.title"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入日程标题"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">内容</label>
                <textarea
                  v-model="scheduleForm.content"
                  rows="3"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入日程内容（可选）"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">开始时间</label>
                <input
                  v-model="scheduleForm.start_time"
                  type="datetime-local"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">结束时间</label>
                <input
                  v-model="scheduleForm.end_time"
                  type="datetime-local"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">提醒时间</label>
                <input
                  v-model="scheduleForm.reminder_time"
                  type="datetime-local"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">日程类型</label>
                <select
                  v-model="scheduleForm.schedule_type"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                >
                  <option value="MANUAL">手动日程</option>
                  <option value="INTERVIEW">面试</option>
                  <option value="JOB_FAIR">双选会</option>
                  <option value="INFO_SESSION">宣讲会</option>
                </select>
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                保存
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getSchedules,
  createSchedule,
  updateSchedule,
  deleteSchedule as deleteScheduleAPI,
  completeSchedule as completeScheduleAPI,
  uncompleteSchedule as uncompleteScheduleAPI,
  type Schedule,
  type ScheduleCreateRequest,
  type ScheduleUpdateRequest
} from '@/api/schedules'
import Pagination from '@/components/Pagination.vue'

const schedules = ref<Schedule[]>([])
const loading = ref(false)
const typeFilter = ref('')
const completedFilter = ref<boolean | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingSchedule = ref<Schedule | null>(null)
const scheduleForm = ref<ScheduleCreateRequest & { id?: string }>({
  title: '',
  content: '',
  start_time: '',
  end_time: '',
  reminder_time: '',
  schedule_type: 'MANUAL'
})

const getTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    INTERVIEW: '面试',
    JOB_FAIR: '双选会',
    INFO_SESSION: '宣讲会',
    MANUAL: '手动日程'
  }
  return typeMap[type] || type
}

const getTypeClass = (type: string) => {
  const classMap: Record<string, string> = {
    INTERVIEW: 'bg-purple-100 text-purple-800',
    JOB_FAIR: 'bg-blue-100 text-blue-800',
    INFO_SESSION: 'bg-green-100 text-green-800',
    MANUAL: 'bg-gray-100 text-gray-800'
  }
  return classMap[type] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadSchedules = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (typeFilter.value) {
      params.schedule_type = typeFilter.value
    }
    const res = await getSchedules(params)
    schedules.value = res.items
    total.value = res.total
    
    // 客户端过滤完成状态
    if (completedFilter.value !== null) {
      schedules.value = schedules.value.filter(s => s.is_completed === completedFilter.value)
    }
  } catch (error: any) {
    console.error('加载日程失败:', error)
    alert('加载日程失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadSchedules()
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingSchedule.value = null
  scheduleForm.value = {
    title: '',
    content: '',
    start_time: '',
    end_time: '',
    reminder_time: '',
    schedule_type: 'MANUAL'
  }
}

const editSchedule = (schedule: Schedule) => {
  editingSchedule.value = schedule
  scheduleForm.value = {
    id: schedule.id,
    title: schedule.title,
    content: schedule.content || '',
    start_time: schedule.start_time.substring(0, 16),
    end_time: schedule.end_time ? schedule.end_time.substring(0, 16) : '',
    reminder_time: schedule.reminder_time ? schedule.reminder_time.substring(0, 16) : '',
    schedule_type: schedule.schedule_type
  }
  showEditModal.value = true
}

const saveSchedule = async () => {
  try {
    if (showEditModal.value && editingSchedule.value) {
      const updateData: ScheduleUpdateRequest = {
        title: scheduleForm.value.title,
        content: scheduleForm.value.content,
        start_time: scheduleForm.value.start_time,
        end_time: scheduleForm.value.end_time,
        reminder_time: scheduleForm.value.reminder_time
      }
      await updateSchedule(editingSchedule.value.id, updateData)
      alert('更新成功！')
    } else {
      const createData: ScheduleCreateRequest = {
        title: scheduleForm.value.title,
        content: scheduleForm.value.content,
        start_time: scheduleForm.value.start_time,
        end_time: scheduleForm.value.end_time,
        reminder_time: scheduleForm.value.reminder_time,
        schedule_type: scheduleForm.value.schedule_type
      }
      await createSchedule(createData)
      alert('创建成功！')
    }
    closeModal()
    loadSchedules()
  } catch (error: any) {
    console.error('保存日程失败:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

const completeSchedule = async (id: string) => {
  try {
    await completeScheduleAPI(id)
    await loadSchedules()
  } catch (error: any) {
    console.error('标记完成失败:', error)
    alert('标记完成失败: ' + (error.response?.data?.detail || error.message))
  }
}

const uncompleteSchedule = async (id: string) => {
  try {
    await uncompleteScheduleAPI(id)
    await loadSchedules()
  } catch (error: any) {
    console.error('取消完成失败:', error)
    alert('取消完成失败: ' + (error.response?.data?.detail || error.message))
  }
}

const deleteScheduleHandler = async (id: string) => {
  if (!confirm('确定要删除这个日程吗？')) return
  try {
    await deleteScheduleAPI(id)
    await loadSchedules()
  } catch (error: any) {
    console.error('删除日程失败:', error)
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadSchedules()
})
</script>

<style scoped>
.enterprise-schedules {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

