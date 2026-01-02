<template>
  <div class="admin-verifications w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8 flex items-center">
      <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      </svg>
      认证审核
    </h1>

    <!-- 标签页 -->
    <div class="mb-6 border-b border-gray-200">
      <nav class="-mb-px flex space-x-8">
        <button
          @click="activeTab = 'enterprise'"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
            activeTab === 'enterprise'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          企业认证
          <span v-if="enterprisePendingCount > 0" class="ml-2 px-2 py-0.5 text-xs bg-red-500 text-white rounded-full">
            {{ enterprisePendingCount }}
          </span>
        </button>
        <button
          @click="activeTab = 'personal'"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
            activeTab === 'personal'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          个人身份认证
          <span v-if="personalPendingCount > 0" class="ml-2 px-2 py-0.5 text-xs bg-red-500 text-white rounded-full">
            {{ personalPendingCount }}
          </span>
        </button>
        <button
          @click="activeTab = 'school'"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
            activeTab === 'school'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          学校认证
          <span v-if="schoolPendingCount > 0" class="ml-2 px-2 py-0.5 text-xs bg-red-500 text-white rounded-full">
            {{ schoolPendingCount }}
          </span>
        </button>
      </nav>
    </div>

    <!-- 企业认证列表 -->
    <div v-if="activeTab === 'enterprise'" class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div v-if="loadingEnterprise" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="enterpriseVerifications.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-lg">暂无企业认证申请</p>
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">企业名称</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">申请时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="verification in enterpriseVerifications" :key="verification.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ getEnterpriseName(verification.enterprise_id) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                {{ formatDate(verification.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    verification.status === 'APPROVED' ? 'bg-green-100 text-green-800' :
                    verification.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]"
                >
                  {{ getStatusText(verification.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="viewEnterpriseVerification(verification.id)"
                  class="btn btn-primary btn-sm mr-2"
                >
                  查看详情
                </button>
                <button
                  v-if="verification.status === 'PENDING'"
                  @click="reviewEnterpriseVerification(verification.id)"
                  class="btn btn-success btn-sm"
                >
                  审核
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 个人身份认证列表 -->
    <div v-if="activeTab === 'personal'" class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div v-if="loadingPersonal" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="personalVerifications.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-lg">暂无个人身份认证申请</p>
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">用户</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">真实姓名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">申请时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="verification in personalVerifications" :key="verification.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ getUserName(verification.user_id) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                {{ verification.real_name || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                {{ formatDate(verification.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    verification.status === 'APPROVED' ? 'bg-green-100 text-green-800' :
                    verification.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]"
                >
                  {{ getStatusText(verification.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="viewPersonalVerification(verification.id)"
                  class="btn btn-primary btn-sm mr-2"
                >
                  查看详情
                </button>
                <button
                  v-if="verification.status === 'PENDING'"
                  @click="reviewPersonalVerification(verification.id)"
                  class="btn btn-success btn-sm"
                >
                  审核
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 学校认证列表 -->
    <div v-if="activeTab === 'school'" class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div v-if="loadingSchool" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="schoolVerifications.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-lg">暂无学校认证申请</p>
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学校</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">教师</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">申请时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="verification in schoolVerifications" :key="verification.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ getSchoolName(verification.school_id) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                {{ getTeacherName(verification.teacher_id) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                {{ formatDate(verification.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    verification.status === 'APPROVED' ? 'bg-green-100 text-green-800' :
                    verification.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]"
                >
                  {{ getStatusText(verification.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="viewSchoolVerification(verification.id)"
                  class="btn btn-primary btn-sm mr-2"
                >
                  查看详情
                </button>
                <button
                  v-if="verification.status === 'PENDING'"
                  @click="reviewSchoolVerification(verification.id)"
                  class="btn btn-success btn-sm"
                >
                  审核
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 审核对话框 -->
    <div v-if="showReviewModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="closeReviewModal">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-2/3 lg:w-1/2 shadow-lg rounded-xl bg-white">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold text-gray-900">审核认证申请</h3>
          <button @click="closeReviewModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div v-if="reviewingVerification" class="space-y-4">
          <!-- 显示认证详情 -->
          <div class="bg-gray-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-2">认证材料</h4>
            <div class="space-y-2 text-sm text-gray-600">
              <!-- 企业认证材料 -->
              <template v-if="reviewType === 'enterprise'">
                <div v-if="(reviewingVerification as EnterpriseVerification).business_license_url">
                  <span class="font-medium">营业执照：</span>
                  <a :href="(reviewingVerification as EnterpriseVerification).business_license_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as EnterpriseVerification).legal_person_id_front_url">
                  <span class="font-medium">法人身份证正面：</span>
                  <a :href="(reviewingVerification as EnterpriseVerification).legal_person_id_front_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as EnterpriseVerification).legal_person_id_back_url">
                  <span class="font-medium">法人身份证反面：</span>
                  <a :href="(reviewingVerification as EnterpriseVerification).legal_person_id_back_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as EnterpriseVerification).authorization_letter_url">
                  <span class="font-medium">授权委托书：</span>
                  <a :href="(reviewingVerification as EnterpriseVerification).authorization_letter_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
              </template>
              <!-- 个人身份认证材料 -->
              <template v-else-if="reviewType === 'personal'">
                <div v-if="(reviewingVerification as PersonalVerification).id_card_front_url">
                  <span class="font-medium">身份证正面：</span>
                  <a :href="(reviewingVerification as PersonalVerification).id_card_front_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as PersonalVerification).id_card_back_url">
                  <span class="font-medium">身份证反面：</span>
                  <a :href="(reviewingVerification as PersonalVerification).id_card_back_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as PersonalVerification).real_name">
                  <span class="font-medium">真实姓名：</span>
                  <span class="ml-2">{{ (reviewingVerification as PersonalVerification).real_name }}</span>
                </div>
                <div v-if="(reviewingVerification as PersonalVerification).id_card_number">
                  <span class="font-medium">身份证号：</span>
                  <span class="ml-2">{{ (reviewingVerification as PersonalVerification).id_card_number }}</span>
                </div>
              </template>
              <!-- 学校认证材料 -->
              <template v-else-if="reviewType === 'school'">
                <div v-if="(reviewingVerification as SchoolVerification).school_certificate_url">
                  <span class="font-medium">学校证明文件：</span>
                  <a :href="(reviewingVerification as SchoolVerification).school_certificate_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as SchoolVerification).teacher_work_certificate_url">
                  <span class="font-medium">教师工作证明：</span>
                  <a :href="(reviewingVerification as SchoolVerification).teacher_work_certificate_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as SchoolVerification).teacher_id_card_front_url">
                  <span class="font-medium">身份证正面：</span>
                  <a :href="(reviewingVerification as SchoolVerification).teacher_id_card_front_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as SchoolVerification).teacher_id_card_back_url">
                  <span class="font-medium">身份证反面：</span>
                  <a :href="(reviewingVerification as SchoolVerification).teacher_id_card_back_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as SchoolVerification).authorization_letter_url">
                  <span class="font-medium">授权委托书：</span>
                  <a :href="(reviewingVerification as SchoolVerification).authorization_letter_url" target="_blank" class="text-blue-600 hover:underline ml-2">
                    查看文件
                  </a>
                </div>
                <div v-if="(reviewingVerification as SchoolVerification).contact_person">
                  <span class="font-medium">联系人：</span>
                  <span class="ml-2">{{ (reviewingVerification as SchoolVerification).contact_person }}</span>
                </div>
                <div v-if="(reviewingVerification as SchoolVerification).contact_phone">
                  <span class="font-medium">联系电话：</span>
                  <span class="ml-2">{{ (reviewingVerification as SchoolVerification).contact_phone }}</span>
                </div>
                <div v-if="(reviewingVerification as SchoolVerification).contact_email">
                  <span class="font-medium">联系邮箱：</span>
                  <span class="ml-2">{{ (reviewingVerification as SchoolVerification).contact_email }}</span>
                </div>
              </template>
            </div>
          </div>

          <!-- 审核意见 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">审核意见</label>
            <textarea
              v-model="reviewComment"
              rows="4"
              class="textarea-base w-full"
              placeholder="请输入审核意见（可选）"
            ></textarea>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-end space-x-4 pt-4 border-t">
            <button @click="closeReviewModal" class="btn btn-outline-secondary btn-md">
              取消
            </button>
            <button @click="submitReview('REJECTED')" class="btn btn-danger btn-md">
              拒绝
            </button>
            <button @click="submitReview('APPROVED')" class="btn btn-success btn-md">
              通过
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {
  getEnterpriseVerifications,
  updateEnterpriseVerification,
  type EnterpriseVerification
} from '@/api/verifications'
import {
  getPersonalVerifications,
  updatePersonalVerification,
  type PersonalVerification
} from '@/api/verifications'
import {
  getSchoolVerifications,
  updateSchoolVerification,
  type SchoolVerification
} from '@/api/verifications'
import { getUsers, type User } from '@/api/users'
import { getSchools, type School } from '@/api/schools'
import { getTeacherProfile } from '@/api/profile'

const activeTab = ref<'enterprise' | 'personal' | 'school'>('enterprise')
const loadingEnterprise = ref(false)
const loadingPersonal = ref(false)
const loadingSchool = ref(false)

const enterpriseVerifications = ref<EnterpriseVerification[]>([])
const personalVerifications = ref<PersonalVerification[]>([])
const schoolVerifications = ref<SchoolVerification[]>([])

const showReviewModal = ref(false)
const reviewingVerification = ref<EnterpriseVerification | PersonalVerification | SchoolVerification | null>(null)
const reviewComment = ref('')
const reviewType = ref<'enterprise' | 'personal' | 'school'>('enterprise')

// 用户、学校、教师、企业信息缓存
const usersCache = ref<Map<string, User>>(new Map())
const schoolsCache = ref<Map<string, School>>(new Map())
const teachersCache = ref<Map<string, any>>(new Map())
const enterprisesCache = ref<Map<string, any>>(new Map())

// 显示名称的响应式数据
const enterpriseNames = ref<Map<string, string>>(new Map())
const userNames = ref<Map<string, string>>(new Map())
const schoolNames = ref<Map<string, string>>(new Map())
const teacherNames = ref<Map<string, string>>(new Map())

// 待审核数量
const enterprisePendingCount = computed(() => {
  return enterpriseVerifications.value.filter(v => v.status === 'PENDING').length
})

const personalPendingCount = computed(() => {
  return personalVerifications.value.filter(v => v.status === 'PENDING').length
})

const schoolPendingCount = computed(() => {
  return schoolVerifications.value.filter(v => v.status === 'PENDING').length
})

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'PENDING': '待审核',
    'APPROVED': '已通过',
    'REJECTED': '已拒绝'
  }
  return statusMap[status] || status
}

// 获取企业名称
const getEnterpriseName = (enterpriseId: string) => {
  return enterpriseNames.value.get(enterpriseId) || `企业ID: ${enterpriseId}`
}

// 获取用户名
const getUserName = (userId: string) => {
  return userNames.value.get(userId) || userId
}

// 获取学校名称
const getSchoolName = (schoolId: string) => {
  return schoolNames.value.get(schoolId) || schoolId
}

// 获取教师名称
const getTeacherName = (teacherId: string) => {
  return teacherNames.value.get(teacherId) || teacherId
}

// 加载企业名称（从后端返回的数据中获取）
const loadEnterpriseNames = async () => {
  enterpriseVerifications.value.forEach(v => {
    if (v.enterprise_name && !enterpriseNames.value.has(v.enterprise_id)) {
      enterpriseNames.value.set(v.enterprise_id, v.enterprise_name)
    }
  })
}

// 加载用户名称
const loadUserNames = async () => {
  const userIds = new Set<string>()
  personalVerifications.value.forEach(v => userIds.add(v.user_id))
  
  if (userIds.size > 0) {
    try {
      const users = await getUsers({ page_size: 1000 })
      users.items.forEach(user => {
        userNames.value.set(user.id, user.username)
        usersCache.value.set(user.id, user)
      })
    } catch {
      // 如果获取失败，忽略
    }
  }
}

// 加载学校名称
const loadSchoolNames = async () => {
  const schoolIds = new Set<string>()
  schoolVerifications.value.forEach(v => schoolIds.add(v.school_id))
  
  if (schoolIds.size > 0) {
    try {
      const schools = await getSchools({ page_size: 1000 })
      schools.items.forEach(school => {
        schoolNames.value.set(school.id, school.name)
        schoolsCache.value.set(school.id, school)
      })
    } catch {
      // 如果获取失败，忽略
    }
  }
}

// 加载教师名称（从后端返回的数据中获取）
const loadTeacherNames = async () => {
  schoolVerifications.value.forEach(v => {
    if (v.teacher_name && !teacherNames.value.has(v.teacher_id)) {
      teacherNames.value.set(v.teacher_id, v.teacher_name)
    }
  })
}

// 加载企业认证列表
const loadEnterpriseVerifications = async () => {
  loadingEnterprise.value = true
  try {
    const response = await getEnterpriseVerifications({ page_size: 100 })
    enterpriseVerifications.value = response.items
    await loadEnterpriseNames()
  } catch (error: any) {
    console.error('加载企业认证列表失败:', error)
    alert('加载企业认证列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loadingEnterprise.value = false
  }
}

// 加载个人身份认证列表
const loadPersonalVerifications = async () => {
  loadingPersonal.value = true
  try {
    const response = await getPersonalVerifications({ page_size: 100 })
    personalVerifications.value = response.items
    await loadUserNames()
  } catch (error: any) {
    console.error('加载个人身份认证列表失败:', error)
    alert('加载个人身份认证列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loadingPersonal.value = false
  }
}

// 加载学校认证列表
const loadSchoolVerifications = async () => {
  loadingSchool.value = true
  try {
    const response = await getSchoolVerifications({ page_size: 100 })
    schoolVerifications.value = response.items
    await Promise.all([loadSchoolNames(), loadTeacherNames()])
  } catch (error: any) {
    console.error('加载学校认证列表失败:', error)
    alert('加载学校认证列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loadingSchool.value = false
  }
}

// 查看企业认证详情
const viewEnterpriseVerification = async (id: string) => {
  const verification = enterpriseVerifications.value.find(v => v.id === id)
  if (verification) {
    reviewingVerification.value = verification
    reviewType.value = 'enterprise'
    showReviewModal.value = true
  }
}

// 查看个人身份认证详情
const viewPersonalVerification = async (id: string) => {
  const verification = personalVerifications.value.find(v => v.id === id)
  if (verification) {
    reviewingVerification.value = verification
    reviewType.value = 'personal'
    showReviewModal.value = true
  }
}

// 查看学校认证详情
const viewSchoolVerification = async (id: string) => {
  const verification = schoolVerifications.value.find(v => v.id === id)
  if (verification) {
    reviewingVerification.value = verification
    reviewType.value = 'school'
    showReviewModal.value = true
  }
}

// 审核企业认证
const reviewEnterpriseVerification = async (id: string) => {
  await viewEnterpriseVerification(id)
}

// 审核个人身份认证
const reviewPersonalVerification = async (id: string) => {
  await viewPersonalVerification(id)
}

// 审核学校认证
const reviewSchoolVerification = async (id: string) => {
  await viewSchoolVerification(id)
}

// 关闭审核对话框
const closeReviewModal = () => {
  showReviewModal.value = false
  reviewingVerification.value = null
  reviewComment.value = ''
}

// 提交审核
const submitReview = async (status: 'APPROVED' | 'REJECTED') => {
  if (!reviewingVerification.value) return

  try {
    if (reviewType.value === 'enterprise') {
      await updateEnterpriseVerification(reviewingVerification.value.id, {
        status,
        review_comment: reviewComment.value || undefined
      })
      await loadEnterpriseVerifications()
    } else if (reviewType.value === 'personal') {
      await updatePersonalVerification(reviewingVerification.value.id, {
        status,
        review_comment: reviewComment.value || undefined
      })
      await loadPersonalVerifications()
    } else if (reviewType.value === 'school') {
      await updateSchoolVerification(reviewingVerification.value.id, {
        status,
        review_comment: reviewComment.value || undefined
      })
      await loadSchoolVerifications()
    }
    
    alert('审核成功！')
    closeReviewModal()
  } catch (error: any) {
    alert('审核失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 监听标签页切换
const watchTab = () => {
  if (activeTab.value === 'enterprise' && enterpriseVerifications.value.length === 0) {
    loadEnterpriseVerifications()
  } else if (activeTab.value === 'personal' && personalVerifications.value.length === 0) {
    loadPersonalVerifications()
  } else if (activeTab.value === 'school' && schoolVerifications.value.length === 0) {
    loadSchoolVerifications()
  }
}

onMounted(() => {
  loadEnterpriseVerifications()
  loadPersonalVerifications()
  loadSchoolVerifications()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

