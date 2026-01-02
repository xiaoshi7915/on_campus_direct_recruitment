<template>
  <nav v-if="items.length > 0" class="mb-6 animate-fade-in-up relative z-10" style="overflow: visible;" aria-label="面包屑导航">
    <ol class="flex items-center space-x-2 text-sm" style="overflow: visible;">
      <li v-for="(item, index) in items" :key="index" class="flex items-center relative" style="overflow: visible; z-index: 100;">
        <!-- 有下拉菜单的模块项 -->
        <div
          v-if="item.moduleItems && item.moduleItems.length > 0"
          class="relative group"
          style="overflow: visible; position: relative; z-index: 100;"
          @mouseenter="() => {
            // 鼠标进入外层容器，立即显示下拉菜单
            setHoveredModule(index, true)
          }"
          @mouseleave="() => {
            // 延迟关闭，给用户时间移动到下拉菜单
            setHoveredModule(null, false)
          }"
        >
          <button
            class="text-gray-600 hover:text-primary-600 transition-colors duration-200 font-medium flex items-center space-x-1 relative z-10"
            :class="{ 'text-primary-600': hoveredModule === index }"
            style="pointer-events: auto; cursor: pointer;"
            @mouseenter="() => {
              // 鼠标进入按钮，立即显示下拉菜单
              setHoveredModule(index, true)
            }"
          >
            <span>{{ item.name }}</span>
            <svg
              class="w-4 h-4 transition-transform duration-200"
              :class="{ 'rotate-180': hoveredModule === index }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          <!-- 下拉菜单 -->
          <div
            v-if="hoveredModule === index"
            class="absolute top-full left-0 mt-1 w-56 bg-white rounded-xl shadow-lg border border-gray-100/50 py-2 z-[9999] min-w-max transition-all duration-200 ease-out"
            style="pointer-events: auto !important; display: block !important; opacity: 1 !important; visibility: visible !important; position: absolute !important;"
            :key="`dropdown-${index}-${hoveredModule}`"
            @mouseenter="() => {
              // 鼠标进入下拉菜单，立即显示并清除关闭定时器
              setHoveredModule(index, true)
            }"
            @mouseleave="() => {
              // 鼠标离开下拉菜单，延迟关闭
              setHoveredModule(null, false)
            }"
          >
              <router-link
                v-for="menuItem in item.moduleItems"
                :key="menuItem.path"
                :to="menuItem.path"
                class="block px-4 py-2.5 text-gray-700 hover:text-primary-600 hover:bg-primary-50 transition-all duration-200 text-sm whitespace-nowrap"
                active-class="text-primary-600 bg-primary-50 font-semibold"
                @click="setHoveredModule(null)"
              >
                {{ menuItem.name }}
              </router-link>
          </div>
        </div>
        
        <!-- 普通链接项 -->
        <router-link
          v-else-if="item.path && index < items.length - 1"
          :to="item.path"
          class="text-gray-600 hover:text-primary-600 transition-colors duration-200 font-medium"
        >
          {{ item.name }}
        </router-link>
        
        <!-- 当前页项（无链接） -->
        <span
          v-else
          class="text-gray-900 font-semibold"
        >
          {{ item.name }}
        </span>
        
        <!-- 分隔符 -->
        <svg
          v-if="index < items.length - 1"
          class="w-4 h-4 mx-2 text-gray-400"
          style="pointer-events: none;"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getMenuByUserType } from '@/config/menuConfig'
import type { MenuItem } from '@/config/menuConfig'

interface BreadcrumbItem {
  name: string
  path?: string
  moduleItems?: MenuItem[] // 模块下的菜单项
  moduleId?: string // 模块ID（用于调试）
}

// Props
interface Props {
  unreadCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  unreadCount: 0,
})

const route = useRoute()
const authStore = useAuthStore()
const hoveredModule = ref<number | null>(null)
// 延迟关闭定时器
let closeTimer: ReturnType<typeof setTimeout> | null = null

// 注意：在 Vue 3 模板中，ref 应该自动解包，但为了确保正确性，我们使用 hoveredModule.value
// 在模板中，我们直接使用 hoveredModule，Vue 会自动解包

