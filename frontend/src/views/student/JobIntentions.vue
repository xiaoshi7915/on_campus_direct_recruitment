<template>
  <div class="student-job-intentions w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">求职意向</h1>
      <button
        @click="showForm = true; editingIntention = null; resetForm()"
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
              <!-- 求职类型 -->
              <span v-if="intention.job_nature" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                求职类型：{{ intention.job_nature === 'FULL_TIME' ? '全职' : '兼职' }}
              </span>
              <!-- 职位类型（多选） -->
              <span v-if="getJobTypeList(intention).length > 0" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                职位类型：{{ getJobTypeList(intention).join('、') }}
              </span>
              <!-- 行业（多选） -->
              <span v-if="getIndustryList(intention).length > 0" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                行业：{{ getIndustryList(intention).join('、') }}
              </span>
              <!-- 薪资范围 -->
              <span v-if="intention.salary_min || intention.salary_max" class="flex items-center text-blue-600 font-semibold">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                期望薪资：{{ formatSalaryRange(intention) }}
              </span>
              <!-- 工作地点（多选） -->
              <span v-if="getWorkLocationList(intention).length > 0" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                工作地点：{{ getWorkLocationList(intention).join('、') }}
              </span>
              <!-- 兼职信息 -->
              <span v-if="intention.job_nature === 'PART_TIME' && intention.part_time_days" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                每周工作：{{ intention.part_time_days }}
              </span>
              <span v-if="intention.job_nature === 'PART_TIME' && intention.work_time_slot" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                工作时间：{{ intention.work_time_slot }}
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
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-2xl p-8 w-full max-w-2xl shadow-2xl border border-gray-100 my-8">
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
          <!-- 求职类型 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">求职类型 <span class="text-red-500">*</span></label>
            <div class="flex space-x-4">
              <label class="flex items-center cursor-pointer">
                <input
                  type="radio"
                  v-model="formData.job_nature"
                  value="FULL_TIME"
                  class="w-4 h-4 text-blue-600 focus:ring-blue-500"
                />
                <span class="ml-2 text-gray-700">全职</span>
              </label>
              <label class="flex items-center cursor-pointer">
                <input
                  type="radio"
                  v-model="formData.job_nature"
                  value="PART_TIME"
                  class="w-4 h-4 text-blue-600 focus:ring-blue-500"
                />
                <span class="ml-2 text-gray-700">兼职</span>
              </label>
            </div>
          </div>

          <!-- 行业（多选，先选） -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">行业 <span class="text-red-500">*</span></label>
            <div class="space-y-3">
              <!-- 一级行业 -->
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-2">一级行业</label>
                <MultiSelect
                  v-model="selectedCategories"
                  :options="industryCategories"
                  placeholder="请选择一级行业"
                  searchable
                  option-value="id"
                  option-label="name"
                  @update:modelValue="onCategoryChange"
                />
              </div>
              <!-- 二级行业（根据选中的一级行业显示） -->
              <div v-if="selectedCategories.length > 0">
                <label class="block text-xs font-medium text-gray-600 mb-2">细分行业（可选）</label>
                <MultiSelect
                  v-model="selectedSubIndustries"
                  :options="availableSubIndustries"
                  placeholder="请选择细分行业"
                  searchable
                  option-value="id"
                  option-label="name"
                />
              </div>
            </div>
          </div>

          <!-- 职位类型（多选，根据选中的行业显示） -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">职位类型 <span class="text-red-500">*</span></label>
            <div v-if="selectedCategories.length === 0 && selectedSubIndustries.length === 0" class="text-sm text-gray-500 py-2">
              请先选择行业
            </div>
            <MultiSelect
              v-else
              v-model="selectedJobTypes"
              :options="availableJobTypes"
              placeholder="请选择职位类型"
              searchable
              option-value="id"
              option-label="name"
            />
          </div>

          <!-- 工作地点（多选） -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">工作地点 <span class="text-red-500">*</span></label>
            <MultiSelect
              v-model="formData.work_location_list"
              :options="workLocations"
              placeholder="请选择工作地点"
              searchable
            />
          </div>

          <!-- 薪资范围（以k为单位，下拉框勾选） -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">期望薪资范围（千元/月）</label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-2">最低薪资</label>
                <Select
                  v-model="formData.salary_min"
                  :options="salaryOptions.map(s => ({ value: s, label: `${s}k` }))"
                  placeholder="请选择最低薪资"
                  option-value="value"
                  option-label="label"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-2">最高薪资</label>
                <Select
                  v-model="formData.salary_max"
                  :options="salaryOptions.map(s => ({ value: s, label: `${s}k` }))"
                  placeholder="请选择最高薪资"
                  option-value="value"
                  option-label="label"
                />
              </div>
            </div>
          </div>

          <!-- 兼职选项（仅当选择兼职时显示） -->
          <div v-if="formData.job_nature === 'PART_TIME'" class="space-y-4 border-t pt-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">每周工作天数</label>
              <Select
                v-model="formData.part_time_days"
                :options="partTimeDaysOptions"
                placeholder="请选择每周工作天数"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">工作时间段</label>
              <Select
                v-model="formData.work_time_slot"
                :options="workTimeSlotOptions"
                placeholder="请选择工作时间段"
              />
            </div>
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
import { ref, onMounted, computed } from 'vue'
import MultiSelect from '@/components/MultiSelect.vue'
import Select from '@/components/Select.vue'
import {
  getJobIntentions,
  createJobIntention,
  updateJobIntention,
  deleteJobIntention
} from '@/api/jobIntentions'
import {
  getIndustryCategories,
  getSubIndustries,
  getJobTypes,
  type IndustryCategory,
  type SubIndustry,
  type JobType
} from '@/api/industryJobTypes'
import type { JobIntentionResponse } from '@/types/index'

