<template>
  <div class="departments-page">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">院系信息管理</h1>
      <button
        @click="showCreateModal = true"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        创建院系
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">关键词搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索院系名称或代码"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">学校ID</label>
          <input
            v-model="schoolIdFilter"
            type="text"
            placeholder="筛选学校ID"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
            @keyup.enter="handleSearch"
          />
        </div>
        <div class="flex items-end">
          <button
            @click="handleSearch"
            class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 院系列表 -->
    <div class="bg-white rounded-lg shadow">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="departments.length === 0" class="text-center py-12 text-gray-500">
        暂无院系信息
      </div>
      <div v-else>
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">院系名称</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">院系代码</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">描述</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">资质荣誉</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="dept in departments" :key="dept.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ dept.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ dept.code || '-' }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">
                <div class="max-w-xs truncate">{{ dept.description || '-' }}</div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                <div class="max-w-xs truncate">{{ dept.honors || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="editDepartment(dept)"
                  class="text-blue-600 hover:text-blue-900 mr-4"
                >
                  编辑
                </button>
                <button
                  @click="confirmDelete(dept)"
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

    <!-- 创建/编辑模态框 -->
    <div
      v-if="showCreateModal || showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4 text-gray-900">
            {{ showEditModal ? '编辑院系' : '创建院系' }}
          </h2>
          <form @submit.prevent="saveDepartment">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  院系名称 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="departmentForm.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入院系名称"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">院系代码</label>
                <input
                  v-model="departmentForm.code"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入院系代码"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
                <textarea
                  v-model="departmentForm.description"
                  rows="4"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入院系描述"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">资质荣誉</label>
                <textarea
                  v-model="departmentForm.honors"
                  rows="4"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入资质荣誉信息"
                ></textarea>
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
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
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-4 text-gray-900">确认删除</h2>
          <p class="text-gray-700 mb-6">
            确定要删除院系 "{{ departmentToDelete?.name }}" 吗？此操作不可恢复。
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

    <!-- 院校实名认证模态框 -->
    <div
      v-if="showVerificationModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showVerificationModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4 text-gray-900">院校实名认证</h2>
          <div v-if="school" class="mb-4 p-4 bg-gray-50 rounded-lg">
            <p class="text-sm text-gray-600 mb-2">当前学校：<strong class="text-gray-900">{{ school.name }}</strong></p>
            <p class="text-sm text-gray-600">认证状态：<span :class="school.is_verified ? 'text-green-600' : 'text-yellow-600'">{{ school.is_verified ? '已认证' : '未认证' }}</span></p>
          </div>
          <form @submit.prevent="handleVerification">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">认证材料</label>
                <textarea
                  v-model="verificationForm.verification_documents"
                  rows="4"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请描述或上传认证材料（如：营业执照、组织机构代码证等）"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">联系人</label>
                <input
                  v-model="verificationForm.contact_person"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入联系人姓名"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">联系电话</label>
                <input
                  v-model="verificationForm.contact_phone"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入联系电话"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">联系邮箱</label>
                <input
                  v-model="verificationForm.contact_email"
                  type="email"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入联系邮箱"
                />
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-4">
              <button
                type="button"
                @click="showVerificationModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
              >
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
.departments-page {
  max-width: 1400px;
  margin: 0 auto;
}
</style>

