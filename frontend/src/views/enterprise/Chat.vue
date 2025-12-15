<template>
  <div class="enterprise-chat max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" style="height: calc(100vh - 120px);">
    <div class="flex h-full bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <!-- 会话列表 -->
      <div class="w-1/3 border-r border-gray-200 bg-gray-50 flex flex-col">
        <div class="p-6 border-b border-gray-200 bg-white">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            聊天
          </h2>
        </div>
        <div class="flex-1 overflow-y-auto">
          <div v-if="loading" class="p-8 text-center">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-3 text-gray-600">加载中...</p>
          </div>
          <div v-else-if="sessions.length === 0" class="p-8 text-center text-gray-500">
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <p class="text-sm">暂无聊天记录</p>
          </div>
          <div
            v-for="session in sessions"
            :key="session.id"
            @click="selectSession(session)"
            :class="[
              'p-4 border-b border-gray-200 cursor-pointer transition-all duration-200',
              currentSessionId === session.id ? 'bg-blue-50 border-l-4 border-l-blue-500' : 'hover:bg-gray-100'
            ]"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-gray-900 truncate">{{ getOtherUserName(session) }}</p>
                <p class="text-sm text-gray-500 truncate mt-1">
                  {{ session.last_message_at ? formatDate(session.last_message_at) : '暂无消息' }}
                </p>
              </div>
              <span
                v-if="getUnreadCount(session) > 0"
                class="ml-2 bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-[20px] text-center flex-shrink-0"
              >
                {{ getUnreadCount(session) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天窗口 -->
      <div class="flex-1 flex flex-col min-h-0 bg-white">
        <div v-if="!currentSession" class="flex-1 flex items-center justify-center text-gray-500 bg-gray-50">
          <div class="text-center">
            <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <p class="text-lg">请选择一个会话</p>
          </div>
        </div>
        <div v-else class="flex-1 flex flex-col min-h-0 overflow-hidden">
          <!-- 聊天头部 -->
          <div class="p-6 border-b border-gray-200 bg-white flex-shrink-0">
            <div class="flex justify-between items-center flex-wrap gap-3">
              <h3 class="text-xl font-bold text-gray-900">{{ getOtherUserName(currentSession) }}</h3>
              <!-- 快捷操作按钮 -->
              <div class="flex flex-wrap gap-2">
                <!-- 学生相关快捷操作 -->
                <template v-if="otherUserType === 'STUDENT'">
                  <button
                    @click="viewStudentResume"
                    class="px-4 py-2 text-sm bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="查看简历"
                  >
                    查看简历
                  </button>
                  <button
                    @click="markResume"
                    class="px-4 py-2 text-sm bg-yellow-600 text-white rounded-xl hover:bg-yellow-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="标记简历"
                  >
                    标记简历
                  </button>
                  <button
                    @click="toggleResumeFavorite"
                    :class="isResumeFavorited ? 'bg-red-600 hover:bg-red-700' : 'bg-gray-600 hover:bg-gray-700'"
                    class="px-4 py-2 text-sm text-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    :title="isResumeFavorited ? '取消收藏' : '收藏简历'"
                  >
                    {{ isResumeFavorited ? '已收藏' : '收藏简历' }}
                  </button>
                  <button
                    @click="downloadResume"
                    class="px-4 py-2 text-sm bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="下载简历"
                  >
                    下载简历
                  </button>
                  <button
                    @click="inviteToInfoSession"
                    class="px-4 py-2 text-sm bg-purple-600 text-white rounded-xl hover:bg-purple-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="宣讲会邀请"
                  >
                    宣讲会邀请
                  </button>
                  <button
                    @click="inviteToInterview"
                    class="px-4 py-2 text-sm bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="面试邀请"
                  >
                    面试邀请
                  </button>
                </template>
                <!-- 学校相关快捷操作（直接与学校聊天或通过教师） -->
                <template v-else-if="otherUserType === 'SCHOOL' || (otherUserType === 'TEACHER' && teacherSchoolId)">
                  <button
                    @click="viewSchoolDetail"
                    class="px-4 py-2 text-sm bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="查看学校主页"
                  >
                    查看学校
                  </button>
                  <button
                    @click="markSchool"
                    class="px-4 py-2 text-sm bg-yellow-600 text-white rounded-xl hover:bg-yellow-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="标记学校"
                  >
                    标记学校
                  </button>
                  <button
                    @click="toggleSchoolFavorite"
                    :class="isSchoolFavorited ? 'bg-red-600 hover:bg-red-700' : 'bg-gray-600 hover:bg-gray-700'"
                    class="px-4 py-2 text-sm text-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    :title="isSchoolFavorited ? '取消收藏' : '收藏学校'"
                  >
                    {{ isSchoolFavorited ? '已收藏' : '收藏学校' }}
                  </button>
                  <button
                    @click="shareSchool"
                    class="px-4 py-2 text-sm bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="分享学校"
                  >
                    分享学校
                  </button>
                  <button
                    @click="requestOfflineInfoSession"
                    class="px-4 py-2 text-sm bg-purple-600 text-white rounded-xl hover:bg-purple-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium"
                    title="申请线下宣讲会"
                  >
                    申请宣讲会
                  </button>
                </template>
                <!-- 调试信息（开发时可见） -->
                <div v-if="!otherUserType || otherUserType === 'UNKNOWN'" class="text-xs text-gray-500 px-3 py-2 bg-gray-100 rounded-xl">
                  用户类型: {{ otherUserType || '未设置' }}
                </div>
              </div>
            </div>
          </div>

          <!-- 消息列表 -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 bg-gray-50 min-h-0">
            <div v-if="messagesLoading" class="text-center py-8">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p class="mt-3 text-gray-600">加载中...</p>
            </div>
            <div v-else-if="messages.length === 0" class="text-center py-12 text-gray-500">
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p>暂无消息</p>
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="message in messages"
                :key="message.id"
                :class="[
                  'flex',
                  message.sender_id === currentUserId ? 'justify-end' : 'justify-start'
                ]"
              >
                <div
                  :class="[
                    'max-w-xs lg:max-w-md px-4 py-3 rounded-xl shadow-sm',
                    message.sender_id === currentUserId
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-800 border border-gray-200'
                  ]"
                >
                  <p class="break-words">{{ message.content }}</p>
                  <p
                    :class="[
                      'text-xs mt-2',
                      message.sender_id === currentUserId ? 'text-blue-100' : 'text-gray-500'
                    ]"
                  >
                    {{ formatDateTime(message.created_at) }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入框 -->
          <div class="p-6 border-t border-gray-200 bg-white flex-shrink-0">
            <form @submit.prevent="handleSendMessage" class="flex space-x-3">
              <input
                v-model="messageContent"
                type="text"
                placeholder="输入消息..."
                class="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
              <button
                type="submit"
                class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                发送
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- 标记简历模态框 -->
    <div v-if="showMarkResumeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          标记简历
        </h2>
        <form @submit.prevent="saveResumeMark" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">备注</label>
            <textarea
              v-model="markForm.note"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">标记颜色</label>
            <select
              v-model="markForm.color"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            >
              <option value="blue">蓝色</option>
              <option value="red">红色</option>
              <option value="green">绿色</option>
              <option value="yellow">黄色</option>
            </select>
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showMarkResumeModal = false"
              class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
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

    <!-- 标记学校模态框 -->
    <div v-if="showMarkSchoolModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          标记学校
        </h2>
        <form @submit.prevent="saveSchoolMark" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">备注</label>
            <textarea
              v-model="markForm.note"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">标记颜色</label>
            <select
              v-model="markForm.color"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            >
              <option value="blue">蓝色</option>
              <option value="red">红色</option>
              <option value="green">绿色</option>
              <option value="yellow">黄色</option>
            </select>
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showMarkSchoolModal = false"
              class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
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

    <!-- 宣讲会邀请模态框 -->
    <div v-if="showInviteInfoSessionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full max-h-96 overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          选择宣讲会
        </h2>
        <div v-if="infoSessions.length === 0" class="text-center py-8 text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <p>暂无可邀请的宣讲会</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="session in infoSessions"
            :key="session.id"
            class="p-4 border-2 border-gray-200 rounded-xl hover:border-purple-300 hover:bg-purple-50 cursor-pointer transition-all duration-200"
            @click="submitInfoSessionInvite(session.id)"
          >
            <h3 class="font-semibold text-gray-900 mb-1">{{ session.title }}</h3>
            <p class="text-sm text-gray-600">{{ new Date(session.start_time).toLocaleString('zh-CN') }}</p>
          </div>
        </div>
        <div class="mt-6 pt-4 border-t border-gray-200 flex justify-end">
          <button
            @click="showInviteInfoSessionModal = false"
            class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
          >
            取消
          </button>
        </div>
      </div>
    </div>

    <!-- 面试邀请模态框 -->
    <div v-if="showInviteInterviewModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full max-h-96 overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          选择申请
        </h2>
        <div v-if="applications.length === 0" class="text-center py-8 text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>暂无可邀请的申请</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="app in applications"
            :key="app.id"
            class="p-4 border-2 border-gray-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50 cursor-pointer transition-all duration-200"
            @click="submitInterviewInvite(app.id)"
          >
            <h3 class="font-semibold text-gray-900 mb-1">{{ app.job_title || '职位' }}</h3>
            <p class="text-sm text-gray-600">申请时间：{{ new Date(app.created_at).toLocaleString('zh-CN') }}</p>
          </div>
        </div>
        <div class="mt-6 pt-4 border-t border-gray-200 flex justify-end">
          <button
            @click="showInviteInterviewModal = false"
            class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
          >
            取消
          </button>
        </div>
      </div>
    </div>

    <!-- 申请线下宣讲会模态框 -->
    <div v-if="showRequestInfoSessionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          申请线下宣讲会
        </h2>
        <form @submit.prevent="submitRequestInfoSession" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">宣讲会标题 *</label>
            <input
              v-model="requestForm.title"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
            <textarea
              v-model="requestForm.description"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
            />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">建议开始时间 *</label>
              <input
                v-model="requestForm.proposed_start_time"
                type="datetime-local"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">建议结束时间 *</label>
              <input
                v-model="requestForm.proposed_end_time"
                type="datetime-local"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">建议地点</label>
            <input
              v-model="requestForm.proposed_location"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">最大学生数</label>
            <input
              v-model.number="requestForm.max_students"
              type="number"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">联系人</label>
              <input
                v-model="requestForm.contact_person"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">联系电话</label>
              <input
                v-model="requestForm.contact_phone"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">联系邮箱</label>
              <input
                v-model="requestForm.contact_email"
                type="email"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">申请留言</label>
            <textarea
              v-model="requestForm.message"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
            />
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showRequestInfoSessionModal = false"
              class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              提交申请
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCurrentUser, type User } from '@/api/users'
import {
  getChatSessions,
  getSessionMessages,
  type ChatSession,
  type Message,
} from '@/api/chat'
import { getStudentProfile, type StudentProfile } from '@/api/profile'
import { getTeacherProfile, type TeacherProfile } from '@/api/profile'
import { getResumes, type Resume } from '@/api/resumes'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'
import { getMark, createMark, updateMark, deleteMark, type Mark, type MarkCreateRequest } from '@/api/marks'
import { getSchool, getSchoolShareLink, requestOfflineInfoSession as requestOfflineInfoSessionAPI, type School, type OfflineInfoSessionRequest } from '@/api/schools'
import { downloadResume as downloadResumeAPI } from '@/api/resumes'
import { inviteStudentToInfoSession, searchStudents } from '@/api/infoSessions'
import { createInterview, type InterviewCreateRequest } from '@/api/interviews'
import { getInfoSessions } from '@/api/infoSessions'
import { getApplications } from '@/api/applications'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