// 清除延迟关闭定时器
const clearCloseTimer = () => {
  if (closeTimer) {
    clearTimeout(closeTimer)
    closeTimer = null
  }
}

// 延迟关闭下拉框
const scheduleClose = (index: number | null) => {
  clearCloseTimer()
  closeTimer = setTimeout(() => {
    hoveredModule.value = index
    closeTimer = null
  }, 150) // 150ms 延迟，给用户足够时间移动到下拉菜单
}

// 辅助函数：设置 hoveredModule（用于模板中的事件处理）
const setHoveredModule = (index: number | null, immediate: boolean = false) => {
  clearCloseTimer()
  if (immediate) {
    hoveredModule.value = index
  } else {
    // 如果是关闭操作，使用延迟；如果是打开操作，立即执行
    if (index === null) {
      scheduleClose(null)
    } else {
      hoveredModule.value = index
    }
  }
}

// 使用computed确保响应式更新菜单配置
const menuModules = computed(() => {
  const user = authStore.userInfo
  if (!user) {
    if ((import.meta as any).env?.DEV) {
      console.log('[Breadcrumb] userInfo is null, returning empty menu modules')
    }
    return []
  }
  // 使用props传递的未读消息数量
  const modules = getMenuByUserType(user.user_type, user, props.unreadCount)
  if ((import.meta as any).env?.DEV) {
    console.log('[Breadcrumb] menuModules:', modules, 'unreadCount:', props.unreadCount)
  }
  return modules
})

// 监听用户信息变化，确保菜单配置更新
watch(() => authStore.userInfo, (newUser) => {
  if (newUser && (import.meta as any).env?.DEV) {
    console.log('[Breadcrumb] userInfo updated:', newUser)
  }
}, { immediate: true })

// 组件挂载时确保用户信息已加载
onMounted(async () => {
  if (authStore.isAuthenticated() && !authStore.userInfo) {
    if ((import.meta as any).env?.DEV) {
      console.log('[Breadcrumb] Fetching user info on mount')
    }
    try {
      await authStore.fetchUserInfo()
    } catch (error) {
      console.error('[Breadcrumb] Failed to fetch user info:', error)
    }
  }
})

// 模块化面包屑路径映射（添加moduleId用于匹配）
interface BreadcrumbMapItem {
  moduleId?: string // 模块ID，用于匹配menuConfig中的模块
  module?: string // 模块名称（保留用于显示）
  items: BreadcrumbItem[]
}

