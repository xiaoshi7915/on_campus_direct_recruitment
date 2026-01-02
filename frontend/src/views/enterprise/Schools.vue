<template>
  <div class="enterprise-schools w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">学校搜索</h1>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-100">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">关键词搜索</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索学校名称、代码..."
              class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              @keyup.enter="loadSchools"
            />
          </div>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">省份</label>
          <input
            v-model="provinceFilter"
            type="text"
            placeholder="省份"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @keyup.enter="loadSchools"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">城市</label>
          <input
            v-model="cityFilter"
            type="text"
            placeholder="城市"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            @keyup.enter="loadSchools"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">认证状态</label>
          <select
            v-model="verifiedFilter"
            @change="loadSchools"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
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
          class="btn btn-primary btn-md"
        >
          <svg class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          搜索
        </button>
      </div>
    </div>

    <!-- 学校列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="schools.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
        </svg>
        <p class="text-gray-500 text-lg">暂无学校数据</p>
        <p class="text-gray-400 text-sm mt-2">尝试调整搜索条件</p>
      </div>
      <div
        v-for="school in schools"
        :key="school.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200 cursor-pointer"
        @click="viewSchoolDetail(school.id)"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-4 mb-3">
              <div class="w-20 h-20 rounded-xl overflow-hidden bg-gray-100 border-2 border-gray-200 flex items-center justify-center shadow-sm">
                <img
                  v-if="school.logo_url"
                  :src="school.logo_url"
                  :alt="school.name"
                  class="w-full h-full object-cover"
                />
                <svg v-else class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ school.name }}</h3>
                <div class="flex items-center space-x-2">
                  <span
                    v-if="school.is_verified"
                    class="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 flex items-center"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    已认证
                  </span>
                  <span
                    v-else
                    class="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    未认证
                  </span>
                </div>
              </div>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-24">
              <span v-if="school.province || school.city" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                地区：{{ [school.province, school.city].filter(Boolean).join(' ') }}
              </span>
              <span v-if="school.code" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                </svg>
                学校代码：{{ school.code }}
              </span>
              <span v-if="school.student_count !== undefined" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                学生数量：{{ school.student_count }}
              </span>
              <span v-if="school.department_count !== undefined" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                院系数量：{{ school.department_count }}
              </span>
            </div>
            <p v-if="school.description" class="text-gray-700 line-clamp-2 ml-24 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {{ school.description }}
            </p>
          </div>
          <div class="ml-6 flex flex-col space-y-2">
            <button
              @click.stop="viewSchoolDetail(school.id)"
              class="btn btn-primary btn-md whitespace-nowrap"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              查看详情
            </button>
            <button
              @click.stop="toggleFavorite(school)"
              :class="[
                'btn btn-md whitespace-nowrap',
                isFavorited(school.id) ? 'btn-warning' : 'btn-secondary'
              ]"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              {{ isFavorited(school.id) ? '已收藏' : '收藏' }}
            </button>
            <button
              @click.stop="handleShare(school)"
              class="btn btn-success btn-md whitespace-nowrap"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
              </svg>
              分享
            </button>
            <button
              @click.stop="showRequestModal(school)"
              class="btn btn-primary btn-md whitespace-nowrap"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              申请宣讲会
            </button>
            <button
              @click.stop="startChat(school.id)"
              class="btn btn-primary btn-md whitespace-nowrap"
            >
              <svg class="w-4 h-4 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
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

    <!-- 申请宣讲会模态框 -->
    <div v-if="showRequestInfoSessionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-100">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            申请线下宣讲会
          </h2>
          <button
            @click="showRequestInfoSessionModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleRequestInfoSession" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">宣讲会标题 *</label>
            <input
              v-model="requestForm.title"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
            <textarea
              v-model="requestForm.description"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
            />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">建议开始时间 *</label>
              <input
                v-model="requestForm.proposed_start_time"
                type="datetime-local"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">建议结束时间 *</label>
              <input
                v-model="requestForm.proposed_end_time"
                type="datetime-local"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">建议地点</label>
            <input
              v-model="requestForm.proposed_location"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">最大学生数</label>
            <input
              v-model.number="requestForm.max_students"
              type="number"
              min="1"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
            />
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">联系人</label>
              <input
                v-model="requestForm.contact_person"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">联系电话</label>
              <input
                v-model="requestForm.contact_phone"
                type="tel"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">联系邮箱</label>
              <input
                v-model="requestForm.contact_email"
                type="email"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">申请留言</label>
            <textarea
              v-model="requestForm.message"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200 resize-none"
            />
          </div>
          <div class="pt-4 border-t border-gray-200 flex justify-end space-x-4">
            <button
              type="button"
              @click="showRequestInfoSessionModal = false"
              class="btn btn-secondary btn-md"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="btn btn-primary btn-md"
            >
              <svg v-if="!submitting" class="w-5 h-5 btn-icon-left" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else class="animate-spin h-5 w-5 btn-icon-left" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
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
import { createOrGetChatSession } from '@/api/chat'
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

// 发起聊天
const startChat = async (schoolId: string) => {
  try {
    // 创建或获取与学校的聊天会话
    const session = await createOrGetChatSession(undefined, undefined, schoolId)
    // 跳转到聊天页面
    router.push(`/enterprise/chat?session_id=${session.id}`)
  } catch (error: any) {
    console.error('发起聊天失败:', error)
    alert('发起聊天失败: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadSchools()
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

