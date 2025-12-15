<template>
  <div class="student-resumes max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">我的简历</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        创建简历
      </button>
    </div>

    <!-- 简历列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="resumes.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无简历</p>
        <p class="text-gray-400 text-sm mt-2">点击上方按钮创建第一份简历</p>
      </div>
      <div
        v-for="resume in resumes"
        :key="resume.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ resume.title }}</h3>
              <span
                v-if="resume.is_default"
                class="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-medium"
              >
                默认简历
              </span>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                查看次数：{{ resume.view_count }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                下载次数：{{ resume.download_count }}
              </span>
            </div>
            <p class="text-gray-700 line-clamp-3 mb-3 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ resume.content }}
            </p>
            <p class="text-gray-500 text-sm mt-3 ml-11 flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              创建时间：{{ formatDate(resume.created_at) }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editResume(resume)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              编辑
            </button>
            <button
              @click="setDefault(resume.id)"
              v-if="!resume.is_default"
              class="px-5 py-2.5 border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium"
            >
              设为默认
            </button>
            <button
              @click="handleDeleteResume(resume.id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center justify-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
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
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-gray-100 w-full max-w-4xl max-h-[95vh] flex flex-col overflow-hidden">
        <!-- 固定头部 -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200 flex-shrink-0">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            {{ editingResume ? '编辑简历' : '创建简历' }}
          </h2>
          <button
            @click="closeModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <!-- 可滚动内容区域 -->
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">简历标题</label>
            <input
              v-model="resumeForm.title"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              placeholder="例如：前端开发工程师简历"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">简历内容</label>
            <textarea
              v-model="resumeForm.content"
              required
              rows="15"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
              placeholder="请输入简历内容..."
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">电子版简历文件（PDF、Word等）</label>
            <div class="space-y-3">
              <div class="flex items-center space-x-4">
                <input
                  type="file"
                  ref="fileInput"
                  @change="handleFileSelect"
                  accept=".pdf,.doc,.docx"
                  class="hidden"
                />
                <button
                  type="button"
                  @click="fileInput?.click()"
                  class="px-5 py-2.5 border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium flex items-center"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  选择文件
                </button>
                <span v-if="selectedFile" class="text-sm text-gray-600 flex items-center">
                  <svg class="w-4 h-4 mr-1 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ selectedFile.name }}
                </span>
                <button
                  v-if="resumeForm.file_url"
                  type="button"
                  @click="previewFile"
                  class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm flex items-center"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  预览当前文件
                </button>
              </div>
              <p v-if="uploading" class="text-sm text-blue-600 flex items-center">
                <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                上传中...
              </p>
              <p v-if="resumeForm.file_url" class="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-200">
                已上传文件：{{ resumeForm.file_url }}
              </p>
            </div>
          </div>
          <div>
            <label class="flex items-center cursor-pointer">
              <input
                v-model="resumeForm.is_default"
                type="checkbox"
                class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <span class="ml-2 text-sm text-gray-700 font-medium">设为默认简历</span>
            </label>
          </div>
          </div>
        </div>
        <!-- 固定底部按钮 -->
        <div class="flex justify-end space-x-4 p-6 border-t border-gray-200 bg-gray-50 flex-shrink-0">
          <button
            type="button"
            @click="closeModal"
            class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
          >
            取消
          </button>
          <button
            type="button"
            @click="saveResume"
            class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getResumes, createResume, updateResume, deleteResume, type Resume } from '@/api/resumes'
import { uploadDocument } from '@/api/upload'
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
  file_url: '',
  is_default: false,
})

// 文件上传
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const uploading = ref(false)

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

// 选择文件
const handleFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  
  selectedFile.value = file
  uploading.value = true
  
  try {
    // 上传文件
    const response = await uploadDocument(file, 'resume')
    resumeForm.value.file_url = response.url
    alert('文件上传成功！')
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
    selectedFile.value = null
  } finally {
    uploading.value = false
  }
}

// 预览文件
const previewFile = () => {
  if (resumeForm.value.file_url) {
    window.open(resumeForm.value.file_url, '_blank')
  }
}

// 编辑简历
const editResume = (resume: Resume) => {
  editingResume.value = resume
  resumeForm.value = {
    title: resume.title,
    content: resume.content,
    file_url: resume.file_url || '',
    is_default: resume.is_default,
  }
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
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
/* 样式已内联到模板中 */
</style>