const breadcrumbMap: Record<string, BreadcrumbMapItem> = {
  // 学生端
  '/student': { items: [{ name: '学生端', path: '/student' }, { name: '首页' }] },
  '/student/jobs': { moduleId: 'job_center', module: '求职中心', items: [{ name: '学生端', path: '/student' }, { name: '求职中心' }, { name: '职位搜索', path: '/student/jobs' }] },
  '/student/applications': { moduleId: 'job_center', module: '求职中心', items: [{ name: '学生端', path: '/student' }, { name: '求职中心' }, { name: '我的申请' }] },
  '/student/offers': { moduleId: 'job_center', module: '求职中心', items: [{ name: '学生端', path: '/student' }, { name: '求职中心' }, { name: '我的Offer' }] },
  '/student/job-intentions': { moduleId: 'job_center', module: '求职中心', items: [{ name: '学生端', path: '/student' }, { name: '求职中心' }, { name: '求职意向' }] },
  '/student/resumes': { moduleId: 'personal', module: '个人管理', items: [{ name: '学生端', path: '/student' }, { name: '个人管理' }, { name: '我的简历', path: '/student/resumes' }] },
  '/student/favorites': { moduleId: 'personal', module: '个人管理', items: [{ name: '学生端', path: '/student' }, { name: '个人管理' }, { name: '我的收藏' }] },
  '/student/todos': { moduleId: 'personal', module: '个人管理', items: [{ name: '学生端', path: '/student' }, { name: '个人管理' }, { name: '待办中心' }] },
  '/student/job-fairs': { moduleId: 'campus', module: '校园活动', items: [{ name: '学生端', path: '/student' }, { name: '校园活动' }, { name: '双选会' }] },
  '/student/info-sessions': { moduleId: 'campus', module: '校园活动', items: [{ name: '学生端', path: '/student' }, { name: '校园活动' }, { name: '宣讲会' }] },
  '/student/profile': { moduleId: 'settings', module: '个人设置', items: [{ name: '学生端', path: '/student' }, { name: '个人设置' }, { name: '个人中心' }] },
  '/student/system-messages': { moduleId: 'settings', module: '个人设置', items: [{ name: '学生端', path: '/student' }, { name: '个人设置' }, { name: '系统消息' }] },
  '/student/schedules': { moduleId: 'settings', module: '个人设置', items: [{ name: '学生端', path: '/student' }, { name: '个人设置' }, { name: '日程管理' }] },
  '/student/feedback': { moduleId: 'settings', module: '个人设置', items: [{ name: '学生端', path: '/student' }, { name: '个人设置' }, { name: '意见反馈' }] },
  '/student/chat': { moduleId: 'communication', module: '沟通交流', items: [{ name: '学生端', path: '/student' }, { name: '沟通交流' }, { name: '聊天' }] },
  
  // 企业端
  '/enterprise': { items: [{ name: '企业端', path: '/enterprise' }, { name: '首页' }] },
  '/enterprise/jobs': { moduleId: 'job', module: '职位管理', items: [{ name: '企业端', path: '/enterprise' }, { name: '职位管理' }, { name: '职位管理', path: '/enterprise/jobs' }] },
  '/enterprise/talents': { moduleId: 'talent', module: '人才管理', items: [{ name: '企业端', path: '/enterprise' }, { name: '人才管理' }, { name: '人才搜索' }] },
  '/enterprise/talent-library': { moduleId: 'talent', module: '人才管理', items: [{ name: '企业端', path: '/enterprise' }, { name: '人才管理' }, { name: '人才库' }] },
  '/enterprise/applications': { moduleId: 'talent', module: '人才管理', items: [{ name: '企业端', path: '/enterprise' }, { name: '人才管理' }, { name: '申请管理', path: '/enterprise/applications' }] },
  '/enterprise/schools': { moduleId: 'school', module: '学校管理', items: [{ name: '企业端', path: '/enterprise' }, { name: '学校管理' }, { name: '学校搜索' }] },
  '/enterprise/job-fairs': { moduleId: 'school', module: '学校管理', items: [{ name: '企业端', path: '/enterprise' }, { name: '学校管理' }, { name: '双选会' }] },
  '/enterprise/info-sessions': { moduleId: 'school', module: '学校管理', items: [{ name: '企业端', path: '/enterprise' }, { name: '学校管理' }, { name: '宣讲会' }] },
  '/enterprise/profile': { moduleId: 'settings', module: '个人设置', items: [{ name: '企业端', path: '/enterprise' }, { name: '个人设置' }, { name: '企业中心' }] },
  '/enterprise/sub-accounts': { moduleId: 'settings', module: '个人设置', items: [{ name: '企业端', path: '/enterprise' }, { name: '个人设置' }, { name: '子账号管理' }] },
  '/enterprise/system-messages': { moduleId: 'settings', module: '个人设置', items: [{ name: '企业端', path: '/enterprise' }, { name: '个人设置' }, { name: '系统消息' }] },
  '/enterprise/schedules': { moduleId: 'settings', module: '个人设置', items: [{ name: '企业端', path: '/enterprise' }, { name: '个人设置' }, { name: '日程管理' }] },
  '/enterprise/feedback': { moduleId: 'settings', module: '个人设置', items: [{ name: '企业端', path: '/enterprise' }, { name: '个人设置' }, { name: '意见反馈' }] },
  '/enterprise/preview': { moduleId: 'settings', module: '个人设置', items: [{ name: '企业端', path: '/enterprise' }, { name: '个人设置' }, { name: '宣传页预览' }] },
  '/enterprise/statistics': { moduleId: 'statistics', module: '数据报表', items: [{ name: '企业端', path: '/enterprise' }, { name: '数据报表' }, { name: '数据报表' }] },
  '/enterprise/chat': { moduleId: 'communication', module: '沟通交流', items: [{ name: '企业端', path: '/enterprise' }, { name: '沟通交流' }, { name: '聊天' }] },
  
  // 教师端
  '/teacher': { items: [{ name: '教师端', path: '/teacher' }, { name: '工作台' }] },
  '/teacher/students': { moduleId: 'student', module: '学生管理', items: [{ name: '教师端', path: '/teacher' }, { name: '学生管理' }, { name: '学生管理' }] },
  '/teacher/student-comments': { moduleId: 'student', module: '学生管理', items: [{ name: '教师端', path: '/teacher' }, { name: '学生管理' }, { name: '学生点评' }] },
  '/teacher/talent-recommendations': { moduleId: 'student', module: '学生管理', items: [{ name: '教师端', path: '/teacher' }, { name: '学生管理' }, { name: '人才推荐' }] },
  '/teacher/departments': { moduleId: 'school', module: '学校管理', items: [{ name: '教师端', path: '/teacher' }, { name: '学校管理' }, { name: '我的院校' }] },
  '/teacher/job-fairs': { moduleId: 'school', module: '学校管理', items: [{ name: '教师端', path: '/teacher' }, { name: '学校管理' }, { name: '双选会管理' }] },
  '/teacher/info-sessions': { moduleId: 'school', module: '学校管理', items: [{ name: '教师端', path: '/teacher' }, { name: '学校管理' }, { name: '宣讲会管理' }] },
  '/teacher/profile': { moduleId: 'settings', module: '个人设置', items: [{ name: '教师端', path: '/teacher' }, { name: '个人设置' }, { name: '个人中心' }] },
  '/teacher/sub-accounts': { moduleId: 'settings', module: '个人设置', items: [{ name: '教师端', path: '/teacher' }, { name: '个人设置' }, { name: '子账号管理' }] },
  '/teacher/system-messages': { moduleId: 'settings', module: '个人设置', items: [{ name: '教师端', path: '/teacher' }, { name: '个人设置' }, { name: '系统消息' }] },
  '/teacher/statistics': { moduleId: 'statistics', module: '数据统计', items: [{ name: '教师端', path: '/teacher' }, { name: '数据统计' }, { name: '数据统计' }] },
  '/teacher/chat': { moduleId: 'communication', module: '沟通交流', items: [{ name: '教师端', path: '/teacher' }, { name: '沟通交流' }, { name: '聊天' }] },
  
  // 管理员端
  '/admin': { items: [{ name: '管理端', path: '/admin' }, { name: '管理后台' }] },
  '/admin/users': { moduleId: 'user_management', module: '用户管理', items: [{ name: '管理端', path: '/admin' }, { name: '用户管理' }, { name: '用户管理' }] },
  '/admin/teacher-approvals': { moduleId: 'user_management', module: '用户管理', items: [{ name: '管理端', path: '/admin' }, { name: '用户管理' }, { name: '教师审批' }] },
  '/admin/rights': { moduleId: 'system', module: '系统设置', items: [{ name: '管理端', path: '/admin' }, { name: '系统设置' }, { name: '权益管理' }] },
  '/admin/statistics': { moduleId: 'statistics', module: '数据统计', items: [{ name: '管理端', path: '/admin' }, { name: '数据统计' }, { name: '数据统计' }] },
}

