<template>
  <div class="sub-accounts-page">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">子账号管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        创建子账号
      </button>
    </div>

    <!-- 子账号列表 -->
    <div class="bg-white rounded-lg shadow">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="subAccounts.length === 0" class="text-center py-12 text-gray-500">
        暂无子账号
      </div>
      <div v-else>
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">用户名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">真实姓名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">联系方式</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">职称/职务</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="account in subAccounts" :key="account.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ account.username }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ account.real_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>{{ account.phone || '-' }}</div>
                <div class="text-xs text-gray-400">{{ account.email || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>{{ account.title || '-' }}</div>
                <div class="text-xs text-gray-400">{{ account.position || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="getStatusClass(account.status)"
                  class="px-2 py-1 rounded text-xs font-medium"
                >
                  {{ getStatusText(account.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="confirmDelete(account)"
                  class="text-red-600 hover:text-red-900"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分页 -->
        <div class="p-4 border-t">
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
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showCreateModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4 text-gray-900">创建子账号</h2>
          <form @submit.prevent="saveSubAccount">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  用户名 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="subAccountForm.username"
                  type="text"
                  required
                  minlength="3"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入用户名"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  密码 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="subAccountForm.password"
                  type="password"
                  required
                  minlength="6"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入密码（至少6位）"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  真实姓名 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="subAccountForm.real_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入真实姓名"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">手机号</label>
                <input
                  v-model="subAccountForm.phone"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入手机号"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
                <input
                  v-model="subAccountForm.email"
                  type="email"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入邮箱"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">职称</label>
                <input
                  v-model="subAccountForm.title"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入职称"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">职务名称</label>
                <input
                  v-model="subAccountForm.position"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入职务名称"
                />
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-4">
              <button
                type="button"
                @click="showCreateModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
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
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-4 text-gray-900">确认删除</h2>
          <p class="text-gray-700 mb-6">
            确定要删除子账号 "{{ accountToDelete?.username }}" 吗？此操作不可恢复。
          </p>
          <div class="flex justify-end space-x-4">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              取消
            </button>
            <button
              @click="handleDelete"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
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
  type Teacher,
  type SubAccountCreate
} from '@/api/teacherManagement'
import Pagination from '@/components/Pagination.vue'

// 数据
const subAccounts = ref<Teacher[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 模态框状态
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const accountToDelete = ref<Teacher | null>(null)

// 表单数据
const subAccountForm = ref<SubAccountCreate>({
  username: '',
  password: '',
  real_name: '',
  phone: '',
  email: '',
  title: '',
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
    alert('加载子账号列表失败: ' + (error.response?.data?.detail || error.message))
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
      title: '',
      position: ''
    }
    loadSubAccounts()
  } catch (error: any) {
    console.error('创建子账号失败:', error)
    alert('创建失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 确认删除
const confirmDelete = (account: Teacher) => {
  accountToDelete.value = account
  showDeleteModal.value = true
}

// 删除子账号
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
.sub-accounts-page {
  max-width: 1400px;
  margin: 0 auto;
}
</style>

