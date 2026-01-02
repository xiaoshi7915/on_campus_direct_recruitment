<template>
  <div class="admin-rights w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900 flex items-center">
        <svg class="w-8 h-8 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        权益管理
      </h1>
      <div class="flex space-x-3">
        <button
          @click="showCreateRightModal = true"
          class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          创建权益
        </button>
        <button
          @click="showPackageTab = !showPackageTab"
          class="px-6 py-3 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-semibold"
        >
          {{ showPackageTab ? '权益列表' : '权益套餐' }}
        </button>
      </div>
    </div>

    <!-- 权益列表 -->
    <div v-if="!showPackageTab" class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="rights.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        <p class="text-lg">暂无权益信息</p>
      </div>
      <div
        v-for="right in rights"
        :key="right.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border border-gray-100"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ right.name }}</h3>
              <span
                :class="right.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ right.is_active ? '激活' : '禁用' }}
              </span>
            </div>
            <p v-if="right.description" class="text-gray-700 mb-4 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">{{ right.description }}</p>
            <div class="text-gray-600 text-sm ml-11 space-y-1">
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                代码：{{ right.code }}
              </p>
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                类型：{{ right.type }}
              </p>
              <p v-if="right.value !== null && right.value !== undefined" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                权益值：{{ right.value }}
              </p>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editRight(right)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              编辑
            </button>
            <button
              @click="handleDeleteRight(right.id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 权益套餐列表 -->
    <div v-else class="space-y-4">
      <div class="flex justify-end mb-6">
        <button
          @click="showCreatePackageModal = true"
          class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200 font-semibold flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          创建套餐
        </button>
      </div>
      <div v-if="loadingPackages" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="packages.length === 0" class="text-center py-16 text-gray-500">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        </svg>
        <p class="text-lg">暂无权益套餐</p>
      </div>
      <div
        v-for="pkg in packages"
        :key="pkg.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border border-gray-100"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-purple-50 rounded-lg">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ pkg.name }}</h3>
              <span
                :class="pkg.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ pkg.is_active ? '激活' : '禁用' }}
              </span>
            </div>
            <p v-if="pkg.description" class="text-gray-700 mb-4 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">{{ pkg.description }}</p>
            <div class="text-gray-600 text-sm mb-3 ml-11 space-y-1">
              <p class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                价格：¥{{ pkg.price }}
              </p>
              <p v-if="pkg.duration_days" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                时长：{{ pkg.duration_days }}天
              </p>
              <p v-if="pkg.items && pkg.items.length > 0" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                包含权益：{{ pkg.items.length }}项
              </p>
            </div>
            <div v-if="pkg.items && pkg.items.length > 0" class="mt-4 ml-11">
              <p class="text-sm font-semibold text-gray-700 mb-2">套餐内容：</p>
              <div class="space-y-2">
                <div v-for="item in pkg.items" :key="item.id" class="text-sm text-gray-600 bg-gray-50 p-2 rounded-lg border border-gray-200">
                  <span class="font-medium">权益ID:</span> {{ item.rights_id }} <span class="font-medium">数量:</span> {{ item.quantity }}
                </div>
              </div>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editPackage(pkg)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              编辑
            </button>
            <button
              @click="handleDeletePackage(pkg.id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium text-sm"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑权益模态框 -->
    <div v-if="showCreateRightModal || showEditRightModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          {{ showEditRightModal ? '编辑权益' : '创建权益' }}
        </h2>
        <form @submit.prevent="saveRight">
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">名称</label>
              <input v-model="rightForm.name" type="text" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">代码</label>
              <input v-model="rightForm.code" type="text" required :disabled="showEditRightModal" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 disabled:bg-gray-100" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
              <textarea v-model="rightForm.description" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"></textarea>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">类型</label>
              <input v-model="rightForm.type" type="text" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">权益值</label>
              <input v-model.number="rightForm.value" type="number" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="flex items-center space-x-3 cursor-pointer">
                <input v-model="rightForm.is_active" type="checkbox" class="w-5 h-5 text-blue-600 rounded focus:ring-blue-500" />
                <span class="text-sm font-semibold text-gray-700">是否激活</span>
              </label>
            </div>
          </div>
          <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
            <button type="button" @click="showCreateRightModal = false; showEditRightModal = false" class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium">取消</button>
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

    <!-- 创建/编辑套餐模态框 -->
    <div v-if="showCreatePackageModal || showEditPackageModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 flex items-center">
          <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
          {{ showEditPackageModal ? '编辑套餐' : '创建套餐' }}
        </h2>
        <form @submit.prevent="savePackage">
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">名称</label>
              <input v-model="packageForm.name" type="text" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
              <textarea v-model="packageForm.description" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">价格</label>
                <input v-model.number="packageForm.price" type="number" step="0.01" min="0" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">时长（天）</label>
                <input v-model.number="packageForm.duration_days" type="number" min="1" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200" />
              </div>
            </div>
            <div>
              <label class="flex items-center space-x-3 cursor-pointer">
                <input v-model="packageForm.is_active" type="checkbox" class="w-5 h-5 text-blue-600 rounded focus:ring-blue-500" />
                <span class="text-sm font-semibold text-gray-700">是否激活</span>
              </label>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">套餐项（权益ID:数量，每行一个）</label>
              <textarea v-model="packageItemsText" rows="5" placeholder="例如：&#10;rights_id_1:5&#10;rights_id_2:10" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"></textarea>
            </div>
          </div>
          <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-4">
            <button type="button" @click="showCreatePackageModal = false; showEditPackageModal = false" class="px-6 py-2.5 border-2 border-gray-300 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 font-medium">取消</button>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getRights, createRight, updateRight, deleteRight, getRightsPackages, createRightsPackage, updateRightsPackage, deleteRightsPackage, type Right, type RightsPackage } from '@/api/rights'

