<template>
  <div class="student-job-detail">
    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else-if="!job" class="text-center py-12 text-gray-500">职位不存在</div>
    <div v-else>
      <!-- 返回按钮 -->
      <button
        @click="$router.back()"
        class="mb-4 text-blue-600 hover:text-blue-800"
      >
        ← 返回
      </button>

      <!-- 职位详情 -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h1 class="text-3xl font-bold mb-2">{{ job.title }}</h1>
            <div class="flex flex-wrap gap-4 text-gray-600">
              <span>{{ job.work_location }}</span>
              <span>{{ job.job_type }}</span>
              <span v-if="job.salary_min && job.salary_max">
                {{ job.salary_min }}-{{ job.salary_max }}元
              </span>
              <span>{{ job.education || '不限' }}</span>
            </div>
          </div>
          <div class="flex flex-col space-y-2">
            <button
              @click="handleApply"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              立即申请
            </button>
            <button
              @click="handleFavorite"
              class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              {{ isFavorited ? '已收藏' : '收藏' }}
            </button>
          </div>
        </div>

        <div v-if="job.tags" class="mb-4 flex flex-wrap gap-2">
          <span
            v-for="tag in job.tags.split(',')"
            :key="tag"
            class="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded"
          >
            {{ tag }}
          </span>
        </div>

        <div class="border-t pt-4">
          <h2 class="text-xl font-semibold mb-3">职位描述</h2>
          <div class="text-gray-700 whitespace-pre-wrap">{{ job.description }}</div>
        </div>

        <div v-if="job.requirements" class="border-t pt-4 mt-4">
          <h2 class="text-xl font-semibold mb-3">职位要求</h2>
          <div class="text-gray-700 whitespace-pre-wrap">{{ job.requirements }}</div>
        </div>

        <div class="border-t pt-4 mt-4 text-sm text-gray-500">
          <p>查看次数：{{ job.view_count }} | 申请次数：{{ job.apply_count }}</p>
          <p>发布时间：{{ formatDate(job.created_at) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getJob, type Job } from '@/api/jobs'
import { createApplication } from '@/api/applications'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'

const route = useRoute()
const router = useRouter()

const job = ref<Job | null>(null)
const loading = ref(false)
const isFavorited = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 加载职位详情
const loadJobDetail = async () => {
  loading.value = true
  try {
    const jobId = route.params.id as string
    job.value = await getJob(jobId)
    
    // 检查收藏状态
    if (job.value) {
      isFavorited.value = await checkFavorite('JOB', job.value.id)
    }
  } catch (error) {
    console.error('加载职位详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 申请职位
const handleApply = async () => {
  if (!job.value) return
  
  try {
    await createApplication({ job_id: job.value.id })
    alert('申请成功！')
    router.push('/student/applications')
  } catch (error: any) {
    alert(error.response?.data?.detail || '申请失败，请稍后重试')
  }
}

// 收藏/取消收藏
const handleFavorite = async () => {
  if (!job.value) return
  
  try {
    if (isFavorited.value) {
      await removeFavorite('JOB', job.value.id)
      isFavorited.value = false
    } else {
      await addFavorite('JOB', job.value.id)
      isFavorited.value = true
    }
  } catch (error: any) {
    alert(error.response?.data?.detail || '操作失败，请稍后重试')
  }
}

onMounted(() => {
  loadJobDetail()
})
</script>

<style scoped>
.student-job-detail {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


