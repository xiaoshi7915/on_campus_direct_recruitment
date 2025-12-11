<template>
  <div class="student-todos">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">待办中心</h1>
      <button
        @click="showForm = true; editingTodo = null"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        添加待办
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="completedFilter"
          @change="loadTodos"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="null">全部</option>
          <option :value="false">未完成</option>
          <option :value="true">已完成</option>
        </select>
      </div>
    </div>

    <!-- 待办列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="todos.length === 0" class="text-center py-12 text-gray-500">
        暂无待办事项
      </div>
      <div
        v-for="todo in todos"
        :key="todo.id"
        :class="['bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow', todo.is_completed && 'opacity-60']"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-2 mb-2">
              <input
                type="checkbox"
                :checked="todo.is_completed"
                @change="toggleComplete(todo)"
                class="w-5 h-5"
              />
              <h3 :class="['text-xl font-semibold', todo.is_completed && 'line-through']">
                {{ todo.title }}
              </h3>
              <span :class="getPriorityClass(todo.priority)" class="px-2 py-1 rounded text-xs">
                {{ getPriorityText(todo.priority) }}
              </span>
            </div>
            <div v-if="todo.content" class="text-gray-700 mb-2">{{ todo.content }}</div>
            <div class="text-sm text-gray-500">
              <span v-if="todo.due_date">截止日期：{{ formatDate(todo.due_date) }}</span>
              <span class="ml-4">创建时间：{{ formatDate(todo.created_at) }}</span>
            </div>
          </div>
          <div class="ml-6 flex space-x-2">
            <button
              @click="editTodo(todo)"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              编辑
            </button>
            <button
              @click="deleteTodoItem(todo.id)"
              class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 表单弹窗 -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-2xl font-bold mb-4">{{ editingTodo ? '编辑' : '添加' }}待办</h2>
        <form @submit.prevent="saveTodo">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">标题 *</label>
              <input
                v-model="formData.title"
                type="text"
                required
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">内容</label>
              <textarea
                v-model="formData.content"
                rows="3"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">优先级</label>
              <select
                v-model="formData.priority"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="LOW">低</option>
                <option value="MEDIUM">中</option>
                <option value="HIGH">高</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">截止日期</label>
              <input
                v-model="formData.due_date"
                type="datetime-local"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-2">
            <button
              type="button"
              @click="showForm = false"
              class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
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
import { getTodos, createTodo, updateTodo, deleteTodo, type TodoResponse } from '@/api/todos'

const todos = ref<TodoResponse[]>([])
const loading = ref(false)
const completedFilter = ref<boolean | null>(null)
const showForm = ref(false)
const editingTodo = ref<TodoResponse | null>(null)
const formData = ref({
  title: '',
  content: '',
  priority: 'MEDIUM',
  due_date: ''
})

const loadTodos = async () => {
  loading.value = true
  try {
    const res = await getTodos({
      is_completed: completedFilter.value ?? undefined
    })
    todos.value = res.items
  } catch (error) {
    console.error('加载待办失败:', error)
    alert('加载待办失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const editTodo = (todo: TodoResponse) => {
  editingTodo.value = todo
  formData.value = {
    title: todo.title,
    content: todo.content || '',
    priority: todo.priority,
    due_date: todo.due_date ? new Date(todo.due_date).toISOString().slice(0, 16) : ''
  }
  showForm.value = true
}

const saveTodo = async () => {
  try {
    const data: any = {
      title: formData.value.title,
      content: formData.value.content || undefined,
      priority: formData.value.priority
    }
    if (formData.value.due_date) {
      data.due_date = new Date(formData.value.due_date).toISOString()
    }
    
    if (editingTodo.value) {
      await updateTodo(editingTodo.value.id, data)
      alert('更新成功')
    } else {
      await createTodo(data)
      alert('创建成功')
    }
    showForm.value = false
    editingTodo.value = null
    formData.value = {
      title: '',
      content: '',
      priority: 'MEDIUM',
      due_date: ''
    }
    loadTodos()
  } catch (error: any) {
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  }
}

const toggleComplete = async (todo: TodoResponse) => {
  try {
    await updateTodo(todo.id, { is_completed: !todo.is_completed })
    loadTodos()
  } catch (error: any) {
    alert(error.response?.data?.detail || '更新失败，请稍后重试')
  }
}

const deleteTodoItem = async (id: string) => {
  if (!confirm('确定要删除这个待办吗？')) return
  try {
    await deleteTodo(id)
    alert('删除成功')
    loadTodos()
  } catch (error: any) {
    alert(error.response?.data?.detail || '删除失败，请稍后重试')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const getPriorityClass = (priority: string) => {
  const classes: Record<string, string> = {
    LOW: 'bg-gray-100 text-gray-800',
    MEDIUM: 'bg-yellow-100 text-yellow-800',
    HIGH: 'bg-red-100 text-red-800'
  }
  return classes[priority] || 'bg-gray-100 text-gray-800'
}

const getPriorityText = (priority: string) => {
  const texts: Record<string, string> = {
    LOW: '低',
    MEDIUM: '中',
    HIGH: '高'
  }
  return texts[priority] || priority
}

onMounted(() => {
  loadTodos()
})
</script>

