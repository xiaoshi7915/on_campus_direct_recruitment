<template>
  <div class="student-profile max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">个人中心</h1>

    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧：个人信息 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-xl shadow-md p-8 border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            基本信息
          </h2>
          <div v-if="!profile" class="mb-6 p-4 bg-yellow-50 border-2 border-yellow-200 rounded-xl">
            <p class="text-yellow-800 text-sm flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              您还没有创建学生档案，请填写下方信息创建档案
            </p>
          </div>
          <form @submit.prevent="saveProfile" class="space-y-6">
            <!-- 头像上传 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-3">头像</label>
              <div class="flex items-center space-x-6">
                <div class="w-28 h-28 rounded-full overflow-hidden bg-gray-100 border-4 border-gray-200 flex items-center justify-center shadow-md">
                  <img
                    v-if="profileForm.avatar_url"
                    :src="profileForm.avatar_url"
                    alt="头像"
                    class="w-full h-full object-cover"
                  />
                  <svg v-else class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <input
                    type="file"
                    ref="avatarInput"
                    @change="handleAvatarSelect"
                    accept="image/*"
                    class="hidden"
                  />
                  <button
                    type="button"
                    @click="avatarInput?.click()"
                    class="px-5 py-2.5 border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium flex items-center"
                  >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    上传头像
                  </button>
                  <p v-if="uploadingAvatar" class="text-sm text-blue-600 mt-2 flex items-center">
                    <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    上传中...
                  </p>
                </div>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">真实姓名 *</label>
                <input
                  v-model="profileForm.real_name"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">学号</label>
                <input
                  v-model="profileForm.student_id"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">年级</label>
                <input
                  v-model="profileForm.grade"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">专业</label>
                <input
                  v-model="profileForm.major"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">学校</label>
                <select
                  v-model="profileForm.school_id"
                  @change="onSchoolChange"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                >
                  <option value="">请选择学校</option>
                  <option v-if="mySchool" :value="mySchool.id">{{ mySchool.name }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">院系</label>
                <select
                  v-model="profileForm.department_id"
                  :disabled="!profileForm.school_id"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed text-gray-900 transition-all duration-200"
                >
                  <option value="">请选择院系</option>
                  <option v-for="dept in departmentList" :key="dept.id" :value="dept.id">
                    {{ dept.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">联系方式</label>
                <input
                  v-model="profileForm.phone"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入手机号"
                />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">电子邮箱</label>
              <input
                v-model="profileForm.email"
                type="email"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                placeholder="请输入电子邮箱"
              />
            </div>
            <div class="pt-4 border-t border-gray-200 flex justify-end">
              <button
                type="submit"
                class="px-8 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ profile ? '保存' : '创建档案' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- 右侧：统计信息 -->
      <div class="space-y-6">
        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
            <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            统计信息
          </h2>
          <div class="space-y-6">
            <div class="p-4 bg-blue-50 rounded-xl border border-blue-100">
              <div class="text-gray-600 text-sm mb-1 flex items-center">
                <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                我的简历
              </div>
              <div class="text-3xl font-bold text-blue-600">{{ resumeCount }}</div>
            </div>
            <div class="p-4 bg-green-50 rounded-xl border border-green-100">
              <div class="text-gray-600 text-sm mb-1 flex items-center">
                <svg class="w-4 h-4 mr-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                我的申请
              </div>
              <div class="text-3xl font-bold text-green-600">{{ applicationCount }}</div>
            </div>
            <div class="p-4 bg-orange-50 rounded-xl border border-orange-100">
              <div class="text-gray-600 text-sm mb-1 flex items-center">
                <svg class="w-4 h-4 mr-1 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                待面试
              </div>
              <div class="text-3xl font-bold text-orange-600">{{ interviewCount }}</div>
            </div>
            <div class="p-4 bg-purple-50 rounded-xl border border-purple-100">
              <div class="text-gray-600 text-sm mb-1 flex items-center">
                <svg class="w-4 h-4 mr-1 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                收藏职位
              </div>
              <div class="text-3xl font-bold text-purple-600">{{ favoriteCount }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getStudentProfile, updateStudentProfile, createStudentProfile, type StudentProfile } from '@/api/profile'
import { uploadImage } from '@/api/upload'
import { getResumes } from '@/api/resumes'
import { getApplications } from '@/api/applications'
import { getInterviews } from '@/api/interviews'
import { getFavorites } from '@/api/favorites'
import type { School } from '@/api/schools'
import { getDepartments, type Department } from '@/api/departments'

// 档案数据
const profile = ref<StudentProfile | null>(null)
const loading = ref(false)

// 表单数据
const profileForm = ref({
  real_name: '',
  student_id: '',
  grade: '',
  major: '',
  school_id: '',
  department_id: '',
  phone: '',
  email: '',
  avatar_url: '',
})

// 学校院系列表
const mySchool = ref<School | null>(null)
const departmentList = ref<Department[]>([])

// 头像上传
const avatarInput = ref<HTMLInputElement | null>(null)
const uploadingAvatar = ref(false)

// 统计数据
const resumeCount = ref(0)
const applicationCount = ref(0)
const interviewCount = ref(0)
const favoriteCount = ref(0)

// 加载学校信息
const loadSchool = async (schoolId?: string) => {
  try {
    // 如果学生已经有school_id，使用profile中的学校信息
    if (schoolId && profile.value?.school_name) {
      // 如果profile中有school_name，创建一个临时的school对象用于显示
      mySchool.value = {
        id: schoolId,
        name: profile.value.school_name,
        code: '',
        province: '',
        city: '',
        address: '',
        website: '',
        logo_url: '',
        description: '',
        is_verified: false,
        created_at: '',
        updated_at: ''
      }
    } else {
      // 学生没有权限调用getMySchool API（该API仅限教师），直接设为null
      mySchool.value = null
    }
  } catch (error: any) {
    console.error('加载学校信息失败:', error)
    mySchool.value = null
  }
}

// 加载院系列表
const loadDepartments = async (schoolId: string) => {
  if (!schoolId) {
    departmentList.value = []
    return
  }
  try {
    const response = await getDepartments({ school_id: schoolId, page_size: 100 })
    departmentList.value = response.items
  } catch (error: any) {
    console.error('加载院系列表失败:', error)
    departmentList.value = []
  }
}

// 学校选择变化时加载院系列表
const onSchoolChange = () => {
  profileForm.value.department_id = '' // 清空院系选择
  if (profileForm.value.school_id) {
    loadDepartments(profileForm.value.school_id)
  } else {
    departmentList.value = []
  }
}

// 选择头像文件
const handleAvatarSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  
  uploadingAvatar.value = true
  
  try {
    // 上传头像
    const response = await uploadImage(file, 'avatar')
    profileForm.value.avatar_url = response.url
    // 上传成功后立即保存profile
    if (profile.value) {
      await updateStudentProfile({ avatar_url: response.url })
      alert('头像上传成功！')
      // 重新加载profile以更新显示
      await loadProfile()
    } else {
      alert('头像上传成功！请保存档案以应用更改。')
    }
  } catch (error: any) {
    alert('头像上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploadingAvatar.value = false
    // 清空input，允许重复选择同一文件
    if (target) {
      target.value = ''
    }
  }
}

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
        school_id: profile.value.school_id || '',
        department_id: profile.value.department_id || '',
        phone: profile.value.phone || '',
        email: profile.value.email || '',
        avatar_url: profile.value.avatar_url || '',
      }
      
      // 如果已有学校ID，加载学校信息和院系列表
      if (profile.value.school_id) {
        await loadSchool(profile.value.school_id)
        await loadDepartments(profile.value.school_id)
      } else {
        // 如果没有学校，尝试获取学生可能所属的学校（如果有API）
        await loadSchool()
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
/* 样式已内联到模板中 */
</style>
