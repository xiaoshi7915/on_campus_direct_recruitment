/**
 * 导航菜单配置
 * 定义各角色的模块化菜单结构
 */
import { hasPermission } from '@/utils/permissions'
import type { User } from '@/api/users'

export interface MenuItem {
  name: string
  path: string
  icon?: string
  permission?: string
  badge?: number | (() => number)
}

export interface MenuModule {
  id: string
  name: string
  icon: string
  items: MenuItem[]
  permission?: string
  collapsed?: boolean
}

/**
 * 获取学生端菜单配置
 */
export function getStudentMenu(user: User | null, unreadCount: number = 0): MenuModule[] {
  if (!user) return []

  return [
    {
      id: 'job_center',
      name: '求职中心',
      icon: 'briefcase',
      items: [
        { name: '职位搜索', path: '/student/jobs', icon: 'search', permission: 'job:read' },
        { name: '我的申请', path: '/student/applications', icon: 'file-text', permission: 'application:read' },
        { name: '我的Offer', path: '/student/offers', icon: 'award', permission: 'offer:read' },
        { name: '求职意向', path: '/student/job-intentions', icon: 'target', permission: 'job_intention:read' },
      ],
    },
    {
      id: 'personal',
      name: '个人管理',
      icon: 'user',
      items: [
        { name: '我的简历', path: '/student/resumes', icon: 'file', permission: 'resume:read' },
        { name: '我的收藏', path: '/student/favorites', icon: 'star', permission: 'favorite:read' },
        { name: '待办中心', path: '/student/todos', icon: 'check-square', permission: 'todo:read' },
      ],
    },
    {
      id: 'campus',
      name: '校园活动',
      icon: 'school',
      items: [
        { name: '双选会', path: '/student/job-fairs', icon: 'calendar', permission: 'job_fair:read' },
        { name: '宣讲会', path: '/student/info-sessions', icon: 'video', permission: 'info_session:read' },
      ],
    },
    {
      id: 'settings',
      name: '个人设置',
      icon: 'settings',
      items: [
        { name: '学生中心', path: '/student/profile', icon: 'user-circle', permission: 'profile:read' },
        { name: '系统消息', path: '/student/system-messages', icon: 'bell', badge: unreadCount, permission: 'settings:system_message' },
        { name: '意见反馈', path: '/student/feedback', icon: 'message-square', permission: 'settings:feedback' },
        { name: '日程管理', path: '/student/schedules', icon: 'calendar-alt', permission: 'settings:schedule' },
      ],
    },
    {
      id: 'communication',
      name: '沟通交流',
      icon: 'message-circle',
      items: [
        { name: '聊天', path: '/student/chat', icon: 'message-circle', permission: 'chat:read' },
      ],
    },
  ].filter(module => {
    // 过滤掉没有可访问菜单项的模块
    const accessibleItems = module.items.filter(item => {
      if (item.permission) {
        return hasPermission(item.permission, user)
      }
      return true
    })
    return accessibleItems.length > 0
  }).map(module => ({
    ...module,
    items: module.items.filter(item => {
      if (item.permission) {
        return hasPermission(item.permission, user)
      }
      return true
    }),
  }))
}

/**
 * 获取企业端菜单配置
 */
export function getEnterpriseMenu(user: User | null, unreadCount: number = 0): MenuModule[] {
  if (!user) return []

  // 检查是否是主账号（需要从后端获取，这里暂时假设可以访问）
  const isMainAccount = true // TODO: 从后端API获取

  return [
    {
      id: 'job',
      name: '职位管理',
      icon: 'briefcase',
      items: [
        { name: '职位管理', path: '/enterprise/jobs', icon: 'briefcase', permission: 'job:read' },
      ],
    },
    {
      id: 'talent',
      name: '人才管理',
      icon: 'users',
      items: [
        { name: '人才搜索', path: '/enterprise/talents', icon: 'search', permission: 'talent:search' },
        { name: '人才库', path: '/enterprise/talent-library', icon: 'database', permission: 'talent:library' },
        { name: '申请管理', path: '/enterprise/applications', icon: 'file-text', permission: 'talent:application' },
      ],
    },
    {
      id: 'school',
      name: '学校管理',
      icon: 'school',
      items: [
        { name: '学校搜索', path: '/enterprise/schools', icon: 'search', permission: 'school:search' },
        { name: '双选会', path: '/enterprise/job-fairs', icon: 'calendar', permission: 'school:job_fair' },
        { name: '宣讲会', path: '/enterprise/info-sessions', icon: 'video', permission: 'school:info_session' },
      ],
    },
    {
      id: 'settings',
      name: '个人设置',
      icon: 'settings',
      items: [
        { name: '企业管理员中心', path: '/enterprise/profile', icon: 'building', permission: 'settings:profile' },
        ...(isMainAccount ? [{ name: '子账号管理', path: '/enterprise/sub-accounts', icon: 'users', permission: 'settings:sub_account' }] : []),
        { name: '系统消息', path: '/enterprise/system-messages', icon: 'bell', badge: unreadCount, permission: 'settings:system_message' },
        { name: '日程管理', path: '/enterprise/schedules', icon: 'calendar-alt', permission: 'settings:schedule' },
        { name: '意见反馈', path: '/enterprise/feedback', icon: 'message-square', permission: 'settings:feedback' },
        { name: '宣传页预览', path: '/enterprise/preview', icon: 'eye', permission: 'profile:read' },
      ],
    },
    {
      id: 'statistics',
      name: '数据报表',
      icon: 'chart-bar',
      items: [
        { name: '数据报表', path: '/enterprise/statistics', icon: 'chart-bar', permission: 'statistics:read:enterprise' },
      ],
    },
    {
      id: 'communication',
      name: '沟通交流',
      icon: 'message-circle',
      items: [
        { name: '聊天', path: '/enterprise/chat', icon: 'message-circle', permission: 'chat:read' },
      ],
    },
  ].filter(module => {
    const accessibleItems = module.items.filter(item => {
      if (item.permission) {
        return hasPermission(item.permission, user)
      }
      return true
    })
    return accessibleItems.length > 0
  }).map(module => ({
    ...module,
    items: module.items.filter(item => {
      if (item.permission) {
        return hasPermission(item.permission, user)
      }
      return true
    }),
  }))
}

