<template>
  <div class="teacher-profile max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">教师中心</h1>

    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    <div v-else>
      <div v-if="!profile" class="mb-6 p-4 bg-yellow-50 border-2 border-yellow-200 rounded-xl">
        <p class="text-yellow-800 text-sm flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          您还没有创建教师档案，请填写以下信息创建档案。
        </p>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧：教师信息 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-xl shadow-md p-8 border border-gray-100">
          <h2 class="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            教师信息
          </h2>
          <form @submit.prevent="saveProfile">
            <!-- 头像上传 -->
            <div class="mb-6">
              <label class="block text-sm font-semibold text-gray-700 mb-2">头像</label>
              <div class="flex items-center space-x-4">
                <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-100 flex items-center justify-center border-2 border-gray-200 shadow-sm">
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
                    class="px-5 py-2.5 bg-blue-50 text-blue-700 rounded-xl hover:bg-blue-100 transition-colors duration-200 font-medium"
                  >
                    上传头像
                  </button>
                  <p v-if="uploadingAvatar" class="text-sm text-blue-600 mt-2 flex items-center">
                    <svg class="animate-spin h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24">
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
                <label class="block text-sm font-semibold text-gray-700 mb-2">姓名 *</label>
                <input
                  v-model="profileForm.real_name"
                  type="text"
                  required
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">职称</label>
                <input
                  v-model="profileForm.title"
                  type="text"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="例如：教授、副教授"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">职务名称</label>
                <input
                  v-model="profileForm.position"
                  type="text"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="例如：系主任、副院长"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">授课专业</label>
                <input
                  v-model="profileForm.teaching_major"
                  type="text"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="例如：计算机科学与技术"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">授课年级</label>
                <input
                  v-model="profileForm.teaching_grade"
                  type="text"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="例如：2021级、2022级"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">学校名称</label>
                <select
                  v-model="profileForm.school_id"
                  @change="onSchoolChange"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                >
                  <option value="">请选择学校</option>
                  <option v-if="mySchool" :value="mySchool.id">{{ mySchool.name }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">院系名称</label>
                <select
                  v-model="profileForm.department_id"
                  :disabled="!profileForm.school_id"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 disabled:bg-gray-100"
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
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入联系方式"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">电子邮箱</label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入电子邮箱"
                />
              </div>
            </div>
            <div class="mt-6 flex justify-end">
              <button
                type="submit"
                class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                保存
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- 右侧：统计信息 -->
      <div class="space-y-6">
        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            统计信息
          </h2>
          <div class="space-y-4">
            <div class="flex items-center justify-between p-3 bg-blue-50 rounded-lg border border-blue-100">
              <div class="flex items-center">
                <svg class="w-6 h-6 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <div class="text-gray-700 text-base">管辖学生数</div>
              </div>
              <div class="text-3xl font-bold text-blue-600">{{ studentCount }}</div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { getTeacherProfile, updateTeacherProfile, createTeacherProfile, type TeacherProfile } from '@/api/profile'
import { uploadImage } from '@/api/upload'
import { getStudents } from '@/api/students'
import { getMySchool, type School } from '@/api/schools'
import { getDepartments, type Department } from '@/api/departments'

// 档案数据
const profile = ref<TeacherProfile | null>(null)
const loading = ref(false)

// 表单数据
const profileForm = ref({
  real_name: '',
  title: '',
  position: '',
  teaching_major: '',
  teaching_grade: '',
  phone: '',
  email: '',
  school_id: '',
  department_id: '',
  avatar_url: '',
})

// 头像上传
const avatarInput = ref<HTMLInputElement | null>(null)
const uploadingAvatar = ref(false)

// 学校院系列表
const schoolList = ref<School[]>([])
const departmentList = ref<Department[]>([])
const mySchool = ref<School | null>(null)

// 统计数据
const studentCount = ref(0)

// 加载档案数据
const loadProfile = async () => {
  loading.value = true
  try {
    profile.value = await getTeacherProfile()
    if (profile.value) {
      profileForm.value = {
        real_name: profile.value.real_name || '',
        title: profile.value.title || '',
        position: profile.value.position || '',
        teaching_major: profile.value.teaching_major || '',
        teaching_grade: profile.value.teaching_grade || '',
        phone: profile.value.phone || '',
        email: profile.value.email || '',
        school_id: profile.value.school_id || '',
        department_id: profile.value.department_id || '',
        avatar_url: profile.value.avatar_url || '',
      }
      // 如果已有学校ID，加载院系列表
      if (profile.value.school_id) {
        await loadDepartments(profile.value.school_id)
      }
    }
    
    // 加载学校信息（教师只能看到自己所属的学校）
    await loadSchool()

    // 加载统计数据
    try {
      const studentsRes = await getStudents({ page_size: 1 })
      studentCount.value = studentsRes.total
    } catch {
      studentCount.value = 0
    }
  } catch (error: any) {
    console.error('加载档案失败:', error)
    // 如果档案不存在（404），允许创建
    if (error.response?.status === 404) {
      // 档案不存在，显示提示但不阻止用户填写表单
    } else {
      alert('加载档案失败: ' + (error.response?.data?.detail || error.message))
    }
  } finally {
    loading.value = false
  }
}

// 加载学校信息
const loadSchool = async () => {
  try {
    mySchool.value = await getMySchool()
  } catch (error: any) {
    console.error('加载学校信息失败:', error)
    // 如果学校不存在，不影响其他功能
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
    alert('头像上传成功！')
  } catch (error: any) {
    alert('头像上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploadingAvatar.value = false
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

// 保存档案
const saveProfile = async () => {
  try {
    if (profile.value) {
      // 如果档案存在，更新
      await updateTeacherProfile(profileForm.value)
      alert('保存成功！')
    } else {
      // 如果档案不存在，创建
      await createTeacherProfile(profileForm.value)
      alert('创建成功！')
    }
    loadProfile()
  } catch (error: any) {
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

