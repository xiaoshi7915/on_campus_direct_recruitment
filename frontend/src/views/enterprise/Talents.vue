<template>
  <div class="enterprise-talents">
    <h1 class="text-3xl font-bold mb-6">人才搜索</h1>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">关键词</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索简历..."
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">专业</label>
          <input
            v-model="filters.major"
            type="text"
            placeholder="例如：计算机科学"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">学历</label>
          <select
            v-model="filters.education"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          >
            <option value="">全部</option>
            <option value="BACHELOR">本科</option>
            <option value="MASTER">硕士</option>
            <option value="DOCTOR">博士</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="handleSearch"
            class="w-full px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 简历列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="resumes.length === 0" class="text-center py-12 text-gray-500">
        暂无简历信息
      </div>
      <div
        v-for="resume in resumes"
        :key="resume.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ resume.title }}</h3>
            <div class="text-gray-600 text-sm mb-3">
              <p v-if="resume.major">专业：{{ resume.major }}</p>
              <p v-if="resume.education">学历：{{ resume.education }}</p>
              <p v-if="resume.graduation_year">毕业年份：{{ resume.graduation_year }}</p>
            </div>
            <p class="text-gray-700 line-clamp-3 mb-3">{{ resume.content }}</p>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>查看：{{ resume.view_count }}</span>
              <span>下载：{{ resume.download_count }}</span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewResume(resume.id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看简历
            </button>
            <button
              @click="downloadResume(resume.id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              下载简历
            </button>
            <button
              @click="startChat(resume.student_id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              发起聊天
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <Pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      @change="handlePaginationChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getResumes, type Resume } from '@/api/resumes'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 简历列表
const resumes = ref<Resume[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const filters = ref({
  major: '',
  education: '',
})
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)


// 搜索简历
const handleSearch = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }

    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    if (filters.value.major) {
      params.major = filters.value.major
    }
    if (filters.value.education) {
      params.education = filters.value.education
    }

    const response = await getResumes(params)
    resumes.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('搜索简历失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  handleSearch()
}

// 查看简历
const viewResume = (resumeId: string) => {
  // TODO: 打开简历查看窗口
  alert(`查看简历：${resumeId}`)
}

// 下载简历
const downloadResume = async (resumeId: string) => {
  // TODO: 实现下载功能
  alert(`下载简历：${resumeId}`)
}

// 发起聊天
const startChat = async (studentId: string) => {
  // TODO: 创建或获取聊天会话
  router.push(`/enterprise/chat?user_id=${studentId}`)
}

onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.enterprise-talents {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