// 权益列表
const rights = ref<Right[]>([])
const loading = ref(false)
const showCreateRightModal = ref(false)
const showEditRightModal = ref(false)
const currentRight = ref<Right | null>(null)
const rightForm = ref({
  name: '',
  code: '',
  description: '',
  type: '',
  value: 0,
  is_active: true
})

// 权益套餐列表
const packages = ref<RightsPackage[]>([])
const loadingPackages = ref(false)
const showPackageTab = ref(false)
const showCreatePackageModal = ref(false)
const showEditPackageModal = ref(false)
const currentPackage = ref<RightsPackage | null>(null)
const packageForm = ref({
  name: '',
  description: '',
  price: 0,
  duration_days: 0,
  is_active: true
})
const packageItemsText = ref('')

// 加载权益列表
const loadRights = async () => {
  loading.value = true
  try {
    const response = await getRights()
    rights.value = response.items
  } catch (error: any) {
    console.error('加载权益列表失败:', error)
    alert('加载权益列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 加载权益套餐列表
const loadPackages = async () => {
  loadingPackages.value = true
  try {
    const response = await getRightsPackages()
    packages.value = response.items
  } catch (error: any) {
    console.error('加载权益套餐列表失败:', error)
    alert('加载权益套餐列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loadingPackages.value = false
  }
}

// 编辑权益
const editRight = (right: Right) => {
  currentRight.value = right
  rightForm.value = {
    name: right.name,
    code: right.code,
    description: right.description || '',
    type: right.type,
    value: right.value || 0,
    is_active: right.is_active
  }
  showEditRightModal.value = true
}

// 保存权益
const saveRight = async () => {
  try {
    if (showEditRightModal.value && currentRight.value) {
      await updateRight(currentRight.value.id, rightForm.value)
      alert('更新成功！')
      showEditRightModal.value = false
    } else {
      await createRight(rightForm.value)
      alert('创建成功！')
      showCreateRightModal.value = false
    }
    rightForm.value = {
      name: '',
      code: '',
      description: '',
      type: '',
      value: 0,
      is_active: true
    }
    loadRights()
  } catch (error: any) {
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 删除权益
const handleDeleteRight = async (rightId: string) => {
  if (!confirm('确定要删除这个权益吗？')) {
    return
  }
  try {
    await deleteRight(rightId)
    alert('删除成功！')
    loadRights()
  } catch (error: any) {
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 编辑套餐
const editPackage = (pkg: RightsPackage) => {
  currentPackage.value = pkg
  packageForm.value = {
    name: pkg.name,
    description: pkg.description || '',
    price: pkg.price,
    duration_days: pkg.duration_days || 0,
    is_active: pkg.is_active
  }
  // 将套餐项转换为文本格式
  packageItemsText.value = pkg.items.map(item => `${item.rights_id}:${item.quantity}`).join('\n')
  showEditPackageModal.value = true
}

// 保存套餐
const savePackage = async () => {
  try {
    // 解析套餐项文本
    const items = packageItemsText.value.split('\n')
      .filter(line => line.trim())
      .map(line => {
        const [rights_id, quantity] = line.split(':')
        return {
          rights_id: rights_id.trim(),
          quantity: parseInt(quantity.trim()) || 1
        }
      })
    
    if (showEditPackageModal.value && currentPackage.value) {
      await updateRightsPackage(currentPackage.value.id, packageForm.value)
      alert('更新成功！')
      showEditPackageModal.value = false
    } else {
      await createRightsPackage({
        ...packageForm.value,
        items
      })
      alert('创建成功！')
      showCreatePackageModal.value = false
    }
    packageForm.value = {
      name: '',
      description: '',
      price: 0,
      duration_days: 0,
      is_active: true
    }
    packageItemsText.value = ''
    loadPackages()
  } catch (error: any) {
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 删除套餐
const handleDeletePackage = async (packageId: string) => {
  if (!confirm('确定要删除这个权益套餐吗？')) {
    return
  }
  try {
    await deleteRightsPackage(packageId)
    alert('删除成功！')
    loadPackages()
  } catch (error: any) {
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadRights()
  loadPackages()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

