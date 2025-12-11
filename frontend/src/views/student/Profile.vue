<template>
  <div class="student-profile">
    <h1 class="text-3xl font-bold mb-6">个人中心</h1>

    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧：个人信息 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">基本信息</h2>
          <div v-if="!profile" class="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p class="text-yellow-800 text-sm">您还没有创建学生档案，请填写下方信息创建档案</p>
          </div>
          <form @submit.prevent="saveProfile">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">真实姓名</label>
                <input
                  v-model="profileForm.real_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">学号</label>
                <input
                  v-model="profileForm.student_id"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">年级</label>
                <input
                  v-model="profileForm.grade"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">专业</label>
                <input
                  v-model="profileForm.major"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <div class="mt-6 flex justify-end">
              <button
                type="submit"
                class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                {{ profile ? '保存' : '创建档案' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- 右侧：统计信息 -->
      <div class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">统计信息</h2>
          <div class="space-y-4">
            <div>
              <div class="text-gray-600 text-sm">我的简历</div>
              <div class="text-2xl font-bold text-blue-600">{{ resumeCount }}</div>
            </div>
            <div>
              <div class="text-gray-600 text-sm">我的申请</div>
              <div class="text-2xl font-bold text-green-600">{{ applicationCount }}</div>
            </div>
            <div>
              <div class="text-gray-600 text-sm">待面试</div>
              <div class="text-2xl font-bold text-orange-600">{{ interviewCount }}</div>
            </div>
            <div>
              <div class="text-gray-600 text-sm">收藏职位</div>
              <div class="text-2xl font-bold text-purple-600">{{ favoriteCount }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getStudentProfile, updateStudentProfile, type StudentProfile } from '@/api/profile'
import { getResumes } from '@/api/resumes'
import { getApplications } from '@/api/applications'
import { getInterviews } from '@/api/interviews'
import { getFavorites } from '@/api/favorites'

// 档案数据
const profile = ref<StudentProfile | null>(null)
const loading = ref(false)

// 表单数据
const profileForm = ref({
  real_name: '',
  student_id: '',
  grade: '',
  major: '',
})

// 统计数据
const resumeCount = ref(0)
const applicationCount = ref(0)
const interviewCount = ref(0)
const favoriteCount = ref(0)

// 加载档案数据
const loadProfile = async () => {
  loading.value = true
  try {
    profile.value = await getStudentProfile()
    if (profile.value) {
      profileForm.value = {
        real_name: profile.value.real_name || '',
        student_id: profile.value.student_id || '',
        grade: profile.value.grade || '',
        major: profile.value.major || '',
      }
    }

    // 加载统计数据
    const [resumesRes, applicationsRes, interviewsRes, favoritesRes] = await Promise.all([
      getResumes({ page_size: 1 }).catch(() => ({ total: 0 })),
      getApplications({ page_size: 1 }).catch(() => ({ total: 0 })),
      getInterviews({ status: 'SCHEDULED', page_size: 1 }).catch(() => ({ total: 0 })),
      getFavorites({ target_type: 'JOB', page_size: 1 }).catch(() => ({ total: 0 })),
    ])

    resumeCount.value = resumesRes.total || 0
    applicationCount.value = applicationsRes.total || 0
    interviewCount.value = interviewsRes.total || 0
    favoriteCount.value = favoritesRes.total || 0
  } catch (error: any) {
    console.error('加载档案失败:', error)
    // 如果档案不存在（404），提示用户创建档案
    if (error.response?.status === 404) {
      console.log('学生档案不存在，需要创建')
      // 不显示错误，让用户看到空表单可以填写
    } else {
      alert('加载档案失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
    }
  } finally {
    loading.value = false
  }
}

// 保存档案
const saveProfile = async () => {
  try {
    if (profile.value) {
      // 更新现有档案
      await updateStudentProfile(profileForm.value)
      alert('保存成功！')
    } else {
      // 创建新档案
      const { createStudentProfile } = await import('@/api/profile')
      await createStudentProfile(profileForm.value as any)
      alert('档案创建成功！')
    }
    loadProfile()
  } catch (error: any) {
    const errorMsg = error.response?.data?.detail || '保存失败，请稍后重试'
    alert(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg))
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.student-profile {
  max-width: 1200px;
  margin: 0 auto;
}
</style>