const intentions = ref<JobIntentionResponse[]>([])
const loading = ref(false)
const showForm = ref(false)
const editingIntention = ref<JobIntentionResponse | null>(null)

// 维表数据
const industryCategories = ref<IndustryCategory[]>([])
const subIndustries = ref<SubIndustry[]>([])
const jobTypes = ref<JobType[]>([])

// 表单数据
const selectedCategories = ref<string[]>([])
const selectedSubIndustries = ref<string[]>([])
const selectedJobTypes = ref<string[]>([])

const formData = ref({
  job_nature: 'FULL_TIME' as 'FULL_TIME' | 'PART_TIME',
  work_location_list: [] as string[],
  salary_min: undefined as number | undefined,
  salary_max: undefined as number | undefined,
  part_time_days: '',
  work_time_slot: ''
})

// 工作地点选项
const workLocations = [
  '北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉', 
  '西安', '苏州', '天津', '重庆', '青岛', '大连', '厦门', '其他'
]

// 薪资选项（单位：千元/月）
const salaryOptions = [
  3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20, 25, 30, 35, 40, 50, 60, 80, 100
]

// 兼职每周工作天数选项
const partTimeDaysOptions = ['1-2天', '3-4天', '5天', '灵活']

// 兼职工作时间段选项
const workTimeSlotOptions = ['工作日', '周末', '晚上', '灵活']

// 计算属性：根据选中的一级行业获取可用的细分行业
const availableSubIndustries = computed(() => {
  if (selectedCategories.value.length === 0) return []
  return subIndustries.value.filter(sub => 
    selectedCategories.value.includes(sub.category_id)
  )
})

// 计算属性：根据选中的行业获取可用的职位类型
const availableJobTypes = computed(() => {
  if (selectedCategories.value.length === 0 && selectedSubIndustries.value.length === 0) {
    return []
  }
  
  return jobTypes.value.filter(jobType => {
    // 如果职位类型关联了细分行业，检查是否在选中的细分行业中
    if (jobType.sub_industry_id) {
      return selectedSubIndustries.value.includes(jobType.sub_industry_id)
    }
    // 如果职位类型只关联了一级行业，检查是否在选中的一级行业中
    if (jobType.category_id) {
      return selectedCategories.value.includes(jobType.category_id)
    }
    // 通用职位类型（没有关联行业）始终显示
    return true
  })
})

// 监听一级行业变化，清空细分行业和职位类型选择
const onCategoryChange = () => {
  // 移除不再选中的一级行业下的细分行业
  selectedSubIndustries.value = selectedSubIndustries.value.filter(subId => {
    const sub = subIndustries.value.find(s => s.id === subId)
    return sub && selectedCategories.value.includes(sub.category_id)
  })
  // 清空职位类型选择，让用户重新选择
  selectedJobTypes.value = []
}

// 加载维表数据
const loadDimensionData = async () => {
  try {
    const [categoriesRes, subsRes, typesRes] = await Promise.all([
      getIndustryCategories(),
      getSubIndustries(),
      getJobTypes()
    ])
    // 后端直接返回数组，不是分页响应
    industryCategories.value = Array.isArray(categoriesRes) ? categoriesRes : []
    subIndustries.value = Array.isArray(subsRes) ? subsRes : []
    jobTypes.value = Array.isArray(typesRes) ? typesRes : []
  } catch (error) {
    console.error('加载维表数据失败:', error)
    alert('加载行业职位类型数据失败，请稍后重试')
  }
}

