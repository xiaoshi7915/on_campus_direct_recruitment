<template>
  <div class="admin-users max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8 flex items-center">
      <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
      用户管理
    </h1>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        搜索和筛选
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索用户名、手机号、邮箱..."
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">用户类型</label>
          <select
            v-model="userTypeFilter"
            @change="handleSearch"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
          >
            <option value="">全部</option>
            <option value="STUDENT">学生</option>
            <option value="TEACHER">教师</option>
            <option value="ENTERPRISE">企业</option>
            <option value="ADMIN">管理员</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">状态</label>
          <select
            v-model="statusFilter"
            @change="handleSearch"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
          >
            <option value="">全部</option>
            <option value="ACTIVE">活跃</option>
            <option value="INACTIVE">未激活</option>
            <option value="BANNED">已封禁</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="handleSearch"
            class="w-full px-6 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center justify-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="users.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <p class="text-lg">暂无用户信息</p>
      </div>
      <div
        v-for="user in users"
        :key="user.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border border-gray-100"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ user.username }}</h3>
              <span
                :class="getUserTypeClass(user.user_type)"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ getUserTypeText(user.user_type) }}
              </span>
              <span
                :class="getStatusClass(user.status)"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ getStatusText(user.status) }}
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3 ml-11 space-y-1">
              <p v-if="user.phone" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                手机号：{{ user.phone }}
              </p>
              <p v-if="user.email" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                邮箱：{{ user.email }}
              </p>
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                注册时间：{{ formatDate(user.created_at) }}
              </p>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewUserDetail(user.id)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              查看详情
            </button>
            <button
              v-if="user.status === 'ACTIVE'"
              @click="handleBanUser(user.id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              封禁
            </button>
            <button
              v-else
              @click="handleUnbanUser(user.id)"
              class="px-5 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              解封
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getUsers, type User } from '@/api/users'
import Pagination from '@/components/Pagination.vue'

// 用户列表
const users = ref<User[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const userTypeFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)


// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 获取用户类型文本
const getUserTypeText = (userType: string) => {
  const typeMap: Record<string, string> = {
    STUDENT: '学生',
    TEACHER: '教师',
    ENTERPRISE: '企业',
    ADMIN: '管理员',
  }
  return typeMap[userType] || userType
}

// 获取用户类型样式
const getUserTypeClass = (userType: string) => {
  const classMap: Record<string, string> = {
    STUDENT: 'bg-blue-100 text-blue-800',
    TEACHER: 'bg-green-100 text-green-800',
    ENTERPRISE: 'bg-purple-100 text-purple-800',
    ADMIN: 'bg-red-100 text-red-800',
  }
  return classMap[userType] || 'bg-gray-100 text-gray-800'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    ACTIVE: '活跃',
    INACTIVE: '未激活',
    BANNED: '已封禁',
  }
  return statusMap[status] || status
}

// 获取状态样式
const getStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    ACTIVE: 'bg-green-100 text-green-800',
    INACTIVE: 'bg-yellow-100 text-yellow-800',
    BANNED: 'bg-red-100 text-red-800',
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// 搜索用户
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
    if (userTypeFilter.value) {
      params.user_type = userTypeFilter.value
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }

    const response = await getUsers(params)
    users.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('搜索用户失败:', error)
    // 显示错误信息
    let errorMessage = '获取用户列表失败'
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData === 'string') {
        errorMessage = errorData
      } else if (errorData.detail) {
        errorMessage = Array.isArray(errorData.detail) 
          ? errorData.detail.map((err: any) => err.msg || err).join(', ')
          : errorData.detail
      }
    }
    alert(errorMessage)
    users.value = []
    total.value = 0
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

// 查看用户详情
const viewUserDetail = (userId: string) => {
  // TODO: 打开用户详情窗口
  alert(`查看用户详情：${userId}`)
}

// 封禁用户
const handleBanUser = async (userId: string) => {
  if (!confirm('确定要封禁这个用户吗？')) {
    return
  }
  // TODO: 实现封禁功能
  alert('封禁功能开发中')
}

// 解封用户
const handleUnbanUser = async (userId: string) => {
  // TODO: 实现解封功能
  alert('解封功能开发中')
}

onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

