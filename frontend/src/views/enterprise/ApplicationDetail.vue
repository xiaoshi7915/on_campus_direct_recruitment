<template>
  <div class="enterprise-application-detail">
    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else-if="!application" class="text-center py-12 text-gray-500">申请不存在</div>
    <div v-else>
      <!-- 返回按钮 -->
      <button
        @click="$router.back()"
        class="mb-4 text-blue-600 hover:text-blue-800"
      >
        ← 返回
      </button>

      <!-- 申请详情 -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h1 class="text-3xl font-bold mb-2">职位申请详情</h1>
            <div class="flex flex-wrap gap-4 text-gray-600">
              <span>申请时间：{{ formatDate(application.created_at) }}</span>
              <span>状态：{{ application.status }}</span>
            </div>
          </div>
          <div class="flex flex-col space-y-2">
            <button
              v-if="application.status === 'PENDING'"
              @click="handleAccept"
              class="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              接受申请
            </button>
            <button
              v-if="application.status === 'PENDING'"
              @click="handleReject"
              class="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              拒绝申请
            </button>
          </div>
        </div>

        <div class="border-t pt-4">
          <h2 class="text-xl font-semibold mb-3">申请信息</h2>
          <div class="space-y-2">
            <p><strong>职位：</strong>{{ application.job_title || '未知' }}</p>
            <p><strong>申请人：</strong>{{ application.student_name || '未知' }}</p>
            <p><strong>申请留言：</strong>{{ application.message || '无' }}</p>
          </div>
        </div>
      </div>

      <!-- 简历信息 -->
      <div v-if="resume" class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">简历信息</h2>
        <div class="space-y-4">
          <div>
            <h3 class="font-semibold mb-2">基本信息</h3>
            <div class="text-gray-700 whitespace-pre-wrap">{{ resume.content }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getApplication, updateApplication } from '@/api/applications'
import { getResume } from '@/api/resumes'

const route = useRoute()
const router = useRouter()

const application = ref<any>(null)
const resume = ref<any>(null)
const loading = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 加载申请详情
const loadApplicationDetail = async () => {
  loading.value = true
  try {
    const applicationId = route.params.id as string
    application.value = await getApplication(applicationId)
    
    // 加载简历信息
    if (application.value?.resume_id) {
      try {
        resume.value = await getResume(application.value.resume_id)
      } catch (error) {
        console.error('加载简历失败:', error)
      }
    }
  } catch (error) {
    console.error('加载申请详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 接受申请
const handleAccept = async () => {
  if (!application.value) return
  
  try {
    await updateApplication(application.value.id, { status: 'ACCEPTED' })
    alert('已接受申请！')
    await loadApplicationDetail()
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

// 拒绝申请
const handleReject = async () => {
  if (!application.value) return
  
  if (!confirm('确定要拒绝这个申请吗？')) {
    return
  }
  
  try {
    await updateApplication(application.value.id, { status: 'REJECTED' })
    alert('已拒绝申请！')
    await loadApplicationDetail()
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

onMounted(() => {
  loadApplicationDetail()
})
</script>

<style scoped>
.enterprise-application-detail {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


