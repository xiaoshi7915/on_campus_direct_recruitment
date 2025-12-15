<template>
  <MainLayout>
    <div class="home min-h-screen">
      <!-- 主要内容区域 -->
      <div class="container mx-auto px-4 py-12">
        <!-- 顶部标题区域 -->
        <div class="text-center mb-12">
          <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            校园直聘平台
          </h1>
          <p class="text-xl text-gray-600 mb-2">连接高校人才与企业需求的综合性招聘服务平台</p>
          <p class="text-lg text-gray-500">为高校教师、企业和学生提供便捷的招聘求职服务</p>
        </div>

        <!-- 图片展示区域 -->
        <div class="mb-12 flex justify-center">
          <div class="relative w-full max-w-4xl">
            <img 
              src="/images/background.jpg" 
              alt="校园直聘平台" 
              class="w-full h-auto rounded-2xl shadow-2xl object-cover"
              style="max-height: 500px;"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent rounded-2xl"></div>
          </div>
        </div>

        <!-- 功能特色卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-300 border border-gray-100">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">多角色支持</h3>
            <p class="text-gray-600 text-sm">学生、企业、教师、管理员四种角色</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-300 border border-gray-100">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">实时聊天</h3>
            <p class="text-gray-600 text-sm">支持文字、图片、文件等多种消息类型</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-300 border border-gray-100">
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">数据统计</h3>
            <p class="text-gray-600 text-sm">多维度数据分析和报表</p>
          </div>
        </div>

        <!-- 操作按钮区域 -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <router-link
            to="/login"
            class="btn-primary px-8 py-3 text-base font-semibold"
          >
            立即登录
          </router-link>
          <router-link
            to="/register"
            class="btn-secondary px-8 py-3 text-base font-semibold"
          >
            免费注册
          </router-link>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/components/layouts/MainLayout.vue'
// 首页组件
</script>

<style scoped>
.home {
  background: linear-gradient(135deg, #f9fafb 0%, #e5e7eb 100%);
}

.btn-primary {
  background-color: #2563eb;
  color: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
  transform: translateY(0);
}

.btn-primary:hover {
  background-color: #1d4ed8;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: white;
  color: #2563eb;
  border: 2px solid #2563eb;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
  transform: translateY(0);
}

.btn-secondary:hover {
  background-color: #eff6ff;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}
</style>