// 会话列表
const sessions = ref<ChatSession[]>([])
const currentSession = ref<ChatSession | null>(null)
const currentSessionId = ref<string | null>(null)
const currentUserId = ref<string>('')
const loading = ref(false)
const messagesLoading = ref(false)

// 消息列表
const messages = ref<Message[]>([])
const messageContent = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 对方用户信息
const otherUser = ref<User | null>(null)
const otherUserType = ref<string>('')
const otherStudentProfile = ref<StudentProfile | null>(null)
const otherTeacherProfile = ref<TeacherProfile | null>(null)
const teacherSchoolId = ref<string | null>(null)
const studentResumes = ref<Resume[]>([])
const defaultResume = ref<Resume | null>(null)
const isResumeFavorited = ref(false)
const isSchoolFavorited = ref(false)
const currentResumeMark = ref<Mark | null>(null)
const currentSchoolMark = ref<Mark | null>(null)

// 模态框状态
const showMarkResumeModal = ref(false)
const showMarkSchoolModal = ref(false)
const showInviteInfoSessionModal = ref(false)
const showInviteInterviewModal = ref(false)
const showRequestInfoSessionModal = ref(false)
const markForm = ref({ note: '', color: 'blue' })
const infoSessions = ref<any[]>([])
const applications = ref<any[]>([])
const currentInviteUserId = ref<string | null>(null)  // 当前邀请的用户ID
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

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 获取对方用户名
const getOtherUserName = (session: ChatSession) => {
  // 如果是与学校聊天，显示学校名称
  if (session.school_id && session.school_name) {
    return session.school_name
  }
  // 如果是与用户聊天，显示用户名
  if (session.user1_id === currentUserId.value) {
    return session.user2_name || session.user2_id
  } else {
    return session.user1_name || session.user1_id
  }
}

