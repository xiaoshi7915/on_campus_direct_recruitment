<template>
  <div class="enterprise-school-detail min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p class="text-gray-600 text-lg">加载中...</p>
      </div>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="!school" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="text-6xl mb-4">😕</div>
        <p class="text-gray-500 text-lg">学校不存在</p>
        <button
          @click="$router.back()"
          class="btn btn-primary btn-md mt-4"
        >
          返回
        </button>
      </div>
    </div>
    
    <!-- 主要内容 -->
    <div v-else class="w-full max-w-full px-4 py-8 space-y-6">
      <!-- 返回按钮 -->
      <div class="mb-2 flex justify-end">
        <button
          @click="$router.back()"
          class="flex items-center text-blue-600 hover:text-blue-800 transition-colors group"
        >
          <svg class="w-5 h-5 mr-2 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          返回
        </button>
      </div>

      <!-- 学校基本信息卡片 -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- 顶部横幅区域 -->
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
          <div class="flex items-start justify-between">
            <div class="flex items-start space-x-6 flex-1">
              <!-- Logo -->
              <div class="relative">
                <img
                  v-if="school.logo_url"
                  :src="school.logo_url"
                  :alt="school.name"
                  class="w-32 h-32 rounded-2xl object-cover border-4 border-white shadow-lg"
                />
                <div v-else class="w-32 h-32 rounded-2xl bg-white/20 flex items-center justify-center border-4 border-white shadow-lg">
                  <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
              </div>
              
              <!-- 学校名称和基本信息 -->
              <div class="flex-1 text-white">
                <div class="flex items-center space-x-3 mb-3">
                  <h1 class="text-4xl font-bold">{{ school.name }}</h1>
                  <span
                    v-if="school.is_verified"
                    class="px-4 py-1.5 rounded-full text-sm font-semibold bg-green-500 text-white shadow-md flex items-center"
                  >
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    已认证
                  </span>
                  <span
                    v-else
                    class="px-4 py-1.5 rounded-full text-sm font-semibold bg-white/20 text-white shadow-md"
                  >
                    未认证
                  </span>
                </div>
                
                <!-- 学校标签 -->
                <div v-if="school.f985 === '是' || school.f211 === '是' || school.is_top === '是'" class="flex flex-wrap gap-2 mb-3">
                  <span v-if="school.f985 === '是'" class="px-3 py-1 rounded-full text-xs font-bold bg-red-500 text-white shadow-md">985工程</span>
                  <span v-if="school.f211 === '是'" class="px-3 py-1 rounded-full text-xs font-bold bg-blue-500 text-white shadow-md">211工程</span>
                  <span v-if="school.is_top === '是'" class="px-3 py-1 rounded-full text-xs font-bold bg-purple-500 text-white shadow-md">顶尖高校</span>
                </div>
                
                <!-- 双一流学科 -->
                <div v-if="school.dual_class_name" class="flex items-center space-x-2 text-sm">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span class="font-semibold">双一流学科：</span>
                  <span>{{ school.dual_class_name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 详细信息区域 -->
        <div class="p-8">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- 左侧：详细信息 -->
            <div class="lg:col-span-2 space-y-6">
              <!-- 基本信息网格 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-if="school.code" class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div class="flex items-center space-x-2 text-gray-500 mb-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                    </svg>
                    <span class="text-sm font-medium">学校代码</span>
                  </div>
                  <p class="text-gray-900 font-semibold">{{ school.code }}</p>
                </div>
                
                <div v-if="school.province || school.city" class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div class="flex items-center space-x-2 text-gray-500 mb-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span class="text-sm font-medium">所在地区</span>
                  </div>
                  <p class="text-gray-900 font-semibold">{{ [school.province, school.city].filter(Boolean).join(' ') }}</p>
                </div>
                
                <div v-if="school.charge_dep" class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div class="flex items-center space-x-2 text-gray-500 mb-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <span class="text-sm font-medium">主管部门</span>
                  </div>
                  <p class="text-gray-900 font-semibold">{{ school.charge_dep }}</p>
                </div>
                
                <div v-if="school.address" class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div class="flex items-center space-x-2 text-gray-500 mb-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span class="text-sm font-medium">详细地址</span>
                  </div>
                  <p class="text-gray-900 font-semibold">{{ school.address }}</p>
                </div>
                
                <div v-if="school.website" class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div class="flex items-center space-x-2 text-gray-500 mb-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                    </svg>
                    <span class="text-sm font-medium">官方网站</span>
                  </div>
                  <a :href="school.website" target="_blank" class="text-blue-600 hover:text-blue-800 font-semibold hover:underline flex items-center">
                    {{ school.website }}
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                </div>
              </div>
              
              <!-- 学校属性标签 -->
              <div v-if="school.school_type_name || school.nature_name || school.level_name" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
                <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  学校属性
                </h3>
                <div class="flex flex-wrap gap-3">
                  <span v-if="school.school_type_name" class="px-4 py-2 rounded-lg text-sm font-medium bg-white text-gray-700 shadow-sm border border-gray-200">
                    {{ school.school_type_name }}
                  </span>
                  <span v-if="school.nature_name" class="px-4 py-2 rounded-lg text-sm font-medium bg-green-100 text-green-800 shadow-sm">
                    {{ school.nature_name }}
                  </span>
                  <span v-if="school.level_name" class="px-4 py-2 rounded-lg text-sm font-medium bg-yellow-100 text-yellow-800 shadow-sm">
                    {{ school.level_name }}
                  </span>
                </div>
              </div>
              
              <!-- 统计数据 -->
              <div class="grid grid-cols-2 gap-4">
                <div v-if="school.student_count !== undefined" class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-blue-100 text-sm mb-1">在校学生</p>
                      <p class="text-3xl font-bold">{{ school.student_count.toLocaleString() }}</p>
                    </div>
                    <svg class="w-12 h-12 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                </div>
                <div v-if="school.department_count !== undefined" class="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl p-6 text-white shadow-lg">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-indigo-100 text-sm mb-1">院系数量</p>
                      <p class="text-3xl font-bold">{{ school.department_count.toLocaleString() }}</p>
                    </div>
                    <svg class="w-12 h-12 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 右侧：操作按钮 -->
            <div class="space-y-3">
              <button
                @click="toggleFavorite"
                :class="isFavorited ? 'bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700' : 'bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700'"
                class="w-full px-6 py-3 text-white rounded-xl font-semibold shadow-lg transform transition-all hover:scale-105 flex items-center justify-center space-x-2"
              >
                <svg v-if="isFavorited" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                </svg>
                <span>{{ isFavorited ? '已收藏' : '收藏' }}</span>
              </button>
              <button
                @click="showMarkModal = true"
                class="btn btn-primary btn-md btn-full"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                <span>标记</span>
              </button>
              <button
                @click="handleShare"
                class="btn btn-success btn-md btn-full"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
                <span>分享</span>
              </button>
              <button
                @click="showRequestModal"
                class="btn btn-primary btn-md btn-full"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>申请宣讲会</span>
              </button>
              <button
                @click="startChat"
                class="btn btn-primary btn-md btn-full"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <span>发起聊天</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 学校描述 -->
      <div v-if="school.description" class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-4">
          <h2 class="text-2xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
            学校简介
          </h2>
        </div>
        <div class="p-8">
          <p class="text-gray-700 leading-relaxed whitespace-pre-wrap text-lg">{{ school.description }}</p>
        </div>
      </div>

      <!-- 院系介绍 -->
      <div v-if="school.department" class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-green-600 to-emerald-700 px-8 py-4">
          <h2 class="text-2xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            院系介绍
          </h2>
        </div>
        <div class="p-8">
          <p class="text-gray-700 leading-relaxed whitespace-pre-wrap text-lg">{{ school.department }}</p>
        </div>
      </div>

      <!-- 主要专业介绍 -->
      <div v-if="school.major" class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-purple-600 to-pink-700 px-8 py-4">
          <h2 class="text-2xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            主要专业介绍
          </h2>
        </div>
        <div class="p-8">
          <p class="text-gray-700 leading-relaxed whitespace-pre-wrap text-lg">{{ school.major }}</p>
        </div>
      </div>

      <!-- 该学校的宣讲会列表 -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-orange-600 to-red-700 px-8 py-4">
          <h2 class="text-2xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            该学校的宣讲会
          </h2>
        </div>
        <div class="p-8">
          <!-- 加载状态 -->
          <div v-if="infoSessionsLoading" class="flex items-center justify-center py-12">
            <div class="text-center">
              <div class="inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-orange-600 mb-4"></div>
              <p class="text-gray-600">加载中...</p>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-else-if="infoSessions.length === 0" class="text-center py-12">
            <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p class="text-gray-500 text-lg">暂无宣讲会</p>
          </div>
          
          <!-- 宣讲会列表 -->
          <div v-else class="space-y-4">
            <div
              v-for="session in infoSessions"
              :key="session.id"
              class="border-2 border-gray-200 rounded-xl p-6 hover:border-orange-400 hover:shadow-lg transition-all duration-300 bg-gradient-to-r from-white to-gray-50"
            >
              <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div class="flex-1">
                  <div class="flex items-start justify-between mb-3">
                    <h3 class="text-xl font-bold text-gray-900">{{ session.title }}</h3>
                    <span
                      :class="{
                        'bg-green-100 text-green-800': session.status === 'PUBLISHED' || session.status === 'ONGOING',
                        'bg-yellow-100 text-yellow-800': session.status === 'PENDING',
                        'bg-gray-100 text-gray-800': session.status === 'DRAFT',
                        'bg-red-100 text-red-800': session.status === 'CANCELLED',
                        'bg-blue-100 text-blue-800': session.status === 'ENDED'
                      }"
                      class="px-3 py-1 rounded-full text-xs font-semibold"
                    >
                      {{ getStatusText(session.status) }}
                    </span>
                  </div>
                  
                  <div class="space-y-2 text-gray-600">
                    <div class="flex items-center space-x-2">
                      <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="font-medium">时间：</span>
                      <span>{{ formatDateTime(session.start_time) }} - {{ formatDateTime(session.end_time) }}</span>
                    </div>
                    <div v-if="session.location" class="flex items-center space-x-2">
                      <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <span class="font-medium">地点：</span>
                      <span>{{ session.location }}</span>
                    </div>
                  </div>
                </div>
                
                <button
                  @click="viewInfoSession(session.id)"
                  class="btn btn-danger btn-md whitespace-nowrap"
                >
                  <span>查看详情</span>
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 标记模态框 -->
    <div v-if="showMarkModal" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="showMarkModal = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full transform transition-all animate-scale-in">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4 rounded-t-2xl">
          <h2 class="text-2xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            标记学校
          </h2>
        </div>
        <form @submit.prevent="handleMark" class="p-6 space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">备注</label>
            <textarea
              v-model="markForm.note"
              rows="4"
              placeholder="请输入备注信息..."
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">标记颜色</label>
            <div class="grid grid-cols-5 gap-2">
              <button
                type="button"
                v-for="color in ['blue', 'red', 'green', 'yellow', 'purple']"
                :key="color"
                @click="markForm.color = color"
                :class="{
                  'ring-4 ring-offset-2': markForm.color === color
                }"
                :style="{
                  backgroundColor: color === 'blue' ? '#3b82f6' : color === 'red' ? '#ef4444' : color === 'green' ? '#10b981' : color === 'yellow' ? '#f59e0b' : '#a855f7'
                }"
                class="h-12 rounded-lg shadow-md transform transition-all hover:scale-110"
              />
            </div>
          </div>
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="showMarkModal = false"
              class="btn btn-secondary btn-md"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="btn btn-primary btn-md"
            >
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 申请宣讲会模态框 -->
    <div v-if="showRequestInfoSessionModal" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="showRequestInfoSessionModal = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col transform transition-all animate-scale-in">
        <div class="bg-gradient-to-r from-purple-600 to-pink-700 px-6 py-4 flex-shrink-0">
          <h2 class="text-2xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            申请线下宣讲会
          </h2>
        </div>
        <div class="overflow-y-auto flex-1 p-6">
          <form @submit.prevent="handleRequestInfoSession" class="space-y-5">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">宣讲会标题 <span class="text-red-500">*</span></label>
              <input
                v-model="requestForm.title"
                type="text"
                required
                placeholder="请输入宣讲会标题"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
              <textarea
                v-model="requestForm.description"
                rows="3"
                placeholder="请输入宣讲会描述"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">建议开始时间 <span class="text-red-500">*</span></label>
                <input
                  v-model="requestForm.proposed_start_time"
                  type="datetime-local"
                  required
                  class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">建议结束时间 <span class="text-red-500">*</span></label>
                <input
                  v-model="requestForm.proposed_end_time"
                  type="datetime-local"
                  required
                  class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">建议地点</label>
              <input
                v-model="requestForm.proposed_location"
                type="text"
                placeholder="请输入建议地点"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">最大学生数</label>
              <input
                v-model.number="requestForm.max_students"
                type="number"
                min="1"
                placeholder="请输入最大学生数"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">联系人</label>
                <input
                  v-model="requestForm.contact_person"
                  type="text"
                  placeholder="请输入联系人"
                  class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">联系电话</label>
                <input
                  v-model="requestForm.contact_phone"
                  type="tel"
                  placeholder="请输入联系电话"
                  class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">联系邮箱</label>
                <input
                  v-model="requestForm.contact_email"
                  type="email"
                  placeholder="请输入联系邮箱"
                  class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">申请留言</label>
              <textarea
                v-model="requestForm.message"
                rows="4"
                placeholder="请输入申请留言"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              />
            </div>
          </form>
        </div>
        <div class="flex justify-end space-x-3 p-6 border-t border-gray-200 flex-shrink-0 bg-gray-50">
          <button
            type="button"
            @click="showRequestInfoSessionModal = false"
            class="px-6 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-colors"
          >
            取消
          </button>
          <button
            type="submit"
            @click="handleRequestInfoSession"
            :disabled="submitting"
            class="btn btn-primary btn-md"
          >
            {{ submitting ? '提交中...' : '提交申请' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getSchool, type School, requestOfflineInfoSession, type OfflineInfoSessionRequest } from '@/api/schools'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'
import { createMark, getMark, updateMark, type MarkCreateRequest } from '@/api/marks'
import { getSchoolShareLink } from '@/api/schools'
import { getInfoSessions, type InfoSession } from '@/api/infoSessions'
import { createOrGetChatSession } from '@/api/chat'

const route = useRoute()
const router = useRouter()

// 数据
const school = ref<School | null>(null)
const loading = ref(false)
const isFavorited = ref(false)
const currentMark = ref<any>(null)

// 宣讲会列表
const infoSessions = ref<InfoSession[]>([])
const infoSessionsLoading = ref(false)

// 标记模态框
const showMarkModal = ref(false)
const submitting = ref(false)
const markForm = ref({
  note: '',
  color: 'blue'
})

// 申请宣讲会模态框
const showRequestInfoSessionModal = ref(false)
const requestForm = ref<OfflineInfoSessionRequest>({
  school_id: '',
  title: '',
  description: '',
  proposed_start_time: '',
  proposed_end_time: '',
  proposed_location: '',
  max_students: undefined,
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  message: ''
})

// 加载学校详情
const loadSchool = async () => {
  const schoolId = route.params.id as string
  if (!schoolId) return

  loading.value = true
  try {
    school.value = await getSchool(schoolId)
    
    // 检查收藏状态
    try {
      isFavorited.value = await checkFavorite('SCHOOL', schoolId)
    } catch (error) {
      isFavorited.value = false
    }

    // 检查标记状态
    try {
      currentMark.value = await getMark('SCHOOL', schoolId)
      if (currentMark.value) {
        markForm.value.note = currentMark.value.note || ''
        markForm.value.color = currentMark.value.color || 'blue'
      }
    } catch (error) {
      // 没有标记
      currentMark.value = null
    }

    // 加载该学校的宣讲会列表
    await loadInfoSessions(schoolId)
  } catch (error: any) {
    console.error('加载学校详情失败:', error)
    alert('加载学校详情失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 加载宣讲会列表
const loadInfoSessions = async (schoolId: string) => {
  infoSessionsLoading.value = true
  try {
    const response = await getInfoSessions({
      school_id: schoolId,
      page_size: 10
    })
    // 只显示该学校的宣讲会
    infoSessions.value = response.items.filter(session => session.school_id === schoolId)
  } catch (error: any) {
    console.error('加载宣讲会列表失败:', error)
  } finally {
    infoSessionsLoading.value = false
  }
}

// 切换收藏状态
const toggleFavorite = async () => {
  if (!school.value) return

  try {
    if (isFavorited.value) {
      await removeFavorite('SCHOOL', school.value.id)
      isFavorited.value = false
      alert('已取消收藏')
    } else {
      await addFavorite('SCHOOL', school.value.id)
      isFavorited.value = true
      alert('已收藏')
    }
  } catch (error: any) {
    console.error('收藏操作失败:', error)
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 分享学校
const handleShare = async () => {
  if (!school.value) return

  try {
    const shareData = await getSchoolShareLink(school.value.id)
    
    // 复制分享链接到剪贴板
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(shareData.share_url)
      alert('分享链接已复制到剪贴板')
    } else {
      // 降级方案：显示分享链接
      prompt('分享链接（请复制）：', shareData.share_url)
    }
  } catch (error: any) {
    console.error('获取分享链接失败:', error)
    alert('获取分享链接失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 保存标记
const handleMark = async () => {
  if (!school.value) return

  submitting.value = true
  try {
    const markData: MarkCreateRequest = {
      target_type: 'SCHOOL',
      target_id: school.value.id,
      note: markForm.value.note,
      color: markForm.value.color
    }

    if (currentMark.value) {
      // 更新现有标记
      await updateMark(currentMark.value.id, {
        note: markForm.value.note,
        color: markForm.value.color
      })
    } else {
      // 创建新标记
      currentMark.value = await createMark(markData)
    }

    alert('标记已保存')
    showMarkModal.value = false
  } catch (error: any) {
    console.error('保存标记失败:', error)
    alert('保存标记失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 发起聊天
const startChat = async () => {
  if (!school.value) return
  
  try {
    // 创建或获取与学校的聊天会话
    const session = await createOrGetChatSession(undefined, undefined, school.value.id)
    // 跳转到聊天页面
    router.push(`/enterprise/chat?session_id=${session.id}`)
  } catch (error: any) {
    console.error('发起聊天失败:', error)
    alert('发起聊天失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 显示申请模态框
const showRequestModal = () => {
  if (!school.value) return

  requestForm.value = {
    school_id: school.value.id,
    title: '',
    description: '',
    proposed_start_time: '',
    proposed_end_time: '',
    proposed_location: '',
    max_students: undefined,
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    message: ''
  }
  showRequestInfoSessionModal.value = true
}

// 提交申请
const handleRequestInfoSession = async () => {
  if (!school.value) return

  submitting.value = true
  try {
    await requestOfflineInfoSession(school.value.id, {
      ...requestForm.value,
      proposed_start_time: new Date(requestForm.value.proposed_start_time).toISOString(),
      proposed_end_time: new Date(requestForm.value.proposed_end_time).toISOString(),
    })
    alert('申请已提交，等待学校审批')
    showRequestInfoSessionModal.value = false
  } catch (error: any) {
    console.error('提交申请失败:', error)
    alert('提交申请失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 查看宣讲会详情
const viewInfoSession = (sessionId: string) => {
  router.push(`/enterprise/info-sessions?session_id=${sessionId}`)
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
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
    DRAFT: '草稿',
    PENDING: '待审批',
    PUBLISHED: '已发布',
    ONGOING: '进行中',
    ENDED: '已结束',
    CANCELLED: '已取消'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadSchool()
})
</script>

<style scoped>
.enterprise-school-detail {
  max-width: 1400px;
  margin: 0 auto;
}

/* 动画效果 */
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scale-in 0.2s ease-out;
}

/* 响应式容器 */
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}

/* 卡片悬停效果 */
.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 渐变背景 */
.bg-gradient-to-br {
  background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

/* 按钮过渡效果 */
.transform {
  transform: translateZ(0);
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* 加载动画 */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>

