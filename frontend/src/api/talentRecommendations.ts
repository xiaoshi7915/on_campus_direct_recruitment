/**
 * 人才推荐相关API
 */
import request from './request'

// 人才推荐接口类型定义
export interface TalentRecommendation {
  id: string
  job_id: string
  student_id: string
  resume_id?: string
  recommendation_note?: string
  status: string
  created_at: string
  updated_at: string
  job_title?: string
  student_name?: string
  enterprise_name?: string
}

export interface TalentRecommendationListResponse {
  items: TalentRecommendation[]
  total: number
  page: number
  page_size: number
}

export interface TalentRecommendationCreate {
  job_id: string
  student_id: string
  resume_id?: string
  recommendation_note?: string
}

// 创建人才推荐
export const recommendTalent = async (data: TalentRecommendationCreate): Promise<TalentRecommendation> => {
  return request.post('/talent-recommendations', data)
}

// 获取人才推荐列表
export const getTalentRecommendations = async (params?: {
  page?: number
  page_size?: number
  job_id?: string
  student_id?: string
}): Promise<TalentRecommendationListResponse> => {
  return request.get('/talent-recommendations', { params })
}



