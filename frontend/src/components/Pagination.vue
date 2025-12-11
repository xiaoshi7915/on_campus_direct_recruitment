<template>
  <div v-if="total > 0" class="pagination-container">
    <div class="flex items-center justify-between">
      <!-- 左侧：每页条数选择 -->
      <div class="flex items-center space-x-2">
        <label class="text-sm text-gray-700">每页显示：</label>
        <select
          v-model="localPageSize"
          @change="handlePageSizeChange"
          class="px-3 py-1 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
        <span class="text-sm text-gray-600">条</span>
      </div>

      <!-- 中间：页码信息 -->
      <div class="flex items-center space-x-2">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          上一页
        </button>
        <span class="px-4 py-2 text-sm text-gray-700">
          第 {{ currentPage }} / {{ totalPages }} 页（共 {{ total }} 条）
        </span>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          下一页
        </button>
      </div>

      <!-- 右侧：跳转页码 -->
      <div class="flex items-center space-x-2">
        <label class="text-sm text-gray-700">跳转到：</label>
        <input
          v-model.number="jumpPage"
          type="number"
          :min="1"
          :max="totalPages"
          @keyup.enter="handleJump"
          class="w-16 px-2 py-1 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="handleJump"
          class="px-3 py-1 text-sm border rounded-lg hover:bg-gray-50"
        >
          跳转
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Props {
  currentPage: number
  pageSize: number
  total: number
}

interface Emits {
  (e: 'update:currentPage', value: number): void
  (e: 'update:pageSize', value: number): void
  (e: 'change', page: number, pageSize: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const localPageSize = ref(props.pageSize)
const jumpPage = ref(props.currentPage)

// 计算总页数
const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

// 监听外部pageSize变化
watch(() => props.pageSize, (newVal) => {
  localPageSize.value = newVal
})

// 监听外部currentPage变化
watch(() => props.currentPage, (newVal) => {
  jumpPage.value = newVal
})

// 切换页码
const changePage = (page: number) => {
  const maxPage = Math.ceil(props.total / props.pageSize)
  if (page >= 1 && page <= maxPage) {
    emit('update:currentPage', page)
    emit('change', page, localPageSize.value)
    jumpPage.value = page
  }
}

// 每页条数变化 - 立即触发更新
const handlePageSizeChange = () => {
  const newPageSize = localPageSize.value
  // 重新计算当前页（如果当前页超出范围，跳转到第一页）
  const newTotalPages = Math.ceil(props.total / newPageSize)
  const newPage = props.currentPage > newTotalPages ? 1 : props.currentPage
  
  // 先更新 pageSize，然后更新 currentPage，最后触发 change 事件
  emit('update:pageSize', newPageSize)
  emit('update:currentPage', newPage)
  // 使用 nextTick 确保 v-model 更新后再触发 change
  setTimeout(() => {
    emit('change', newPage, newPageSize)
  }, 0)
  jumpPage.value = newPage
}

// 跳转页码
const handleJump = () => {
  const page = Number(jumpPage.value)
  if (page >= 1 && page <= totalPages.value) {
    changePage(page)
  } else {
    alert(`请输入1-${totalPages.value}之间的页码`)
    jumpPage.value = props.currentPage
  }
}
</script>

<style scoped>
.pagination-container {
  margin-top: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}
</style>

