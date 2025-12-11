<template>
  <div class="teacher-students">
    <h1 class="text-3xl font-bold mb-6">学生管理</h1>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索学生姓名或学号..."
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">年级</label>
          <input
            v-model="filters.grade"
            type="text"
            placeholder="例如：2024"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">专业</label>
          <input
            v-model="filters.major"
            type="text"
            placeholder="例如：计算机科学"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          />
        </div>
      </div>
    </div>

    <!-- 学生列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="students.length === 0" class="text-center py-12 text-gray-500">
        暂无学生信息
      </div>
      <div
        v-for="student in students"
        :key="student.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ student.real_name }}</h3>
            <div class="text-gray-600 text-sm mb-3">
              <p v-if="student.student_id">学号：{{ student.student_id }}</p>
              <p v-if="student.grade">年级：{{ student.grade }}</p>
              <p v-if="student.major">专业：{{ student.major }}</p>
            </div>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>简历数：{{ student.resume_count || 0 }}</span>
              <span>申请数：{{ student.application_count || 0 }}</span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewStudentDetail(student.id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看详情
            </button>
            <button
              @click="viewStudentResumes(student.id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              查看简历
            </button>
            <button
              @click="openCommentModal(student)"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              点评
            </button>
            <button
              @click="confirmRemoveStudent(student)"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              移除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <Pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      @change="handlePaginationChange"
    />

    <!-- 点评模态框 -->
    <div
      v-if="showCommentModalVisible"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showCommentModalVisible = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4 text-gray-900">学生点评</h2>
          <div v-if="selectedStudent" class="mb-4 p-4 bg-gray-50 rounded-lg">
            <p class="text-sm text-gray-600">学生：<strong class="text-gray-900">{{ selectedStudent.real_name }}</strong></p>
            <p v-if="selectedStudent.student_id" class="text-sm text-gray-600">学号：{{ selectedStudent.student_id }}</p>
          </div>
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
                @click="showCommentModalVisible = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
              >
                保存
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 移除确认模态框 -->
    <div
      v-if="showRemoveModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showRemoveModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-4 text-gray-900">确认移除</h2>
          <p class="text-gray-700 mb-6">
            确定要将学生 "{{ selectedStudent?.real_name }}" 从管辖范围内移除吗？此操作不会删除学生数据，只是将其移出您的管辖范围。
          </p>
          <div class="flex justify-end space-x-4">
            <button
              @click="showRemoveModal = false"
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              取消
            </button>
            <button
              @click="handleRemoveStudent"
              class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              确认移除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getStudents, getStudent, removeStudent, type Student } from '@/api/students'
import { getResumes } from '@/api/resumes'
import { createStudentComment, getStudentComments, type StudentCommentCreate } from '@/api/studentComments'
import { useRouter } from 'vue-router'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 学生列表
const students = ref<Student[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const filters = ref({
  grade: '',
  major: '',
})
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 模态框状态
const showCommentModalVisible = ref(false)
const showRemoveModal = ref(false)
const selectedStudent = ref<Student | null>(null)

// 点评表单
const commentForm = ref<StudentCommentCreate>({
  student_id: '',
  content: '',
  score: undefined,
  tags: '',
  is_public: 'PRIVATE'
})

// 计算总页数
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

// 搜索学生
const handleSearch = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    if (filters.value.grade) {
      params.grade = filters.value.grade
    }
    if (filters.value.major) {
      params.major = filters.value.major
    }
    
    const response = await getStudents(params)
    students.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('搜索学生失败:', error)
    alert('加载学生列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  handleSearch()
}

// 查看学生详情
const viewStudentDetail = async (studentId: string) => {
  try {
    const student = await getStudent(studentId)
    alert(`学生详情：\n姓名：${student.real_name}\n学号：${student.student_id || '未设置'}\n年级：${student.grade || '未设置'}\n专业：${student.major || '未设置'}\n简历数：${student.resume_count}\n申请数：${student.application_count}`)
  } catch (error: any) {
    alert('加载学生详情失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 查看学生简历
const viewStudentResumes = async (studentId: string) => {
  try {
    // 获取学生信息以获取user_id
    const student = await getStudent(studentId)
    // 跳转到简历列表页面，通过student_id过滤
    router.push(`/teacher/resumes?student_id=${studentId}`)
  } catch (error: any) {
    alert('查看简历失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 显示点评模态框
const openCommentModal = (student: Student) => {
  selectedStudent.value = student
  commentForm.value = {
    student_id: student.id,
    content: '',
    score: undefined,
    tags: '',
    is_public: 'PRIVATE'
  }
  showCommentModalVisible.value = true
}

// 保存点评
const saveComment = async () => {
  if (!selectedStudent.value) return
  
  try {
    await createStudentComment(commentForm.value)
    alert('点评成功！')
    showCommentModalVisible.value = false
    selectedStudent.value = null
    commentForm.value = {
      student_id: '',
      content: '',
      score: undefined,
      tags: '',
      is_public: 'PRIVATE'
    }
  } catch (error: any) {
    alert('点评失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 确认移除学生
const confirmRemoveStudent = (student: Student) => {
  selectedStudent.value = student
  showRemoveModal.value = true
}

// 移除学生
const handleRemoveStudent = async () => {
  if (!selectedStudent.value) return
  
  try {
    await removeStudent(selectedStudent.value.id)
    alert('移除成功！')
    showRemoveModal.value = false
    selectedStudent.value = null
    handleSearch() // 刷新列表
  } catch (error: any) {
    alert('移除失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.teacher-students {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

