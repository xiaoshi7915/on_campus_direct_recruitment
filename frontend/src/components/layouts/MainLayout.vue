<template>
  <div class="main-layout">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm">
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
              class="text-gray-700 hover:text-blue-600 transition-colors"
              active-class="text-blue-600 font-semibold"
            >
              {{ item.name }}
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
    <main class="container mx-auto px-4 py-8">
      <router-view />
    </main>

    <!-- 底部 -->
    <footer class="bg-gray-800 text-white mt-auto">
      <div class="container mx-auto px-4 py-8">
        <div class="text-center">
          <p>&copy; 2024 校园直聘平台. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCurrentUser } from '@/api/users'
import type { User } from '@/api/users'

const router = useRouter()
const authStore = useAuthStore()

// 用户信息
const userInfo = ref<User | null>(null)

// 导航菜单项（根据用户类型动态显示）
const navItems = ref<Array<{ name: string; path: string }>>([])

// 加载用户信息
const loadUserInfo = async () => {
  if (authStore.isAuthenticated()) {
    try {
      userInfo.value = await getCurrentUser()
      updateNavItems()
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
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
        { name: '我的收藏', path: '/student/favorites' },
        { name: '双选会', path: '/student/job-fairs' },
        { name: '宣讲会', path: '/student/info-sessions' },
        { name: '聊天', path: '/student/chat' },
        { name: '个人中心', path: '/student/profile' },
      ]
      break
    case 'ENTERPRISE':
      navItems.value = [
        { name: '首页', path: '/enterprise' },
        { name: '职位管理', path: '/enterprise/jobs' },
        { name: '人才搜索', path: '/enterprise/talents' },
        { name: '申请管理', path: '/enterprise/applications' },
        { name: '双选会', path: '/enterprise/job-fairs' },
        { name: '宣讲会', path: '/enterprise/info-sessions' },
        { name: '聊天', path: '/enterprise/chat' },
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
</script>

<style scoped>
.main-layout {
  @apply min-h-screen flex flex-col;
}
</style>

