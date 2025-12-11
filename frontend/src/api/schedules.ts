/**
 * 日程相关API
 */
import request from './request'

// 日程接口类型定义
export interface Schedule {
  id: string
  user_id: string
  title: string
  content?: string
  start_time: string
  end_time?: string
  schedule_type: string
  related_id?: string
  reminder_time?: string
  is_completed: boolean
  created_at: string
  updated_at: string
}

export interface ScheduleListResponse {
  items: Schedule[]
  total: number
  page: number
  page_size: number
}

export interface ScheduleCreateRequest {
  title: string
  content?: string
  start_time: string
  end_time?: string
  schedule_type: string
  related_id?: string
  reminder_time?: string
}

export interface ScheduleUpdateRequest {
  title?: string
  content?: string
  start_time?: string
  end_time?: string
  reminder_time?: string
  is_completed?: boolean
}

// 获取日程列表
export const getSchedules = async (params?: {
  page?: number
  page_size?: number
  schedule_type?: string
  start_date?: string
  end_date?: string
}): Promise<ScheduleListResponse> => {
  return request.get('/schedules', { params })
}

// 获取日程详情
export const getSchedule = async (id: string): Promise<Schedule> => {
  return request.get(`/schedules/${id}`)
}

// 创建日程
export const createSchedule = async (data: ScheduleCreateRequest): Promise<Schedule> => {
  return request.post('/schedules', data)
}

// 更新日程
export const updateSchedule = async (id: string, data: ScheduleUpdateRequest): Promise<Schedule> => {
  return request.put(`/schedules/${id}`, data)
}

// 删除日程
export const deleteSchedule = async (id: string): Promise<void> => {
  return request.delete(`/schedules/${id}`)
}

// 标记日程为已完成
export const completeSchedule = async (id: string): Promise<Schedule> => {
  return request.post(`/schedules/${id}/complete`)
}

// 取消日程完成标记
export const uncompleteSchedule = async (id: string): Promise<Schedule> => {
  return request.post(`/schedules/${id}/uncomplete`)
}

