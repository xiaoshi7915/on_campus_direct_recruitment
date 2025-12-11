/**
 * 收藏相关API
 */
import request from './request'

// 收藏接口类型定义
export interface Favorite {
  id: string
  user_id: string
  target_type: string
  target_id: string
  created_at: string
}

export interface FavoriteListResponse {
  items: Favorite[]
  total: number
  page: number
  page_size: number
}

// 获取收藏列表
export const getFavorites = async (params?: {
  page?: number
  page_size?: number
  target_type?: string
}): Promise<FavoriteListResponse> => {
  return request.get('/favorites', { params })
}

// 添加收藏
export const addFavorite = async (targetType: string, targetId: string): Promise<Favorite> => {
  return request.post('/favorites', {
    target_type: targetType,
    target_id: targetId,
  })
}

// 取消收藏
export const removeFavorite = async (targetType: string, targetId: string): Promise<void> => {
  return request.delete(`/favorites/by-target/${targetType}/${targetId}`)
}

// 检查是否已收藏
export const checkFavorite = async (targetType: string, targetId: string): Promise<boolean> => {
  try {
    const response = await request.get(`/favorites/check/${targetType}/${targetId}`)
    return response.is_favorited || false
  } catch {
    return false
  }
}


