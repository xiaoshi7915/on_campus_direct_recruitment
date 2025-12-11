<template>
  <div class="student-offers">
    <h1 class="text-3xl font-bold mb-6">我的Offer</h1>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">状态筛选：</label>
        <select
          v-model="statusFilter"
          @change="loadOffers"
          class="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="offers.length === 0" class="text-center py-12 text-gray-500">
        暂无Offer记录
      </div>
      <div
        v-for="offer in offers"
        :key="offer.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ offer.job_title }}</h3>
            <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-3">
              <span v-if="offer.salary">薪资：{{ offer.salary }}元/月</span>
              <span v-if="offer.start_date">入职日期：{{ formatDate(offer.start_date) }}</span>
              <span v-if="offer.expires_at">过期时间：{{ formatDate(offer.expires_at) }}</span>
              <span>创建时间：{{ formatDate(offer.created_at) }}</span>
            </div>
            <div class="text-gray-700 mb-3 whitespace-pre-wrap">{{ offer.content }}</div>
          </div>
          <div class="ml-6 flex flex-col items-end space-y-2">
            <span
              :class="getStatusClass(offer.status)"
              class="px-3 py-1 rounded-full text-sm"
            >
              {{ getStatusText(offer.status) }}
            </span>
            <div v-if="offer.status === 'PENDING'" class="flex space-x-2">
              <button
                @click="handleAccept(offer.id)"
                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
              >
                接受
              </button>
              <button
                @click="handleReject(offer.id)"
                class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              >
                拒绝
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="mt-6 flex justify-center">
      <button
        v-if="page > 1"
        @click="page--; loadOffers()"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 mr-2"
      >
        上一页
      </button>
      <span class="px-4 py-2">{{ page }} / {{ Math.ceil(total / pageSize) }}</span>
      <button
        v-if="page < Math.ceil(total / pageSize)"
        @click="page++; loadOffers()"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 ml-2"
      >
        下一页
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

