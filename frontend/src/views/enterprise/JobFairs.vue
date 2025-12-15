<template>
  <div class="enterprise-job-fairs max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
        <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        双选会管理
      </h1>
      <div class="flex space-x-3">
        <button
          v-if="!showBrowseMode"
          @click="showMyRegistrations = !showMyRegistrations"
          :class="showMyRegistrations ? 'bg-green-600 hover:bg-green-700' : 'bg-gray-600 hover:bg-gray-700'"
          class="px-6 py-3 text-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 font-semibold"
        >
          {{ showMyRegistrations ? '我的报名' : '我创建的' }}
        </button>
        <button
          v-if="!showBrowseMode"
          @click="showCreateModal = true"
          class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          创建双选会
        </button>
        <button
          @click="showBrowseMode = !showBrowseMode"
          :class="showBrowseMode ? 'bg-purple-600 hover:bg-purple-700' : 'bg-gray-600 hover:bg-gray-700'"
          class="px-6 py-3 text-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 font-semibold"
        >
          {{ showBrowseMode ? '我创建的' : '浏览双选会' }}
        </button>
      </div>
    </div>

    <!-- 双选会列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="jobFairs.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="text-lg">{{ showBrowseMode ? '暂无可报名的双选会' : (showMyRegistrations ? '暂无报名的双选会' : '暂未创建双选会') }}</p>
      </div>
      <div
        v-for="jobFair in jobFairs"
        :key="jobFair.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border border-gray-100"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ jobFair.title }}</h3>
              <span
                :class="getStatusClass(jobFair.status)"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ getStatusText(jobFair.status) }}
              </span>
              <span v-if="(jobFair as any).check_in_time" class="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                已签到
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3 ml-11 space-y-1">
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                时间：{{ formatDateTime(jobFair.start_time) }} - {{ formatDateTime(jobFair.end_time) }}
              </p>
              <p v-if="jobFair.location" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                地点：{{ jobFair.location }}
              </p>
              <p v-if="jobFair.max_enterprises" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                最大企业数：{{ jobFair.max_enterprises }}
              </p>
              <p v-if="(jobFair as any).check_in_time" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                签到时间：{{ formatDateTime((jobFair as any).check_in_time) }}
              </p>
            </div>
            <p v-if="jobFair.description" class="text-gray-700 line-clamp-2 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ jobFair.description }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <template v-if="showMyRegistrations">
              <button
                v-if="!(jobFair as any).check_in_time"
                @click="handleCheckIn(jobFair.id)"
                class="px-4 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
              >
                签到
              </button>
              <button
                v-else
                disabled
                class="px-4 py-2 bg-gray-300 text-gray-600 rounded-xl cursor-not-allowed font-medium text-sm"
              >
                已签到
              </button>
            </template>
            <template v-else-if="showBrowseMode">
              <!-- 浏览模式：显示报名按钮 -->
              <button
                v-if="!registeredJobFairIds.has(jobFair.id)"
                @click="handleRegisterJobFair(jobFair.id)"
                :disabled="jobFair.status !== 'PUBLISHED'"
                class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                报名
              </button>
              <button
                v-else
                disabled
                class="px-4 py-2 bg-gray-300 text-gray-600 rounded-xl cursor-not-allowed font-medium text-sm"
              >
                已报名
              </button>
            </template>
            <template v-else>
              <button
                @click="editJobFair(jobFair)"
                class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
              >
                编辑
              </button>
              <button
                @click="viewRegistrations(jobFair.id)"
                class="px-4 py-2 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium text-sm"
              >
                查看报名
              </button>
              <button
                @click="handleDeleteJobFair(jobFair.id)"
                class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
              >
                删除
              </button>
            </template>
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
          创建双选会
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
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">最大企业数</label>
              <input v-model.number="createForm.max_enterprises" type="number" min="1" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
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
          编辑双选会
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
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">最大企业数</label>
              <input v-model.number="editForm.max_enterprises" type="number" min="1" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
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
                <p class="font-semibold text-gray-900">企业ID: {{ reg.enterprise_id }}</p>
                <p class="text-sm text-gray-600 mt-1">状态: {{ reg.status }}</p>
                <p v-if="reg.check_in_time" class="text-sm text-gray-600 mt-1">签到时间: {{ new Date(reg.check_in_time).toLocaleString() }}</p>
              </div>
              <span :class="{
                'bg-yellow-100 text-yellow-800': reg.status === 'PENDING',
                'bg-green-100 text-green-800': reg.status === 'APPROVED',
                'bg-red-100 text-red-800': reg.status === 'REJECTED',
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
import { ref, onMounted, computed, watch } from 'vue'
import { getJobFairs, createJobFair, updateJobFair, deleteJobFair, getJobFairRegistrations, getMyJobFairRegistrations, getMyCreatedJobFairs, checkInJobFair, registerJobFair, type JobFair, type JobFairRegistration } from '@/api/jobFairs'
import Pagination from '@/components/Pagination.vue'

