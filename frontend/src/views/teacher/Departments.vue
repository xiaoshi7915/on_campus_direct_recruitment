<template>
  <div class="departments-page max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
        <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        院系信息管理
      </h1>
      <button
        @click="showCreateModal = true"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        创建院系
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-xl shadow-md border border-gray-100 p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">关键词搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索院系名称或代码"
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">学校ID</label>
          <input
            v-model="schoolIdFilter"
            type="text"
            placeholder="筛选学校ID"
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @keyup.enter="handleSearch"
          />
        </div>
        <div class="flex items-end">
          <button
            @click="handleSearch"
            class="w-full px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center justify-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 院系列表 -->
    <div class="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="departments.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <p class="text-lg">暂无院系信息</p>
      </div>
      <div v-else>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">院系名称</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">院系代码</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">描述</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">资质荣誉</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="dept in departments" :key="dept.id" class="hover:bg-gray-50 transition-colors duration-200">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ dept.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ dept.code || '-' }}</td>
                <td class="px-6 py-4 text-sm text-gray-600">
                  <div class="max-w-xs truncate">{{ dept.description || '-' }}</div>
                </td>
                <td class="px-6 py-4 text-sm text-gray-600">
                  <div class="max-w-xs truncate">{{ dept.honors || '-' }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center space-x-3">
                    <button
                      @click="editDepartment(dept)"
                      class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
                    >
                      编辑
                    </button>
                    <button
                      @click="confirmDelete(dept)"
                      class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
                    >
                      删除
                    </button>
                  </div>
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

    <!-- 创建/编辑模态框 -->
    <div
      v-if="showCreateModal || showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <div class="p-8">
          <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            {{ showEditModal ? '编辑院系' : '创建院系' }}
          </h2>
          <form @submit.prevent="saveDepartment">
            <div class="space-y-5">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">
                  院系名称 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="departmentForm.name"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入院系名称"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">院系代码</label>
                <input
                  v-model="departmentForm.code"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                  placeholder="请输入院系代码"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
                <textarea
                  v-model="departmentForm.description"
                  rows="4"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
                  placeholder="请输入院系描述"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">资质荣誉</label>
                <textarea
                  v-model="departmentForm.honors"
                  rows="4"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
                  placeholder="请输入资质荣誉信息"
                ></textarea>
              </div>
            </div>
            <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
              <button
                type="button"
                @click="closeModal"
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
            确定要删除院系 "{{ departmentToDelete?.name }}" 吗？此操作不可恢复。
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

    <!-- 院校实名认证模态框 -->
    <div
      v-if="showVerificationModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showVerificationModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <div class="p-8">
          <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            院校实名认证
          </h2>
          <div v-if="school" class="mb-6 p-4 bg-gray-50 rounded-xl border border-gray-200">
            <p class="text-sm text-gray-600 mb-2">当前学校：<strong class="text-gray-900">{{ school.name }}</strong></p>
            <p class="text-sm text-gray-600">认证状态：<span :class="school.is_verified ? 'text-green-600 font-semibold' : 'text-yellow-600 font-semibold'">{{ school.is_verified ? '已认证' : '未认证' }}</span></p>
          </div>
          <form @submit.prevent="handleVerification">
            <div class="space-y-5">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">认证材料</label>
                <textarea
                  v-model="verificationForm.verification_documents"
                  rows="4"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
                  placeholder="请描述或上传认证材料（如：营业执照、组织机构代码证等）"
                ></textarea>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">联系人</label>
                  <input
                    v-model="verificationForm.contact_person"
                    type="text"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                    placeholder="请输入联系人姓名"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">联系电话</label>
                  <input
                    v-model="verificationForm.contact_phone"
                    type="text"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                    placeholder="请输入联系电话"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">联系邮箱</label>
                  <input
                    v-model="verificationForm.contact_email"
                    type="email"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
                    placeholder="请输入联系邮箱"
                  />
                </div>
              </div>
            </div>
            <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
              <button
                type="button"
                @click="showVerificationModal = false"
                class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium"
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
                提交认证申请
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getDepartments,
  createDepartment,
  updateDepartment,
  deleteDepartment,
  type Department,
  type DepartmentCreate,
  type DepartmentUpdate
} from '@/api/departments'
import {
  getMySchool,
  requestSchoolVerification,
  type School,
  type SchoolVerificationRequest
} from '@/api/schools'
import Pagination from '@/components/Pagination.vue'

