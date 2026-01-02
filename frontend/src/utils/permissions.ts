/**
 * 权限管理工具函数
 * 用于前端权限检查和模块访问控制
 */

import { useAuthStore } from '@/stores/auth'
import type { User } from '@/api/users'

// 权限模块定义（与后端保持一致）
export interface PermissionModule {
  id: string
  name: string
  icon: string
  permissions: string[]
}

export const MODULES: Record<string, PermissionModule> = {
  settings: {
    id: 'settings',
    name: '个人设置',
    icon: 'settings',
    permissions: [
      'settings:profile',
      'settings:feedback',
      'settings:sub_account',
      'settings:system_message',
      'settings:schedule',
    ],
  },
  job: {
    id: 'job',
    name: '职位管理',
    icon: 'briefcase',
    permissions: [
      'job:create',
      'job:read',
      'job:update',
      'job:delete',
      'job:apply',
      'job:publish',
    ],
  },
  talent: {
    id: 'talent',
    name: '人才管理',
    icon: 'users',
    permissions: [
      'talent:search',
      'talent:library',
      'talent:application',
      'talent:resume',
      'talent:recommend',
      'talent:mark',
    ],
  },
  school: {
    id: 'school',
    name: '学校管理',
    icon: 'school',
    permissions: [
      'school:search',
      'school:job_fair',
      'school:info_session',
      'school:department',
      'school:read',
      'school:update',
      'school:verify',
    ],
  },
  student: {
    id: 'student',
    name: '学生管理',
    icon: 'graduation-cap',
    permissions: [
      'student:read',
      'student:update',
      'student:comment',
      'student:recommend',
    ],
  },
  statistics: {
    id: 'statistics',
    name: '数据统计',
    icon: 'chart-bar',
    permissions: [
      'statistics:read:personal',
      'statistics:read:enterprise',
      'statistics:read:teacher',
      'statistics:read:admin',
    ],
  },
}

// 角色可访问的模块映射
const ROLE_MODULES: Record<string, string[]> = {
  STUDENT: ['settings', 'job', 'school', 'statistics'],
  ENTERPRISE: ['settings', 'job', 'talent', 'school', 'statistics'],
  TEACHER: ['settings', 'student', 'school', 'statistics'],
  ADMIN: ['settings', 'job', 'talent', 'school', 'student', 'statistics'],
}

// 角色权限映射（简化版，实际权限检查应在后端）
const ROLE_PERMISSIONS: Record<string, Set<string>> = {
  STUDENT: new Set([
    'resume:create',
    'resume:read',
    'resume:update',
    'resume:delete',
    'job:read',
    'job:apply',
    'application:read',
    'application:create',
    'application:cancel',
    'offer:read',
    'offer:update',
    'job_fair:read',
    'job_fair:register',
    'info_session:read',
    'info_session:register',
    'chat:read',
    'chat:write',
    'profile:read',
    'profile:update',
    'schedule:read',
    'schedule:write',
    'schedule:delete',
    'favorite:read',
    'favorite:write',
    'favorite:delete',
    'todo:read',
    'todo:write',
    'todo:delete',
    'feedback:create',
    'settings:profile',
    'settings:system_message',
    'settings:feedback',
    'settings:schedule',
    'statistics:read:personal',
    'job_intention:read',
    'job_intention:write',
    'job_intention:delete',
  ]),
  ENTERPRISE: new Set([
    'job:create',
    'job:read',
    'job:update',
    'job:delete',
    'resume:read',
    'application:read',
    'application:update',
    'interview:create',
    'interview:read',
    'interview:update',
    'offer:create',
    'offer:read',
    'offer:update',
    'offer:delete',
    'job_fair:read',
    'job_fair:register',
    'info_session:create',
    'info_session:read',
    'info_session:update',
    'info_session:delete',
    'school:read',
    'school:search',
    'school:job_fair',
    'school:info_session',
    'chat:read',
    'chat:write',
    'sub_account:create',
    'sub_account:read',
    'sub_account:delete',
    'profile:read',
    'profile:update',
    'schedule:read',
    'schedule:write',
    'statistics:read:personal',
    'statistics:read:enterprise',
    'talent:read',
    'talent:search',
    'talent:library',
    'talent:application',
    'talent:resume',
    'talent:mark',
    'settings:profile',
    'settings:system_message',
    'settings:schedule',
    'settings:feedback',
    'settings:sub_account',
  ]),
  TEACHER: new Set([
    'student:read',
    'student:update',
    'student:comment',
    'student:recommend',
    'resume:read',
    'job_fair:create',
    'job_fair:read',
    'job_fair:update',
    'job_fair:delete',
    'info_session:create',
    'info_session:read',
    'info_session:update',
    'department:read',
    'school:read',
    'school:update',
    'chat:read',
    'chat:write',
    'sub_account:create',
    'sub_account:read',
    'sub_account:delete',
    'profile:read',
    'profile:update',
    'schedule:read',
    'schedule:write',
    'statistics:read:student_activity',
    'statistics:read:job_fair',
    'statistics:read:info_session',
    'statistics:read:teacher',
    'settings:profile',
    'settings:system_message',
    'settings:feedback',
    'settings:sub_account',
  ]),
  ADMIN: new Set(['*']), // 管理员拥有所有权限
}

