<template>
  <div class="student-resumes">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">我的简历</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        创建简历
      </button>
    </div>

    <!-- 简历列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="resumes.length === 0" class="text-center py-12 text-gray-500">
        暂无简历，点击上方按钮创建第一份简历
      </div>
      <div
        v-for="resume in resumes"
        :key="resume.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ resume.title }}</h3>
              <span
                v-if="resume.is_default"
                class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
              >
                默认简历
              </span>
            </div>
            <p class="text-gray-600 text-sm mb-3">
              查看次数：{{ resume.view_count }} | 下载次数：{{ resume.download_count }}
            </p>
            <p class="text-gray-700 line-clamp-3">{{ resume.content }}</p>
            <p class="text-gray-500 text-sm mt-3">
              创建时间：{{ formatDate(resume.created_at) }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editResume(resume)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="setDefault(resume.id)"
              v-if="!resume.is_default"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              设为默认
            </button>
            <button
              @click="handleDeleteResume(resume.id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              删除
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

    <!-- 创建/编辑简历模态框 -->
    <div
      v-if="showCreateModal || editingResume"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">
          {{ editingResume ? '编辑简历' : '创建简历' }}
        </h2>
        <form @submit.prevent="saveResume">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">简历标题</label>
            <input
              v-model="resumeForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：前端开发工程师简历"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">简历内容</label>
            <textarea
              v-model="resumeForm.content"
              required
              rows="15"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入简历内容..."
            />
          </div>
          <div class="mb-4">
            <label class="flex items-center">
              <input
                v-model="resumeForm.is_default"
                type="checkbox"
                class="mr-2"
              />
              <span class="text-sm text-gray-700">设为默认简历</span>
            </label>
          </div>
          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="closeModal"
              class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
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
import { getResumes, createResume, updateResume, deleteResume, type Resume } from '@/api/resumes'
import Pagination from '@/components/Pagination.vue'

// 简历列表
const resumes = ref<Resume[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const editingResume = ref<Resume | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 表单数据
const resumeForm = ref({
  title: '',
  content: '',
  is_default: false,
})

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
    const response = await getResumes({
      page: currentPage.value,
      page_size: pageSize.value,
    })
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

// 编辑简历
const editResume = (resume: Resume) => {
  editingResume.value = resume
  resumeForm.value = {
    title: resume.title,
    content: resume.content,
    is_default: resume.is_default,
  }
}

// 保存简历
const saveResume = async () => {
  try {
    if (editingResume.value) {
      await updateResume(editingResume.value.id, resumeForm.value)
    } else {
      await createResume(resumeForm.value)
    }
    closeModal()
    loadResumes()
  } catch (error: any) {
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  }
}

// 设为默认
const setDefault = async (resumeId: string) => {
  try {
    await updateResume(resumeId, { is_default: true })
    loadResumes()
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

// 删除简历
const handleDeleteResume = async (resumeId: string) => {
  if (!confirm('确定要删除这份简历吗？')) {
    return
  }
  try {
    await deleteResume(resumeId)
    loadResumes()
  } catch (error: any) {
    alert(error.response?.data?.detail || '删除失败，请稍后重试')
  }
}

// 关闭模态框
const closeModal = () => {
  showCreateModal.value = false
  editingResume.value = null
  resumeForm.value = {
    title: '',
    content: '',
    is_default: false,
  }
}

onMounted(() => {
  loadResumes()
})
</script>

<style scoped>
.student-resumes {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

