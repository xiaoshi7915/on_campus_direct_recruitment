<template>
  <div :class="['main-layout', isChatPage ? 'h-screen flex flex-col' : 'h-screen flex flex-col overflow-hidden']">
    <!-- 顶部导航栏 -->
    <header :class="['bg-white/95 backdrop-blur-md shadow-lg relative z-20 border-b border-gray-100/50', isChatPage ? 'flex-shrink-0' : '']">
      <nav class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <router-link to="/" class="flex items-center space-x-3 group animate-fade-in-up">
            <div class="relative p-2.5 bg-gradient-primary rounded-xl shadow-md group-hover:shadow-lg transition-all duration-300 transform group-hover:scale-105">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </div>
            <span class="text-2xl font-display font-bold text-gray-900">校园直聘</span>
          </router-link>
          
          <!-- 导航菜单 - 模块化分组 -->
          <div class="flex items-center space-x-1 overflow-x-auto scrollbar-hide" style="overflow: visible;">
            <!-- 首页链接 -->
            <router-link
              :to="homePath"
              class="px-4 py-2.5 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300 relative font-medium text-sm group"
              active-class="text-primary-600 bg-gradient-to-r from-primary-50 to-primary-100/50 font-semibold shadow-sm"
            >
              <span class="relative z-10">首页</span>
              <div class="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-5 rounded-xl transition-opacity"></div>
            </router-link>
            
            <!-- 未登录用户可见的导航菜单 -->
            <template v-if="!authStore.isAuthenticated()">
              <router-link
                to="/student/applications"
                class="px-4 py-2.5 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300 relative font-medium text-sm group"
                active-class="text-primary-600 bg-gradient-to-r from-primary-50 to-primary-100/50 font-semibold shadow-sm"
              >
                <span class="relative z-10">面试专区</span>
                <div class="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-5 rounded-xl transition-opacity"></div>
              </router-link>
              
              <router-link
                to="/student/resumes"
                class="px-4 py-2.5 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300 relative font-medium text-sm group"
                active-class="text-primary-600 bg-gradient-to-r from-primary-50 to-primary-100/50 font-semibold shadow-sm"
              >
                <span class="relative z-10">简历投递</span>
                <div class="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-5 rounded-xl transition-opacity"></div>
              </router-link>
            </template>
            
            <!-- 已登录用户的模块分组下拉菜单 -->
            <template v-else>
              <div
                v-for="module in menuModules"
                :key="module.id"
                class="relative group"
                style="overflow: visible; z-index: 100;"
                @mouseenter="setHoveredModule(module.id, true)"
                @mouseleave="setHoveredModule(null, false)"
              >
                <button
                  class="px-4 py-2.5 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300 font-medium text-sm flex items-center space-x-1"
                  :class="{ 'text-primary-600 bg-gradient-to-r from-primary-50 to-primary-100/50 font-semibold shadow-sm': isModuleActive(module) }"
                  @click="() => {
                    if (module.items && module.items.length > 0) {
                      router.push(module.items[0].path)
                    }
                  }"
                >
                  <span>{{ module.name }}</span>
                  <svg class="w-4 h-4 transition-transform duration-200" :class="{ 'rotate-180': hoveredModule === module.id }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                <!-- 下拉菜单 -->
                <div
                  v-if="hoveredModule === module.id"
                  class="absolute top-full left-0 mt-1 w-56 bg-white rounded-xl shadow-lg border border-gray-100/50 py-2 z-[9999] min-w-max"
                  style="pointer-events: auto !important; display: block !important; opacity: 1 !important; visibility: visible !important; position: absolute !important;"
                  @mouseenter="setHoveredModule(module.id, true)"
                  @mouseleave="setHoveredModule(null, false)"
                >
                  <router-link
                    v-for="item in module.items"
                    :key="item.path"
                    :to="item.path"
                    class="block px-4 py-2.5 text-gray-700 hover:text-primary-600 hover:bg-primary-50 transition-all duration-200 text-sm flex items-center justify-between"
                    active-class="text-primary-600 bg-primary-50 font-semibold"
                  >
                    <span class="flex items-center space-x-2">
                      <span>{{ item.name }}</span>
                    </span>
                    <span
                      v-if="typeof item.badge === 'number' && item.badge > 0"
                      class="bg-gradient-warm text-white text-xs rounded-full px-2 py-0.5 min-w-[20px] text-center"
                    >
                      {{ item.badge > 99 ? '99+' : item.badge }}
                    </span>
                  </router-link>
                </div>
              </div>
              
              <!-- 直接链接的菜单项（聊天等） -->
              <router-link
                v-for="item in directNavItems"
                :key="item.path"
                :to="item.path"
                class="px-4 py-2.5 text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300 relative font-medium text-sm group"
                active-class="text-primary-600 bg-gradient-to-r from-primary-50 to-primary-100/50 font-semibold shadow-sm"
              >
                <span class="relative z-10">{{ item.name }}</span>
                <div class="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-5 rounded-xl transition-opacity"></div>
              </router-link>
            </template>
            
            <!-- 用户信息 -->
            <div v-if="authStore.isAuthenticated()" class="flex items-center space-x-3 ml-4 pl-4 border-l border-gray-200/50">
              <div class="flex items-center space-x-2.5 px-4 py-2 bg-gradient-to-r from-primary-50 to-secondary-50 rounded-xl border border-primary-100/50 shadow-sm">
                <div class="w-9 h-9 bg-gradient-primary rounded-full flex items-center justify-center text-white font-semibold text-sm shadow-md">
                  {{ userInfo?.username?.charAt(0).toUpperCase() || 'U' }}
                </div>
                <span class="text-gray-700 font-medium text-sm">{{ userInfo?.username }}</span>
              </div>
              <button
                @click="handleLogout"
                class="px-5 py-2.5 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 shadow-md hover:shadow-lg transition-all duration-300 font-medium transform hover:scale-105"
              >
                退出
              </button>
            </div>
            <div v-else class="flex items-center space-x-3">
              <router-link
                to="/login"
                class="px-5 py-2.5 text-gray-700 hover:text-primary-600 font-medium transition-all duration-300 rounded-xl hover:bg-primary-50"
              >
                登录
              </router-link>
              <router-link
                to="/register"
                class="px-5 py-2.5 bg-gradient-primary text-white rounded-xl hover:shadow-lg transition-all duration-300 font-medium transform hover:scale-105 shadow-md"
              >
                注册
              </router-link>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <!-- 主要内容区域 -->
    <main :class="['relative z-10 flex-1 flex flex-col', isChatPage ? 'min-h-0' : (route.path === '/' ? 'min-h-0 overflow-hidden' : 'container mx-auto px-4 py-8')]">
      <!-- 面包屑导航 -->
      <Breadcrumb v-if="!isChatPage && route.path !== '/'" :unread-count="unreadMessageCount" />
      <router-view />
    </main>

    <!-- 底部（聊天页面不显示） -->
    <footer v-if="!isChatPage" class="bg-gradient-to-br from-gray-800 via-gray-900 to-gray-800 text-white mt-auto relative z-20 border-t border-gray-700/50">
      <div class="container mx-auto px-4 py-10">
        <div class="text-center">
          <div class="flex items-center justify-center space-x-2 mb-3">
            <div class="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <span class="text-lg font-display font-semibold">校园直聘平台</span>
          </div>
          <p class="text-gray-400 text-sm">&copy; 2025 mr stone的个人网站. All rights reserved.</p>
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
import Breadcrumb from '@/components/Breadcrumb.vue'
import { getMenuByUserType } from '@/config/menuConfig'
import type { MenuModule, MenuItem } from '@/config/menuConfig'
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

