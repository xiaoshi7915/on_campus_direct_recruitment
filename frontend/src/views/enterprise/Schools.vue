<template>
  <div class="enterprise-schools">
    <h1 class="text-3xl font-bold mb-6">学校搜索</h1>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">关键词搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索学校名称、代码..."
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="loadSchools"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">省份</label>
          <input
            v-model="provinceFilter"
            type="text"
            placeholder="省份"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="loadSchools"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">城市</label>
          <input
            v-model="cityFilter"
            type="text"
            placeholder="城市"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            @keyup.enter="loadSchools"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">认证状态</label>
          <select
            v-model="verifiedFilter"
            @change="loadSchools"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option :value="undefined">全部</option>
            <option :value="true">已认证</option>
            <option :value="false">未认证</option>
          </select>
        </div>
      </div>
      <div class="mt-4 flex justify-end">
        <button
          @click="loadSchools"
          class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          搜索
        </button>
      </div>
    </div>

    <!-- 学校列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="schools.length === 0" class="text-center py-12 text-gray-500">
        暂无学校数据
      </div>
      <div
        v-for="school in schools"
        :key="school.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer"
        @click="viewSchoolDetail(school.id)"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <img
                v-if="school.logo_url"
                :src="school.logo_url"
                :alt="school.name"
                class="w-16 h-16 rounded-lg object-cover"
              />
              <div>
                <h3 class="text-xl font-semibold">{{ school.name }}</h3>
                <div class="flex items-center space-x-2 mt-1">
                  <span
                    v-if="school.is_verified"
                    class="px-2 py-1 rounded text-xs bg-green-100 text-green-800"
                  >
                    已认证
                  </span>
                  <span
                    v-else
                    class="px-2 py-1 rounded text-xs bg-gray-100 text-gray-800"
                  >
                    未认证
                  </span>
                </div>
              </div>
            </div>
            <div class="text-gray-600 text-sm mb-3">
              <p v-if="school.province || school.city">
                地区：{{ [school.province, school.city].filter(Boolean).join(' ') }}
              </p>
              <p v-if="school.code">学校代码：{{ school.code }}</p>
              <p v-if="school.student_count !== undefined">学生数量：{{ school.student_count }}</p>
              <p v-if="school.department_count !== undefined">院系数量：{{ school.department_count }}</p>
            </div>
            <p v-if="school.description" class="text-gray-700 line-clamp-2">
              {{ school.description }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click.stop="viewSchoolDetail(school.id)"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              查看详情
            </button>
            <button
              @click.stop="toggleFavorite(school)"
              :class="isFavorited(school.id) ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-gray-500 hover:bg-gray-600'"
              class="px-4 py-2 text-white rounded-lg"
            >
              {{ isFavorited(school.id) ? '已收藏' : '收藏' }}
            </button>
            <button
              @click.stop="handleShare(school)"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              分享
            </button>
            <button
              @click.stop="showRequestModal(school)"
              class="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600"
            >
              申请宣讲会
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSchools, type School, requestOfflineInfoSession, type OfflineInfoSessionRequest } from '@/api/schools'
import { addFavorite, removeFavorite, checkFavorite } from '@/api/favorites'
import { getSchoolShareLink } from '@/api/schools'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()

// 数据
const schools = ref<School[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const searchKeyword = ref('')
const provinceFilter = ref('')
const cityFilter = ref('')
const verifiedFilter = ref<boolean | undefined>(undefined)

// 收藏状态
const favoritedSchoolIds = ref<Set<string>>(new Set())

// 申请宣讲会模态框
const showRequestInfoSessionModal = ref(false)
const currentRequestSchool = ref<School | null>(null)
const submitting = ref(false)
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

// 加载学校列表
const loadSchools = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    if (provinceFilter.value) {
      params.province = provinceFilter.value
    }
    if (cityFilter.value) {
      params.city = cityFilter.value
    }
    if (verifiedFilter.value !== undefined) {
      params.is_verified = verifiedFilter.value
    }

    const response = await getSchools(params)
    schools.value = response.items
    total.value = response.total

    // 检查收藏状态
    await checkFavoritesStatus()
  } catch (error: any) {
    console.error('加载学校列表失败:', error)
    alert('加载学校列表失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 检查收藏状态
const checkFavoritesStatus = async () => {
  for (const school of schools.value) {
    try {
      const isFavorited = await checkFavorite('SCHOOL', school.id)
      if (isFavorited) {
        favoritedSchoolIds.value.add(school.id)
      }
    } catch (error) {
      // 忽略错误，可能未收藏
    }
  }
}

// 分页变化处理
const handlePaginationChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
  loadSchools()
}

// 查看学校详情
const viewSchoolDetail = (schoolId: string) => {
  router.push(`/enterprise/schools/${schoolId}`)
}

// 切换收藏状态
const toggleFavorite = async (school: School) => {
  try {
    if (isFavorited(school.id)) {
      await removeFavorite('SCHOOL', school.id)
      favoritedSchoolIds.value.delete(school.id)
      alert('已取消收藏')
    } else {
      await addFavorite('SCHOOL', school.id)
      favoritedSchoolIds.value.add(school.id)
      alert('已收藏')
    }
  } catch (error: any) {
    console.error('收藏操作失败:', error)
    alert('操作失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 检查是否已收藏
const isFavorited = (schoolId: string): boolean => {
  return favoritedSchoolIds.value.has(schoolId)
}

// 分享学校
const handleShare = async (school: School) => {
  try {
    const shareData = await getSchoolShareLink(school.id)
    
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

// 显示申请宣讲会模态框
const showRequestModal = (school: School) => {
  currentRequestSchool.value = school
  requestForm.value = {
    school_id: school.id,
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
  if (!currentRequestSchool.value) return

  submitting.value = true
  try {
    await requestOfflineInfoSession(currentRequestSchool.value.id, {
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

onMounted(() => {
  loadSchools()
})
</script>

<style scoped>
.enterprise-schools {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

