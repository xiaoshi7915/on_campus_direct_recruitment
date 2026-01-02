/**
 * Vue Router配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/components/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
      },
    ],
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/ForgotPassword.vue'),
    meta: { title: '忘记密码' },
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: () => import('@/views/ChangePassword.vue'),
    meta: { title: '修改密码', requiresAuth: true },
  },
  // 学生端路由
  {
    path: '/student',
    component: () => import('@/components/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'StudentDashboard',
        component: () => import('@/views/student/Dashboard.vue'),
      },
      {
        path: 'jobs',
        name: 'StudentJobs',
        component: () => import('@/views/student/Jobs.vue'),
        meta: {
          module: 'job_center',
          title: '职位搜索',
          // 未登录用户也可以查看职位搜索
        },
      },
      {
        path: 'jobs/:id',
        name: 'StudentJobDetail',
        component: () => import('@/views/student/JobDetail.vue'),
      },
      {
        path: 'resumes',
        name: 'StudentResumes',
        component: () => import('@/views/student/Resumes.vue'),
        meta: {
          module: 'personal',
          title: '我的简历',
          permission: 'resume:read',
        },
      },
      {
        path: 'resumes/:id',
        name: 'StudentResumeDetail',
        component: () => import('@/views/common/ResumeDetail.vue'),
      },
      {
        path: 'applications',
        name: 'StudentApplications',
        component: () => import('@/views/student/Applications.vue'),
        meta: {
          module: 'job_center',
          title: '我的申请',
          permission: 'application:read',
        },
      },
      {
        path: 'job-fairs',
        name: 'StudentJobFairs',
        component: () => import('@/views/student/JobFairs.vue'),
      },
      {
        path: 'info-sessions',
        name: 'StudentInfoSessions',
        component: () => import('@/views/student/InfoSessions.vue'),
      },
      {
        path: 'chat',
        name: 'StudentChat',
        component: () => import('@/views/student/Chat.vue'),
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: () => import('@/views/student/Profile.vue'),
        meta: {
          module: 'settings',
          title: '学生中心',
          permission: 'profile:read',
        },
      },
      {
        path: 'favorites',
        name: 'StudentFavorites',
        component: () => import('@/views/student/Favorites.vue'),
      },
      {
        path: 'offers',
        name: 'StudentOffers',
        component: () => import('@/views/student/Offers.vue'),
      },
      {
        path: 'job-intentions',
        name: 'StudentJobIntentions',
        component: () => import('@/views/student/JobIntentions.vue'),
      },
      {
        path: 'feedback',
        name: 'StudentFeedback',
        component: () => import('@/views/student/Feedback.vue'),
      },
      {
        path: 'system-messages',
        name: 'StudentSystemMessages',
        component: () => import('@/views/student/SystemMessages.vue'),
      },
      {
        path: 'todos',
        name: 'StudentTodos',
        component: () => import('@/views/student/Todos.vue'),
      },
      {
        path: 'schedules',
        name: 'StudentSchedules',
        component: () => import('@/views/student/Schedules.vue'),
        meta: {
          module: 'settings',
          title: '日程管理',
          permission: 'settings:schedule',
        },
      },
    ],
  },
  // 企业端路由
  {
    path: '/enterprise',
    component: () => import('@/components/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'EnterpriseDashboard',
        component: () => import('@/views/enterprise/Dashboard.vue'),
      },
      {
        path: 'jobs',
        name: 'EnterpriseJobs',
        component: () => import('@/views/enterprise/Jobs.vue'),
        meta: {
          module: 'job',
          title: '职位管理',
          permission: 'job:read',
        },
      },
      {
        path: 'jobs/:id',
        name: 'EnterpriseJobDetail',
        component: () => import('@/views/enterprise/JobDetail.vue'),
      },
      {
        path: 'jobs/:id/edit',
        name: 'EnterpriseJobEdit',
        component: () => import('@/views/enterprise/JobEdit.vue'),
      },
      {
        path: 'applications',
        name: 'EnterpriseApplications',
        component: () => import('@/views/enterprise/Applications.vue'),
      },
      {
        path: 'applications/:id',
        name: 'EnterpriseApplicationDetail',
        component: () => import('@/views/enterprise/ApplicationDetail.vue'),
      },
      {
        path: 'interviews/create',
        name: 'EnterpriseCreateInterview',
        component: () => import('@/views/enterprise/CreateInterview.vue'),
      },
      {
        path: 'talents',
        name: 'EnterpriseTalents',
        component: () => import('@/views/enterprise/Talents.vue'),
        meta: {
          module: 'talent',
          title: '人才搜索',
          permission: 'talent:search',
        },
      },
      {
        path: 'job-fairs',
        name: 'EnterpriseJobFairs',
        component: () => import('@/views/enterprise/JobFairs.vue'),
      },
      {
        path: 'info-sessions',
        name: 'EnterpriseInfoSessions',
        component: () => import('@/views/enterprise/InfoSessions.vue'),
      },
      {
        path: 'chat',
        name: 'EnterpriseChat',
        component: () => import('@/views/enterprise/Chat.vue'),
      },
      {
        path: 'profile',
        name: 'EnterpriseProfile',
        component: () => import('@/views/enterprise/Profile.vue'),
      },
      {
        path: 'sub-accounts',
        name: 'EnterpriseSubAccounts',
        component: () => import('@/views/enterprise/SubAccounts.vue'),
        meta: {
          module: 'settings',
          title: '子账号管理',
          permission: 'settings:sub_account',
        },
      },
      {
        path: 'talent-library',
        name: 'EnterpriseTalentLibrary',
        component: () => import('@/views/enterprise/TalentLibrary.vue'),
      },
      {
        path: 'statistics',
        name: 'EnterpriseStatistics',
        component: () => import('@/views/enterprise/Statistics.vue'),
      },
      {
        path: 'schools',
        name: 'EnterpriseSchools',
        component: () => import('@/views/enterprise/Schools.vue'),
      },
      {
        path: 'schools/:id',
        name: 'EnterpriseSchoolDetail',
        component: () => import('@/views/enterprise/SchoolDetail.vue'),
      },
      {
        path: 'system-messages',
        name: 'EnterpriseSystemMessages',
        component: () => import('@/views/enterprise/SystemMessages.vue'),
      },
      {
        path: 'feedback',
        name: 'EnterpriseFeedback',
        component: () => import('@/views/enterprise/Feedback.vue'),
      },
      {
        path: 'schedules',
        name: 'EnterpriseSchedules',
        component: () => import('@/views/enterprise/Schedules.vue'),
      },
      {
        path: 'preview',
        name: 'EnterprisePreview',
        component: () => import('@/views/enterprise/PreviewPage.vue'),
      },
      {
        path: 'resumes/:id',
        name: 'EnterpriseResumeDetail',
        component: () => import('@/views/common/ResumeDetail.vue'),
      },
      {
        path: 'verification',
        name: 'EnterpriseVerification',
        component: () => import('@/views/enterprise/EnterpriseVerification.vue'),
        meta: { title: '企业认证', requiresAuth: true },
      },
      {
        path: 'personal-verification',
        name: 'EnterprisePersonalVerification',
        component: () => import('@/views/enterprise/PersonalVerification.vue'),
        meta: { title: '个人身份认证', requiresAuth: true },
      },
    ],
  },
  // 教师端路由
  {
    path: '/teacher',
    component: () => import('@/components/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'TeacherDashboard',
        component: () => import('@/views/teacher/Dashboard.vue'),
      },
      {
        path: 'students',
        name: 'TeacherStudents',
        component: () => import('@/views/teacher/Students.vue'),
        meta: {
          module: 'student',
          title: '学生管理',
          permission: 'student:read',
        },
      },
      {
        path: 'job-fairs',
        name: 'TeacherJobFairs',
        component: () => import('@/views/teacher/JobFairs.vue'),
      },
      {
        path: 'info-sessions',
        name: 'TeacherInfoSessions',
        component: () => import('@/views/teacher/InfoSessions.vue'),
      },
      {
        path: 'statistics',
        name: 'TeacherStatistics',
        component: () => import('@/views/teacher/Statistics.vue'),
      },
      {
        path: 'resumes',
        name: 'TeacherResumes',
        component: () => import('@/views/teacher/Resumes.vue'),
      },
      {
        path: 'resumes/:id',
        name: 'ResumeDetail',
        component: () => import('@/views/common/ResumeDetail.vue'),
      },
      {
        path: 'profile',
        name: 'TeacherProfile',
        component: () => import('@/views/teacher/Profile.vue'),
      },
      {
        path: 'school-verification',
        name: 'TeacherSchoolVerification',
        component: () => import('@/views/teacher/SchoolVerification.vue'),
        meta: { title: '学校认证', requiresAuth: true },
      },
      {
        path: 'departments',
        name: 'TeacherDepartments',
        component: () => import('@/views/teacher/Departments.vue'),
      },
      {
        path: 'student-comments',
        name: 'TeacherStudentComments',
        component: () => import('@/views/teacher/StudentComments.vue'),
      },
      {
        path: 'talent-recommendations',
        name: 'TeacherTalentRecommendations',
        component: () => import('@/views/teacher/TalentRecommendations.vue'),
      },
      {
        path: 'sub-accounts',
        name: 'TeacherSubAccounts',
        component: () => import('@/views/teacher/SubAccounts.vue'),
        meta: {
          module: 'settings',
          title: '子账号管理',
          permission: 'settings:sub_account',
        },
      },
      {
        path: 'chat',
        name: 'TeacherChat',
        component: () => import('@/views/teacher/Chat.vue'),
      },
      {
        path: 'system-messages',
        name: 'TeacherSystemMessages',
        component: () => import('@/views/teacher/SystemMessages.vue'),
      },
      {
        path: 'feedback',
        name: 'TeacherFeedback',
        component: () => import('@/views/teacher/Feedback.vue'),
        meta: {
          module: 'settings',
          title: '意见反馈',
          permission: 'settings:feedback',
        },
      },
    ],
  },
  // 运营管理端路由
  {
    path: '/admin',
    component: () => import('@/components/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue'),
      },
      {
        path: 'rights',
        name: 'AdminRights',
        component: () => import('@/views/admin/Rights.vue'),
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/views/admin/Statistics.vue'),
      },
      {
        path: 'teacher-approvals',
        name: 'AdminTeacherApprovals',
        component: () => import('@/views/admin/TeacherApprovals.vue'),
      },
      {
        path: 'verifications',
        name: 'AdminVerifications',
        component: () => import('@/views/admin/Verifications.vue'),
      },
    ],
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫 - 权限检查
router.beforeEach(async (to, from, next) => {
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('access_token')
    if (!token) {
      next({
        path: '/login',
        query: { redirect: to.fullPath },
      })
      return
    }
  }

  // 检查权限（如果有定义）
  // 某些路由允许未登录用户访问（如职位搜索、学校搜索）
  const publicRoutes = ['/student/jobs', '/enterprise/schools', '/teacher/schools']
  const isPublicRoute = publicRoutes.some(route => to.path.startsWith(route))
  
  if (to.meta.permission && !isPublicRoute) {
    try {
      const { hasPermission } = await import('@/utils/permissions')
      const { useAuthStore } = await import('@/stores/auth')
      const authStore = useAuthStore()
      
      // 确保用户信息已加载
      if (authStore.isAuthenticated() && !authStore.userInfo) {
        console.log('[Router] User info not loaded, fetching...')
        await authStore.fetchUserInfo()
      }
      
      const user = authStore.userInfo
      
      console.log('[Router] Permission check:', {
        path: to.path,
        permission: to.meta.permission,
        hasUser: !!user,
        userType: user?.user_type,
        hasPermission: hasPermission(to.meta.permission as string, user)
      })

      if (!hasPermission(to.meta.permission as string, user)) {
        // 无权限，跳转到首页或显示错误
        const homePath = user
          ? user.user_type === 'STUDENT'
            ? '/student'
            : user.user_type === 'ENTERPRISE'
            ? '/enterprise'
            : user.user_type === 'TEACHER'
            ? '/teacher'
            : user.user_type === 'ADMIN'
            ? '/admin'
            : '/'
          : '/'
        console.warn('[Router] Permission denied, redirecting to:', homePath)
        next({
          path: homePath,
          query: { error: 'no_permission' },
        })
        return
      }
    } catch (error) {
      console.error('[Router] 权限检查失败:', error)
      // 权限检查失败时允许访问（避免阻塞正常使用）
    }
  }

  next()
})

export default router

