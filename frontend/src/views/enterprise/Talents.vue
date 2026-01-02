<template>
  <div class="enterprise-talents w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">人才搜索</h1>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">关键词</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索简历..."
              class="input-search"
              @keyup.enter="handleSearch"
            />
          </div>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">专业</label>
          <input
            v-model="filters.major"
            type="text"
            placeholder="例如：计算机科学"
            class="input-base"
            @change="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">学历</label>
          <select
            v-model="filters.education"
            class="select-base"
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
            class="btn btn-primary btn-md btn-full"
          >
            <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            搜索
          </button>
        </div>
      </div>
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
        <p class="text-gray-500 text-lg">暂无简历信息</p>
        <p class="text-gray-400 text-sm mt-2">尝试调整搜索条件</p>
      </div>
      <div
        v-for="resume in resumes"
        :key="resume.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-green-50 rounded-lg">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ resume.title }}</h3>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-11">
              <span v-if="resume.major" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
                </svg>
                专业：{{ resume.major }}
              </span>
              <span v-if="resume.education" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                </svg>
                学历：{{ resume.education }}
              </span>
              <span v-if="resume.graduation_year" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                毕业年份：{{ resume.graduation_year }}
              </span>
            </div>
            <p class="text-gray-700 line-clamp-3 mb-3 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">{{ resume.content }}</p>
            <div class="flex items-center space-x-4 text-sm text-gray-500 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                查看：{{ resume.view_count }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                下载：{{ resume.download_count }}
              </span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewResume(resume.id)"
              class="btn btn-primary btn-md"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              查看简历
            </button>
            <button
              @click="downloadResume(resume.id)"
              class="btn btn-outline-primary btn-md"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              下载简历
            </button>
            <button
              @click="markResume(resume.id)"
              :class="[
                'btn btn-md',
                resumeMarkMap[resume.id] ? 'btn-warning' : 'btn-outline-warning'
              ]"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              {{ resumeMarkMap[resume.id] ? '已标记' : '标记' }}
            </button>
            <button
              @click="shareResume(resume.id)"
              class="btn btn-outline-success btn-md whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
              </svg>
              分享
            </button>
            <button
              @click="startChat(resume.student_id)"
              class="btn btn-outline-primary btn-md whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
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

    <!-- 标记模态框 -->
    <div
      v-if="showMarkModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showMarkModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full border border-gray-100">
        <div class="p-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center">
              <svg class="w-6 h-6 mr-2 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              标记简历
            </h2>
            <button
              @click="showMarkModal = false"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">备注</label>
              <textarea
                v-model="markNote"
                rows="3"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
                placeholder="请输入备注（可选）"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">标记颜色</label>
              <select
                v-model="markColor"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              >
                <option value="blue">蓝色</option>
                <option value="red">红色</option>
                <option value="green">绿色</option>
                <option value="yellow">黄色</option>
                <option value="purple">紫色</option>
              </select>
            </div>
          </div>
          <div class="mt-6 pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              @click="showMarkModal = false"
              class="btn btn-secondary btn-md"
            >
              取消
            </button>
            <button
              @click="saveMark"
              class="btn btn-primary btn-md"
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getResumes, type Resume } from '@/api/resumes'
import { getMark, createMark, deleteMark, type Mark } from '@/api/marks'
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

// 简历标记映射
const resumeMarkMap = ref<Record<string, Mark>>({})
const showMarkModal = ref(false)
const currentResumeId = ref<string | null>(null)
const markNote = ref('')
const markColor = ref('blue')


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
  // 跳转到企业端简历详情页面
  router.push(`/enterprise/resumes/${resumeId}`)
}

// 下载简历
const downloadResume = async (resumeId: string) => {
  try {
    const { downloadResume: downloadResumeAPI } = await import('@/api/resumes')
    await downloadResumeAPI(resumeId)
  } catch (error: any) {
    alert('下载失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 发起聊天
const startChat = async (studentId: string) => {
  // studentId 是 student_profiles.id，需要转换为 users.id
  // 由于前端无法直接查询，我们通过创建聊天会话API来处理
  // 后端API应该支持通过student_id创建会话
  try {
    const { createOrGetChatSession } = await import('@/api/chat')
    // 注意：这里需要后端API支持通过student_id创建会话
    // 暂时先尝试使用studentId作为user_id（如果后端支持）
    // 或者需要先查询student_id对应的user_id
    router.push(`/enterprise/chat?student_id=${studentId}`)
  } catch (error) {
    console.error('发起聊天失败:', error)
  }
}

// 标记简历
const markResume = async (resumeId: string) => {
  try {
    // 检查是否已有标记
    const existingMark = resumeMarkMap.value[resumeId]
    if (existingMark) {
      // 如果已有标记，显示标记详情或删除
      if (confirm('是否删除此标记？')) {
        await deleteMark(existingMark.id)
        delete resumeMarkMap.value[resumeId]
        alert('标记已删除')
      }
    } else {
      // 创建新标记
      currentResumeId.value = resumeId
      markNote.value = ''
      markColor.value = 'blue'
      showMarkModal.value = true
    }
  } catch (error: any) {
    console.error('标记操作失败:', error)
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 保存标记
const saveMark = async () => {
  if (!currentResumeId.value) return
  try {
    const mark = await createMark({
      target_type: 'RESUME',
      target_id: currentResumeId.value,
      note: markNote.value || undefined,
      color: markColor.value
    })
    resumeMarkMap.value[currentResumeId.value] = mark
    showMarkModal.value = false
    alert('标记成功')
  } catch (error: any) {
    console.error('保存标记失败:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 分享简历
const shareResume = async (resumeId: string) => {
  try {
    const resume = resumes.value.find(r => r.id === resumeId)
    if (!resume) return
    
    // 生成分享链接
    const shareUrl = `${window.location.origin}/resumes/${resumeId}`
    const shareText = `推荐简历：${resume.title}\n${shareUrl}`
    
    // 尝试使用Web Share API
    if (navigator.share) {
      try {
        await navigator.share({
          title: resume.title,
          text: shareText,
          url: shareUrl
        })
        return
      } catch (err) {
        // 用户取消分享，继续使用复制方式
      }
    }
    
    // 复制到剪贴板 - 优先使用现代 Clipboard API，降级到传统方法
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(shareText)
      alert('分享链接已复制到剪贴板')
    } else {
      // 降级方案：使用传统的 document.execCommand 方法
      const textArea = document.createElement('textarea')
      textArea.value = shareText
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      
      try {
        const successful = document.execCommand('copy')
        if (successful) {
          alert('分享链接已复制到剪贴板')
        } else {
          throw new Error('复制失败，请手动复制')
        }
      } finally {
        document.body.removeChild(textArea)
      }
    }
  } catch (error: any) {
    console.error('分享失败:', error)
    alert('分享失败: ' + (error.message || '未知错误'))
  }
}

// 加载简历标记
const loadResumeMarks = async () => {
  try {
    const { getMarks } = await import('@/api/marks')
    const response = await getMarks({
      target_type: 'RESUME',
      page_size: 100
    })
    // 构建标记映射
    resumeMarkMap.value = {}
    response.items.forEach(mark => {
      resumeMarkMap.value[mark.target_id] = mark
    })
  } catch (error) {
    console.error('加载标记失败:', error)
  }
}

onMounted(() => {
  handleSearch()
  loadResumeMarks()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

