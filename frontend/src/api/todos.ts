/**
 * 待办事项相关API
 */
import request from './request'

export interface TodoResponse {
  id: string
  user_id: string
  title: string
  content?: string
  priority: string
  due_date?: string
  is_completed: boolean
  completed_at?: string
  created_at: string
  updated_at: string
}

export interface TodoListResponse {
  items: TodoResponse[]
  total: number
  page: number
  page_size: number
}

/**
 * 获取待办事项列表
 */
export function getTodos(params?: {
  page?: number
  page_size?: number
  is_completed?: boolean
  priority?: string
}) {
  return request.get<TodoListResponse>('/todos', { params })
}

/**
 * 创建待办事项
 */
export function createTodo(data: {
  title: string
  content?: string
  priority?: string
  due_date?: string
}) {
  return request.post<TodoResponse>('/todos', data)
}

/**
 * 更新待办事项
 */
export function updateTodo(todoId: string, data: {
  title?: string
  content?: string
  priority?: string
  due_date?: string
  is_completed?: boolean
}) {
  return request.put<TodoResponse>(`/todos/${todoId}`, data)
}

/**
 * 删除待办事项
 */
export function deleteTodo(todoId: string) {
  return request.delete(`/todos/${todoId}`)
}
