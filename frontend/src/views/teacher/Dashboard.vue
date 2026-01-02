<template>
  <div class="teacher-dashboard w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-5xl font-display font-bold text-gray-900 mb-10 bg-gradient-primary bg-clip-text text-transparent animate-fade-in-up">教师工作台</h1>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.1s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">管辖学生</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">{{ statistics.total_students }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.2s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">活跃学生</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-secondary-600 to-secondary-400 bg-clip-text text-transparent">{{ statistics.active_students }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-secondary-100 to-secondary-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.3s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">双选会</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-accent-600 to-accent-400 bg-clip-text text-transparent">{{ jobFairAnalysis.total_job_fairs }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-accent-100 to-accent-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="card-elevated rounded-2xl p-6 group cursor-pointer animate-fade-in-up" style="animation-delay: 0.4s;">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="text-gray-600 text-sm font-semibold mb-3">宣讲会</div>
            <div class="text-4xl font-display font-bold bg-gradient-to-r from-warm-600 to-warm-400 bg-clip-text text-transparent">{{ infoSessionAnalysis.total_info_sessions }}</div>
          </div>
          <div class="ml-4 p-4 bg-gradient-to-br from-warm-100 to-warm-200 rounded-2xl transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
            <svg class="w-7 h-7 text-warm-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 学生活跃度统计 -->
    <div class="card-elevated rounded-2xl mb-8 border border-gray-100/50">
      <div class="p-6 border-b border-gray-100/50">
        <h2 class="text-2xl font-display font-semibold text-gray-900 flex items-center">
          <div class="w-1 h-6 bg-gradient-primary rounded-full mr-3"></div>
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          学生活跃度统计
        </h2>
      </div>
      <div class="p-6">
        <!-- 筛选条件 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">开始日期</label>
            <input
              v-model="studentFilter.start_date"
              type="date"
              class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
              @change="loadStudentStatistics"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">结束日期</label>
            <input
              v-model="studentFilter.end_date"
              type="date"
              class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
              @change="loadStudentStatistics"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">院系ID</label>
            <input
              v-model="studentFilter.department_id"
              type="text"
              placeholder="院系ID（可选）"
              class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
              @change="loadStudentStatistics"
            />
          </div>
        </div>
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-3 text-gray-600">加载中...</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="p-4 bg-blue-50 rounded-xl border border-blue-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              学生总数
            </div>
            <div class="text-2xl font-bold text-blue-600">{{ statistics.total_students }}</div>
          </div>
          <div class="p-4 bg-green-50 rounded-xl border border-green-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              活跃学生
            </div>
            <div class="text-2xl font-bold text-green-600">{{ statistics.active_students }}</div>
          </div>
          <div class="p-4 bg-purple-50 rounded-xl border border-purple-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              简历数量
            </div>
            <div class="text-2xl font-bold text-purple-600">{{ statistics.resume_count }}</div>
          </div>
          <div class="p-4 bg-orange-50 rounded-xl border border-orange-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              申请数量
            </div>
            <div class="text-2xl font-bold text-orange-600">{{ statistics.application_count }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 双选会统计分析 -->
    <div class="card-elevated rounded-2xl mb-8 border border-gray-100/50">
      <div class="p-6 border-b border-gray-100/50">
        <h2 class="text-2xl font-display font-semibold text-gray-900 flex items-center">
          <div class="w-1 h-6 bg-gradient-primary rounded-full mr-3"></div>
          <svg class="w-6 h-6 mr-2 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          双选会统计分析
        </h2>
      </div>
      <div class="p-6">
        <!-- 筛选条件 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">开始日期</label>
            <input
              v-model="jobFairFilter.start_date"
              type="date"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadJobFairAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">结束日期</label>
            <input
              v-model="jobFairFilter.end_date"
              type="date"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadJobFairAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">学校ID</label>
            <input
              v-model="jobFairFilter.school_id"
              type="text"
              placeholder="学校ID（可选）"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadJobFairAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">状态</label>
            <select
              v-model="jobFairFilter.status"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadJobFairAnalysis"
            >
              <option value="">全部</option>
              <option value="DRAFT">草稿</option>
              <option value="PUBLISHED">已发布</option>
              <option value="ONGOING">进行中</option>
              <option value="ENDED">已结束</option>
              <option value="CANCELLED">已取消</option>
            </select>
          </div>
        </div>
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-3 text-gray-600">加载中...</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-4 bg-blue-50 rounded-xl border border-blue-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              双选会总数
            </div>
            <div class="text-2xl font-bold text-blue-600">{{ jobFairAnalysis.total_job_fairs }}</div>
          </div>
          <div class="p-4 bg-green-50 rounded-xl border border-green-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              报名企业数
            </div>
            <div class="text-2xl font-bold text-green-600">{{ jobFairAnalysis.registered_enterprises }}</div>
          </div>
          <div class="p-4 bg-purple-50 rounded-xl border border-purple-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              报名学生数
            </div>
            <div class="text-2xl font-bold text-purple-600">{{ jobFairAnalysis.registered_students }}</div>
          </div>
        </div>
        <!-- 按状态统计 -->
        <div v-if="jobFairAnalysis.by_status && jobFairAnalysis.by_status.length > 0" class="mt-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">按状态统计</h3>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div
              v-for="item in jobFairAnalysis.by_status"
              :key="item.status"
              class="border-2 border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:shadow-md transition-all duration-200 bg-white"
            >
              <div class="text-sm text-gray-600 mb-1">{{ getStatusName(item.status) }}</div>
              <div class="text-xl font-bold text-gray-900">{{ item.count }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 宣讲会统计分析 -->
    <div class="card-elevated rounded-2xl mb-8 border border-gray-100/50">
      <div class="p-6 border-b border-gray-100/50">
        <h2 class="text-2xl font-display font-semibold text-gray-900 flex items-center">
          <div class="w-1 h-6 bg-gradient-primary rounded-full mr-3"></div>
          <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          宣讲会统计分析
        </h2>
      </div>
      <div class="p-6">
        <!-- 筛选条件 -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">开始日期</label>
            <input
              v-model="infoSessionFilter.start_date"
              type="date"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">结束日期</label>
            <input
              v-model="infoSessionFilter.end_date"
              type="date"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">学校ID</label>
            <input
              v-model="infoSessionFilter.school_id"
              type="text"
              placeholder="学校ID（可选）"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">企业ID</label>
            <input
              v-model="infoSessionFilter.enterprise_id"
              type="text"
              placeholder="企业ID（可选）"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadInfoSessionAnalysis"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">状态</label>
            <select
              v-model="infoSessionFilter.status"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @change="loadInfoSessionAnalysis"
            >
              <option value="">全部</option>
              <option value="DRAFT">草稿</option>
              <option value="PUBLISHED">已发布</option>
              <option value="ONGOING">进行中</option>
              <option value="ENDED">已结束</option>
              <option value="CANCELLED">已取消</option>
            </select>
          </div>
        </div>
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-3 text-gray-600">加载中...</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="p-4 bg-blue-50 rounded-xl border border-blue-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              宣讲会总数
            </div>
            <div class="text-2xl font-bold text-blue-600">{{ infoSessionAnalysis.total_info_sessions }}</div>
          </div>
          <div class="p-4 bg-green-50 rounded-xl border border-green-100">
            <div class="text-gray-600 text-sm mb-1 flex items-center">
              <svg class="w-4 h-4 mr-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              报名学生数
            </div>
            <div class="text-2xl font-bold text-green-600">{{ infoSessionAnalysis.registered_students }}</div>
          </div>
        </div>
        <!-- 按状态统计 -->
        <div v-if="infoSessionAnalysis.by_status && infoSessionAnalysis.by_status.length > 0" class="mt-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">按状态统计</h3>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div
              v-for="item in infoSessionAnalysis.by_status"
              :key="item.status"
              class="border-2 border-gray-200 rounded-xl p-4 hover:border-purple-300 hover:shadow-md transition-all duration-200 bg-white"
            >
              <div class="text-sm text-gray-600 mb-1">{{ getStatusName(item.status) }}</div>
              <div class="text-xl font-bold text-gray-900">{{ item.count }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 日程管理 -->
    <div class="card-elevated rounded-2xl border border-gray-100/50">
      <div class="p-6 border-b border-gray-100/50">
        <h2 class="text-2xl font-display font-semibold text-gray-900 flex items-center">
          <div class="w-1 h-6 bg-gradient-primary rounded-full mr-3"></div>
          <svg class="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          日程管理
        </h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-3 text-gray-600">加载中...</p>
        </div>
        <div v-else-if="schedules.length === 0" class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p class="text-gray-500 text-lg">暂无日程记录</p>
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="schedule in schedules"
            :key="schedule.id"
            class="border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg hover:border-blue-200 transition-all duration-200 bg-white"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <div class="flex items-center space-x-3 mb-3">
                  <div class="p-2 bg-indigo-50 rounded-lg">
                    <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h3 class="font-semibold text-lg text-gray-900">{{ schedule.title || '未命名日程' }}</h3>
                  <span class="px-3 py-1 text-xs font-medium rounded-full" :class="getScheduleTypeClass(schedule.schedule_type)">
                    {{ getScheduleTypeName(schedule.schedule_type) }}
                  </span>
                </div>
                <p class="text-gray-600 text-sm mb-2 ml-11">
                  {{ schedule.description || '无描述' }}
                </p>
                <div class="text-gray-500 text-sm ml-11 flex items-center space-x-4">
                  <span class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ formatDate(schedule.start_time) }} - {{ formatDate(schedule.end_time) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getStudentActivityStatistics,
  getJobFairAnalysis,
  getInfoSessionAnalysis,
} from '@/api/statistics'
import { getSchedules } from '@/api/schedules'

// 统计数据
const statistics = ref({
  total_students: 0,
  active_students: 0,
  resume_count: 0,
  application_count: 0,
})
const jobFairAnalysis = ref({
  total_job_fairs: 0,
  registered_enterprises: 0,
  registered_students: 0,
  by_status: [] as Array<{ status: string; count: number }>,
  by_school: [] as Array<{ school_id: string; count: number }>,
})
const infoSessionAnalysis = ref({
  total_info_sessions: 0,
  registered_students: 0,
  by_status: [] as Array<{ status: string; count: number }>,
  by_enterprise: [] as Array<{ enterprise_id: string; count: number }>,
})
const schedules = ref<any[]>([])
const loading = ref(false)

// 筛选条件
const studentFilter = ref({
  start_date: '',
  end_date: '',
  department_id: '',
})
const jobFairFilter = ref({
  start_date: '',
  end_date: '',
  school_id: '',
  status: '',
})
const infoSessionFilter = ref({
  start_date: '',
  end_date: '',
  school_id: '',
  enterprise_id: '',
  status: '',
})

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 获取状态名称
const getStatusName = (status: string) => {
  const statusMap: Record<string, string> = {
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    ONGOING: '进行中',
    ENDED: '已结束',
    CANCELLED: '已取消',
  }
  return statusMap[status] || status
}

// 获取日程类型名称
const getScheduleTypeName = (type: string) => {
  const typeMap: Record<string, string> = {
    JOB_FAIR: '双选会',
    INFO_SESSION: '宣讲会',
    INTERVIEW: '面试',
    OTHER: '其他',
  }
  return typeMap[type] || type
}

// 获取日程类型样式
const getScheduleTypeClass = (type: string) => {
  const classMap: Record<string, string> = {
    JOB_FAIR: 'bg-orange-100 text-orange-800',
    INFO_SESSION: 'bg-purple-100 text-purple-800',
    INTERVIEW: 'bg-blue-100 text-blue-800',
    OTHER: 'bg-gray-100 text-gray-800',
  }
  return classMap[type] || 'bg-gray-100 text-gray-800'
}

// 加载学生统计数据
const loadStudentStatistics = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (studentFilter.value.start_date) {
      params.start_date = studentFilter.value.start_date
    }
    if (studentFilter.value.end_date) {
      params.end_date = studentFilter.value.end_date
    }
    if (studentFilter.value.department_id) {
      params.department_id = studentFilter.value.department_id
    }
    const response = await getStudentActivityStatistics(params)
    statistics.value = response
  } catch (error) {
    console.error('加载学生统计数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载双选会统计分析
const loadJobFairAnalysis = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (jobFairFilter.value.start_date) {
      params.start_date = jobFairFilter.value.start_date
    }
    if (jobFairFilter.value.end_date) {
      params.end_date = jobFairFilter.value.end_date
    }
    if (jobFairFilter.value.school_id) {
      params.school_id = jobFairFilter.value.school_id
    }
    if (jobFairFilter.value.status) {
      params.status = jobFairFilter.value.status
    }
    const response = await getJobFairAnalysis(params)
    jobFairAnalysis.value = response
  } catch (error) {
    console.error('加载双选会统计分析失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载宣讲会统计分析
const loadInfoSessionAnalysis = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (infoSessionFilter.value.start_date) {
      params.start_date = infoSessionFilter.value.start_date
    }
    if (infoSessionFilter.value.end_date) {
      params.end_date = infoSessionFilter.value.end_date
    }
    if (infoSessionFilter.value.school_id) {
      params.school_id = infoSessionFilter.value.school_id
    }
    if (infoSessionFilter.value.enterprise_id) {
      params.enterprise_id = infoSessionFilter.value.enterprise_id
    }
    if (infoSessionFilter.value.status) {
      params.status = infoSessionFilter.value.status
    }
    const response = await getInfoSessionAnalysis(params)
    infoSessionAnalysis.value = response
  } catch (error) {
    console.error('加载宣讲会统计分析失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载日程
const loadSchedules = async () => {
  loading.value = true
  try {
    // 加载双选会和宣讲会相关的日程
    const [jobFairSchedules, infoSessionSchedules] = await Promise.all([
      getSchedules({ page_size: 5, schedule_type: 'JOB_FAIR' }).catch(() => ({ items: [] })),
      getSchedules({ page_size: 5, schedule_type: 'INFO_SESSION' }).catch(() => ({ items: [] })),
    ])
    schedules.value = [
      ...(jobFairSchedules.items || []),
      ...(infoSessionSchedules.items || []),
    ].slice(0, 10) // 最多显示10条
  } catch (error) {
    console.error('加载日程失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载所有数据
const loadData = async () => {
  await Promise.all([
    loadStudentStatistics(),
    loadJobFairAnalysis(),
    loadInfoSessionAnalysis(),
    loadSchedules(),
  ])
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>



