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
            <!-- 头像上传 -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">头像</label>
              <div class="flex items-center space-x-4">
                <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 flex items-center justify-center">
                  <img
                    v-if="profileForm.avatar_url"
                    :src="profileForm.avatar_url"
                    alt="头像"
                    class="w-full h-full object-cover"
                  />
                  <span v-else class="text-gray-400 text-2xl">头像</span>
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
                    class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    上传头像
                  </button>
                  <p v-if="uploadingAvatar" class="text-sm text-blue-600 mt-2">上传中...</p>
                </div>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">真实姓名 *</label>
                <input
                  v-model="profileForm.real_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">学号</label>
                <input
                  v-model="profileForm.student_id"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">年级</label>
                <input
                  v-model="profileForm.grade"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">专业</label>
                <input
                  v-model="profileForm.major"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">学校</label>
                <select
                  v-model="profileForm.school_id"
                  @change="onSchoolChange"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                >
                  <option value="">请选择学校</option>
                  <option v-if="mySchool" :value="mySchool.id">{{ mySchool.name }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">院系</label>
                <select
                  v-model="profileForm.department_id"
                  :disabled="!profileForm.school_id"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 text-gray-900"
                >
                  <option value="">请选择院系</option>
                  <option v-for="dept in departmentList" :key="dept.id" :value="dept.id">
                    {{ dept.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">联系方式</label>
                <input
                  v-model="profileForm.phone"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入手机号"
                />
              </div>
            </div>
            <div class="mt-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">电子邮箱</label>
              <input
                v-model="profileForm.email"
                type="email"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                placeholder="请输入电子邮箱"
              />
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
.student-profile {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
