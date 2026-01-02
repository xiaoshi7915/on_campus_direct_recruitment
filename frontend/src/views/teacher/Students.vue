<template>
  <div class="teacher-students w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-5xl font-display font-bold text-gray-900 mb-10 animate-fade-in-up flex items-center">
      <div class="w-12 h-12 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mr-4 shadow-lg">
        <svg class="w-7 h-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      </div>
      学生管理
    </h1>

    <!-- 搜索和筛选 -->
    <div class="card-elevated rounded-2xl p-6 mb-8 border border-gray-100/50 animate-fade-in-up" style="animation-delay: 0.1s;">
      <h2 class="text-xl font-display font-semibold text-gray-900 mb-6 flex items-center">
        <div class="w-1 h-5 bg-gradient-primary rounded-full mr-3"></div>
        <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        搜索和筛选
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索学生姓名或学号..."
            class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">年级</label>
          <input
            v-model="filters.grade"
            type="text"
            placeholder="例如：2024"
            class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
            @change="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">专业</label>
          <input
            v-model="filters.major"
            type="text"
            placeholder="例如：计算机科学"
            class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-gray-900 bg-white/80 transition-all duration-300 hover:border-primary-300"
            @change="handleSearch"
          />
        </div>
      </div>
    </div>

    <!-- 学生列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="students.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <p class="text-lg">暂无学生信息</p>
      </div>
      <div
        v-for="student in students"
        :key="student.id"
        class="card-elevated rounded-2xl p-6 border-2 border-gray-200 hover:border-primary-300 hover:bg-gradient-to-br hover:from-primary-50/30 hover:to-transparent transition-all duration-300"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 class="text-xl font-display font-semibold text-gray-900">{{ student.real_name }}</h3>
            </div>
            <div class="text-gray-600 text-sm mb-3 ml-11 space-y-1">
              <p v-if="student.student_id" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                </svg>
                学号：{{ student.student_id }}
              </p>
              <p v-if="student.grade" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                年级：{{ student.grade }}
              </p>
              <p v-if="student.major" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                专业：{{ student.major }}
              </p>
            </div>
            <div class="flex items-center space-x-6 text-sm text-gray-500 ml-11">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                简历数：{{ student.resume_count || 0 }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                申请数：{{ student.application_count || 0 }}
              </span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewStudentDetail(student.id)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              查看详情
            </button>
            <button
              @click="viewStudentResumes(student.id)"
              class="px-5 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium text-sm"
            >
              查看简历
            </button>
            <button
              @click="openCommentModal(student)"
              class="px-5 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              点评
            </button>
            <button
              @click="confirmRemoveStudent(student)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              移除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <Pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      @change="handlePaginationChange"
    />

    <!-- 点评模态框 -->
    <div
      v-if="showCommentModalVisible"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showCommentModalVisible = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <div class="p-8">
          <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
            学生点评
          </h2>
          <div v-if="selectedStudent" class="mb-6 p-4 bg-blue-50 rounded-xl border border-blue-100">
            <p class="text-sm text-gray-700 font-semibold">学生：<span class="text-gray-900">{{ selectedStudent.real_name }}</span></p>
            <p v-if="selectedStudent.student_id" class="text-sm text-gray-600 mt-1">学号：{{ selectedStudent.student_id }}</p>
          </div>
          <form @submit.prevent="saveComment">
            <div class="space-y-5">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">点评内容 <span class="text-red-500">*</span></label>
                <textarea
                  v-model="commentForm.content"
                  rows="6"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
                  placeholder="请输入点评内容"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">评分（1-5分）</label>
                <input
                  v-model.number="commentForm.score"
                  type="number"
                  min="1"
                  max="5"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入评分"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">标签（逗号分隔）</label>
                <input
                  v-model="commentForm.tags"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="例如：学习能力强,团队合作好"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">是否公开</label>
                <select
                  v-model="commentForm.is_public"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                >
                  <option value="PRIVATE">仅教师可见</option>
                  <option value="PUBLIC">公开</option>
                </select>
              </div>
            </div>
            <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
              <button
                type="button"
                @click="showCommentModalVisible = false"
                class="px-6 py-2.5 border-2 border-gray-300 rounded-xl text-gray-700 hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-6 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
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
    </div>

    <!-- 学生详情模态框 -->
    <div
      v-if="showDetailModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showDetailModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <div class="p-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center">
              <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              学生详情
            </h2>
            <button
              @click="showDetailModal = false"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div v-if="studentDetail" class="space-y-6">
            <!-- 基本信息卡片 -->
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
              <div class="flex items-center space-x-4 mb-4">
                <div class="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
                  <span class="text-white text-2xl font-bold">{{ studentDetail.real_name?.charAt(0) || '学' }}</span>
                </div>
                <div>
                  <h3 class="text-2xl font-bold text-gray-900">{{ studentDetail.real_name }}</h3>
                  <p v-if="studentDetail.student_id" class="text-gray-600 mt-1">学号：{{ studentDetail.student_id }}</p>
                </div>
              </div>
            </div>
            
            <!-- 详细信息 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center mb-2">
                  <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="text-sm font-semibold text-gray-700">年级</span>
                </div>
                <p class="text-gray-900 text-lg">{{ studentDetail.grade || '未设置' }}</p>
              </div>
              
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center mb-2">
                  <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <span class="text-sm font-semibold text-gray-700">专业</span>
                </div>
                <p class="text-gray-900 text-lg">{{ studentDetail.major || '未设置' }}</p>
              </div>
              
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center mb-2">
                  <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span class="text-sm font-semibold text-gray-700">简历数</span>
                </div>
                <p class="text-gray-900 text-lg">{{ studentDetail.resume_count || 0 }} 份</p>
              </div>
              
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center mb-2">
                  <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <span class="text-sm font-semibold text-gray-700">申请数</span>
                </div>
                <p class="text-gray-900 text-lg">{{ studentDetail.application_count || 0 }} 份</p>
              </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="flex justify-end space-x-4 pt-4 border-t border-gray-200">
              <button
                @click="showDetailModal = false"
                class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
              >
                关闭
              </button>
              <button
                v-if="studentDetail.id"
                @click="viewStudentResumes(studentDetail.id); showDetailModal = false"
                class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                查看简历
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 移除确认模态框 -->
    <div
      v-if="showRemoveModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showRemoveModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full border border-gray-100">
        <div class="p-8">
          <div class="flex items-center mb-4">
            <div class="p-3 bg-red-50 rounded-lg mr-4">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-900">确认移除</h2>
          </div>
          <p class="text-gray-700 mb-6 ml-16">
            确定要将学生 "{{ selectedStudent?.real_name }}" 从管辖范围内移除吗？此操作不会删除学生数据，只是将其移出您的管辖范围。
          </p>
          <div class="flex justify-end space-x-4 pt-4 border-t border-gray-200">
            <button
              @click="showRemoveModal = false"
              class="px-6 py-2.5 border-2 border-gray-300 rounded-xl text-gray-700 hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              取消
            </button>
            <button
              @click="handleRemoveStudent"
              class="px-6 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              确认移除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getStudents, getStudent, removeStudent, type Student } from '@/api/students'
import { getResumes } from '@/api/resumes'
import { createStudentComment, getStudentComments, type StudentCommentCreate } from '@/api/studentComments'
import { useRouter } from 'vue-router'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 学生列表
const students = ref<Student[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const filters = ref({
  grade: '',
  major: '',
})
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 模态框状态
const showCommentModalVisible = ref(false)
const showRemoveModal = ref(false)
const showDetailModal = ref(false)
const selectedStudent = ref<Student | null>(null)
const studentDetail = ref<any>(null)

// 点评表单
const commentForm = ref<StudentCommentCreate>({
  student_id: '',
  content: '',
  score: undefined,
  tags: '',
  is_public: 'PRIVATE'
})

// 计算总页数
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

// 搜索学生
const handleSearch = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    if (filters.value.grade) {
      params.grade = filters.value.grade
    }
    if (filters.value.major) {
      params.major = filters.value.major
    }
    
    const response = await getStudents(params)
    students.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('搜索学生失败:', error)
    alert('加载学生列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  handleSearch()
}

// 查看学生详情
const viewStudentDetail = async (studentId: string) => {
  try {
    const student = await getStudent(studentId)
    studentDetail.value = student
    showDetailModal.value = true
  } catch (error: any) {
    alert('加载学生详情失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 查看学生简历
const viewStudentResumes = async (studentId: string) => {
  try {
    // 获取学生信息以获取user_id
    const student = await getStudent(studentId)
    
    // 先获取该学生的简历列表
    const resumeParams: any = {
      page: 1,
      page_size: 10,
      student_id: studentId
    }
    const resumeResponse = await getResumes(resumeParams)
    
    // 如果只有一份简历，直接跳转到简历详情页
    if (resumeResponse.items && resumeResponse.items.length === 1) {
      router.push(`/teacher/resumes/${resumeResponse.items[0].id}`)
    } else if (resumeResponse.items && resumeResponse.items.length > 1) {
      // 如果有多份简历，跳转到简历列表页面
      router.push({ path: '/teacher/resumes', query: { student_id: studentId } })
    } else {
      // 如果没有简历，跳转到简历列表页面并提示
      router.push({ path: '/teacher/resumes', query: { student_id: studentId } })
      alert('该学生暂无简历')
    }
  } catch (error: any) {
    console.error('查看简历失败:', error)
    alert('查看简历失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 显示点评模态框
const openCommentModal = (student: Student) => {
  selectedStudent.value = student
  commentForm.value = {
    student_id: student.id,
    content: '',
    score: undefined,
    tags: '',
    is_public: 'PRIVATE'
  }
  showCommentModalVisible.value = true
}

// 保存点评
const saveComment = async () => {
  if (!selectedStudent.value) return
  
  try {
    await createStudentComment(commentForm.value)
    alert('点评成功！')
    showCommentModalVisible.value = false
    selectedStudent.value = null
    commentForm.value = {
      student_id: '',
      content: '',
      score: undefined,
      tags: '',
      is_public: 'PRIVATE'
    }
  } catch (error: any) {
    alert('点评失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 确认移除学生
const confirmRemoveStudent = (student: Student) => {
  selectedStudent.value = student
  showRemoveModal.value = true
}

// 移除学生
const handleRemoveStudent = async () => {
  if (!selectedStudent.value) return
  
  try {
    await removeStudent(selectedStudent.value.id)
    alert('移除成功！')
    showRemoveModal.value = false
    selectedStudent.value = null
    handleSearch() // 刷新列表
  } catch (error: any) {
    alert('移除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

