<template>
  <div class="teacher-resumes">
    <h1 class="text-3xl font-bold mb-6">简历管理</h1>
    
    <!-- 搜索栏 -->
    <div class="mb-4">
      <input
        v-model="searchStudentId"
        type="text"
        placeholder="输入学生ID筛选（可选）"
        class="px-4 py-2 border rounded-lg w-full max-w-md"
        @keyup.enter="loadResumes"
      />
      <button
        @click="loadResumes"
        class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        搜索
      </button>
    </div>
    
    <!-- 简历列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="resumes.length === 0" class="text-center py-12 text-gray-500">
        暂无简历
      </div>
      <div
        v-for="resume in resumes"
        :key="resume.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ resume.title }}</h3>
            <p class="text-gray-600 text-sm mb-2">
              查看次数：{{ resume.view_count }} | 下载次数：{{ resume.download_count }}
            </p>
            <p class="text-gray-700 line-clamp-3 mb-2">{{ resume.content }}</p>
            <p class="text-gray-500 text-sm">
              创建时间：{{ formatDate(resume.created_at) }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewResume(resume.id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看详情
            </button>
            <button
              v-if="resume.file_url"
              @click="previewResume(resume)"
              class="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600"
            >
              预览文件
            </button>
            <button
              v-if="resume.file_url"
              @click="downloadResumeFile(resume.id)"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              下载文件
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getResumes, downloadResume, type Resume } from '@/api/resumes'
import Pagination from '@/components/Pagination.vue'

const route = useRoute()
const router = useRouter()

// 简历列表
const resumes = ref<Resume[]>([])
const loading = ref(false)
const searchStudentId = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 加载简历列表
const loadResumes = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    
    // 如果URL中有student_id参数，使用它
    const studentIdFromQuery = route.query.student_id as string
    if (studentIdFromQuery) {
      params.student_id = studentIdFromQuery
      searchStudentId.value = studentIdFromQuery
    } else if (searchStudentId.value) {
      params.student_id = searchStudentId.value
    }
    
    const response = await getResumes(params)
    resumes.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载简历失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadResumes()
}

// 查看简历详情
const viewResume = (resumeId: string) => {
  router.push(`/teacher/resumes/${resumeId}`)
}

// 预览简历文件
const previewResume = (resume: Resume) => {
  if (resume.file_url) {
    window.open(resume.file_url, '_blank')
  }
}

// 下载简历文件
const downloadResumeFile = async (resumeId: string) => {
  try {
    await downloadResume(resumeId)
  } catch (error: any) {
    alert('下载失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadResumes()
})
</script>

<style scoped>
.teacher-resumes {
  max-width: 1200px;
  margin: 0 auto;
}
</style>



