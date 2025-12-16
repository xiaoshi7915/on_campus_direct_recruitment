<template>
  <div class="resume-detail-page max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    <div v-else-if="resume" class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
      <!-- 头部信息 -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white">
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h1 class="text-4xl font-bold mb-4">{{ resume.title }}</h1>
            <div class="flex flex-wrap items-center gap-6 text-blue-100">
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                查看次数：{{ resume.view_count }}
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                下载次数：{{ resume.download_count }}
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                创建时间：{{ formatDate(resume.created_at) }}
              </div>
            </div>
          </div>
          <button
            @click="goBack"
            class="px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded-xl transition-all duration-200 font-medium flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            返回
          </button>
        </div>
      </div>

      <!-- 简历内容 -->
      <div class="p-8">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            简历内容
          </h2>
          <div class="bg-gray-50 rounded-xl p-6 border border-gray-200">
            <div class="text-gray-700 whitespace-pre-wrap leading-relaxed">{{ resume.content || '暂无内容' }}</div>
          </div>
        </div>
        
        <!-- 电子版简历附件 -->
        <div v-if="resume.file_url" class="border-t border-gray-200 pt-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            电子版简历附件
          </h2>
          <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border-2 border-blue-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div class="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center">
                  <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-600 mb-1">附件文件</p>
                  <p class="text-sm font-semibold text-gray-900 break-all max-w-md">{{ getFileName(resume.file_url) }}</p>
                </div>
              </div>
              <div class="flex space-x-3">
                <button
                  @click="previewFile"
                  class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  预览文件
                </button>
                <button
                  @click="downloadFile"
                  class="px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  下载文件
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="border-t border-gray-200 pt-8">
          <div class="bg-gray-50 rounded-xl p-6 border border-gray-200 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            <p class="text-gray-500">该简历暂无电子版附件</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-16">
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-12">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-xl text-gray-500 mb-2">简历不存在</p>
        <p class="text-gray-400 mb-6">该简历可能已被删除或不存在</p>
        <button
          @click="goBack"
          class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium"
        >
          返回
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getResume, downloadResume, type Resume } from '@/api/resumes'

const route = useRoute()
const router = useRouter()
const resume = ref<Resume | null>(null)
const loading = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 从URL中提取文件名
const getFileName = (url: string) => {
  try {
    const urlObj = new URL(url)
    const pathname = urlObj.pathname
    const fileName = pathname.split('/').pop() || '简历文件'
    // 解码URL编码的文件名
    return decodeURIComponent(fileName)
  } catch {
    // 如果不是完整URL，尝试提取文件名
    const parts = url.split('/')
    return parts[parts.length - 1] || '简历文件'
  }
}

// 加载简历详情
const loadResume = async () => {
  const resumeId = route.params.id as string
  if (!resumeId) {
    alert('简历ID不存在')
    goBack()
    return
  }
  
  loading.value = true
  try {
    resume.value = await getResume(resumeId)
  } catch (error: any) {
    console.error('加载简历失败:', error)
    const errorMessage = error.response?.data?.detail || error.message || '未知错误'
    console.error('错误详情:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message
    })
    
    // 如果是403权限错误，给出更友好的提示
    if (error.response?.status === 403) {
      alert('无权查看此简历。如果您是企业用户，请联系管理员检查权限设置。')
    } else if (error.response?.status === 404) {
      alert('简历不存在或已被删除')
    } else {
      alert('加载简历失败: ' + errorMessage)
    }
    
    // 如果加载失败，延迟后返回
    setTimeout(() => {
      goBack()
    }, 2000)
  } finally {
    loading.value = false
  }
}

// 预览文件
const previewFile = async () => {
  if (!resume.value) return
  
  if (resume.value.file_url) {
    // file_url已经是签名URL，直接打开
    window.open(resume.value.file_url, '_blank')
  } else if (resume.value.id) {
    // 如果没有file_url但有id，尝试获取预览URL
    try {
      const { getResumePreviewUrl } = await import('@/api/resumes')
      const previewUrl = await getResumePreviewUrl(resume.value.id)
      window.open(previewUrl, '_blank')
    } catch (error: any) {
      alert('预览失败: ' + (error.response?.data?.detail || error.message))
    }
  } else {
    alert('该简历没有电子版文件，无法预览')
  }
}

// 下载文件
const downloadFile = async () => {
  if (!resume.value?.id) {
    alert('简历ID不存在')
    return
  }
  
  try {
    await downloadResume(resume.value.id)
  } catch (error: any) {
    console.error('下载失败:', error)
    console.error('下载错误详情:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message
    })
    
    const errorMessage = error.response?.data?.detail || error.message || '未知错误'
    
    // 如果是403权限错误，给出更友好的提示
    if (error.response?.status === 403) {
      alert('无权下载此简历。如果您是企业用户，请联系管理员检查权限设置。')
    } else if (error.response?.status === 404) {
      alert('该简历没有电子版文件，无法下载。')
    } else {
      // downloadResume函数已经处理了大部分错误，这里只处理特殊情况
      if (!errorMessage.includes('没有电子版文件') && !errorMessage.includes('404')) {
        alert('下载失败: ' + errorMessage)
      }
    }
  }
}

// 返回上一页
const goBack = () => {
  // 根据当前路由判断应该返回哪里
  const currentPath = route.path
  
  if (currentPath.startsWith('/enterprise')) {
    // 企业端：尝试返回申请管理或人才库
    if (window.history.length > 1) {
      router.back()
    } else {
      router.push('/enterprise/applications')
    }
  } else if (currentPath.startsWith('/teacher')) {
    // 教师端：返回简历列表
    if (window.history.length > 1) {
      router.back()
    } else {
      router.push('/teacher/resumes')
    }
  } else if (currentPath.startsWith('/student')) {
    // 学生端：返回简历列表
    if (window.history.length > 1) {
      router.back()
    } else {
      router.push('/student/resumes')
    }
  } else {
    // 默认返回首页
    router.push('/')
  }
}

onMounted(() => {
  loadResume()
})
</script>

<style scoped>
.resume-detail-page {
  min-height: calc(100vh - 120px);
}
</style>
