<template>
  <div class="student-offers w-full max-w-full px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-8">我的Offer</h1>

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
          v-model="statusFilter"
          @change="loadOffers"
          class="px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white transition-all duration-200"
        >
          <option value="">全部</option>
          <option value="PENDING">待处理</option>
          <option value="ACCEPTED">已接受</option>
          <option value="REJECTED">已拒绝</option>
          <option value="EXPIRED">已过期</option>
        </select>
      </div>
    </div>

    <!-- Offer列表 -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      <div v-else-if="offers.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-500 text-lg">暂无Offer记录</p>
        <p class="text-gray-400 text-sm mt-2">等待企业发送Offer</p>
      </div>
      <div
        v-for="offer in offers"
        :key="offer.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-200 border border-gray-200"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-green-50 rounded-lg">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900">{{ offer.job_title }}</h3>
            </div>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3 ml-11">
              <span v-if="offer.salary" class="flex items-center text-blue-600 font-semibold">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                薪资：{{ offer.salary }}元/月
              </span>
              <span v-if="offer.start_date" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                入职日期：{{ formatDate(offer.start_date) }}
              </span>
              <span v-if="offer.expires_at" class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                过期时间：{{ formatDate(offer.expires_at) }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                创建时间：{{ formatDate(offer.created_at) }}
              </span>
            </div>
            <div class="text-gray-700 mb-3 ml-11 bg-gray-50 p-4 rounded-xl border border-gray-200 whitespace-pre-wrap">{{ offer.content }}</div>
          </div>
          <div class="ml-6 flex flex-col items-end space-y-3">
            <span
              :class="getStatusClass(offer.status)"
              class="px-4 py-1.5 rounded-full text-sm font-medium"
            >
              {{ getStatusText(offer.status) }}
            </span>
            <div v-if="offer.status === 'PENDING'" class="flex space-x-2">
              <button
                @click="handleAccept(offer.id)"
                class="px-5 py-2.5 bg-green-600 text-white rounded-xl hover:bg-green-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                接受
              </button>
              <button
                @click="handleReject(offer.id)"
                class="px-5 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 shadow-sm hover:shadow-md transition-all duration-200 font-medium flex items-center"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                拒绝
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="mt-8 flex justify-center items-center space-x-4">
      <button
        v-if="page > 1"
        @click="page--; loadOffers()"
        class="px-5 py-2.5 bg-white border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium flex items-center"
      >
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        上一页
      </button>
      <span class="px-5 py-2.5 bg-white border-2 border-gray-200 rounded-xl text-gray-700 font-medium">
        {{ page }} / {{ Math.ceil(total / pageSize) }}
      </span>
      <button
        v-if="page < Math.ceil(total / pageSize)"
        @click="page++; loadOffers()"
        class="px-5 py-2.5 bg-white border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium flex items-center"
      >
        下一页
        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getOffers, acceptOffer, rejectOffer } from '@/api/offers'
import type { OfferResponse } from '@/types/index'

const offers = ref<OfferResponse[]>([])
const loading = ref(false)
const statusFilter = ref('')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const loadOffers = async () => {
  loading.value = true
  try {
    const res = await getOffers({
      page: page.value,
      page_size: pageSize.value,
      status: statusFilter.value || undefined
    })
    offers.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('加载Offer失败:', error)
    alert('加载Offer失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handleAccept = async (offerId: string) => {
  if (!confirm('确定要接受这个Offer吗？')) return
  try {
    await acceptOffer(offerId)
    alert('接受成功')
    loadOffers()
  } catch (error: any) {
    alert(error.response?.data?.detail || '接受失败，请稍后重试')
  }
}

const handleReject = async (offerId: string) => {
  if (!confirm('确定要拒绝这个Offer吗？')) return
  try {
    await rejectOffer(offerId)
    alert('拒绝成功')
    loadOffers()
  } catch (error: any) {
    alert(error.response?.data?.detail || '拒绝失败，请稍后重试')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    ACCEPTED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800',
    EXPIRED: 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    PENDING: '待处理',
    ACCEPTED: '已接受',
    REJECTED: '已拒绝',
    EXPIRED: '已过期'
  }
  return texts[status] || status
}

onMounted(() => {
  loadOffers()
})
</script>

