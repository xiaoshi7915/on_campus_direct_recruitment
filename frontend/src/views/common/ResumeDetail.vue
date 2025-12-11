<template>
  <div class="resume-detail">
    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else-if="resume" class="bg-white rounded-lg shadow p-6">
      <div class="flex justify-between items-start mb-6">
        <h1 class="text-3xl font-bold">{{ resume.title }}</h1>
        <div class="flex space-x-2">
          <button
            v-if="resume.file_url"
            @click="previewFile"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            预览文件
          </button>
          <button
            v-if="resume.file_url"
            @click="downloadFile"
            class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
          >
            下载文件
          </button>
          <button
            @click="goBack"
            class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
          >
            返回
          </button>
        </div>
      </div>
      
      <div class="mb-4 text-gray-600 text-sm">
        <span>查看次数：{{ resume.view_count }}</span>
        <span class="ml-4">下载次数：{{ resume.download_count }}</span>
        <span class="ml-4">创建时间：{{ formatDate(resume.created_at) }}</span>
      </div>
      
      <div class="border-t pt-6">
        <h2 class="text-xl font-semibold mb-4">简历内容</h2>
        <div class="text-gray-700 whitespace-pre-wrap">{{ resume.content }}</div>
      </div>
      
      <div v-if="resume.file_url" class="mt-6 border-t pt-6">
        <h2 class="text-xl font-semibold mb-4">电子版简历</h2>
        <p class="text-gray-600 mb-2">文件URL：{{ resume.file_url }}</p>
        <div class="flex space-x-2">
          <button
            @click="previewFile"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            预览
          </button>
          <button
            @click="downloadFile"
            class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
          >
            下载
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-12 text-gray-500">
      简历不存在
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
  return date.toLocaleString('zh-CN')
}

// 加载简历详情
const loadResume = async () => {
  const resumeId = route.params.id as string
  if (!resumeId) return
  
  loading.value = true
  try {
    resume.value = await getResume(resumeId)
  } catch (error: any) {
    alert('加载简历失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 预览文件
const previewFile = async () => {
  if (resume.value?.file_url) {
    // file_url已经是签名URL，直接打开
    window.open(resume.value.file_url, '_blank')
  } else if (resume.value?.id) {
    // 如果没有file_url但有id，尝试获取预览URL
    try {
      const { getResumePreviewUrl } = await import('@/api/resumes')
      const previewUrl = await getResumePreviewUrl(resume.value.id)
      window.open(previewUrl, '_blank')
    } catch (error: any) {
      alert('预览失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

// 下载文件
const downloadFile = async () => {
  if (resume.value?.id) {
    try {
      await downloadResume(resume.value.id)
    } catch (error: any) {
      alert('下载失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

// 返回上一页
const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    // 如果没有历史记录，跳转到简历列表页
    router.push('/student/resumes')
  }
}

onMounted(() => {
  loadResume()
})
</script>

<style scoped>
.resume-detail {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

