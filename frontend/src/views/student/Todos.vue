<template>
  <div class="student-todos max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-900">待办中心</h1>
      <button
        @click="showForm = true; editingTodo = null"
        class="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        添加待办
      </button>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-semibold text-gray-700 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          状态筛选：
        </label>
        <select
          v-model="completedFilter"
          @change="loadTodos"
          class="px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
        >
          <option :value="null">全部</option>
          <option :value="false">未完成</option>
          <option :value="true">已完成</option>
        </select>
      </div>
    </div>

    <!-- 待办列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="todos.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        <p class="text-gray-500 text-lg">暂无待办事项</p>
        <p class="text-gray-400 text-sm mt-2">点击上方按钮添加第一个待办</p>
      </div>
      <div
        v-for="todo in todos"
        :key="todo.id"
        :class="[
          'bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-200 border',
          todo.is_completed ? 'border-gray-200 opacity-75' : 'border-gray-200 hover:border-blue-200'
        ]"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <input
                type="checkbox"
                :checked="todo.is_completed"
                @change="toggleComplete(todo)"
                class="w-5 h-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
              />
              <div class="p-2 bg-indigo-50 rounded-lg">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h3 :class="['text-xl font-semibold text-gray-900', todo.is_completed && 'line-through text-gray-400']">
                {{ todo.title }}
              </h3>
              <span :class="getPriorityClass(todo.priority)" class="px-3 py-1 rounded-full text-xs font-medium">
                {{ getPriorityText(todo.priority) }}
              </span>
            </div>
            <div v-if="todo.content" class="text-gray-700 mb-3 ml-11 bg-gray-50 p-3 rounded-lg border border-gray-200">{{ todo.content }}</div>
            <div class="text-sm text-gray-500 ml-11 flex items-center space-x-4">
              <span v-if="todo.due_date" class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                截止日期：{{ formatDate(todo.due_date) }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                创建时间：{{ formatDate(todo.created_at) }}
              </span>
            </div>
          </div>
          <div class="ml-6 flex space-x-2">
            <button
              @click="editTodo(todo)"
              class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              编辑
            </button>
            <button
              @click="deleteTodoItem(todo.id)"
              class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 表单弹窗 -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showForm = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md border border-gray-100">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            {{ editingTodo ? '编辑' : '添加' }}待办
          </h2>
          <button
            @click="showForm = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveTodo" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">标题 *</label>
            <input
              v-model="formData.title"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">内容</label>
            <textarea
              v-model="formData.content"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">优先级</label>
            <select
              v-model="formData.priority"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            >
              <option value="LOW">低</option>
              <option value="MEDIUM">中</option>
              <option value="HIGH">高</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">截止日期</label>
            <input
              v-model="formData.due_date"
              type="datetime-local"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showForm = false"
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

