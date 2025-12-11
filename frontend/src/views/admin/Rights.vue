<template>
  <div class="admin-rights">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">权益管理</h1>
      <div class="flex space-x-3">
        <button
          @click="showCreateRightModal = true"
          class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          创建权益
        </button>
        <button
          @click="showPackageTab = !showPackageTab"
          class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          {{ showPackageTab ? '权益列表' : '权益套餐' }}
        </button>
      </div>
    </div>

    <!-- 权益列表 -->
    <div v-if="!showPackageTab" class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="rights.length === 0" class="text-center py-12 text-gray-500">
        暂无权益信息
      </div>
      <div
        v-for="right in rights"
        :key="right.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ right.name }}</h3>
              <span
                :class="right.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                class="px-2 py-1 rounded text-xs"
              >
                {{ right.is_active ? '激活' : '禁用' }}
              </span>
            </div>
            <p v-if="right.description" class="text-gray-700 mb-3">{{ right.description }}</p>
            <div class="text-gray-600 text-sm">
              <p>代码：{{ right.code }}</p>
              <p>类型：{{ right.type }}</p>
              <p v-if="right.value !== null && right.value !== undefined">权益值：{{ right.value }}</p>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editRight(right)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="handleDeleteRight(right.id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 权益套餐列表 -->
    <div v-else class="space-y-4">
      <div class="flex justify-end mb-4">
        <button
          @click="showCreatePackageModal = true"
          class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          创建套餐
        </button>
      </div>
      <div v-if="loadingPackages" class="text-center py-12">加载中...</div>
      <div v-else-if="packages.length === 0" class="text-center py-12 text-gray-500">
        暂无权益套餐
      </div>
      <div
        v-for="pkg in packages"
        :key="pkg.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold">{{ pkg.name }}</h3>
              <span
                :class="pkg.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                class="px-2 py-1 rounded text-xs"
              >
                {{ pkg.is_active ? '激活' : '禁用' }}
              </span>
            </div>
            <p v-if="pkg.description" class="text-gray-700 mb-3">{{ pkg.description }}</p>
            <div class="text-gray-600 text-sm mb-3">
              <p>价格：¥{{ pkg.price }}</p>
              <p v-if="pkg.duration_days">时长：{{ pkg.duration_days }}天</p>
              <p v-if="pkg.items && pkg.items.length > 0">包含权益：{{ pkg.items.length }}项</p>
            </div>
            <div v-if="pkg.items && pkg.items.length > 0" class="mt-3">
              <p class="text-sm font-medium text-gray-700 mb-2">套餐内容：</p>
              <div class="space-y-1">
                <div v-for="item in pkg.items" :key="item.id" class="text-sm text-gray-600">
                  - 权益ID: {{ item.rights_id }} (数量: {{ item.quantity }})
                </div>
              </div>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="editPackage(pkg)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="handleDeletePackage(pkg.id)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑权益模态框 -->
    <div v-if="showCreateRightModal || showEditRightModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">{{ showEditRightModal ? '编辑权益' : '创建权益' }}</h2>
        <form @submit.prevent="saveRight">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">名称</label>
              <input v-model="rightForm.name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">代码</label>
              <input v-model="rightForm.code" type="text" required :disabled="showEditRightModal" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">描述</label>
              <textarea v-model="rightForm.description" rows="3" class="w-full px-3 py-2 border rounded-lg"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">类型</label>
              <input v-model="rightForm.type" type="text" required class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">权益值</label>
              <input v-model.number="rightForm.value" type="number" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="flex items-center space-x-2">
                <input v-model="rightForm.is_active" type="checkbox" class="rounded" />
                <span>是否激活</span>
              </label>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="showCreateRightModal = false; showEditRightModal = false" class="px-4 py-2 border rounded-lg">取消</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">保存</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 创建/编辑套餐模态框 -->
    <div v-if="showCreatePackageModal || showEditPackageModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">{{ showEditPackageModal ? '编辑套餐' : '创建套餐' }}</h2>
        <form @submit.prevent="savePackage">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">名称</label>
              <input v-model="packageForm.name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">描述</label>
              <textarea v-model="packageForm.description" rows="3" class="w-full px-3 py-2 border rounded-lg"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium mb-2">价格</label>
                <input v-model.number="packageForm.price" type="number" step="0.01" min="0" required class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-2">时长（天）</label>
                <input v-model.number="packageForm.duration_days" type="number" min="1" class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
            <div>
              <label class="flex items-center space-x-2">
                <input v-model="packageForm.is_active" type="checkbox" class="rounded" />
                <span>是否激活</span>
              </label>
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">套餐项（权益ID:数量，每行一个）</label>
              <textarea v-model="packageItemsText" rows="5" placeholder="例如：&#10;rights_id_1:5&#10;rights_id_2:10" class="w-full px-3 py-2 border rounded-lg"></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="showCreatePackageModal = false; showEditPackageModal = false" class="px-4 py-2 border rounded-lg">取消</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">保存</button>
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
.admin-rights {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

