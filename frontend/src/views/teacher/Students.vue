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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getStudents, getStudent, type Student } from '@/api/students'
import { getResumes } from '@/api/resumes'
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

