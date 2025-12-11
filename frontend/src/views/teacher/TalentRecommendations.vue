<template>
  <div class="talent-recommendations-page">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">推荐人才管理</h1>
      <button
        @click="showRecommendModal = true"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        推荐人才
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">职位ID</label>
          <input
            v-model="jobIdFilter"
            type="text"
            placeholder="筛选职位ID"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">学生ID</label>
          <input
            v-model="studentIdFilter"
            type="text"
            placeholder="筛选学生ID"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
            @keyup.enter="handleSearch"
          />
        </div>
        <div class="flex items-end">
          <button
            @click="handleSearch"
            class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 推荐列表 -->
    <div class="bg-white rounded-lg shadow">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="recommendations.length === 0" class="text-center py-12 text-gray-500">
        暂无推荐信息
      </div>
      <div v-else>
        <div class="divide-y divide-gray-200">
          <div
            v-for="rec in recommendations"
            :key="rec.id"
            class="p-6 hover:bg-gray-50"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <div class="flex items-center space-x-3 mb-2">
                  <h3 class="text-lg font-semibold text-gray-900">{{ rec.job_title || '未知职位' }}</h3>
                  <span class="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                    已推荐
                  </span>
                </div>
                <div class="text-gray-600 text-sm mb-2">
                  <p><strong>学生：</strong>{{ rec.student_name || '未知学生' }}</p>
                  <p v-if="rec.enterprise_name"><strong>企业：</strong>{{ rec.enterprise_name }}</p>
                  <p v-if="rec.recommendation_note"><strong>推荐说明：</strong>{{ rec.recommendation_note }}</p>
                </div>
                <p class="text-sm text-gray-500">
                  推荐时间：{{ formatDateTime(rec.created_at) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="p-4 border-t">
          <Pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            @change="handlePaginationChange"
          />
        </div>
      </div>
    </div>

    <!-- 推荐模态框 -->
    <div
      v-if="showRecommendModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showRecommendModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4 text-gray-900">推荐人才</h2>
          <form @submit.prevent="saveRecommendation">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">职位ID <span class="text-red-500">*</span></label>
                <input
                  v-model="recommendationForm.job_id"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入职位ID"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">学生ID <span class="text-red-500">*</span></label>
                <input
                  v-model="recommendationForm.student_id"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入学生ID"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">简历ID</label>
                <input
                  v-model="recommendationForm.resume_id"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入简历ID（可选）"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">推荐说明</label>
                <textarea
                  v-model="recommendationForm.recommendation_note"
                  rows="4"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入推荐说明"
                ></textarea>
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-4">
              <button
                type="button"
                @click="showRecommendModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                推荐
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
  getTalentRecommendations,
  recommendTalent,
  type TalentRecommendation,
  type TalentRecommendationCreate
} from '@/api/talentRecommendations'
import Pagination from '@/components/Pagination.vue'

// 数据
const recommendations = ref<TalentRecommendation[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索和筛选
const jobIdFilter = ref('')
const studentIdFilter = ref('')

// 模态框状态
const showRecommendModal = ref(false)

// 表单数据
const recommendationForm = ref<TalentRecommendationCreate>({
  job_id: '',
  student_id: '',
  resume_id: '',
  recommendation_note: ''
})

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 加载推荐列表
const loadRecommendations = async () => {
  loading.value = true
  try {
    const response = await getTalentRecommendations({
      page: currentPage.value,
      page_size: pageSize.value,
      job_id: jobIdFilter.value || undefined,
      student_id: studentIdFilter.value || undefined
    })
    recommendations.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('加载推荐列表失败:', error)
    alert('加载推荐列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadRecommendations()
}

// 分页变化
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadRecommendations()
}

// 保存推荐
const saveRecommendation = async () => {
  try {
    await recommendTalent(recommendationForm.value)
    alert('推荐成功！')
    showRecommendModal.value = false
    recommendationForm.value = {
      job_id: '',
      student_id: '',
      resume_id: '',
      recommendation_note: ''
    }
    loadRecommendations()
  } catch (error: any) {
    console.error('推荐失败:', error)
    alert('推荐失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadRecommendations()
})
</script>

<style scoped>
.talent-recommendations-page {
  max-width: 1400px;
  margin: 0 auto;
}
</style>