// 获取未读消息数
const getUnreadCount = (session: ChatSession) => {
  return session.user1_id === currentUserId.value
    ? session.unread_count_user1
    : session.unread_count_user2
}

// 加载会话列表
const loadSessions = async () => {
  loading.value = true
  try {
    const response = await getChatSessions()
    sessions.value = response.items
  } catch (error) {
    console.error('加载会话列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取对方用户ID
const getOtherUserId = computed(() => {
  if (!currentSession.value) return null
  return currentSession.value.user1_id === currentUserId.value
    ? currentSession.value.user2_id
    : currentSession.value.user1_id
})

// 加载对方用户信息
const loadOtherUserInfo = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId || !currentSession.value) return

  try {
    // 如果是与学校聊天
    if (currentSession.value.school_id) {
      otherUserType.value = 'SCHOOL'
      teacherSchoolId.value = currentSession.value.school_id
    } else {
      // 如果是与用户聊天，从会话信息中获取对方用户类型
      const otherUserTypeFromSession = currentSession.value.user1_id === currentUserId.value
        ? currentSession.value.user2_type
        : currentSession.value.user1_type
      
      otherUserType.value = otherUserTypeFromSession || 'UNKNOWN'
      
      // 调试信息
      console.log('对方用户类型:', otherUserType.value, '会话信息:', {
        user1_type: currentSession.value.user1_type,
        user2_type: currentSession.value.user2_type,
        user1_id: currentSession.value.user1_id,
        user2_id: currentSession.value.user2_id,
        currentUserId: currentUserId.value
      })
      
      // 如果是教师，尝试获取学校ID
      if (otherUserType.value === 'TEACHER') {
        // 通过教师档案获取学校ID（需要调用API）
        // 暂时先设置为null，后续可以通过API获取
        teacherSchoolId.value = null
      }
    }
    
    // 根据用户类型加载相应的信息
    if (otherUserType.value === 'STUDENT') {
      // 对于学生，加载简历信息
      await loadStudentResumes()
    } else if (otherUserType.value === 'TEACHER') {
      // 对于教师，如果会话中有school_id，使用它
      if (currentSession.value.school_id) {
        teacherSchoolId.value = currentSession.value.school_id
      } else {
        // 如果没有school_id，尝试从会话信息中获取
        // 注意：这需要后端API返回school_id
        teacherSchoolId.value = null
      }
    }
  } catch (error) {
    console.error('加载对方用户信息失败:', error)
  }
}

// 加载学生简历（通过user_id查找）
const loadStudentResumes = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) return
  
  try {
    // 通过user_id获取简历（后端API已支持）
    const response = await getResumes({ user_id: otherUserId, page_size: 10 })
    studentResumes.value = response.items
    defaultResume.value = response.items.find(r => r.is_default) || response.items[0] || null
    
    // 检查默认简历的收藏状态
    if (defaultResume.value) {
      try {
        isResumeFavorited.value = await checkFavorite('RESUME', defaultResume.value.id)
      } catch {
        isResumeFavorited.value = false
      }
      
      // 检查默认简历的标记
      try {
        currentResumeMark.value = await getMark('RESUME', defaultResume.value.id)
        if (currentResumeMark.value) {
          markForm.value.note = currentResumeMark.value.note || ''
          markForm.value.color = currentResumeMark.value.color || 'blue'
        }
      } catch {
        currentResumeMark.value = null
      }
    }
  } catch (error) {
    console.error('加载学生简历失败:', error)
  }
}

