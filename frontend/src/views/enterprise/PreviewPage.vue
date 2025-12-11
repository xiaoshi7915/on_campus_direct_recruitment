<template>
  <div class="enterprise-preview-page">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">企业宣传页预览</h1>
      <div class="flex space-x-4">
        <button
          @click="exportPDF"
          class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
        >
          导出PDF
        </button>
        <button
          @click="sharePage"
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          分享
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else-if="!profile" class="text-center py-12 text-gray-500">
      请先完善企业信息
    </div>
    <div v-else class="bg-white rounded-lg shadow-lg p-8" id="preview-content">
      <!-- 企业Logo和基本信息 -->
      <div class="flex items-start space-x-6 mb-8 pb-8 border-b">
        <div class="w-32 h-32 rounded-lg overflow-hidden bg-gray-200 flex items-center justify-center border-2">
          <img
            v-if="profile.logo_url"
            :src="profile.logo_url"
            alt="企业Logo"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-gray-400 text-sm">Logo</span>
        </div>
        <div class="flex-1">
          <h2 class="text-3xl font-bold mb-2">{{ profile.company_name }}</h2>
          <div class="space-y-2 text-gray-600">
            <p v-if="profile.industry"><strong>行业：</strong>{{ profile.industry }}</p>
            <p v-if="profile.scale"><strong>规模：</strong>{{ profile.scale }}</p>
            <p v-if="profile.address"><strong>地址：</strong>{{ profile.address }}</p>
            <p v-if="profile.website"><strong>网站：</strong><a :href="profile.website" target="_blank" class="text-blue-600 hover:underline">{{ profile.website }}</a></p>
          </div>
        </div>
      </div>

      <!-- 企业简介 -->
      <div class="mb-8">
        <h3 class="text-2xl font-semibold mb-4">企业简介</h3>
        <div class="text-gray-700 whitespace-pre-wrap">{{ profile.description || '暂无简介' }}</div>
      </div>

      <!-- 企业优势 -->
      <div class="mb-8">
        <h3 class="text-2xl font-semibold mb-4">企业优势</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-gray-50 rounded-lg p-4">
            <h4 class="font-semibold mb-2">发展前景</h4>
            <p class="text-gray-600">企业处于快速发展阶段，提供广阔的职业发展空间</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <h4 class="font-semibold mb-2">团队文化</h4>
            <p class="text-gray-600">注重团队协作，营造积极向上的工作氛围</p>
          </div>
        </div>
      </div>

      <!-- 联系方式 -->
      <div class="border-t pt-8">
        <h3 class="text-2xl font-semibold mb-4">联系方式</h3>
        <div class="text-gray-700">
          <p v-if="profile.address"><strong>地址：</strong>{{ profile.address }}</p>
          <p v-if="profile.website"><strong>官网：</strong><a :href="profile.website" target="_blank" class="text-blue-600 hover:underline">{{ profile.website }}</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getEnterpriseProfile, type EnterpriseProfile } from '@/api/profile'

const profile = ref<EnterpriseProfile | null>(null)
const loading = ref(false)

// 加载企业信息
const loadProfile = async () => {
  loading.value = true
  try {
    profile.value = await getEnterpriseProfile()
  } catch (error: any) {
    console.error('加载企业信息失败:', error)
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
  max-width: 1200px;
  margin: 0 auto;
}

#preview-content {
  min-height: 800px;
}
</style>


