<template>
  <div class="student-job-intentions w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">求职意向</h1>
      <button
        @click="showForm = true; editingIntention = null"
        class="btn btn-primary btn-md"
      >
        <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        添加求职意向
      </button>
    </div>

    <!-- 求职意向列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="intentions.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        <p class="text-gray-500 text-lg">暂无求职意向</p>
        <p class="text-gray-400 text-sm mt-2">点击上方按钮添加第一个求职意向</p>
      </div>
      <div
        v-for="intention in intentions"
        :key="intention.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 mb-3 ml-11">
              <span v-if="intention.job_type" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                职位类型：{{ intention.job_type }}
              </span>
              <span v-if="intention.industry" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                行业：{{ intention.industry }}
              </span>
              <span v-if="intention.salary_expect" class="flex items-center text-blue-600 font-semibold">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                期望薪资：{{ intention.salary_expect }}元/月
              </span>
              <span v-if="intention.work_location" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                工作地点：{{ intention.work_location }}
              </span>
            </div>
            <div class="text-sm text-gray-500 ml-11 flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              创建时间：{{ formatDate(intention.created_at) }}
            </div>
          </div>
          <div class="ml-6 flex space-x-2">
            <button
              @click="editIntention(intention)"
              class="btn btn-primary btn-md"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              编辑
            </button>
            <button
              @click="deleteIntention(intention.id)"
              class="btn btn-danger btn-md"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 表单弹窗 -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-2xl p-8 w-full max-w-md shadow-2xl border border-gray-100">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            {{ editingIntention ? '编辑' : '添加' }}求职意向
          </h2>
          <button
            @click="showForm = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveIntention" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">职位类型</label>
            <select
              v-model="formData.job_type"
              class="select-base"
            >
              <option value="">请选择职位类型</option>
              <option value="前端开发">前端开发</option>
              <option value="后端开发">后端开发</option>
              <option value="全栈开发">全栈开发</option>
              <option value="移动开发">移动开发</option>
              <option value="数据开发">数据开发</option>
              <option value="算法工程师">算法工程师</option>
              <option value="产品经理">产品经理</option>
              <option value="UI/UX设计师">UI/UX设计师</option>
              <option value="测试工程师">测试工程师</option>
              <option value="运维工程师">运维工程师</option>
              <option value="数据分析师">数据分析师</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">行业</label>
            <select
              v-model="formData.industry"
              class="select-base"
            >
              <option value="">请选择行业</option>
              <option value="互联网">互联网</option>
              <option value="金融">金融</option>
              <option value="教育">教育</option>
              <option value="医疗">医疗</option>
              <option value="制造业">制造业</option>
              <option value="零售">零售</option>
              <option value="房地产">房地产</option>
              <option value="咨询">咨询</option>
              <option value="媒体">媒体</option>
              <option value="能源">能源</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">期望薪资（元/月）</label>
            <input
              v-model.number="formData.salary_expect"
              type="number"
              min="0"
              class="input-base"
              placeholder="如：8000"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">工作地点</label>
            <select
              v-model="formData.work_location"
              class="select-base"
            >
              <option value="">请选择工作地点</option>
              <option value="北京">北京</option>
              <option value="上海">上海</option>
              <option value="广州">广州</option>
              <option value="深圳">深圳</option>
              <option value="杭州">杭州</option>
              <option value="南京">南京</option>
              <option value="成都">成都</option>
              <option value="武汉">武汉</option>
              <option value="西安">西安</option>
              <option value="苏州">苏州</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showForm = false"
              class="btn btn-secondary btn-md"
            >
              取消
            </button>
            <button
              type="submit"
              class="btn btn-primary btn-md"
            >
              <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
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