const loadIntentions = async () => {
  loading.value = true
  try {
    const res = await getJobIntentions()
    intentions.value = (res as any).items || res || []
  } catch (error) {
    console.error('加载求职意向失败:', error)
    alert('加载求职意向失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 解析JSON字符串数组
const parseJsonArray = (jsonStr?: string): string[] => {
  if (!jsonStr) return []
  try {
    return JSON.parse(jsonStr)
  } catch {
    return []
  }
}

// 获取职位类型名称列表
const getJobTypeNames = (jobTypeIds: string[]): string[] => {
  return jobTypeIds.map(id => {
    const jobType = jobTypes.value.find(t => t.id === id)
    return jobType?.name || id
  })
}

// 获取行业名称列表
const getIndustryNames = (industryIds: string[]): string[] => {
  const names: string[] = []
  industryIds.forEach(id => {
    // 先查找一级行业
    const category = industryCategories.value.find(c => c.id === id)
    if (category) {
      names.push(category.name)
    } else {
      // 再查找细分行业
      const sub = subIndustries.value.find(s => s.id === id)
      if (sub) {
        names.push(sub.name)
      }
    }
  })
  return names
}

// 显示用的辅助函数
const getJobTypeList = (intention: JobIntentionResponse): string[] => {
  if (intention.job_type_list) {
    const ids = parseJsonArray(intention.job_type_list)
    return getJobTypeNames(ids)
  }
  // 兼容旧数据
  return intention.job_type ? [intention.job_type] : []
}

const getIndustryList = (intention: JobIntentionResponse): string[] => {
  if (intention.industry_list) {
    const ids = parseJsonArray(intention.industry_list)
    return getIndustryNames(ids)
  }
  // 兼容旧数据
  return intention.industry ? [intention.industry] : []
}

const getWorkLocationList = (intention: JobIntentionResponse): string[] => {
  if (intention.work_location_list) {
    return parseJsonArray(intention.work_location_list)
  }
  // 兼容旧数据
  return intention.work_location ? [intention.work_location] : []
}

const formatSalaryRange = (intention: JobIntentionResponse): string => {
  if (intention.salary_min && intention.salary_max) {
    return `${intention.salary_min}k-${intention.salary_max}k元/月`
  } else if (intention.salary_min) {
    return `${intention.salary_min}k元以上/月`
  } else if (intention.salary_max) {
    return `${intention.salary_max}k元以下/月`
  } else if (intention.salary_expect) {
    // 兼容旧数据，转换为k单位
    return `${Math.round(intention.salary_expect / 1000)}k元/月`
  }
  return ''
}

const resetForm = () => {
  selectedCategories.value = []
  selectedSubIndustries.value = []
  selectedJobTypes.value = []
  formData.value = {
    job_nature: 'FULL_TIME',
    work_location_list: [],
    salary_min: undefined,
    salary_max: undefined,
    part_time_days: '',
    work_time_slot: ''
  }
}

const editIntention = (intention: JobIntentionResponse) => {
  editingIntention.value = intention
  
  // 解析并设置表单数据
  const jobTypeIds = parseJsonArray(intention.job_type_list)
  const industryIds = parseJsonArray(intention.industry_list)
  const workLocations = parseJsonArray(intention.work_location_list)
  
  // 分离一级行业和细分行业
  const categoryIds: string[] = []
  const subIds: string[] = []
  
  industryIds.forEach(id => {
    if (industryCategories.value.find(c => c.id === id)) {
      categoryIds.push(id)
    } else if (subIndustries.value.find(s => s.id === id)) {
      subIds.push(id)
    }
  })
  
  selectedCategories.value = categoryIds
  selectedSubIndustries.value = subIds
  selectedJobTypes.value = jobTypeIds
  
  formData.value = {
    job_nature: (intention.job_nature as 'FULL_TIME' | 'PART_TIME') || 'FULL_TIME',
    work_location_list: workLocations,
    salary_min: intention.salary_min,
    salary_max: intention.salary_max,
    part_time_days: intention.part_time_days || '',
    work_time_slot: intention.work_time_slot || ''
  }
  
  showForm.value = true
}

const saveIntention = async () => {
  // 验证必填项
  if (!formData.value.job_nature) {
    alert('请选择求职类型')
    return
  }
  if (selectedCategories.value.length === 0) {
    alert('请至少选择一个行业')
    return
  }
  if (selectedJobTypes.value.length === 0) {
    alert('请至少选择一个职位类型')
    return
  }
  if (formData.value.work_location_list.length === 0) {
    alert('请至少选择一个工作地点')
    return
  }
  
  try {
    // 合并一级行业和细分行业ID
    const industryList = [...selectedCategories.value, ...selectedSubIndustries.value]
    
    const data = {
      job_nature: formData.value.job_nature,
      industry_list: industryList,
      job_type_list: selectedJobTypes.value,
      work_location_list: formData.value.work_location_list,
      salary_min: formData.value.salary_min,
      salary_max: formData.value.salary_max,
      part_time_days: formData.value.job_nature === 'PART_TIME' ? formData.value.part_time_days : undefined,
      work_time_slot: formData.value.job_nature === 'PART_TIME' ? formData.value.work_time_slot : undefined
    }
    
    if (editingIntention.value) {
      await updateJobIntention(editingIntention.value.id, data)
      alert('更新成功')
    } else {
      await createJobIntention(data)
      alert('创建成功')
    }
    showForm.value = false
    editingIntention.value = null
    resetForm()
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

onMounted(async () => {
  await loadDimensionData()
  await loadIntentions()
})
</script>

<style scoped>
/* 多选框样式优化 */
input[type="checkbox"]:checked + span {
  font-weight: 600;
}
</style>
