<template>
  <div class="sub-accounts-page w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
        <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        子账号管理
      </h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        创建子账号
      </button>
    </div>

    <!-- 子账号列表 -->
    <div class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="subAccounts.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <p class="text-lg">暂无子账号</p>
      </div>
      <div v-else>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">用户名</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">公司名称</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">联系方式</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">状态</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">创建时间</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="account in subAccounts" :key="account.id" class="hover:bg-gray-50 transition-colors duration-200">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ account.username }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ account.company_name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    {{ account.phone || '-' }}
                  </div>
                  <div class="text-xs text-gray-500 mt-1 flex items-center">
                    <svg class="w-3 h-3 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {{ account.email || '-' }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="getStatusClass(account.status)"
                    class="px-3 py-1 rounded-full text-xs font-medium"
                  >
                    {{ getStatusText(account.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ formatDate(account.created_at) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    @click="confirmDelete(account)"
                    class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
                  >
                    删除
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 分页 -->
        <div class="p-6 border-t border-gray-200 bg-gray-50">
          <Pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            @change="handlePaginationChange"
          />
        </div>
      </div>
    </div>

    <!-- 创建子账号模态框 -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showCreateModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <div class="p-8">
          <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            创建子账号
          </h2>
          <form @submit.prevent="saveSubAccount">
            <div class="space-y-5">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">
                  用户名 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="subAccountForm.username"
                  type="text"
                  required
                  minlength="3"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入用户名"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">
                  密码 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="subAccountForm.password"
                  type="password"
                  required
                  minlength="6"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入密码（至少6位）"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">
                  真实姓名 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="subAccountForm.real_name"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入真实姓名"
                />
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">手机号</label>
                  <input
                    v-model="subAccountForm.phone"
                    type="text"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                    placeholder="请输入手机号"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">邮箱</label>
                  <input
                    v-model="subAccountForm.email"
                    type="email"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                    placeholder="请输入邮箱"
                  />
                </div>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">职位</label>
                <input
                  v-model="subAccountForm.position"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入职位"
                />
              </div>
            </div>
            <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
              <button
                type="button"
                @click="showCreateModal = false"
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
                创建
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 删除确认模态框 -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full border border-gray-100">
        <div class="p-8">
          <div class="flex items-center mb-4">
            <div class="p-3 bg-red-50 rounded-full mr-4">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 class="text-xl font-bold text-gray-900">确认删除</h2>
          </div>
          <p class="text-gray-700 mb-6 ml-16">
            确定要删除子账号 "{{ accountToDelete?.username }}" 吗？此操作不可恢复。
          </p>
          <div class="flex justify-end space-x-4">
            <button
              @click="showDeleteModal = false"
              class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              取消
            </button>
            <button
              @click="handleDelete"
              class="px-6 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-md hover:shadow-lg transition-all duration-200 font-medium flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getSubAccounts,
  createSubAccount,
  deleteSubAccount,
  type EnterpriseSubAccount,
  type SubAccountCreate
} from '@/api/enterpriseManagement'
import Pagination from '@/components/Pagination.vue'

// 数据
const subAccounts = ref<EnterpriseSubAccount[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 模态框状态
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const accountToDelete = ref<EnterpriseSubAccount | null>(null)

// 表单数据
const subAccountForm = ref<SubAccountCreate>({
  username: '',
  password: '',
  real_name: '',
  phone: '',
  email: '',
  position: ''
})

// 获取状态文本
const getStatusText = (status?: string) => {
  const statusMap: Record<string, string> = {
    ACTIVE: '活跃',
    INACTIVE: '未激活',
    BANNED: '已禁用',
    PENDING: '待审批',
    REJECTED: '已拒绝'
  }
  return statusMap[status || ''] || status || '-'
}

// 获取状态样式
const getStatusClass = (status?: string) => {
  const classMap: Record<string, string> = {
    ACTIVE: 'bg-green-100 text-green-800',
    INACTIVE: 'bg-gray-100 text-gray-800',
    BANNED: 'bg-red-100 text-red-800',
    PENDING: 'bg-yellow-100 text-yellow-800',
    REJECTED: 'bg-red-100 text-red-800'
  }
  return classMap[status || ''] || 'bg-gray-100 text-gray-800'
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 加载子账号列表
const loadSubAccounts = async () => {
  loading.value = true
  try {
    const response = await getSubAccounts({
      page: currentPage.value,
      page_size: pageSize.value
    })
    subAccounts.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('加载子账号列表失败:', error)
    const errorMessage = error.response?.data?.detail || error.message
    if (error.response?.status === 403) {
      alert('权限不足：只有主账号才能查看子账号列表。如果您需要此功能，请联系管理员。')
    } else {
      alert('加载子账号列表失败: ' + errorMessage)
    }
  } finally {
    loading.value = false
  }
}

// 分页变化
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadSubAccounts()
}

// 保存子账号
const saveSubAccount = async () => {
  try {
    await createSubAccount(subAccountForm.value)
    alert('创建成功！')
    showCreateModal.value = false
    subAccountForm.value = {
      username: '',
      password: '',
      real_name: '',
      phone: '',
      email: '',
      position: ''
    }
    loadSubAccounts()
  } catch (error: any) {
    console.error('创建子账号失败:', error)
    const errorMessage = error.response?.data?.detail || error.message
    if (error.response?.status === 403) {
      alert('权限不足：只有主账号才能创建子账号。如果您需要此功能，请联系管理员。')
    } else {
      alert('创建失败: ' + errorMessage)
    }
  }
}

// 确认删除
const confirmDelete = (account: EnterpriseSubAccount) => {
  accountToDelete.value = account
  showDeleteModal.value = true
}

// 执行删除
const handleDelete = async () => {
  if (!accountToDelete.value) return
  
  try {
    await deleteSubAccount(accountToDelete.value.id)
    alert('删除成功！')
    showDeleteModal.value = false
    accountToDelete.value = null
    loadSubAccounts()
  } catch (error: any) {
    console.error('删除子账号失败:', error)
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadSubAccounts()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

