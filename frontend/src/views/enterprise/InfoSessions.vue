<template>
  <div class="enterprise-info-sessions max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
        <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        宣讲会管理
      </h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        创建宣讲会
      </button>
    </div>

    <!-- 宣讲会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="infoSessions.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        <p class="text-lg">暂无宣讲会信息</p>
      </div>
      <div
        v-for="session in infoSessions"
        :key="session.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border border-gray-100"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-purple-50 rounded-lg">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ session.title }}</h3>
              <span
                :class="getStatusClass(session.status)"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ getStatusText(session.status) }}
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3 ml-11 space-y-1">
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                时间：{{ formatDateTime(session.start_time) }} - {{ formatDateTime(session.end_time) }}
              </p>
              <p v-if="session.location" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                地点：{{ session.location }}
              </p>
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                类型：{{ getSessionTypeText(session.session_type) }}
              </p>
              <p v-if="session.max_students" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                最大人数：{{ session.max_students }}
              </p>
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                已报名：{{ session.check_in_count }}
              </p>
            </div>
            <p v-if="session.description" class="text-gray-700 line-clamp-2 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ session.description }}
            </p>
            <div v-if="session.live_url" class="mt-3 ml-11">
              <a
                :href="session.live_url"
                target="_blank"
                class="inline-flex items-center px-4 py-2 bg-blue-50 text-blue-600 rounded-xl hover:bg-blue-100 transition-colors duration-200 font-medium text-sm"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                直播链接
              </a>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editInfoSession(session)"
              class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              编辑
            </button>
            <button
              @click="viewRegistrations(session.id)"
              class="px-4 py-2 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium text-sm"
            >
              查看报名
            </button>
            <button
              @click="showInviteModal(session.id)"
              class="px-4 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              邀请学生
            </button>
            <button
              @click="handleDeleteInfoSession(session.id)"
              class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建模态框 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          创建宣讲会
        </h2>
        <form @submit.prevent="saveCreate">
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">标题 *</label>
              <input v-model="createForm.title" type="text" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
              <textarea v-model="createForm.description" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">开始时间 *</label>
                <input v-model="createForm.start_time" type="datetime-local" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">结束时间 *</label>
                <input v-model="createForm.end_time" type="datetime-local" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">地点</label>
              <input v-model="createForm.location" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">类型 *</label>
                <select v-model="createForm.session_type" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200">
                  <option value="OFFLINE">线下</option>
                  <option value="ONLINE">线上</option>
                  <option value="HYBRID">混合</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">最大人数</label>
                <input v-model.number="createForm.max_students" type="number" min="1" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">直播链接</label>
              <input v-model="createForm.live_url" type="url" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">宣讲会资料</label>
              <div class="space-y-2">
                <div v-for="(material, index) in createForm.materials" :key="index" class="flex items-center space-x-2 p-3 bg-gray-50 rounded-xl border border-gray-200">
                  <a :href="material" target="_blank" class="text-blue-600 hover:text-blue-800 flex-1 truncate font-medium">{{ material }}</a>
                  <button type="button" @click="createForm.materials.splice(index, 1)" class="px-3 py-1 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors duration-200 text-sm font-medium">删除</button>
                </div>
                <input
                  type="file"
                  ref="createFileInput"
                  @change="handleCreateFileSelect"
                  accept=".pdf,.doc,.docx,.ppt,.pptx"
                  class="hidden"
                />
                <button
                  type="button"
                  @click="createFileInput?.click()"
                  class="px-4 py-2 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
                >
                  上传资料
                </button>
              </div>
            </div>
          </div>
          <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
            <button type="button" @click="showCreateModal = false" class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium">取消</button>
            <button type="submit" class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              创建
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 编辑模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          编辑宣讲会
        </h2>
        <form @submit.prevent="saveEdit">
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">标题</label>
              <input v-model="editForm.title" type="text" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
              <textarea v-model="editForm.description" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">开始时间</label>
                <input v-model="editForm.start_time" type="datetime-local" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">结束时间</label>
                <input v-model="editForm.end_time" type="datetime-local" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">地点</label>
              <input v-model="editForm.location" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">类型</label>
                <select v-model="editForm.session_type" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200">
                  <option value="OFFLINE">线下</option>
                  <option value="ONLINE">线上</option>
                  <option value="HYBRID">混合</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">状态</label>
                <select v-model="editForm.status" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200">
                  <option value="DRAFT">草稿</option>
                  <option value="PUBLISHED">已发布</option>
                  <option value="ONGOING">进行中</option>
                  <option value="ENDED">已结束</option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">直播链接</label>
              <input v-model="editForm.live_url" type="url" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">最大人数</label>
              <input v-model.number="editForm.max_students" type="number" min="1" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">宣讲会资料</label>
              <div class="space-y-2">
                <div v-for="(material, index) in editForm.materials" :key="index" class="flex items-center space-x-2 p-3 bg-gray-50 rounded-xl border border-gray-200">
                  <a :href="material" target="_blank" class="text-blue-600 hover:text-blue-800 flex-1 truncate font-medium">{{ material }}</a>
                  <button type="button" @click="editForm.materials.splice(index, 1)" class="px-3 py-1 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors duration-200 text-sm font-medium">删除</button>
                </div>
                <input
                  type="file"
                  ref="editFileInput"
                  @change="handleEditFileSelect"
                  accept=".pdf,.doc,.docx,.ppt,.pptx"
                  class="hidden"
                />
                <button
                  type="button"
                  @click="editFileInput?.click()"
                  class="px-4 py-2 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
                >
                  上传资料
                </button>
              </div>
            </div>
          </div>
          <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
            <button type="button" @click="showEditModal = false" class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium">取消</button>
            <button type="submit" class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              保存
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 邀请学生模态框 -->
    <div v-if="showInviteStudentModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          邀请学生参加宣讲会
        </h2>
        
        <!-- 搜索和筛选 -->
        <div class="mb-6 space-y-4">
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">搜索学生（姓名/学号）</label>
              <input v-model="searchKeyword" type="text" @input="handleSearchStudents" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" placeholder="输入姓名或学号" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">院系</label>
              <select v-model="searchDepartmentId" @change="handleSearchStudents" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200">
                <option value="">全部</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">年级</label>
              <select v-model="searchGrade" @change="handleSearchStudents" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200">
                <option value="">全部</option>
                <option value="2021">2021级</option>
                <option value="2022">2022级</option>
                <option value="2023">2023级</option>
                <option value="2024">2024级</option>
                <option value="2025">2025级</option>
              </select>
            </div>
          </div>
          <button @click="handleSearchStudents" class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            搜索
          </button>
        </div>
        
        <!-- 学生列表 -->
        <div class="mb-4 border border-gray-200 rounded-xl max-h-96 overflow-y-auto">
          <div v-if="searchingStudents" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-3 text-gray-600">搜索中...</p>
          </div>
          <div v-else-if="searchStudentsList.length === 0" class="text-center py-12 text-gray-500">
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <p>暂无学生</p>
          </div>
          <div v-else class="divide-y divide-gray-200">
            <div v-for="student in searchStudentsList" :key="student.id" class="p-4 hover:bg-gray-50 transition-colors duration-200 flex items-center justify-between">
              <div class="flex-1">
                <div class="font-semibold text-gray-900">{{ student.real_name }}</div>
                <div class="text-sm text-gray-600 mt-1">学号: {{ student.student_id }} | 年级: {{ student.grade || '-' }} | 专业: {{ student.major || '-' }}</div>
              </div>
              <input
                type="checkbox"
                :value="student.id"
                v-model="selectedStudentIds"
                class="ml-4 w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
        
        <div class="mb-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
          <p class="text-sm font-semibold text-blue-900">已选择 <span class="text-blue-600 text-lg">{{ selectedStudentIds.length }}</span> 名学生</p>
        </div>
        
        <div class="pt-6 border-t border-gray-200 flex justify-end space-x-4">
          <button type="button" @click="closeInviteModal" class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium">取消</button>
          <button type="button" @click="handleInviteStudentsBatch" :disabled="selectedStudentIds.length === 0" class="px-6 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center disabled:opacity-50 disabled:cursor-not-allowed">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            批量邀请 ({{ selectedStudentIds.length }})
          </button>
        </div>
      </div>
    </div>

    <!-- 报名列表模态框 -->
    <div v-if="showRegistrationsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          报名列表
        </h2>
        <div v-if="registrations.length === 0" class="text-center py-12 text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p>暂无报名信息</p>
        </div>
        <div v-else class="space-y-3">
          <div v-for="reg in registrations" :key="reg.id" class="border border-gray-200 rounded-xl p-4 hover:bg-gray-50 transition-colors duration-200">
            <div class="flex justify-between items-center">
              <div>
                <p class="font-semibold text-gray-900">学生ID: {{ reg.student_id }}</p>
                <p class="text-sm text-gray-600 mt-1">状态: {{ reg.status }}</p>
                <p v-if="reg.check_in_time" class="text-sm text-gray-600 mt-1">签到时间: {{ new Date(reg.check_in_time).toLocaleString() }}</p>
              </div>
              <span :class="{
                'bg-yellow-100 text-yellow-800': reg.status === 'PENDING',
                'bg-green-100 text-green-800': reg.status === 'CONFIRMED',
                'bg-red-100 text-red-800': reg.status === 'CANCELLED',
                'bg-blue-100 text-blue-800': reg.status === 'CHECKED_IN'
              }" class="px-3 py-1 rounded-full text-xs font-medium">
                {{ reg.status }}
              </span>
            </div>
          </div>
        </div>
        <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end">
          <button @click="showRegistrationsModal = false" class="px-6 py-2.5 bg-gray-600 text-white rounded-xl hover:bg-gray-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium">关闭</button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="mt-6">
      <Pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        @change="handlePaginationChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getInfoSessions, createInfoSession, updateInfoSession, deleteInfoSession, getInfoSessionRegistrations, inviteStudentToInfoSession, searchStudents, inviteStudentsBatch, type InfoSession, type InfoSessionRegistration, type StudentSearchItem } from '@/api/infoSessions'
