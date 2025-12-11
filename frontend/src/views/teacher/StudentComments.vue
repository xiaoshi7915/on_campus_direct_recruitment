<template>
  <div class="student-comments-page">
    <h1 class="text-3xl font-bold mb-6">学生点评管理</h1>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">学生ID</label>
          <input
            v-model="studentIdFilter"
            type="text"
            placeholder="筛选学生ID"
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

    <!-- 点评列表 -->
    <div class="bg-white rounded-lg shadow">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="comments.length === 0" class="text-center py-12 text-gray-500">
        暂无点评信息
      </div>
      <div v-else>
        <div class="divide-y divide-gray-200">
          <div
            v-for="comment in comments"
            :key="comment.id"
            class="p-6 hover:bg-gray-50"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <div class="flex items-center space-x-3 mb-2">
                  <h3 class="text-lg font-semibold text-gray-900">{{ comment.student_name || '未知学生' }}</h3>
                  <span
                    :class="comment.is_public === 'PUBLIC' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                    class="px-2 py-1 rounded text-xs"
                  >
                    {{ comment.is_public === 'PUBLIC' ? '公开' : '仅教师可见' }}
                  </span>
                  <span v-if="comment.score" class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs">
                    {{ comment.score }}分
                  </span>
                </div>
                <p class="text-gray-700 mb-2">{{ comment.content }}</p>
                <div v-if="comment.tags" class="flex flex-wrap gap-2 mb-2">
                  <span
                    v-for="tag in comment.tags.split(',')"
                    :key="tag"
                    class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs"
                  >
                    {{ tag.trim() }}
                  </span>
                </div>
                <p class="text-sm text-gray-500">
                  创建时间：{{ formatDateTime(comment.created_at) }}
                </p>
              </div>
              <div class="ml-6 flex flex-col space-y-2">
                <button
                  @click="editComment(comment)"
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  编辑
                </button>
                <button
                  @click="confirmDelete(comment)"
                  class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                >
                  删除
                </button>
              </div>
            </div>
          </div>
        </div>

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

    <!-- 编辑模态框 -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showEditModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4 text-gray-900">编辑点评</h2>
          <form @submit.prevent="saveComment">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">点评内容 <span class="text-red-500">*</span></label>
                <textarea
                  v-model="commentForm.content"
                  rows="6"
                  required
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入点评内容"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">评分（1-5分）</label>
                <input
                  v-model.number="commentForm.score"
                  type="number"
                  min="1"
                  max="5"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="请输入评分"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">标签（逗号分隔）</label>
                <input
                  v-model="commentForm.tags"
                  type="text"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  placeholder="例如：学习能力强,团队合作好"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">是否公开</label>
                <select
                  v-model="commentForm.is_public"
                  class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                >
                  <option value="PRIVATE">仅教师可见</option>
                  <option value="PUBLIC">公开</option>
                </select>
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-4">
              <button
                type="button"
                @click="showEditModal = false"
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
            确定要删除这条点评吗？此操作不可恢复。
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
  getStudentComments,
  updateStudentComment,
  deleteStudentComment,
  type StudentComment,
  type StudentCommentUpdate
} from '@/api/studentComments'
import Pagination from '@/components/Pagination.vue'

// 数据
const comments = ref<StudentComment[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索和筛选
const studentIdFilter = ref('')

// 模态框状态
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const commentToDelete = ref<StudentComment | null>(null)

// 表单数据
const commentForm = ref<StudentCommentUpdate>({
  content: '',
  score: undefined,
  tags: '',
  is_public: 'PRIVATE'
})

const editingCommentId = ref<string | null>(null)

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 加载点评列表
const loadComments = async () => {
  loading.value = true
  try {
    const response = await getStudentComments({
      page: currentPage.value,
      page_size: pageSize.value,
      student_id: studentIdFilter.value || undefined
    })
    comments.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('加载点评列表失败:', error)
    alert('加载点评列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadComments()
}

// 分页变化
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadComments()
}

// 编辑点评
const editComment = (comment: StudentComment) => {
  editingCommentId.value = comment.id
  commentForm.value = {
    content: comment.content,
    score: comment.score,
    tags: comment.tags || '',
    is_public: comment.is_public
  }
  showEditModal.value = true
}

// 保存点评
const saveComment = async () => {
  if (!editingCommentId.value) return
  
  try {
    await updateStudentComment(editingCommentId.value, commentForm.value)
    alert('更新成功！')
    showEditModal.value = false
    editingCommentId.value = null
    commentForm.value = {
      content: '',
      score: undefined,
      tags: '',
      is_public: 'PRIVATE'
    }
    loadComments()
  } catch (error: any) {
    console.error('保存点评失败:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 确认删除
const confirmDelete = (comment: StudentComment) => {
  commentToDelete.value = comment
  showDeleteModal.value = true
}

// 删除点评
const handleDelete = async () => {
  if (!commentToDelete.value) return
  
  try {
    await deleteStudentComment(commentToDelete.value.id)
    alert('删除成功！')
    showDeleteModal.value = false
    commentToDelete.value = null
    loadComments()
  } catch (error: any) {
    console.error('删除点评失败:', error)
    alert('删除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadComments()
})
</script>

<style scoped>
.student-comments-page {
  max-width: 1400px;
  margin: 0 auto;
}
</style>

