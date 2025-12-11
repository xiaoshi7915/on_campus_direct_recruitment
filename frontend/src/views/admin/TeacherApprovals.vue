<template>
  <div class="teacher-approvals-page">
    <h1 class="text-3xl font-bold mb-6">教师注册审批</h1>

    <!-- 待审批教师列表 -->
    <div class="bg-white rounded-lg shadow">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="teachers.length === 0" class="text-center py-12 text-gray-500">
        暂无待审批教师
      </div>
      <div v-else>
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">用户名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">真实姓名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">联系方式</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学校/院系</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">职称/职务</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">注册时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="teacher in teachers" :key="teacher.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ teacher.username }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ teacher.real_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>{{ teacher.phone || '-' }}</div>
                <div class="text-xs text-gray-400">{{ teacher.email || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>学校ID: {{ teacher.school_id || '-' }}</div>
                <div class="text-xs text-gray-400">院系ID: {{ teacher.department_id || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>{{ teacher.title || '-' }}</div>
                <div class="text-xs text-gray-400">{{ teacher.position || '-' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDateTime(teacher.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="approveTeacher(teacher.id, 'APPROVE')"
                  class="text-green-600 hover:text-green-900 mr-4"
                >
                  通过
                </button>
                <button
                  @click="approveTeacher(teacher.id, 'REJECT')"
                  class="text-red-600 hover:text-red-900"
                >
                  拒绝
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getPendingTeacherApprovals,
  approveTeacherRegistration,
  type Teacher
} from '@/api/teacherManagement'
import Pagination from '@/components/Pagination.vue'

// 数据
const teachers = ref<Teacher[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

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

// 加载待审批教师列表
const loadTeachers = async () => {
  loading.value = true
  try {
    const response = await getPendingTeacherApprovals({
      page: currentPage.value,
      page_size: pageSize.value
    })
    teachers.value = response.items
    total.value = response.total
  } catch (error: any) {
    console.error('加载待审批教师列表失败:', error)
    alert('加载待审批教师列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 分页变化
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadTeachers()
}

// 审批教师
const approveTeacher = async (teacherId: string, action: string) => {
  const actionText = action === 'APPROVE' ? '通过' : '拒绝'
  if (!confirm(`确定要${actionText}此教师的注册申请吗？`)) {
    return
  }
  
  try {
    await approveTeacherRegistration(teacherId, { action, comment: '' })
    alert(`${actionText}成功！`)
    loadTeachers()
  } catch (error: any) {
    console.error('审批失败:', error)
    alert('审批失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadTeachers()
})
</script>

<style scoped>
.teacher-approvals-page {
  max-width: 1400px;
  margin: 0 auto;
}
</style>



