<template>
  <div class="enterprise-school-detail">
    <div v-if="loading" class="text-center py-12">加载中...</div>
    <div v-else-if="!school" class="text-center py-12 text-gray-500">学校不存在</div>
    <div v-else class="space-y-6">
      <!-- 返回按钮 -->
      <button
        @click="$router.back()"
        class="text-blue-600 hover:text-blue-800 mb-4"
      >
        ← 返回
      </button>

      <!-- 学校基本信息 -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-start space-x-6">
          <img
            v-if="school.logo_url"
            :src="school.logo_url"
            :alt="school.name"
            class="w-32 h-32 rounded-lg object-cover"
          />
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h1 class="text-3xl font-bold">{{ school.name }}</h1>
              <span
                v-if="school.is_verified"
                class="px-3 py-1 rounded-full text-sm bg-green-100 text-green-800"
              >
                已认证
              </span>
              <span
                v-else
                class="px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-800"
              >
                未认证
              </span>
            </div>
            <div class="text-gray-600 space-y-1 mb-4">
              <p v-if="school.code">学校代码：{{ school.code }}</p>
              <p v-if="school.province || school.city">
                地区：{{ [school.province, school.city].filter(Boolean).join(' ') }}
              </p>
              <p v-if="school.address">地址：{{ school.address }}</p>
              <p v-if="school.website">
                网站：<a :href="school.website" target="_blank" class="text-blue-600 hover:underline">{{ school.website }}</a>
              </p>
            </div>
            <div class="flex items-center space-x-4 text-sm text-gray-600">
              <span v-if="school.student_count !== undefined">
                <strong>学生数量：</strong>{{ school.student_count }}
              </span>
              <span v-if="school.department_count !== undefined">
                <strong>院系数量：</strong>{{ school.department_count }}
              </span>
            </div>
          </div>
          <div class="flex flex-col space-y-2">
            <button
              @click="toggleFavorite"
              :class="isFavorited ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-gray-500 hover:bg-gray-600'"
              class="px-6 py-2 text-white rounded-lg"
            >
              {{ isFavorited ? '已收藏' : '收藏' }}
            </button>
            <button
              @click="showMarkModal = true"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              标记
            </button>
            <button
              @click="handleShare"
              class="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              分享
            </button>
            <button
              @click="showRequestModal"
              class="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600"
            >
              申请宣讲会
            </button>
            <button
              @click="startChat"
              class="px-6 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600"
            >
              发起聊天
            </button>
          </div>
        </div>
      </div>

      <!-- 学校描述 -->
      <div v-if="school.description" class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">学校简介</h2>
        <p class="text-gray-700 whitespace-pre-wrap">{{ school.description }}</p>
      </div>

      <!-- 该学校的宣讲会列表 -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">该学校的宣讲会</h2>
        <div v-if="infoSessionsLoading" class="text-center py-8">加载中...</div>
        <div v-else-if="infoSessions.length === 0" class="text-center py-8 text-gray-500">
          暂无宣讲会
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="session in infoSessions"
            :key="session.id"
            class="border rounded-lg p-4 hover:bg-gray-50"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="text-lg font-semibold">{{ session.title }}</h3>
                <div class="text-gray-600 text-sm mt-2">
                  <p>时间：{{ formatDateTime(session.start_time) }} - {{ formatDateTime(session.end_time) }}</p>
                  <p v-if="session.location">地点：{{ session.location }}</p>
                  <p>状态：{{ getStatusText(session.status) }}</p>
                </div>
              </div>
              <button
                @click="viewInfoSession(session.id)"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                查看详情
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 标记模态框 -->
    <div v-if="showMarkModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-4">标记学校</h2>
        <form @submit.prevent="handleMark" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">备注</label>
            <textarea
              v-model="markForm.note"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">标记颜色</label>
            <select
              v-model="markForm.color"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="blue">蓝色</option>
              <option value="red">红色</option>
              <option value="green">绿色</option>
              <option value="yellow">黄色</option>
              <option value="purple">紫色</option>
            </select>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              @click="showMarkModal = false"
              class="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
            >
              {{ submitting ? '提交中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 申请宣讲会模态框 -->
    <div v-if="showRequestInfoSessionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-4">申请线下宣讲会</h2>
        <form @submit.prevent="handleRequestInfoSession" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">宣讲会标题 *</label>
            <input
              v-model="requestForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
            <textarea
              v-model="requestForm.description"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">建议开始时间 *</label>
              <input
                v-model="requestForm.proposed_start_time"
                type="datetime-local"
                required
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">建议结束时间 *</label>
              <input
                v-model="requestForm.proposed_end_time"
                type="datetime-local"
                required
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">建议地点</label>
            <input
              v-model="requestForm.proposed_location"
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">最大学生数</label>
            <input
              v-model.number="requestForm.max_students"
              type="number"
              min="1"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">联系人</label>
              <input
                v-model="requestForm.contact_person"
                type="text"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">联系电话</label>
              <input
                v-model="requestForm.contact_phone"
                type="tel"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">联系邮箱</label>
              <input
                v-model="requestForm.contact_email"
                type="email"
                class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">申请留言</label>
            <textarea
              v-model="requestForm.message"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              @click="showRequestInfoSessionModal = false"
              class="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
            >
              {{ submitting ? '提交中...' : '提交申请' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getSchool, type School, requestOfflineInfoSession, type OfflineInfoSessionRequest } from '@/api/schools'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'
import { createMark, getMark, updateMark, deleteMark, type MarkCreateRequest } from '@/api/marks'
import { getSchoolShareLink } from '@/api/schools'
import { getInfoSessions, type InfoSession, type InfoSessionListResponse } from '@/api/infoSessions'
import { createOrGetChatSession } from '@/api/chat'

const route = useRoute()
const router = useRouter()

// 数据
const school = ref<School | null>(null)
const loading = ref(false)
const isFavorited = ref(false)
const currentMark = ref<any>(null)

// 宣讲会列表
const infoSessions = ref<InfoSession[]>([])
const infoSessionsLoading = ref(false)

// 标记模态框
const showMarkModal = ref(false)
const submitting = ref(false)
const markForm = ref({
  note: '',
  color: 'blue'
})

// 申请宣讲会模态框
const showRequestInfoSessionModal = ref(false)
const requestForm = ref<OfflineInfoSessionRequest>({
  school_id: '',
  title: '',
  description: '',
  proposed_start_time: '',
  proposed_end_time: '',
  proposed_location: '',
  max_students: undefined,
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  message: ''
})

// 加载学校详情
const loadSchool = async () => {
  const schoolId = route.params.id as string
  if (!schoolId) return

  loading.value = true
  try {
    school.value = await getSchool(schoolId)
    
    // 检查收藏状态
    try {
      isFavorited.value = await checkFavorite('SCHOOL', schoolId)
    } catch (error) {
      isFavorited.value = false
    }

    // 检查标记状态
    try {
      currentMark.value = await getMark('SCHOOL', schoolId)
      if (currentMark.value) {
        markForm.value.note = currentMark.value.note || ''
        markForm.value.color = currentMark.value.color || 'blue'
      }
    } catch (error) {
      // 没有标记
      currentMark.value = null
    }

    // 加载该学校的宣讲会列表
    await loadInfoSessions(schoolId)
  } catch (error: any) {
    console.error('加载学校详情失败:', error)
    alert('加载学校详情失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 加载宣讲会列表
const loadInfoSessions = async (schoolId: string) => {
  infoSessionsLoading.value = true
  try {
    const response = await getInfoSessions({
      school_id: schoolId,
      page_size: 10
    })
    // 只显示该学校的宣讲会
    infoSessions.value = response.items.filter(session => session.school_id === schoolId)
  } catch (error: any) {
    console.error('加载宣讲会列表失败:', error)
  } finally {
    infoSessionsLoading.value = false
  }
}

// 切换收藏状态
const toggleFavorite = async () => {
  if (!school.value) return

  try {
    if (isFavorited.value) {
      await removeFavorite('SCHOOL', school.value.id)
      isFavorited.value = false
      alert('已取消收藏')
    } else {
      await addFavorite('SCHOOL', school.value.id)
      isFavorited.value = true
      alert('已收藏')
    }
  } catch (error: any) {
    console.error('收藏操作失败:', error)
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 分享学校
const handleShare = async () => {
  if (!school.value) return

  try {
    const shareData = await getSchoolShareLink(school.value.id)
    
    // 复制分享链接到剪贴板
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(shareData.share_url)
      alert('分享链接已复制到剪贴板')
    } else {
      // 降级方案：显示分享链接
      prompt('分享链接（请复制）：', shareData.share_url)
    }
  } catch (error: any) {
    console.error('获取分享链接失败:', error)
    alert('获取分享链接失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 保存标记
const handleMark = async () => {
  if (!school.value) return

  submitting.value = true
  try {
    const markData: MarkCreateRequest = {
      target_type: 'SCHOOL',
      target_id: school.value.id,
      note: markForm.value.note,
      color: markForm.value.color
    }

    if (currentMark.value) {
      // 更新现有标记
      await updateMark(currentMark.value.id, {
        note: markForm.value.note,
        color: markForm.value.color
      })
    } else {
      // 创建新标记
      currentMark.value = await createMark(markData)
    }

    alert('标记已保存')
    showMarkModal.value = false
  } catch (error: any) {
    console.error('保存标记失败:', error)
    alert('保存标记失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 发起聊天
const startChat = async () => {
  if (!school.value) return
  
  try {
    // 创建或获取与学校的聊天会话
    const session = await createOrGetChatSession(undefined, undefined, school.value.id)
    // 跳转到聊天页面
    router.push(`/enterprise/chat?session_id=${session.id}`)
  } catch (error: any) {
    console.error('发起聊天失败:', error)
    alert('发起聊天失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 显示申请模态框
const showRequestModal = () => {
  if (!school.value) return

  requestForm.value = {
    school_id: school.value.id,
    title: '',
    description: '',
    proposed_start_time: '',
    proposed_end_time: '',
    proposed_location: '',
    max_students: undefined,
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    message: ''
  }
  showRequestInfoSessionModal.value = true
}

// 提交申请
const handleRequestInfoSession = async () => {
  if (!school.value) return

  submitting.value = true
  try {
    await requestOfflineInfoSession(school.value.id, {
      ...requestForm.value,
      proposed_start_time: new Date(requestForm.value.proposed_start_time).toISOString(),
      proposed_end_time: new Date(requestForm.value.proposed_end_time).toISOString(),
    })
    alert('申请已提交，等待学校审批')
    showRequestInfoSessionModal.value = false
  } catch (error: any) {
    console.error('提交申请失败:', error)
    alert('提交申请失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 查看宣讲会详情
const viewInfoSession = (sessionId: string) => {
  router.push(`/enterprise/info-sessions?session_id=${sessionId}`)
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    DRAFT: '草稿',
    PENDING: '待审批',
    PUBLISHED: '已发布',
    ONGOING: '进行中',
    ENDED: '已结束',
    CANCELLED: '已取消'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadSchool()
})
</script>

<style scoped>
.enterprise-school-detail {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

