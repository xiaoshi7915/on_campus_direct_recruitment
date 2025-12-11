<template>
  <div class="enterprise-job-edit">
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

      <!-- 编辑表单 -->
      <div class="bg-white rounded-lg shadow p-6">
        <h1 class="text-3xl font-bold mb-6">编辑职位</h1>
        <form @submit.prevent="saveJob">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">职位标题 *</label>
              <input
                v-model="jobForm.title"
                type="text"
                required
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">部门</label>
              <input
                v-model="jobForm.department"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">职位类型</label>
              <select
                v-model="jobForm.job_type"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="FULL_TIME">全职</option>
                <option value="PART_TIME">兼职</option>
                <option value="INTERN">实习</option>
                <option value="CONTRACT">合同</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">工作地点</label>
              <input
                v-model="jobForm.work_location"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">最低薪资</label>
              <input
                v-model.number="jobForm.salary_min"
                type="number"
                min="0"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">最高薪资</label>
              <input
                v-model.number="jobForm.salary_max"
                type="number"
                min="0"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">工作经验</label>
              <input
                v-model="jobForm.experience"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例如：1-3年"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">学历要求</label>
              <select
                v-model="jobForm.education"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="不限">不限</option>
                <option value="高中">高中</option>
                <option value="大专">大专</option>
                <option value="本科">本科</option>
                <option value="硕士">硕士</option>
                <option value="博士">博士</option>
              </select>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">职位描述 *</label>
            <textarea
              v-model="jobForm.description"
              required
              rows="6"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入职位描述..."
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">职位要求</label>
            <textarea
              v-model="jobForm.requirements"
              rows="4"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入职位要求..."
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">标签（用逗号分隔）</label>
            <input
              v-model="jobForm.tags"
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：高薪,五险一金,带薪年假"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
            <select
              v-model="jobForm.status"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="DRAFT">草稿</option>
              <option value="PUBLISHED">已发布</option>
              <option value="CLOSED">已关闭</option>
            </select>
          </div>
          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="$router.back()"
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
import { useRoute, useRouter } from 'vue-router'
import { getJob, updateJob, type Job } from '@/api/jobs'

const route = useRoute()
const router = useRouter()

const job = ref<Job | null>(null)
const loading = ref(false)

// 表单数据
const jobForm = ref({
  title: '',
  department: '',
  job_type: 'FULL_TIME',
  work_location: '',
  salary_min: undefined as number | undefined,
  salary_max: undefined as number | undefined,
  experience: '',
  education: '不限',
  description: '',
  requirements: '',
  tags: '',
  status: 'PUBLISHED',
})

// 加载职位详情
const loadJobDetail = async () => {
  loading.value = true
  try {
    const jobId = route.params.id as string
    job.value = await getJob(jobId)
    
    if (job.value) {
      jobForm.value = {
        title: job.value.title,
        department: job.value.department || '',
        job_type: job.value.job_type || 'FULL_TIME',
        work_location: job.value.work_location || '',
        salary_min: job.value.salary_min,
        salary_max: job.value.salary_max,
        experience: job.value.experience || '',
        education: job.value.education || '不限',
        description: job.value.description,
        requirements: job.value.requirements || '',
        tags: job.value.tags || '',
        status: job.value.status,
      }
    }
  } catch (error) {
    console.error('加载职位详情失败:', error)
    alert('加载职位详情失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 保存职位
const saveJob = async () => {
  if (!job.value) return
  
  try {
    await updateJob(job.value.id, jobForm.value)
    alert('保存成功！')
    router.push(`/enterprise/jobs/${job.value.id}`)
  } catch (error: any) {
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  }
}

onMounted(() => {
  loadJobDetail()
})
</script>

<style scoped>
.enterprise-job-edit {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