// 模块化菜单配置
const menuModules = ref<MenuModule[]>([])
const directNavItems = ref<Array<{ name: string; path: string }>>([])
const hoveredModule = ref<string | null>(null)
// 延迟关闭定时器
let closeTimer: ReturnType<typeof setTimeout> | null = null

// 清除延迟关闭定时器
const clearCloseTimer = () => {
  if (closeTimer) {
    clearTimeout(closeTimer)
    closeTimer = null
  }
}

// 延迟关闭下拉框
const scheduleClose = (moduleId: string | null) => {
  clearCloseTimer()
  closeTimer = setTimeout(() => {
    hoveredModule.value = moduleId
    closeTimer = null
  }, 150) // 150ms 延迟，给用户足够时间移动到下拉菜单
}

// 设置悬停模块（带延迟关闭）
const setHoveredModule = (moduleId: string | null, immediate: boolean = false) => {
  clearCloseTimer()
  if (immediate) {
    hoveredModule.value = moduleId
  } else {
    // 如果是关闭操作，使用延迟；如果是打开操作，立即执行
    if (moduleId === null) {
      scheduleClose(null)
    } else {
      hoveredModule.value = moduleId
    }
  }
}

// 首页路径
const homePath = computed(() => {
  if (!userInfo.value) return '/'
  switch (userInfo.value.user_type) {
    case 'STUDENT':
      return '/student'
    case 'ENTERPRISE':
      return '/enterprise'
    case 'TEACHER':
      return '/teacher'
    case 'ADMIN':
      return '/admin'
    default:
      return '/'
  }
})

// 检查模块是否激活（当前路由是否在该模块下）
const isModuleActive = (module: MenuModule): boolean => {
  return module.items.some(item => route.path.startsWith(item.path))
}

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

// 根据用户类型更新导航菜单（模块化）
const updateNavItems = () => {
  if (!userInfo.value) {
    menuModules.value = []
    directNavItems.value = []
    return
  }

  const userType = userInfo.value.user_type
  const modules = getMenuByUserType(userType, userInfo.value, unreadMessageCount.value)
  
  // 分离模块化菜单和直接链接
  menuModules.value = modules.filter(module => module.id !== 'communication')
  
  // 沟通交流模块作为直接链接
  const communicationModule = modules.find(m => m.id === 'communication')
  if (communicationModule && communicationModule.items.length > 0) {
    directNavItems.value = communicationModule.items.map(item => ({
      name: item.name,
      path: item.path,
    }))
  } else {
    directNavItems.value = []
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
  clearCloseTimer()
})
</script>

<style scoped>
.main-layout {
  @apply flex flex-col;
  height: 100vh;
  max-height: 100vh;
  overflow: hidden;
}
</style>

