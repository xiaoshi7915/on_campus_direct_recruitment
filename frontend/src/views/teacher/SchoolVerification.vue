<template>
  <div class="school-verification w-full max-w-full px-4 py-8">
    <div class="mb-6">
      <h1 class="text-3xl font-bold">学校认证</h1>
      <p class="text-gray-600 mt-2">提交学校认证材料，通过审核后可成为学校管理员（主账号）</p>
    </div>

    <!-- 认证状态提示 -->
    <div v-if="currentVerification" class="mb-6">
      <div
        v-if="currentVerification.status === 'APPROVED'"
        class="bg-green-50 border border-green-200 rounded-lg p-4"
      >
        <div class="flex items-center">
          <svg class="w-6 h-6 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="text-lg font-semibold text-green-800">认证已通过</h3>
            <p class="text-green-600 text-sm mt-1">您的学校认证已通过审核，您已成为学校管理员（主账号）</p>
            <p v-if="currentVerification.reviewed_at" class="text-green-600 text-xs mt-1">
              审核时间：{{ formatDate(currentVerification.reviewed_at) }}
            </p>
          </div>
        </div>
      </div>
      <div
        v-else-if="currentVerification.status === 'PENDING'"
        class="bg-yellow-50 border border-yellow-200 rounded-lg p-4"
      >
        <div class="flex items-center">
          <svg class="w-6 h-6 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="text-lg font-semibold text-yellow-800">审核中</h3>
            <p class="text-yellow-600 text-sm mt-1">您的认证申请正在审核中，请耐心等待</p>
            <p v-if="currentVerification.created_at" class="text-yellow-600 text-xs mt-1">
              提交时间：{{ formatDate(currentVerification.created_at) }}
            </p>
          </div>
        </div>
      </div>
      <div
        v-else-if="currentVerification.status === 'REJECTED'"
        class="bg-red-50 border border-red-200 rounded-lg p-4"
      >
        <div class="flex items-center">
          <svg class="w-6 h-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="text-lg font-semibold text-red-800">认证未通过</h3>
            <p class="text-red-600 text-sm mt-1">您的认证申请未通过审核</p>
            <p v-if="currentVerification.review_comment" class="text-red-600 text-sm mt-2">
              审核意见：{{ currentVerification.review_comment }}
            </p>
            <p v-if="currentVerification.reviewed_at" class="text-red-600 text-xs mt-1">
              审核时间：{{ formatDate(currentVerification.reviewed_at) }}
            </p>
            <button
              @click="showForm = true"
              class="mt-3 btn btn-primary btn-md"
            >
              重新提交
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 认证申请表单 -->
    <div v-if="showForm || !currentVerification" class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-6">提交认证材料</h2>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- 选择学校 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            选择学校 <span class="text-red-500">*</span>
          </label>
          <div class="md:col-span-2">
            <select
              v-model="form.school_id"
              required
              class="select-base w-full"
            >
              <option value="">请选择学校</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">
                {{ school.name }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">请选择您要认证的学校</p>
          </div>
        </div>

        <!-- 学校证明文件 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            学校证明文件
          </label>
          <div class="md:col-span-2">
            <input
              ref="schoolCertificateInput"
              type="file"
              accept="image/*,.pdf"
              @change="handleFileUpload('school_certificate', $event)"
              class="hidden"
            />
            <div class="flex flex-col space-y-2">
              <button
                type="button"
                @click="($refs.schoolCertificateInput as HTMLInputElement)?.click()"
                class="btn btn-outline-secondary btn-md"
              >
                选择文件
              </button>
              <div v-if="form.school_certificate_url" class="flex items-center space-x-3">
                <span class="text-sm text-green-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  已上传
                </span>
                <a :href="form.school_certificate_url" target="_blank" class="text-sm text-blue-600 hover:underline">
                  查看文件
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 教师工作证明 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            教师工作证明
          </label>
          <div class="md:col-span-2">
            <input
              ref="teacherCertificateInput"
              type="file"
              accept="image/*,.pdf"
              @change="handleFileUpload('teacher_certificate', $event)"
              class="hidden"
            />
            <div class="flex flex-col space-y-2">
              <button
                type="button"
                @click="($refs.teacherCertificateInput as HTMLInputElement)?.click()"
                class="btn btn-outline-secondary btn-md"
              >
                选择文件
              </button>
              <div v-if="form.teacher_work_certificate_url" class="flex items-center space-x-3">
                <span class="text-sm text-green-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  已上传
                </span>
                <a :href="form.teacher_work_certificate_url" target="_blank" class="text-sm text-blue-600 hover:underline">
                  查看文件
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 身份证正面 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            身份证正面
          </label>
          <div class="md:col-span-2">
            <input
              ref="idCardFrontInput"
              type="file"
              accept="image/*"
              @change="handleFileUpload('id_card_front', $event)"
              class="hidden"
            />
            <div class="flex flex-col space-y-2">
              <button
                type="button"
                @click="($refs.idCardFrontInput as HTMLInputElement)?.click()"
                class="btn btn-outline-secondary btn-md"
              >
                选择文件
              </button>
              <div v-if="form.teacher_id_card_front_url" class="flex items-center space-x-3">
                <span class="text-sm text-green-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  已上传
                </span>
                <a :href="form.teacher_id_card_front_url" target="_blank" class="text-sm text-blue-600 hover:underline">
                  查看文件
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 身份证反面 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            身份证反面
          </label>
          <div class="md:col-span-2">
            <input
              ref="idCardBackInput"
              type="file"
              accept="image/*"
              @change="handleFileUpload('id_card_back', $event)"
              class="hidden"
            />
            <div class="flex flex-col space-y-2">
              <button
                type="button"
                @click="($refs.idCardBackInput as HTMLInputElement)?.click()"
                class="btn btn-outline-secondary btn-md"
              >
                选择文件
              </button>
              <div v-if="form.teacher_id_card_back_url" class="flex items-center space-x-3">
                <span class="text-sm text-green-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  已上传
                </span>
                <a :href="form.teacher_id_card_back_url" target="_blank" class="text-sm text-blue-600 hover:underline">
                  查看文件
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 授权委托书 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            授权委托书
          </label>
          <div class="md:col-span-2">
            <input
              ref="authorizationLetterInput"
              type="file"
              accept="image/*,.pdf"
              @change="handleFileUpload('authorization_letter', $event)"
              class="hidden"
            />
            <div class="flex flex-col space-y-2">
              <button
                type="button"
                @click="($refs.authorizationLetterInput as HTMLInputElement)?.click()"
                class="btn btn-outline-secondary btn-md"
              >
                选择文件
              </button>
              <div v-if="form.authorization_letter_url" class="flex items-center space-x-3">
                <span class="text-sm text-green-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  已上传
                </span>
                <a :href="form.authorization_letter_url" target="_blank" class="text-sm text-blue-600 hover:underline">
                  查看文件
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 联系信息 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            联系人
          </label>
          <div class="md:col-span-2">
            <input
              v-model="form.contact_person"
              type="text"
              class="input-base w-full"
              placeholder="请输入联系人姓名"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            联系电话
          </label>
          <div class="md:col-span-2">
            <input
              v-model="form.contact_phone"
              type="tel"
              class="input-base w-full"
              placeholder="请输入联系电话"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            联系邮箱
          </label>
          <div class="md:col-span-2">
            <input
              v-model="form.contact_email"
              type="email"
              class="input-base w-full"
              placeholder="请输入联系邮箱"
            />
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="flex justify-end space-x-4 pt-4 border-t">
          <button
            v-if="currentVerification && currentVerification.status !== 'REJECTED'"
            type="button"
            @click="showForm = false"
            class="btn btn-outline-secondary btn-md"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="submitting || !form.school_id"
            class="btn btn-primary btn-md"
          >
            {{ submitting ? '提交中...' : '提交认证' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  createSchoolVerification,
  getSchoolVerifications,
  type SchoolVerification,
  type SchoolVerificationCreateRequest
} from '@/api/verifications'
import { getSchools, type School } from '@/api/schools'
import { uploadDocument } from '@/api/upload'

const currentVerification = ref<SchoolVerification | null>(null)
const showForm = ref(false)
const submitting = ref(false)
const schools = ref<School[]>([])

const form = ref<SchoolVerificationCreateRequest>({
  school_id: '',
  school_certificate_url: undefined,
  teacher_work_certificate_url: undefined,
  teacher_id_card_front_url: undefined,
  teacher_id_card_back_url: undefined,
  authorization_letter_url: undefined,
  other_documents: [],
  contact_person: undefined,
  contact_phone: undefined,
  contact_email: undefined
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

// 加载学校列表
const loadSchools = async () => {
  try {
    // 分批加载，每次最多100条
    const response = await getSchools({ page_size: 100 })
    schools.value = response.items || []
    // 如果总数超过100，继续加载
    if (response.total > 100) {
      const pages = Math.ceil(response.total / 100)
      for (let page = 2; page <= pages; page++) {
        const nextResponse = await getSchools({ page, page_size: 100 })
        schools.value.push(...(nextResponse.items || []))
      }
    }
  } catch (error: any) {
    console.error('加载学校列表失败:', error)
    alert('加载学校列表失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 加载当前认证状态
const loadVerification = async () => {
  try {
    const response = await getSchoolVerifications({ page_size: 1 })
    if (response.items.length > 0) {
      currentVerification.value = response.items[0]
      // 如果状态不是待审核，不显示表单
      if (currentVerification.value.status !== 'PENDING') {
        showForm.value = false
      }
      // 如果已通过，填充学校ID
      if (currentVerification.value.status === 'APPROVED') {
        form.value.school_id = currentVerification.value.school_id
      }
    } else {
      showForm.value = true
    }
  } catch (error: any) {
    console.error('加载认证状态失败:', error)
  }
}

// 处理文件上传
const handleFileUpload = async (field: string, event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  try {
    submitting.value = true
    const response = await uploadDocument(file, 'verification')
    if (response.url) {
      if (field === 'school_certificate') {
        form.value.school_certificate_url = response.url
      } else if (field === 'teacher_certificate') {
        form.value.teacher_work_certificate_url = response.url
      } else if (field === 'id_card_front') {
        form.value.teacher_id_card_front_url = response.url
      } else if (field === 'id_card_back') {
        form.value.teacher_id_card_back_url = response.url
      } else if (field === 'authorization_letter') {
        form.value.authorization_letter_url = response.url
      }
    }
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!form.value.school_id) {
    alert('请选择学校')
    return
  }

  try {
    submitting.value = true
    const response = await createSchoolVerification(form.value)
    currentVerification.value = response
    showForm.value = false
    alert('认证申请提交成功，请等待审核')
  } catch (error: any) {
    alert('提交失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadSchools()
  loadVerification()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

