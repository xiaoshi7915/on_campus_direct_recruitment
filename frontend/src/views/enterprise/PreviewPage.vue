<template>
  <div class="enterprise-preview-page w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
        <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        企业宣传页预览
      </h1>
      <div class="flex space-x-4">
        <button
          @click="exportPDF"
          class="px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          导出PDF
        </button>
        <button
          @click="sharePage"
          class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342c-.864 0-1.873.864-1.873 2.05 0 1.186.99 2.05 1.873 2.05.884 0 1.874-.864 1.874-2.05 0-1.186-.99-2.05-1.874-2.05zm2.632-2.05c0-1.186.99-2.05 1.874-2.05.884 0 1.873.864 1.873 2.05 0 1.186-.99 2.05-1.873 2.05-.884 0-1.874-.864-1.874-2.05zm4.737 0c0-1.186.99-2.05 1.874-2.05.884 0 1.873.864 1.873 2.05 0 1.186-.99 2.05-1.873 2.05-.884 0-1.874-.864-1.874-2.05z" />
          </svg>
          分享
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-16">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    <div v-else-if="!profile" class="text-center py-16 text-gray-500">
      <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <p class="text-lg">请先完善企业信息</p>
    </div>
    <div v-else class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden" id="preview-content">
      <!-- 企业Logo和基本信息 -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white">
        <div class="flex items-start space-x-6">
          <div class="w-32 h-32 rounded-2xl overflow-hidden bg-white flex items-center justify-center border-4 border-white shadow-lg flex-shrink-0">
            <img
              v-if="profile.logo_url"
              :src="profile.logo_url"
              alt="企业Logo"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-gray-400 text-sm font-semibold">Logo</span>
          </div>
          <div class="flex-1">
            <h2 class="text-4xl font-bold mb-4">{{ profile.company_name }}</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-blue-50">
              <div v-if="profile.industry" class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span><strong>行业：</strong>{{ profile.industry }}</span>
              </div>
              <div v-if="profile.scale" class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span><strong>规模：</strong>{{ profile.scale }}</span>
              </div>
              <div v-if="profile.address" class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span><strong>地址：</strong>{{ profile.address }}</span>
              </div>
              <div v-if="profile.website" class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
                <span><strong>网站：</strong><a :href="profile.website" target="_blank" class="underline hover:text-white">{{ profile.website }}</a></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 企业简介 -->
      <div class="p-8 border-b border-gray-200">
        <h3 class="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          企业简介
        </h3>
        <div class="text-gray-700 whitespace-pre-wrap leading-relaxed">{{ profile.description || '暂无简介' }}</div>
      </div>

      <!-- 企业优势 -->
      <div class="p-8 border-b border-gray-200 bg-gray-50">
        <h3 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          企业优势
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
            <div class="flex items-center mb-3">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <h4 class="text-lg font-semibold text-gray-900">发展前景</h4>
            </div>
            <p class="text-gray-600">企业处于快速发展阶段，提供广阔的职业发展空间</p>
          </div>
          <div class="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
            <div class="flex items-center mb-3">
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h4 class="text-lg font-semibold text-gray-900">团队文化</h4>
            </div>
            <p class="text-gray-600">注重团队协作，营造积极向上的工作氛围</p>
          </div>
        </div>
      </div>

      <!-- 联系方式 -->
      <div class="p-8">
        <h3 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          联系方式
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
          <div v-if="profile.address" class="flex items-center p-4 bg-gray-50 rounded-xl">
            <svg class="w-5 h-5 mr-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <div>
              <p class="text-sm text-gray-500">地址</p>
              <p class="font-semibold">{{ profile.address }}</p>
            </div>
          </div>
          <div v-if="profile.website" class="flex items-center p-4 bg-gray-50 rounded-xl">
            <svg class="w-5 h-5 mr-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
            <div>
              <p class="text-sm text-gray-500">官网</p>
              <a :href="profile.website" target="_blank" class="font-semibold text-blue-600 hover:text-blue-700 hover:underline">{{ profile.website }}</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getEnterpriseProfile, type EnterpriseProfile } from '@/api/profile'

const router = useRouter()

const profile = ref<EnterpriseProfile | null>(null)
const loading = ref(false)

// 加载企业信息
const loadProfile = async () => {
  loading.value = true
  try {
    profile.value = await getEnterpriseProfile()
  } catch (error: any) {
    console.error('加载企业信息失败:', error)
    // 如果是企业档案不存在的错误，直接跳转到企业中心页面，不显示错误提示
    if (error.response?.status === 404 && (error.response?.data?.detail?.includes('企业信息不存在') || error.response?.data?.detail?.includes('企业档案不存在'))) {
      // 直接跳转，不显示错误提示（全局错误处理已经跳过显示）
      router.push('/enterprise/profile')
      return
    }
    // 其他错误才显示提示
    alert('加载企业信息失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 导出PDF
const exportPDF = async () => {
  try {
    // 使用html2pdf库或调用后端API生成PDF
    alert('PDF导出功能需要集成PDF生成库（如html2pdf.js或后端PDF生成服务）')
    // TODO: 实现PDF导出功能
  } catch (error: any) {
    console.error('导出PDF失败:', error)
    alert('导出失败: ' + (error.message || '未知错误'))
  }
}

// 分享页面
const sharePage = async () => {
  try {
    const shareUrl = `${window.location.origin}/enterprise/preview`
    const shareText = `查看${profile.value?.company_name || '我们'}的企业宣传页：${shareUrl}`
    
    // 尝试使用Web Share API
    if (navigator.share) {
      try {
        await navigator.share({
          title: profile.value?.company_name || '企业宣传页',
          text: shareText,
          url: shareUrl
        })
        return
      } catch (err) {
        // 用户取消分享，继续使用复制方式
      }
    }
    
    // 复制到剪贴板
    await navigator.clipboard.writeText(shareText)
    alert('分享链接已复制到剪贴板')
  } catch (error: any) {
    console.error('分享失败:', error)
    alert('分享失败: ' + (error.message || '未知错误'))
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.enterprise-preview-page {
  min-height: calc(100vh - 120px);
}

#preview-content {
  min-height: 800px;
}
</style>
