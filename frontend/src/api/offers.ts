/**
 * Offer相关API
 */
import request from './request'
import type { OfferResponse, OfferListResponse } from '../types/index'

/**
 * 获取Offer列表
 */
export function getOffers(params?: {
  page?: number
  page_size?: number
  status?: string
}) {
  return request.get<OfferListResponse>('/interviews/offers', { params })
}

/**
 * 获取Offer详情
 */
export function getOffer(offerId: string) {
  return request.get<OfferResponse>(`/interviews/offers/${offerId}`)
}

/**
 * 接受Offer
 */
export function acceptOffer(offerId: string) {
  return request.post<OfferResponse>(`/interviews/offers/${offerId}/accept`)
}

/**
 * 拒绝Offer
 */
export function rejectOffer(offerId: string) {
  return request.post<OfferResponse>(`/interviews/offers/${offerId}/reject`)
}

