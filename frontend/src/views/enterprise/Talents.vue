<template>
  <div class="enterprise-talents">
    <h1 class="text-3xl font-bold mb-6">人才搜索</h1>

    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">关键词</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索简历..."
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="handleSearch"
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
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">学历</label>
          <select
            v-model="filters.education"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="handleSearch"
          >
            <option value="">全部</option>
            <option value="BACHELOR">本科</option>
            <option value="MASTER">硕士</option>
            <option value="DOCTOR">博士</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="handleSearch"
            class="w-full px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 简历列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="resumes.length === 0" class="text-center py-12 text-gray-500">
        暂无简历信息
      </div>
      <div
        v-for="resume in resumes"
        :key="resume.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ resume.title }}</h3>
            <div class="text-gray-600 text-sm mb-3">
              <p v-if="resume.major">专业：{{ resume.major }}</p>
              <p v-if="resume.education">学历：{{ resume.education }}</p>
              <p v-if="resume.graduation_year">毕业年份：{{ resume.graduation_year }}</p>
            </div>
            <p class="text-gray-700 line-clamp-3 mb-3">{{ resume.content }}</p>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>查看：{{ resume.view_count }}</span>
              <span>下载：{{ resume.download_count }}</span>
            </div>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click="viewResume(resume.id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看简历
            </button>
            <button
              @click="downloadResume(resume.id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              下载简历
            </button>
            <button
              @click="markResume(resume.id)"
              :class="['px-4 py-2 border rounded-lg hover:bg-gray-50', resumeMarkMap[resume.id] ? 'bg-yellow-100 border-yellow-300' : 'border-gray-300']"
            >
              {{ resumeMarkMap[resume.id] ? '已标记' : '标记' }}
            </button>
            <button
              @click="shareResume(resume.id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              分享
            </button>
            <button
              @click="startChat(resume.student_id)"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              发起聊天
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

    <!-- 标记模态框 -->
    <div
      v-if="showMarkModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showMarkModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-4">标记简历</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">备注</label>
              <textarea
                v-model="markNote"
                rows="3"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入备注（可选）"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">标记颜色</label>
              <select
                v-model="markColor"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="blue">蓝色</option>
                <option value="red">红色</option>
                <option value="green">绿色</option>
                <option value="yellow">黄色</option>
                <option value="purple">紫色</option>
              </select>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-4">
            <button
              @click="showMarkModal = false"
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              取消
            </button>
            <button
              @click="saveMark"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              保存
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getResumes, type Resume } from '@/api/resumes'
import { getMark, createMark, deleteMark, type Mark } from '@/api/marks'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 简历列表
const resumes = ref<Resume[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const filters = ref({
  major: '',
  education: '',
})
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 简历标记映射
const resumeMarkMap = ref<Record<string, Mark>>({})
const showMarkModal = ref(false)
const currentResumeId = ref<string | null>(null)
const markNote = ref('')
const markColor = ref('blue')


// 搜索简历
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
    if (filters.value.major) {
      params.major = filters.value.major
    }
    if (filters.value.education) {
      params.education = filters.value.education
    }

    const response = await getResumes(params)
    resumes.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('搜索简历失败:', error)
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

// 查看简历
const viewResume = (resumeId: string) => {
  // 跳转到简历详情页面（使用教师端路由，因为通用路由在教师端下）
  router.push(`/teacher/resumes/${resumeId}`)
}

// 下载简历
const downloadResume = async (resumeId: string) => {
  try {
    const { downloadResume: downloadResumeAPI } = await import('@/api/resumes')
    await downloadResumeAPI(resumeId)
  } catch (error: any) {
    alert('下载失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 发起聊天
const startChat = async (studentId: string) => {
  // TODO: 创建或获取聊天会话
  router.push(`/enterprise/chat?user_id=${studentId}`)
}

// 标记简历
const markResume = async (resumeId: string) => {
  try {
    // 检查是否已有标记
    const existingMark = resumeMarkMap.value[resumeId]
    if (existingMark) {
      // 如果已有标记，显示标记详情或删除
      if (confirm('是否删除此标记？')) {
        await deleteMark(existingMark.id)
        delete resumeMarkMap.value[resumeId]
        alert('标记已删除')
      }
    } else {
      // 创建新标记
      currentResumeId.value = resumeId
      markNote.value = ''
      markColor.value = 'blue'
      showMarkModal.value = true
    }
  } catch (error: any) {
    console.error('标记操作失败:', error)
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 保存标记
const saveMark = async () => {
  if (!currentResumeId.value) return
  try {
    const mark = await createMark({
      target_type: 'RESUME',
      target_id: currentResumeId.value,
      note: markNote.value || undefined,
      color: markColor.value
    })
    resumeMarkMap.value[currentResumeId.value] = mark
    showMarkModal.value = false
    alert('标记成功')
  } catch (error: any) {
    console.error('保存标记失败:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 分享简历
const shareResume = async (resumeId: string) => {
  try {
    const resume = resumes.value.find(r => r.id === resumeId)
    if (!resume) return
    
    // 生成分享链接
    const shareUrl = `${window.location.origin}/resumes/${resumeId}`
    const shareText = `推荐简历：${resume.title}\n${shareUrl}`
    
    // 尝试使用Web Share API
    if (navigator.share) {
      try {
        await navigator.share({
          title: resume.title,
          text: shareText,
          url: shareUrl
        })
        return
      } catch (err) {
        // 用户取消分享，继续使用复制方式
      }
    }
    
    // 复制到剪贴板
    await navigator.clipboard.writeText(shareText)
    alert('分享链接已复制到剪贴板')
  } catch (error: any) {
    console.error('分享失败:', error)
    alert('分享失败: ' + (error.message || '未知错误'))
  }
}

// 加载简历标记
const loadResumeMarks = async () => {
  try {
    const { getMarks } = await import('@/api/marks')
    const response = await getMarks({
      target_type: 'RESUME',
      page_size: 100
    })
    // 构建标记映射
    resumeMarkMap.value = {}
    response.items.forEach(mark => {
      resumeMarkMap.value[mark.target_id] = mark
    })
  } catch (error) {
    console.error('加载标记失败:', error)
  }
}

onMounted(() => {
  handleSearch()
  loadResumeMarks()
})
</script>

<style scoped>
.enterprise-talents {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