// 选择会话
const selectSession = async (session: ChatSession) => {
  currentSession.value = session
  currentSessionId.value = session.id
  await loadMessages(session.id)
  await loadOtherUserInfo()
}

// 加载消息
const loadMessages = async (sessionId: string) => {
  messagesLoading.value = true
  try {
    const response = await getSessionMessages(sessionId, {
      page: 1,
      page_size: 50,
    })
    messages.value = response.items.reverse()
    
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('加载消息失败:', error)
  } finally {
    messagesLoading.value = false
  }
}

// 发送消息
const handleSendMessage = async () => {
  if (!messageContent.value.trim() || !currentSession.value) return

  try {
    const { sendMessage: sendMessageAPI } = await import('@/api/chat')
    const newMessage = await sendMessageAPI(currentSession.value.id, {
      receiver_id:
        currentSession.value.user1_id === currentUserId.value
          ? currentSession.value.user2_id
          : currentSession.value.user1_id,
      content: messageContent.value,
    })
    messages.value.push(newMessage)
    messageContent.value = ''
    
    await nextTick()
    scrollToBottom()
    
    loadSessions()
  } catch (error: any) {
    alert(error.response?.data?.detail || '发送失败，请稍后重试')
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

// ==================== 学生相关快捷操作 ====================

// 查看学生简历
const viewStudentResume = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  // 先加载简历
  if (studentResumes.value.length === 0) {
    await loadStudentResumes()
  }
  
  if (defaultResume.value) {
    // 打开新窗口查看简历
    window.open(`/enterprise/resumes/${defaultResume.value.id}`, '_blank')
  } else {
    alert('该学生暂无简历')
  }
}

// 标记简历
const markResume = () => {
  if (!defaultResume.value) {
    alert('该学生暂无简历')
    return
  }
  showMarkResumeModal.value = true
}

// 保存简历标记
const saveResumeMark = async () => {
  if (!defaultResume.value) return
  
  try {
    const markData: MarkCreateRequest = {
      target_type: 'RESUME',
      target_id: defaultResume.value.id,
      note: markForm.value.note,
      color: markForm.value.color
    }
    
    if (currentResumeMark.value) {
      await updateMark(currentResumeMark.value.id, {
        note: markForm.value.note,
        color: markForm.value.color
      })
    } else {
      currentResumeMark.value = await createMark(markData)
    }
    
    alert('标记已保存')
    showMarkResumeModal.value = false
  } catch (error: any) {
    alert('保存标记失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 切换简历收藏状态
const toggleResumeFavorite = async () => {
  if (!defaultResume.value) {
    alert('该学生暂无简历')
    return
  }
  
  try {
    if (isResumeFavorited.value) {
      await removeFavorite('RESUME', defaultResume.value.id)
      isResumeFavorited.value = false
      alert('已取消收藏')
    } else {
      await addFavorite('RESUME', defaultResume.value.id)
      isResumeFavorited.value = true
      alert('已收藏')
    }
  } catch (error: any) {
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 下载简历
const downloadResume = async () => {
  if (!defaultResume.value) {
    alert('该学生暂无简历')
    return
  }
  
  try {
    await downloadResumeAPI(defaultResume.value.id)
    alert('简历下载成功')
  } catch (error: any) {
    alert('下载失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 获取学生ID（通过user_id）
const getStudentIdByUserId = async (userId: string): Promise<string | null> => {
  try {
    // 通过简历API获取简历列表，然后找到对应的student_id
    // 注意：这需要后端API支持通过user_id查询，或者我们需要其他方式
    const resumesResponse = await getResumes({ page_size: 100 })
    
    // 由于无法直接通过user_id查询student_id，我们需要通过其他方式
    // 暂时返回null，让用户知道需要学生信息
    // TODO: 需要后端API支持通过user_id查询student_id
    return null
  } catch (error) {
    console.error('获取学生ID失败:', error)
    return null
  }
}

// 宣讲会邀请
const inviteToInfoSession = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  // 加载宣讲会列表
  try {
    const response = await getInfoSessions({ page_size: 100 })
    infoSessions.value = response.items.filter(s => s.status === 'PUBLISHED')
    
    // 存储当前用户ID，用于邀请时查找学生ID
    currentInviteUserId.value = otherUserId
    showInviteInfoSessionModal.value = true
  } catch (error: any) {
    alert('加载宣讲会列表失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 提交宣讲会邀请
const submitInfoSessionInvite = async (sessionId: string) => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  try {
    // 使用user_id邀请（后端API会转换为student_id）
    await inviteStudentToInfoSession(sessionId, undefined, otherUserId)
    alert('邀请成功')
    showInviteInfoSessionModal.value = false
  } catch (error: any) {
    alert('邀请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 面试邀请
const inviteToInterview = async () => {
  const otherUserId = getOtherUserId.value
  if (!otherUserId) {
    alert('无法获取用户信息')
    return
  }
  
  // 加载申请列表（通过user_id查找）
  try {
    // 通过user_id查找申请（后端API已支持）
    const response = await getApplications({ user_id: otherUserId, page_size: 100 })
    applications.value = response.items.filter(a => a.status === 'ACCEPTED')
    
    if (applications.value.length === 0) {
      alert('该学生暂无已通过的申请，无法安排面试')
      return
    }
    
    showInviteInterviewModal.value = true
  } catch (error: any) {
    alert('加载申请列表失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 提交面试邀请
const submitInterviewInvite = async (applicationId: string) => {
  try {
    router.push(`/enterprise/interviews/create?application_id=${applicationId}`)
    showInviteInterviewModal.value = false
  } catch (error: any) {
    alert('跳转失败: ' + (error.response?.data?.detail || error.message))
  }
}

// ==================== 学校相关快捷操作 ====================

// 查看学校详情
const viewSchoolDetail = () => {
  if (teacherSchoolId.value) {
    router.push(`/enterprise/schools/${teacherSchoolId.value}`)
  } else {
    alert('该教师未关联学校')
  }
}

// 标记学校
const markSchool = () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  showMarkSchoolModal.value = true
}

// 保存学校标记
const saveSchoolMark = async () => {
  if (!teacherSchoolId.value) return
  
  try {
    const markData: MarkCreateRequest = {
      target_type: 'SCHOOL',
      target_id: teacherSchoolId.value,
      note: markForm.value.note,
      color: markForm.value.color
    }
    
    if (currentSchoolMark.value) {
      await updateMark(currentSchoolMark.value.id, {
        note: markForm.value.note,
        color: markForm.value.color
      })
    } else {
      currentSchoolMark.value = await createMark(markData)
    }
    
    alert('标记已保存')
    showMarkSchoolModal.value = false
  } catch (error: any) {
    alert('保存标记失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 切换学校收藏状态
const toggleSchoolFavorite = async () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  
  try {
    if (isSchoolFavorited.value) {
      await removeFavorite('SCHOOL', teacherSchoolId.value)
      isSchoolFavorited.value = false
      alert('已取消收藏')
    } else {
      await addFavorite('SCHOOL', teacherSchoolId.value)
      isSchoolFavorited.value = true
      alert('已收藏')
    }
  } catch (error: any) {
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 分享学校
const shareSchool = async () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  
  try {
    const shareData = await getSchoolShareLink(teacherSchoolId.value)
    
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(shareData.share_url)
      alert('分享链接已复制到剪贴板')
    } else {
      prompt('分享链接（请复制）：', shareData.share_url)
    }
  } catch (error: any) {
    alert('获取分享链接失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 申请线下宣讲会
const requestOfflineInfoSession = () => {
  if (!teacherSchoolId.value) {
    alert('该教师未关联学校')
    return
  }
  
  requestForm.value = {
    school_id: teacherSchoolId.value,
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

// 提交申请线下宣讲会
const submitRequestInfoSession = async () => {
  if (!teacherSchoolId.value) return
  
  try {
    await requestOfflineInfoSessionAPI(teacherSchoolId.value, requestForm.value)
    alert('申请已提交')
    showRequestInfoSessionModal.value = false
  } catch (error: any) {
    alert('申请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 初始化聊天（处理URL参数）
const initChat = async () => {
  try {
    const user = await getCurrentUser()
    currentUserId.value = user.id
    
    // 加载会话列表
    await loadSessions()
    
    // 检查URL参数中是否有user_id或student_id（从人才搜索发起聊天）
    const userIdParam = route.query.user_id as string
    const studentIdParam = route.query.student_id as string
    
    if (userIdParam || studentIdParam) {
      // 创建或获取聊天会话
      try {
        const { createOrGetChatSession } = await import('@/api/chat')
        let session
        
        if (studentIdParam) {
          // 如果提供了student_id，使用student_id创建会话
          // 后端API会将其转换为user_id
          session = await createOrGetChatSession('', studentIdParam)
        } else {
          // 使用user_id创建会话
          session = await createOrGetChatSession(userIdParam)
        }
        
        // 刷新会话列表
        await loadSessions()
        
        // 选择该会话
        await selectSession(session)
        
        // 清除URL参数
        router.replace({ path: route.path, query: {} })
      } catch (error: any) {
        console.error('创建聊天会话失败:', error)
        alert('创建聊天会话失败: ' + (error.response?.data?.detail || error.message))
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

onMounted(() => {
  initChat()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