// 数据
const departments = ref<Department[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索和筛选
const searchKeyword = ref('')
const schoolIdFilter = ref('')

// 学校信息
const school = ref<School | null>(null)
const loadingSchool = ref(false)

// 模态框状态
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showVerificationModal = ref(false)
const departmentToDelete = ref<Department | null>(null)

// 认证表单
const verificationForm = ref<SchoolVerificationRequest>({
  verification_documents: '',
  contact_person: '',
  contact_phone: '',
  contact_email: ''
})

// 表单数据
const departmentForm = ref<DepartmentCreate>({
  name: '',
  code: '',
  description: '',
  honors: ''
})

const editingDepartmentId = ref<string | null>(null)

// 加载学校信息
const loadSchool = async () => {
  loadingSchool.value = true
  try {
    school.value = await getMySchool()
  } catch (error: any) {
    if (error.response?.status !== 404) {
      console.error('加载学校信息失败:', error)
    }
    school.value = null
  } finally {
    loadingSchool.value = false
  }
}

// 申请院校实名认证
const handleVerification = async () => {
  try {
    await requestSchoolVerification(verificationForm.value)
    alert('认证申请已提交，请等待管理员审核！')
    showVerificationModal.value = false
    verificationForm.value = {
      verification_documents: '',
      contact_person: '',
      contact_phone: '',
      contact_email: ''
    }
    loadSchool()
  } catch (error: any) {
    console.error('申请认证失败:', error)
    alert('申请失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 加载院系列表
const loadDepartments = async () => {
  loading.value = true
  try {
    const response = await getDepartments({
      page: currentPage.value,
      page_size: pageSize.value,
      keyword: searchKeyword.value || undefined,
      school_id: schoolIdFilter.value || undefined
    })
    departments.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('加载院系列表失败:', error)
    alert('加载院系列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadDepartments()
}

// 分页变化
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadDepartments()
}

// 编辑院系
const editDepartment = (dept: Department) => {
  editingDepartmentId.value = dept.id
  departmentForm.value = {
    name: dept.name,
    code: dept.code || '',
    description: dept.description || '',
    honors: dept.honors || ''
  }
  showEditModal.value = true
}

// 保存院系
const saveDepartment = async () => {
  try {
    if (editingDepartmentId.value) {
      // 更新
      await updateDepartment(editingDepartmentId.value, departmentForm.value as DepartmentUpdate)
      alert('更新成功！')
    } else {
      // 创建
      await createDepartment(departmentForm.value)
      alert('创建成功！')
    }
    closeModal()
    loadDepartments()
  } catch (error: any) {
    console.error('保存院系失败:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 确认删除
const confirmDelete = (dept: Department) => {
  departmentToDelete.value = dept
  showDeleteModal.value = true
}

// 删除院系
const handleDelete = async () => {
  if (!departmentToDelete.value) return
  
  try {
    await deleteDepartment(departmentToDelete.value.id)
    alert('删除成功！')
    showDeleteModal.value = false
    departmentToDelete.value = null
    loadDepartments()
  } catch (error: any) {
    console.error('删除院系失败:', error)
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 关闭模态框
const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingDepartmentId.value = null
  departmentForm.value = {
    name: '',
    code: '',
    description: '',
    honors: ''
  }
}

onMounted(() => {
  loadSchool()
  loadDepartments()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

