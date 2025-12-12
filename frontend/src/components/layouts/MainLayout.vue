<template>
  <div :class="['main-layout', isChatPage ? 'h-screen flex flex-col' : '']">
    <!-- 顶部导航栏 -->
    <header :class="['bg-white shadow-sm', isChatPage ? 'flex-shrink-0' : '']">
      <nav class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <router-link to="/" class="text-2xl font-bold text-blue-600">
            校园直聘
          </router-link>
          
          <!-- 导航菜单 -->
          <div class="flex items-center space-x-6">
            <router-link
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="text-gray-700 hover:text-blue-600 transition-colors relative"
              active-class="text-blue-600 font-semibold"
            >
              {{ item.name }}
              <!-- 系统消息未读提醒 -->
              <span
                v-if="item.path.includes('system-messages') && unreadMessageCount > 0"
                class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
              >
                {{ unreadMessageCount > 99 ? '99+' : unreadMessageCount }}
              </span>
            </router-link>
            
            <!-- 用户信息 -->
            <div v-if="authStore.isAuthenticated()" class="flex items-center space-x-4">
              <span class="text-gray-700">{{ userInfo?.username }}</span>
              <button
                @click="handleLogout"
                class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              >
                退出
              </button>
            </div>
            <div v-else class="flex items-center space-x-4">
              <router-link
                to="/login"
                class="px-4 py-2 text-gray-700 hover:text-blue-600"
              >
                登录
              </router-link>
              <router-link
                to="/register"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                注册
              </router-link>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <!-- 主要内容区域 -->
    <main :class="isChatPage ? 'flex-1 flex flex-col min-h-0' : 'container mx-auto px-4 py-8'">
      <router-view />
    </main>

    <!-- 底部（聊天页面不显示） -->
    <footer v-if="!isChatPage" class="bg-gray-800 text-white mt-auto">
      <div class="container mx-auto px-4 py-8">
        <div class="text-center">
          <p>&copy; 2024 校园直聘平台. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCurrentUser } from '@/api/users'
import { getUnreadCount } from '@/api/systemMessages'
import type { User } from '@/api/users'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 判断是否是聊天页面
const isChatPage = computed(() => {
  return route.path.includes('/chat')
})

// 用户信息
const userInfo = ref<User | null>(null)

// 导航菜单项（根据用户类型动态显示）
const navItems = ref<Array<{ name: string; path: string }>>([])

// 未读消息数量
const unreadMessageCount = ref(0)
let unreadCountInterval: number | null = null

// 加载用户信息
const loadUserInfo = async () => {
  if (authStore.isAuthenticated()) {
    try {
      userInfo.value = await getCurrentUser()
      updateNavItems()
      // 加载未读消息数量
      loadUnreadCount()
      // 启动定时刷新未读消息数量（每30秒）
      startUnreadCountPolling()
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }
}

// 加载未读消息数量
const loadUnreadCount = async () => {
  if (authStore.isAuthenticated()) {
    try {
      const res = await getUnreadCount()
      unreadMessageCount.value = res.unread_count || 0
    } catch (error) {
      // 静默处理错误，不影响页面加载
    }
  }
}

// 启动未读消息数量轮询
const startUnreadCountPolling = () => {
  // 清除之前的定时器
  if (unreadCountInterval !== null) {
    clearInterval(unreadCountInterval)
  }
  // 每30秒刷新一次未读消息数量
  unreadCountInterval = window.setInterval(() => {
    loadUnreadCount()
  }, 30000)
}

// 停止未读消息数量轮询
const stopUnreadCountPolling = () => {
  if (unreadCountInterval !== null) {
    clearInterval(unreadCountInterval)
    unreadCountInterval = null
  }
}

// 根据用户类型更新导航菜单
const updateNavItems = () => {
  if (!userInfo.value) {
    navItems.value = []
    return
  }

  const userType = userInfo.value.user_type
  switch (userType) {
    case 'STUDENT':
      navItems.value = [
        { name: '首页', path: '/student' },
        { name: '职位搜索', path: '/student/jobs' },
        { name: '我的简历', path: '/student/resumes' },
        { name: '我的申请', path: '/student/applications' },
        { name: '我的Offer', path: '/student/offers' },
        { name: '求职意向', path: '/student/job-intentions' },
        { name: '我的收藏', path: '/student/favorites' },
        { name: '双选会', path: '/student/job-fairs' },
        { name: '宣讲会', path: '/student/info-sessions' },
        { name: '聊天', path: '/student/chat' },
        { name: '系统消息', path: '/student/system-messages' },
        { name: '待办中心', path: '/student/todos' },
        { name: '意见反馈', path: '/student/feedback' },
        { name: '个人中心', path: '/student/profile' },
      ]
      break
    case 'ENTERPRISE':
      navItems.value = [
        { name: '首页', path: '/enterprise' },
        { name: '职位管理', path: '/enterprise/jobs' },
        { name: '人才搜索', path: '/enterprise/talents' },
        { name: '人才库', path: '/enterprise/talent-library' },
        { name: '申请管理', path: '/enterprise/applications' },
        { name: '学校搜索', path: '/enterprise/schools' },
        { name: '双选会', path: '/enterprise/job-fairs' },
        { name: '宣讲会', path: '/enterprise/info-sessions' },
        { name: '聊天', path: '/enterprise/chat' },
        { name: '日程管理', path: '/enterprise/schedules' },
        { name: '系统消息', path: '/enterprise/system-messages' },
        { name: '数据报表', path: '/enterprise/statistics' },
        { name: '子账号管理', path: '/enterprise/sub-accounts' },
        { name: '意见反馈', path: '/enterprise/feedback' },
        { name: '宣传页预览', path: '/enterprise/preview' },
        { name: '企业中心', path: '/enterprise/profile' },
      ]
      break
    case 'TEACHER':
      navItems.value = [
        { name: '工作台', path: '/teacher' },
        { name: '学生管理', path: '/teacher/students' },
        { name: '我的院校', path: '/teacher/departments' },
        { name: '子账号管理', path: '/teacher/sub-accounts' },
        { name: '双选会管理', path: '/teacher/job-fairs' },
        { name: '宣讲会管理', path: '/teacher/info-sessions' },
        { name: '聊天', path: '/teacher/chat' },
        { name: '系统消息', path: '/teacher/system-messages' },
        { name: '数据统计', path: '/teacher/statistics' },
        { name: '个人中心', path: '/teacher/profile' },
      ]
      break
    case 'ADMIN':
      navItems.value = [
        { name: '管理后台', path: '/admin' },
        { name: '用户管理', path: '/admin/users' },
        { name: '教师审批', path: '/admin/teacher-approvals' },
        { name: '权益管理', path: '/admin/rights' },
        { name: '数据统计', path: '/admin/statistics' },
      ]
      break
    default:
      navItems.value = []
  }
}

// 退出登录
const handleLogout = () => {
  authStore.userLogout()
  router.push('/login')
}

onMounted(() => {
  loadUserInfo()
})

onUnmounted(() => {
  stopUnreadCountPolling()
})
</script>

<style scoped>
.main-layout {
  @apply min-h-screen flex flex-col;
}
</style>