// 企业子账号权限限制
const ENTERPRISE_SUB_ACCOUNT_RESTRICTIONS = new Set([
  'job:create',
  'job:delete',
  'sub_account:create',
  'sub_account:delete',
  'verification:create:enterprise',
  'verification:create:personal',
  'job_fair:create',
])

// 教师子账号权限限制
const TEACHER_SUB_ACCOUNT_RESTRICTIONS = new Set([
  'job_fair:create',
  'info_session:create',
  'sub_account:create',
  'sub_account:delete',
  'permission:transfer',
  'class:transfer',
  'school:verify',
])

/**
 * 检查用户是否拥有指定权限
 * 注意：这是前端简化检查，实际权限验证应在后端进行
 */
export function hasPermission(permission: string, user?: User | null): boolean {
  if (!user) {
    const authStore = useAuthStore()
    user = authStore.userInfo
  }

  if (!user) {
    console.log('[Permissions] hasPermission: no user', { permission })
    return false
  }

  // 管理员拥有所有权限
  if (user.user_type === 'ADMIN') {
    console.log('[Permissions] hasPermission: admin user, allowing', { permission })
    return true
  }

  // 获取角色权限
  const rolePermissions = ROLE_PERMISSIONS[user.user_type] || new Set()
  
  console.log('[Permissions] hasPermission check:', {
    permission,
    userType: user.user_type,
    hasWildcard: rolePermissions.has('*'),
    hasPermission: rolePermissions.has(permission),
    allPermissions: Array.from(rolePermissions)
  })

  // 检查通配符权限
  if (rolePermissions.has('*')) {
    return true
  }

  // 检查具体权限
  if (rolePermissions.has(permission)) {
    // 如果是子账号，检查是否有权限限制
    // 注意：这里需要从后端获取is_main_account信息，暂时简化处理
    // 实际应该通过API获取用户详细信息
    return true
  }

  console.log('[Permissions] hasPermission: denied', { permission, userType: user.user_type })
  return false
}

/**
 * 获取用户可访问的模块列表
 */
export function getUserModules(user?: User | null): string[] {
  if (!user) {
    const authStore = useAuthStore()
    user = authStore.userInfo
  }

  if (!user) {
    return []
  }

  // 管理员可以访问所有模块
  if (user.user_type === 'ADMIN') {
    return Object.keys(MODULES)
  }

  // 获取角色可访问的模块
  return ROLE_MODULES[user.user_type] || []
}

/**
 * 检查用户是否有模块访问权限
 */
export function hasModuleAccess(moduleId: string, user?: User | null): boolean {
  const modules = getUserModules(user)
  return modules.includes(moduleId)
}

/**
 * 获取模块信息
 */
export function getModule(moduleId: string): PermissionModule | undefined {
  return MODULES[moduleId]
}

/**
 * 检查用户是否是主账号
 * 注意：这需要从后端API获取，这里只是占位函数
 */
export async function isMainAccount(user?: User | null): Promise<boolean> {
  // TODO: 从后端API获取用户详细信息，检查is_main_account字段
  // 暂时返回true，实际应该调用API
  return true
}

