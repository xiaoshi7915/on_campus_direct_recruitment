/**
 * 数据统计相关API
 */
import request from './request'

/**
 * 获取学生活跃度统计（教师）
 */
export const getStudentActivityStatistics = async (params?: {
  start_date?: string
  end_date?: string
  department_id?: string
}) => {
  return request.get('/statistics/students/activity', { params })
}

/**
 * 获取双选会统计分析（教师）
 */
export const getJobFairAnalysis = async (params?: {
  start_date?: string
  end_date?: string
  school_id?: string
  department_id?: string
  status?: string
}) => {
  return request.get('/statistics/job-fairs/analysis', { params })
}

/**
 * 获取宣讲会统计分析（教师）
 */
export const getInfoSessionAnalysis = async (params?: {
  start_date?: string
  end_date?: string
  school_id?: string
  department_id?: string
  enterprise_id?: string
  status?: string
}) => {
  return request.get('/statistics/info-sessions/analysis', { params })
}

/**
 * 获取平台概览统计（管理员）
 */
export const getPlatformOverview = async () => {
  return request.get('/statistics/platform/overview')
}

/**
 * 获取企业个人数据统计
 */
export const getEnterprisePersonalStatistics = async () => {
  return request.get('/statistics/enterprise/personal')
}