// 双选会列表
const jobFairs = ref<JobFair[]>([])
const loading = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showRegistrationsModal = ref(false)
const showMyRegistrations = ref(false)
const showBrowseMode = ref(false) // 浏览模式：true=浏览所有双选会，false=我的双选会
const registeredJobFairIds = ref<Set<string>>(new Set()) // 已报名的双选会ID集合
const currentJobFair = ref<JobFair | null>(null)
const registrations = ref<JobFairRegistration[]>([])
const createForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  max_enterprises: 0,
})
const editForm = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  location: '',
  max_enterprises: 0,
  status: 'DRAFT'
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

// 加载双选会列表
const loadJobFairs = async () => {
  loading.value = true
  try {
    let response
    if (showBrowseMode.value) {
      // 浏览模式：加载所有已发布的双选会
      response = await getJobFairs({ 
        page: currentPage.value,
        page_size: pageSize.value,
        status: 'PUBLISHED' // 只显示已发布的
      })
      // 加载已报名的双选会ID列表
      try {
        const myRegistrations = await getMyJobFairRegistrations({ page: 1, page_size: 1000 })
        registeredJobFairIds.value = new Set(myRegistrations.items.map(jf => jf.id))
      } catch (error) {
        console.error('加载已报名列表失败:', error)
        registeredJobFairIds.value = new Set()
      }
    } else if (showMyRegistrations.value) {
      // 加载企业报名的双选会（只显示报名过的）
      response = await getMyJobFairRegistrations({ 
        page: currentPage.value,
        page_size: pageSize.value
      })
    } else {
      // 默认显示企业创建的双选会（使用专门的API）
      response = await getMyCreatedJobFairs({ 
        page: currentPage.value,
        page_size: pageSize.value
      })
    }
    jobFairs.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('加载双选会列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 双选会签到
const handleCheckIn = async (jobFairId: string) => {
  if (!confirm('确定要签到吗？')) {
    return
  }
  try {
    await checkInJobFair(jobFairId)
    alert('签到成功！')
    loadJobFairs()
  } catch (error: any) {
    alert('签到失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadJobFairs()
}

// 报名双选会
const handleRegisterJobFair = async (jobFairId: string) => {
  if (!confirm('确定要报名这个双选会吗？')) {
    return
  }
  try {
    await registerJobFair(jobFairId)
    alert('报名成功！')
    // 添加到已报名列表
    registeredJobFairIds.value.add(jobFairId)
    loadJobFairs()
  } catch (error: any) {
    alert('报名失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 监听显示模式变化
watch(showMyRegistrations, () => {
  currentPage.value = 1
  loadJobFairs()
})

watch(showBrowseMode, () => {
  currentPage.value = 1
  loadJobFairs()
})

// 保存创建
const saveCreate = async () => {
  try {
    await createJobFair({
      ...createForm.value,
      start_time: new Date(createForm.value.start_time).toISOString(),
      end_time: new Date(createForm.value.end_time).toISOString(),
    })
    alert('创建成功！')
    showCreateModal.value = false
    createForm.value = {
      title: '',
      description: '',
      start_time: '',
      end_time: '',
      location: '',
      max_enterprises: 0,
    }
    loadJobFairs()
  } catch (error: any) {
    alert('创建失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 编辑双选会
const editJobFair = (jobFair: JobFair) => {
  currentJobFair.value = jobFair
  editForm.value = {
    title: jobFair.title,
    description: jobFair.description || '',
    start_time: jobFair.start_time ? new Date(jobFair.start_time).toISOString().slice(0, 16) : '',
    end_time: jobFair.end_time ? new Date(jobFair.end_time).toISOString().slice(0, 16) : '',
    location: jobFair.location || '',
    max_enterprises: jobFair.max_enterprises || 0,
    status: jobFair.status
  }
  showEditModal.value = true
}

// 保存编辑
const saveEdit = async () => {
  if (!currentJobFair.value) return
  
  try {
    await updateJobFair(currentJobFair.value.id, {
      ...editForm.value,
      start_time: new Date(editForm.value.start_time).toISOString(),
      end_time: new Date(editForm.value.end_time).toISOString(),
    })
    alert('更新成功！')
    showEditModal.value = false
    loadJobFairs()
  } catch (error: any) {
    alert('更新失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 查看报名
const viewRegistrations = async (jobFairId: string) => {
  try {
    registrations.value = await getJobFairRegistrations(jobFairId)
    showRegistrationsModal.value = true
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || error.message
    if (error.response?.status === 403) {
      alert('权限不足：只能查看自己创建或已报名的双选会的报名信息。')
    } else {
      alert('加载报名信息失败: ' + errorMessage)
    }
  }
}

// 删除双选会
const handleDeleteJobFair = async (jobFairId: string) => {
  if (!confirm('确定要删除这个双选会吗？')) {
    return
  }
  try {
    await deleteJobFair(jobFairId)
    alert('删除成功！')
    loadJobFairs()
  } catch (error: any) {
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadJobFairs()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

