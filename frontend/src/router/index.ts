/**
 * Vue Router配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
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
      },
      {
        path: 'applications',
        name: 'StudentApplications',
        component: () => import('@/views/student/Applications.vue'),
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
      },
      {
        path: 'favorites',
        name: 'StudentFavorites',
        component: () => import('@/views/student/Favorites.vue'),
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
        path: 'talents',
        name: 'EnterpriseTalents',
        component: () => import('@/views/enterprise/Talents.vue'),
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
        path: 'profile',
        name: 'TeacherProfile',
        component: () => import('@/views/teacher/Profile.vue'),
      },
      {
        path: 'departments',
        name: 'TeacherDepartments',
        component: () => import('@/views/teacher/Departments.vue'),
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
    ],
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

