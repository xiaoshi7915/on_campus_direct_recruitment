<template>
  <div class="teacher-profile">
    <h1 class="text-3xl font-bold mb-6">教师中心</h1>

    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else>
      <div v-if="!profile" class="mb-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p class="text-yellow-800">您还没有创建教师档案，请填写以下信息创建档案。</p>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧：教师信息 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">教师信息</h2>
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
                <label class="block text-sm font-medium text-gray-700 mb-2">姓名 *</label>
                <input
                  v-model="profileForm.real_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">职称</label>
                <input
                  v-model="profileForm.title"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="例如：教授、副教授"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">职务名称</label>
                <input
                  v-model="profileForm.position"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="例如：系主任、副院长"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">授课专业</label>
                <input
                  v-model="profileForm.teaching_major"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="例如：计算机科学与技术"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">授课年级</label>
                <input
                  v-model="profileForm.teaching_grade"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="例如：2021级、2022级"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">学校名称</label>
                <select
                  v-model="profileForm.school_id"
                  @change="onSchoolChange"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">请选择学校</option>
                  <option v-if="mySchool" :value="mySchool.id">{{ mySchool.name }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">院系名称</label>
                <select
                  v-model="profileForm.department_id"
                  :disabled="!profileForm.school_id"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
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
                  placeholder="请输入联系方式"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">电子邮箱</label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入电子邮箱"
                />
              </div>
            </div>
            <div class="mt-6 flex justify-end">
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

      <!-- 右侧：统计信息 -->
      <div class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">统计信息</h2>
          <div class="space-y-4">
            <div>
              <div class="text-gray-600 text-sm">管辖学生数</div>
              <div class="text-2xl font-bold text-blue-600">{{ studentCount }}</div>
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
.teacher-profile {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

