<template>
  <div class="student-job-intentions">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">求职意向</h1>
      <button
        @click="showForm = true; editingIntention = null"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        添加求职意向
      </button>
    </div>

    <!-- 求职意向列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="intentions.length === 0" class="text-center py-12 text-gray-500">
        暂无求职意向，点击上方按钮添加
      </div>
      <div
        v-for="intention in intentions"
        :key="intention.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex flex-wrap gap-4 text-gray-600 mb-3">
              <span v-if="intention.job_type">职位类型：{{ intention.job_type }}</span>
              <span v-if="intention.industry">行业：{{ intention.industry }}</span>
              <span v-if="intention.salary_expect">期望薪资：{{ intention.salary_expect }}元/月</span>
              <span v-if="intention.work_location">工作地点：{{ intention.work_location }}</span>
            </div>
            <div class="text-sm text-gray-500">
              创建时间：{{ formatDate(intention.created_at) }}
            </div>
          </div>
          <div class="ml-6 flex space-x-2">
            <button
              @click="editIntention(intention)"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="deleteIntention(intention.id)"
              class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 表单弹窗 -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-2xl font-bold mb-4">
          {{ editingIntention ? '编辑' : '添加' }}求职意向
        </h2>
        <form @submit.prevent="saveIntention">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">职位类型</label>
              <input
                v-model="formData.job_type"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="如：前端开发、后端开发等"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">行业</label>
              <input
                v-model="formData.industry"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="如：互联网、金融等"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">期望薪资（元/月）</label>
              <input
                v-model.number="formData.salary_expect"
                type="number"
                min="0"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="如：8000"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">工作地点</label>
              <input
                v-model="formData.work_location"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="如：北京、上海等"
              />
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-2">
            <button
              type="button"
              @click="showForm = false"
              class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              保存
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getJobIntentions,
  createJobIntention,
  updateJobIntention,
  deleteJobIntention
} from '@/api/jobIntentions'
import type { JobIntentionResponse } from '@/types/index'

const intentions = ref<JobIntentionResponse[]>([])
const loading = ref(false)
const showForm = ref(false)
const editingIntention = ref<JobIntentionResponse | null>(null)
const formData = ref({
  job_type: '',
  industry: '',
  salary_expect: undefined as number | undefined,
  work_location: ''
})

const loadIntentions = async () => {
  loading.value = true
  try {
    const res = await getJobIntentions()
    intentions.value = res.items
  } catch (error) {
    console.error('加载求职意向失败:', error)
    alert('加载求职意向失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const editIntention = (intention: JobIntentionResponse) => {
  editingIntention.value = intention
  formData.value = {
    job_type: intention.job_type || '',
    industry: intention.industry || '',
    salary_expect: intention.salary_expect || undefined,
    work_location: intention.work_location || ''
  }
  showForm.value = true
}

const saveIntention = async () => {
  try {
    if (editingIntention.value) {
      await updateJobIntention(editingIntention.value.id, formData.value)
      alert('更新成功')
    } else {
      await createJobIntention(formData.value)
      alert('创建成功')
    }
    showForm.value = false
    editingIntention.value = null
    formData.value = {
      job_type: '',
      industry: '',
      salary_expect: undefined,
      work_location: ''
    }
    loadIntentions()
  } catch (error: any) {
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  }
}

const deleteIntention = async (id: string) => {
  if (!confirm('确定要删除这个求职意向吗？')) return
  try {
    await deleteJobIntention(id)
    alert('删除成功')
    loadIntentions()
  } catch (error: any) {
    alert(error.response?.data?.detail || '删除失败，请稍后重试')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(() => {
  loadIntentions()
})
</script>