// 根据路由生成面包屑
const items = computed<BreadcrumbItem[]>(() => {
  const path = route.path
  const modules = menuModules.value
  
  if ((import.meta as any).env?.DEV) {
    console.log('[Breadcrumb] Generating breadcrumb for path:', path)
    console.log('[Breadcrumb] Available modules:', modules.map(m => ({ id: m.id, name: m.name })))
  }
  
  // 先尝试精确匹配
  let breadcrumbItems: BreadcrumbItem[] = []
  let currentConfig: BreadcrumbMapItem | undefined = undefined
  
  if (breadcrumbMap[path]) {
    breadcrumbItems = [...breadcrumbMap[path].items]
    currentConfig = breadcrumbMap[path]
  } else {
    // 处理动态路由（如 /jobs/:id, /resumes/:id）
    for (const [pattern, config] of Object.entries(breadcrumbMap)) {
      // 处理动态路由匹配
      let regexPattern = pattern.replace(/:[^/]+/g, '[^/]+')
      // 确保路径末尾匹配
      if (!regexPattern.endsWith('$')) {
        regexPattern = '^' + regexPattern + '(?:/[^/]+)?$'
      } else {
        regexPattern = '^' + regexPattern
      }
      const regex = new RegExp(regexPattern)
      
      if (regex.test(path)) {
        breadcrumbItems = [...config.items]
        currentConfig = config
        // 如果是详情页，添加详情项
        const pathSegments = path.split('/').filter(s => s)
        if (pathSegments.length >= 3) {
          const lastSegment = pathSegments[pathSegments.length - 1]
          if (lastSegment && lastSegment !== 'new' && lastSegment !== 'edit' && !isNaN(Number(lastSegment))) {
            const detailName = path.includes('/jobs/') ? '职位详情' :
                              path.includes('/applications/') ? '申请详情' :
                              path.includes('/resumes/') ? '简历详情' :
                              path.includes('/schools/') ? '学校详情' :
                              '详情'
            breadcrumbItems.push({ name: detailName })
          }
        }
        break
      }
    }
    
    // 特殊处理企业端简历详情页
    if (path.startsWith('/enterprise/resumes/') && path !== '/enterprise/resumes') {
      const resumeId = path.split('/').pop()
      if (resumeId && resumeId !== 'new' && resumeId !== 'edit') {
        breadcrumbItems = [
          { name: '企业端', path: '/enterprise' },
          { name: '人才管理', moduleId: 'talent' },
          { name: '简历详情' }
        ]
        currentConfig = { moduleId: 'talent', module: '人才管理', items: breadcrumbItems }
      }
    }
    
    // 默认处理：根据路径前缀生成
    if (breadcrumbItems.length === 0) {
      if (path.startsWith('/student')) {
        breadcrumbItems = [{ name: '学生端', path: '/student' }, { name: '未知页面' }]
      } else if (path.startsWith('/enterprise')) {
        breadcrumbItems = [{ name: '企业端', path: '/enterprise' }, { name: '未知页面' }]
      } else if (path.startsWith('/teacher')) {
        breadcrumbItems = [{ name: '教师端', path: '/teacher' }, { name: '未知页面' }]
      } else if (path.startsWith('/admin')) {
        breadcrumbItems = [{ name: '管理端', path: '/admin' }, { name: '未知页面' }]
      }
    }
  }
  
  // 为模块名称添加下拉菜单项
  const result = breadcrumbItems.map((item) => {
    // 优先通过名称匹配模块（每个item应该根据名称匹配）
    let module = modules.find(m => m.name === item.name)
    
    // 如果名称匹配失败，且当前配置有moduleId，且item名称与模块名称可能相关，尝试通过moduleId匹配
    if (!module && currentConfig?.moduleId) {
      const moduleById = modules.find(m => m.id === currentConfig.moduleId)
      // 只有当通过ID找到的模块名称与item名称匹配时，才使用它
      if (moduleById && moduleById.name === item.name) {
        module = moduleById
      }
    }
    
    if (module && module.items && module.items.length > 0) {
      // 过滤掉当前页面的菜单项，避免重复
      const filteredItems = module.items.filter(menuItem => menuItem.path !== path)
      // 只要有模块项，就显示下拉菜单（即使只有一个菜单项或过滤后没有剩余项，也显示所有项）
      // 如果有过滤后的项，使用过滤后的；否则使用所有项（包括当前页面）
      const itemsToShow = filteredItems.length > 0 ? filteredItems : module.items
      if ((import.meta as any).env?.DEV) {
        console.log(`[Breadcrumb] Adding dropdown menu for "${item.name}" with ${itemsToShow.length} items`)
      }
      const resultItem = {
        ...item,
        moduleItems: itemsToShow.map(menuItem => ({
          name: menuItem.name,
          path: menuItem.path,
        })),
      }
      return resultItem
    } else if ((import.meta as any).env?.DEV && item.name !== '学生端' && item.name !== '企业端' && item.name !== '教师端' && item.name !== '管理端') {
      console.log(`[Breadcrumb] No module found for "${item.name}"`)
    }
    return item
  })
  
  if ((import.meta as any).env?.DEV) {
    console.log('[Breadcrumb] Final breadcrumb items:', result)
  }
  
  return result
})
</script>

<style scoped>
/* 样式已内联到模板中 */
</style>

