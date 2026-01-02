<template>
  <div class="enterprise-profile w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">企业中心</h1>

    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    <div v-else>
      <div v-if="!profile" class="mb-6 bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4">
        <p class="text-yellow-800 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          您还没有创建企业档案，请填写以下信息创建档案。
        </p>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧：企业信息 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-xl shadow-md p-8 border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            企业信息
          </h2>
          <form @submit.prevent="saveProfile" class="space-y-6">
            <!-- Logo上传 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-3">企业Logo</label>
              <div class="flex items-center space-x-6">
                <div class="w-28 h-28 rounded-xl overflow-hidden bg-gray-100 border-4 border-gray-200 flex items-center justify-center shadow-md">
                  <img
                    v-if="profileForm.logo_url"
                    :src="profileForm.logo_url"
                    alt="Logo"
                    class="w-full h-full object-cover"
                  />
                  <svg v-else class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div class="flex-1">
                  <input
                    type="file"
                    ref="logoInput"
                    @change="handleLogoSelect"
                    accept="image/*"
                    class="hidden"
                  />
                  <button
                    type="button"
                    @click="logoInput?.click()"
                    class="px-5 py-2.5 border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium flex items-center"
                  >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    上传Logo
                  </button>
                  <p v-if="uploadingLogo" class="text-sm text-blue-600 mt-2 flex items-center">
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
                <label class="block text-sm font-semibold text-gray-700 mb-2">公司名称 *</label>
                <input
                  v-model="profileForm.company_name"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">统一社会信用代码</label>
                <input
                  v-model="profileForm.unified_code"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">法人代表</label>
                <input
                  v-model="profileForm.legal_person"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">行业</label>
                <input
                  v-model="profileForm.industry"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="例如：互联网"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">规模</label>
                <select
                  v-model="profileForm.scale"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                >
                  <option value="">请选择</option>
                  <option value="1-50人">1-50人</option>
                  <option value="51-200人">51-200人</option>
                  <option value="201-500人">201-500人</option>
                  <option value="501-1000人">501-1000人</option>
                  <option value="1000人以上">1000人以上</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">地址</label>
                <input
                  v-model="profileForm.address"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">网站</label>
                <input
                  v-model="profileForm.website"
                  type="url"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="https://"
                />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">公司描述</label>
              <textarea
                v-model="profileForm.description"
                rows="4"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
                placeholder="请输入公司描述..."
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
                保存
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.564 23.564 0 0112 15c-3.183 0-6.22-1.04-8.755-2.745M9 10a3 3 0 11-6 0 3 3 0 016 0zm12 0a3 3 0 11-6 0 3 3 0 016 0zm-9 10a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                发布职位
              </div>
              <div class="text-3xl font-bold text-blue-600">{{ jobCount }}</div>
            </div>
            <div class="p-4 bg-green-50 rounded-xl border border-green-100">
              <div class="text-gray-600 text-sm mb-1 flex items-center">
                <svg class="w-4 h-4 mr-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                收到申请
              </div>
              <div class="text-3xl font-bold text-green-600">{{ applicationCount }}</div>
            </div>
            <div class="p-4 bg-orange-50 rounded-xl border border-orange-100">
              <div class="text-gray-600 text-sm mb-1 flex items-center">
                <svg class="w-4 h-4 mr-1 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                待处理面试
              </div>
              <div class="text-3xl font-bold text-orange-600">{{ interviewCount }}</div>
            </div>
            <div class="p-4 bg-purple-50 rounded-xl border border-purple-100">
              <div class="text-gray-600 text-sm mb-1 flex items-center">
                <svg class="w-4 h-4 mr-1 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                已发Offer
              </div>
              <div class="text-3xl font-bold text-purple-600">{{ offerCount }}</div>
            </div>
          </div>
        </div>
        <div v-if="profile?.is_verified" class="bg-green-50 border-2 border-green-200 rounded-xl p-4">
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="text-green-600 font-semibold">企业已认证</span>
          </div>
        </div>
        <div v-else class="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4">
          <div class="flex items-center justify-between">
            <span class="text-yellow-600 font-semibold flex items-center">
              <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              企业未认证
            </span>
            <router-link
              to="/enterprise/verification"
              class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 text-sm font-medium"
            >
              立即认证
            </router-link>
          </div>
        </div>
        <div>
          <router-link
            to="/enterprise/personal-verification"
            class="block px-4 py-2.5 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 text-center font-medium transition-all duration-200 border-2 border-gray-200 hover:border-gray-300"
          >
            个人身份认证
          </router-link>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getEnterpriseProfile, updateEnterpriseProfile, createEnterpriseProfile, type EnterpriseProfile } from '@/api/profile'
import { uploadImage } from '@/api/upload'
import { getJobs } from '@/api/jobs'
import { getApplications } from '@/api/applications'
import { getInterviews } from '@/api/interviews'

// 档案数据
const profile = ref<EnterpriseProfile | null>(null)
const loading = ref(false)

// 表单数据
const profileForm = ref({
  company_name: '',
  unified_code: '',
  legal_person: '',
  industry: '',
  scale: '',
  address: '',
  website: '',
  description: '',
  logo_url: '',
})

// Logo上传
const logoInput = ref<HTMLInputElement | null>(null)
const uploadingLogo = ref(false)

// 统计数据
const jobCount = ref(0)
const applicationCount = ref(0)
const interviewCount = ref(0)
const offerCount = ref(0)

// 加载档案数据
const loadProfile = async () => {
  loading.value = true
  try {
    profile.value = await getEnterpriseProfile()
    if (profile.value) {
      profileForm.value = {
        company_name: profile.value.company_name || '',
        unified_code: profile.value.unified_code || '',
        legal_person: profile.value.legal_person || '',
        industry: profile.value.industry || '',
        scale: profile.value.scale || '',
        address: profile.value.address || '',
        website: profile.value.website || '',
        description: profile.value.description || '',
        logo_url: profile.value.logo_url || '',
      }
    }

    // 加载统计数据
    const [jobsRes, applicationsRes, interviewsRes] = await Promise.all([
      getJobs({ page_size: 1 }),
      getApplications({ page_size: 1 }),
      getInterviews({ page_size: 1 }),
    ])

    jobCount.value = jobsRes.total
    applicationCount.value = applicationsRes.total
    interviewCount.value = interviewsRes.total
    offerCount.value = 0 // TODO: 获取Offer数量
  } catch (error: any) {
    console.error('加载档案失败:', error)
    // 如果档案不存在（404），允许创建，不显示错误提示
    if (error.response?.status === 404) {
      // 档案不存在，显示提示但不阻止用户填写表单，也不显示错误提示
      console.log('企业档案不存在，可以创建新档案')
      // 表单已经显示，用户可以填写后保存（会自动创建）
    } else {
      alert('加载档案失败: ' + (error.response?.data?.detail || error.message))
    }
  } finally {
    loading.value = false
  }
}

// 选择Logo文件
const handleLogoSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  
  uploadingLogo.value = true
  
  try {
    // 上传Logo
    const response = await uploadImage(file, 'logo')
    profileForm.value.logo_url = response.url
    alert('Logo上传成功！')
  } catch (error: any) {
    alert('Logo上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploadingLogo.value = false
  }
}

// 保存档案
const saveProfile = async () => {
  try {
    if (profile.value) {
      // 如果档案存在，更新
      await updateEnterpriseProfile(profileForm.value)
      alert('保存成功！')
    } else {
      // 如果档案不存在，创建
      await createEnterpriseProfile(profileForm.value)
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