/**
 * 获取教师端菜单配置
 */
export function getTeacherMenu(user: User | null, unreadCount: number = 0): MenuModule[] {
  if (!user) return []

  // 检查是否是主账号
  const isMainAccount = true // TODO: 从后端API获取

  return [
    {
      id: 'student',
      name: '学生管理',
      icon: 'graduation-cap',
      items: [
        { name: '学生管理', path: '/teacher/students', icon: 'users', permission: 'student:read' },
        { name: '学生点评', path: '/teacher/student-comments', icon: 'message-circle', permission: 'student:comment' },
        { name: '人才推荐', path: '/teacher/talent-recommendations', icon: 'star', permission: 'student:recommend' },
        { name: '简历管理', path: '/teacher/resumes', icon: 'file', permission: 'resume:read' },
      ],
    },
    {
      id: 'school',
      name: '学校管理',
      icon: 'school',
      items: [
        { name: '我的院校', path: '/teacher/departments', icon: 'building', permission: 'school:read' },
        { name: '双选会管理', path: '/teacher/job-fairs', icon: 'calendar', permission: 'school:job_fair' },
        { name: '宣讲会管理', path: '/teacher/info-sessions', icon: 'video', permission: 'school:info_session' },
      ],
    },
    {
      id: 'settings',
      name: '个人设置',
      icon: 'settings',
      items: [
        { name: '教师中心', path: '/teacher/profile', icon: 'user-circle', permission: 'settings:profile' },
        ...(isMainAccount ? [{ name: '子账号管理', path: '/teacher/sub-accounts', icon: 'users', permission: 'settings:sub_account' }] : []),
        { name: '系统消息', path: '/teacher/system-messages', icon: 'bell', badge: unreadCount, permission: 'settings:system_message' },
        { name: '意见反馈', path: '/teacher/feedback', icon: 'message-square', permission: 'settings:feedback' },
      ],
    },
    {
      id: 'statistics',
      name: '数据统计',
      icon: 'chart-bar',
      items: [
        { name: '数据统计', path: '/teacher/statistics', icon: 'chart-bar', permission: 'statistics:read:teacher' },
      ],
    },
    {
      id: 'communication',
      name: '沟通交流',
      icon: 'message-circle',
      items: [
        { name: '聊天', path: '/teacher/chat', icon: 'message-circle', permission: 'chat:read' },
      ],
    },
  ].filter(module => {
    const accessibleItems = module.items.filter(item => {
      if (item.permission) {
        return hasPermission(item.permission, user)
      }
      return true
    })
    return accessibleItems.length > 0
  }).map(module => ({
    ...module,
    items: module.items.filter(item => {
      if (item.permission) {
        return hasPermission(item.permission, user)
      }
      return true
    }),
  }))
}

/**
 * 获取管理员端菜单配置
 */
export function getAdminMenu(user: User | null): MenuModule[] {
  if (!user) return []

  return [
    {
      id: 'user_management',
      name: '用户管理',
      icon: 'users',
      items: [
        { name: '用户管理', path: '/admin/users', icon: 'users' },
        { name: '教师审批', path: '/admin/teacher-approvals', icon: 'check-circle' },
        { name: '认证审核', path: '/admin/verifications', icon: 'shield-check' },
      ],
    },
    {
      id: 'system',
      name: '系统设置',
      icon: 'settings',
      items: [
        { name: '管理员中心', path: '/admin', icon: 'user-circle' },
        { name: '权益管理', path: '/admin/rights', icon: 'shield' },
      ],
    },
    {
      id: 'statistics',
      name: '数据统计',
      icon: 'chart-bar',
      items: [
        { name: '数据统计', path: '/admin/statistics', icon: 'chart-bar' },
      ],
    },
  ]
}

/**
 * 根据用户类型获取菜单配置
 */
export function getMenuByUserType(
  userType: string,
  user: User | null,
  unreadCount: number = 0
): MenuModule[] {
  switch (userType) {
    case 'STUDENT':
      return getStudentMenu(user, unreadCount)
    case 'ENTERPRISE':
      return getEnterpriseMenu(user, unreadCount)
    case 'TEACHER':
      return getTeacherMenu(user, unreadCount)
    case 'ADMIN':
      return getAdminMenu(user)
    default:
      return []
  }
}

