<template>
  <div class="enterprise-profile">
    <h1 class="text-3xl font-bold mb-6">企业中心</h1>

    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else>
      <div v-if="!profile" class="mb-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p class="text-yellow-800">您还没有创建企业档案，请填写以下信息创建档案。</p>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧：企业信息 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">企业信息</h2>
          <form @submit.prevent="saveProfile">
            <!-- Logo上传 -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">企业Logo</label>
              <div class="flex items-center space-x-4">
                <div class="w-24 h-24 rounded-lg overflow-hidden bg-gray-200 flex items-center justify-center border">
                  <img
                    v-if="profileForm.logo_url"
                    :src="profileForm.logo_url"
                    alt="Logo"
                    class="w-full h-full object-cover"
                  />
                  <span v-else class="text-gray-400 text-sm">Logo</span>
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
                    class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    上传Logo
                  </button>
                  <p v-if="uploadingLogo" class="text-sm text-blue-600 mt-2">上传中...</p>
                </div>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">公司名称 *</label>
                <input
                  v-model="profileForm.company_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">统一社会信用代码</label>
                <input
                  v-model="profileForm.unified_code"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">法人代表</label>
                <input
                  v-model="profileForm.legal_person"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">行业</label>
                <input
                  v-model="profileForm.industry"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="例如：互联网"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">规模</label>
                <select
                  v-model="profileForm.scale"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
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
                <label class="block text-sm font-medium text-gray-700 mb-2">地址</label>
                <input
                  v-model="profileForm.address"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">网站</label>
                <input
                  v-model="profileForm.website"
                  type="url"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="https://"
                />
              </div>
            </div>
            <div class="mt-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">公司描述</label>
              <textarea
                v-model="profileForm.description"
                rows="4"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入公司描述..."
              />
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
              <div class="text-gray-600 text-sm">发布职位</div>
              <div class="text-2xl font-bold text-blue-600">{{ jobCount }}</div>
            </div>
            <div>
              <div class="text-gray-600 text-sm">收到申请</div>
              <div class="text-2xl font-bold text-green-600">{{ applicationCount }}</div>
            </div>
            <div>
              <div class="text-gray-600 text-sm">待处理面试</div>
              <div class="text-2xl font-bold text-orange-600">{{ interviewCount }}</div>
            </div>
            <div>
              <div class="text-gray-600 text-sm">已发Offer</div>
              <div class="text-2xl font-bold text-purple-600">{{ offerCount }}</div>
            </div>
          </div>
        </div>
        <div v-if="profile?.is_verified" class="bg-green-50 border border-green-200 rounded-lg p-4">
          <div class="flex items-center space-x-2">
            <span class="text-green-600 font-semibold">✓ 企业已认证</span>
          </div>
        </div>
        <div v-else class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <span class="text-yellow-600 font-semibold">⚠ 企业未认证</span>
            <router-link
              to="/enterprise/verification"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm"
            >
              立即认证
            </router-link>
          </div>
        </div>
        <div class="mt-4">
          <router-link
            to="/enterprise/personal-verification"
            class="block px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-center"
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
    // 如果档案不存在（404），允许创建
    if (error.response?.status === 404) {
      // 档案不存在，显示提示但不阻止用户填写表单
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
.enterprise-profile {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