import { getDepartments, type Department } from '@/api/departments'
import { uploadDocument } from '@/api/upload'
import Pagination from '@/components/Pagination.vue'

// 宣讲会列表
const infoSessions = ref<InfoSession[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showRegistrationsModal = ref(false)
const showInviteStudentModal = ref(false)
const currentSession = ref<InfoSession | null>(null)
const currentInviteSessionId = ref<string | null>(null)
const inviteStudentId = ref('')
const registrations = ref<InfoSessionRegistration[]>([])
const searchKeyword = ref('')
const searchDepartmentId = ref('')
const searchGrade = ref('')
const searchStudentsList = ref<StudentSearchItem[]>([])
const selectedStudentIds = ref<string[]>([])
const searchingStudents = ref(false)
const departments = ref<Department[]>([])
const createFileInput = ref<HTMLInputElement | null>(null)
const editFileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

const createForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  session_type: 'OFFLINE',
  live_url: '',
  max_students: 0,
  materials: [] as string[],
})
const editForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  session_type: 'OFFLINE',
  live_url: '',
  max_students: 0,
  status: 'DRAFT',
  materials: [] as string[],
})

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 获取宣讲会类型文本
const getSessionTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    OFFLINE: '线下',
    ONLINE: '线上',
    HYBRID: '混合',
  }
  return typeMap[type] || type
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    ONGOING: '进行中',
    ENDED: '已结束',
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    DRAFT: 'bg-gray-100 text-gray-800',
    PUBLISHED: 'bg-green-100 text-green-800',
    ONGOING: 'bg-blue-100 text-blue-800',
    ENDED: 'bg-gray-100 text-gray-500',
  }
  return classMap[status] || ''
}

