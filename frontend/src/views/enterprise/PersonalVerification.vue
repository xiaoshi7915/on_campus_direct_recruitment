<template>
  <div class="personal-verification">
    <div class="mb-6">
      <h1 class="text-3xl font-bold">个人身份认证</h1>
      <p class="text-gray-600 mt-2">提交个人身份认证材料，通过审核后可获得认证标识</p>
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
            <p class="text-green-600 text-sm mt-1">您的个人身份认证已通过审核</p>
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
              class="mt-3 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
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
        <!-- 真实姓名 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            真实姓名 <span class="text-red-500">*</span>
          </label>
          <div class="md:col-span-2">
            <input
              v-model="form.real_name"
              type="text"
              required
              maxlength="50"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入真实姓名"
            />
          </div>
        </div>

        <!-- 身份证号 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            身份证号 <span class="text-red-500">*</span>
          </label>
          <div class="md:col-span-2">
            <input
              v-model="form.id_card_number"
              type="text"
              required
              maxlength="18"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="请输入18位身份证号"
            />
          </div>
        </div>

        <!-- 身份证正面 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            身份证正面 <span class="text-red-500">*</span>
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
                @click="$refs.idCardFrontInput.click()"
                class="w-full md:w-auto px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-left"
              >
                选择文件
              </button>
              <div v-if="form.id_card_front_url" class="flex items-center space-x-3">
                <span class="text-sm text-green-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  已上传
                </span>
                <a
                  :href="form.id_card_front_url"
                  target="_blank"
                  class="text-sm text-blue-600 hover:underline"
                >
                  查看文件
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 身份证反面 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            身份证反面 <span class="text-red-500">*</span>
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
                @click="$refs.idCardBackInput.click()"
                class="w-full md:w-auto px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-left"
              >
                选择文件
              </button>
              <div v-if="form.id_card_back_url" class="flex items-center space-x-3">
                <span class="text-sm text-green-600 flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  已上传
                </span>
                <a
                  :href="form.id_card_back_url"
                  target="_blank"
                  class="text-sm text-blue-600 hover:underline"
                >
                  查看文件
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 其他材料 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          <label class="md:col-span-1 text-sm font-medium text-gray-700 pt-2">
            其他材料
          </label>
          <div class="md:col-span-2">
            <div class="space-y-3">
              <div
                v-for="(doc, index) in otherDocuments"
                :key="index"
                class="flex items-center justify-between p-2 bg-gray-50 rounded-lg"
              >
                <a :href="doc" target="_blank" class="text-sm text-blue-600 hover:underline flex-1">
                  材料 {{ index + 1 }}
                </a>
                <button
                  type="button"
                  @click="removeOtherDocument(index)"
                  class="text-sm text-red-600 hover:text-red-800 px-2"
                >
                  删除
                </button>
              </div>
              <input
                ref="otherDocumentsInput"
                type="file"
                accept="image/*,.pdf"
                @change="handleOtherDocumentUpload"
                class="hidden"
              />
              <button
                type="button"
                @click="$refs.otherDocumentsInput.click()"
                class="w-full md:w-auto px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-left"
              >
                添加其他材料
              </button>
            </div>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="flex justify-end space-x-4 pt-4 border-t">
          <button
            v-if="currentVerification && currentVerification.status !== 'REJECTED'"
            type="button"
            @click="showForm = false"
            class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="submitting || !form.real_name || !form.id_card_number || !form.id_card_front_url || !form.id_card_back_url"
            class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
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
  createPersonalVerification,
  getPersonalVerifications,
  type PersonalVerification,
  type PersonalVerificationCreateRequest
} from '@/api/verifications'
import { uploadDocument } from '@/api/upload'

const currentVerification = ref<PersonalVerification | null>(null)
const showForm = ref(false)
const submitting = ref(false)
const otherDocuments = ref<string[]>([])

const form = ref<PersonalVerificationCreateRequest>({
  real_name: undefined,
  id_card_number: undefined,
  id_card_front_url: undefined,
  id_card_back_url: undefined,
  other_documents: []
})

// 加载当前认证状态
const loadVerification = async () => {
  try {
    const response = await getPersonalVerifications({ page_size: 1 })
    if (response.items.length > 0) {
      currentVerification.value = response.items[0]
      // 如果状态不是待审核，不显示表单
      if (currentVerification.value.status !== 'PENDING') {
        showForm.value = false
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
      if (field === 'id_card_front') {
        form.value.id_card_front_url = response.url
      } else if (field === 'id_card_back') {
        form.value.id_card_back_url = response.url
      }
    }
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 处理其他材料上传
const handleOtherDocumentUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  try {
    submitting.value = true
    const response = await uploadDocument(file, 'verification')
    if (response.url) {
      otherDocuments.value.push(response.url)
      form.value.other_documents = otherDocuments.value
    }
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
    // 清空input，允许重复上传同一文件
    if (target) {
      target.value = ''
    }
  }
}

// 删除其他材料
const removeOtherDocument = (index: number) => {
  otherDocuments.value.splice(index, 1)
  form.value.other_documents = otherDocuments.value
}

// 提交认证申请
const handleSubmit = async () => {
  if (!form.value.real_name || !form.value.id_card_number || !form.value.id_card_front_url || !form.value.id_card_back_url) {
    alert('请填写必填信息并上传必填材料')
    return
  }

  submitting.value = true
  try {
    await createPersonalVerification(form.value)
    alert('认证申请已提交，请等待审核')
    showForm.value = false
    await loadVerification()
  } catch (error: any) {
    alert('提交失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadVerification()
})
</script>

