<template>
  <div class="admin-users">
    <h1 class="text-3xl font-bold mb-6">用户管理</h1>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索用户名、手机号、邮箱..."
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">用户类型</label>
          <select
            v-model="userTypeFilter"
            @change="handleSearch"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">全部</option>
            <option value="STUDENT">学生</option>
            <option value="TEACHER">教师</option>
            <option value="ENTERPRISE">企业</option>
            <option value="ADMIN">管理员</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
          <select
            v-model="statusFilter"
            @change="handleSearch"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
            class="w-full px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="users.length === 0" class="text-center py-12 text-gray-500">
        暂无用户信息
      </div>
      <div
        v-for="user in users"
        :key="user.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ user.username }}</h3>
              <span
                :class="getUserTypeClass(user.user_type)"
                class="px-2 py-1 rounded text-xs"
              >
                {{ getUserTypeText(user.user_type) }}
              </span>
              <span
                :class="getStatusClass(user.status)"
                class="px-2 py-1 rounded text-xs"
              >
                {{ getStatusText(user.status) }}
              </span>
            </div>
            <div class="text-gray-600 text-sm mb-3">
              <p v-if="user.phone">手机号：{{ user.phone }}</p>
              <p v-if="user.email">邮箱：{{ user.email }}</p>
              <p>注册时间：{{ formatDate(user.created_at) }}</p>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewUserDetail(user.id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看详情
            </button>
            <button
              v-if="user.status === 'ACTIVE'"
              @click="handleBanUser(user.id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              封禁
            </button>
            <button
              v-else
              @click="handleUnbanUser(user.id)"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
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
.admin-users {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