// 分页相关
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 加载宣讲会列表
const loadInfoSessions = async () => {
  loading.value = true
  try {
    const response = await getInfoSessions({ 
      page: currentPage.value,
      page_size: pageSize.value,
      status: undefined 
    })
    infoSessions.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载宣讲会列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadInfoSessions()
}

// 保存创建
const saveCreate = async () => {
  try {
    const response = await createInfoSession({
      ...createForm.value,
      start_time: new Date(createForm.value.start_time).toISOString(),
      end_time: new Date(createForm.value.end_time).toISOString(),
      materials: createForm.value.materials.length > 0 ? createForm.value.materials : undefined,
    })
    alert('创建成功！')
    showCreateModal.value = false
    createForm.value = {
      title: '',
      description: '',
      start_time: '',
      end_time: '',
      location: '',
      session_type: 'OFFLINE',
      live_url: '',
      max_students: 0,
      materials: [],
    }
    // 刷新列表
    await loadInfoSessions()
  } catch (error: any) {
    alert('创建失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 处理创建时的文件选择
const handleCreateFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  
  uploading.value = true
  try {
    const response = await uploadDocument(file, 'info_session')
    createForm.value.materials.push(response.url)
    alert('文件上传成功！')
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploading.value = false
    if (createFileInput.value) {
      createFileInput.value.value = ''
    }
  }
}

// 处理编辑时的文件选择
const handleEditFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  
  uploading.value = true
  try {
    const response = await uploadDocument(file, 'info_session')
    editForm.value.materials.push(response.url)
    alert('文件上传成功！')
  } catch (error: any) {
    alert('文件上传失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    uploading.value = false
    if (editFileInput.value) {
      editFileInput.value.value = ''
    }
  }
}

// 编辑宣讲会
const editInfoSession = (session: InfoSession) => {
  currentSession.value = session
  // 解析materials字段（可能是JSON字符串或数组）
  let materials: string[] = []
  if (session.materials) {
    if (typeof session.materials === 'string') {
      try {
        materials = JSON.parse(session.materials)
      } catch {
        materials = [session.materials]
      }
    } else if (Array.isArray(session.materials)) {
      materials = session.materials
    }
  }
  
  editForm.value = {
    title: session.title,
    description: session.description || '',
    start_time: session.start_time ? new Date(session.start_time).toISOString().slice(0, 16) : '',
    end_time: session.end_time ? new Date(session.end_time).toISOString().slice(0, 16) : '',
    location: session.location || '',
    session_type: session.session_type,
    live_url: session.live_url || '',
    max_students: session.max_students || 0,
    status: session.status,
    materials: materials
  }
  showEditModal.value = true
}

// 保存编辑
const saveEdit = async () => {
  if (!currentSession.value) return
  
  try {
    await updateInfoSession(currentSession.value.id, {
      ...editForm.value,
      start_time: new Date(editForm.value.start_time).toISOString(),
      end_time: new Date(editForm.value.end_time).toISOString(),
      materials: editForm.value.materials.length > 0 ? editForm.value.materials : undefined,
    })
    alert('更新成功！')
    showEditModal.value = false
    loadInfoSessions()
  } catch (error: any) {
    alert('更新失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 查看报名
const viewRegistrations = async (sessionId: string) => {
  try {
    registrations.value = await getInfoSessionRegistrations(sessionId)
    showRegistrationsModal.value = true
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || error.message
    if (error.response?.status === 403) {
      alert('权限不足：只能查看自己创建的宣讲会的报名信息。')
    } else {
      alert('加载报名信息失败: ' + errorMessage)
    }
  }
}

// 加载院系列表
const loadDepartments = async () => {
  try {
    const response = await getDepartments({ page_size: 100 })
    departments.value = response.items
  } catch (error) {
    console.error('加载院系列表失败:', error)
  }
}

// 显示邀请模态框
const showInviteModal = (sessionId: string) => {
  console.log('显示邀请模态框，sessionId:', sessionId)
  console.log('当前宣讲会列表:', infoSessions.value.map(s => ({ id: s.id, title: s.title })))
  if (!sessionId) {
    alert('宣讲会ID不存在，无法邀请学生')
    return
  }
  currentInviteSessionId.value = sessionId
  searchKeyword.value = ''
  searchDepartmentId.value = ''
  searchGrade.value = ''
  searchStudentsList.value = []
  selectedStudentIds.value = []
  showInviteStudentModal.value = true
  loadDepartments()
  handleSearchStudents()
}

// 关闭邀请模态框
const closeInviteModal = () => {
  showInviteStudentModal.value = false
  searchKeyword.value = ''
  searchDepartmentId.value = ''
  searchGrade.value = ''
  searchStudentsList.value = []
  selectedStudentIds.value = []
  currentInviteSessionId.value = null
}

// 搜索学生
const handleSearchStudents = async () => {
  // 搜索学生不需要session_id，可以独立搜索
  searchingStudents.value = true
  try {
    const response = await searchStudents({
      keyword: searchKeyword.value || undefined,
      department_id: searchDepartmentId.value || undefined,
      grade: searchGrade.value || undefined,
      page: 1,
      page_size: 100
    })
    searchStudentsList.value = response.items
  } catch (error: any) {
    console.error('搜索学生失败:', error)
    alert('搜索学生失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    searchingStudents.value = false
  }
}

// 批量邀请学生
const handleInviteStudentsBatch = async () => {
  if (!currentInviteSessionId.value || selectedStudentIds.value.length === 0) {
    alert('请选择要邀请的学生')
    return
  }
  
  console.log('开始批量邀请，session_id:', currentInviteSessionId.value)
  console.log('选中的学生IDs:', selectedStudentIds.value)
  
  // 验证session_id是否在列表中
  const sessionExists = infoSessions.value.some(s => s.id === currentInviteSessionId.value)
  if (!sessionExists) {
    console.error('宣讲会不在列表中！session_id:', currentInviteSessionId.value)
    console.error('当前列表中的宣讲会IDs:', infoSessions.value.map(s => s.id))
    alert('宣讲会不存在于当前列表中，请刷新页面后重试')
    return
  }
  
  try {
    const result = await inviteStudentsBatch(currentInviteSessionId.value, selectedStudentIds.value)
    alert(`邀请完成！成功: ${result.success_count}，失败: ${result.failed_count}`)
    if (result.failed_reasons.length > 0) {
      console.log('失败原因:', result.failed_reasons)
    }
    closeInviteModal()
    // 刷新报名列表
    if (showRegistrationsModal.value && currentInviteSessionId.value) {
      await viewRegistrations(currentInviteSessionId.value)
    }
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || error.message
    console.error('批量邀请失败:', error)
    console.error('session_id:', currentInviteSessionId.value)
    console.error('student_ids:', selectedStudentIds.value)
    console.error('错误响应:', error.response?.data)
    alert('批量邀请失败: ' + errorMessage)
  }
}

// 删除宣讲会
const handleDeleteInfoSession = async (sessionId: string) => {
  if (!confirm('确定要删除这个宣讲会吗？')) {
    return
  }
  try {
    await deleteInfoSession(sessionId)
    alert('删除成功！')
    loadInfoSessions()
  } catch (error: any) {
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadInfoSessions()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

