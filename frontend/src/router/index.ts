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
        path: 'interviews/create',
        name: 'EnterpriseCreateInterview',
        component: () => import('@/views/enterprise/CreateInterview.vue'),
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
      {
        path: 'sub-accounts',
        name: 'EnterpriseSubAccounts',
        component: () => import('@/views/enterprise/SubAccounts.vue'),
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
    ],
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

