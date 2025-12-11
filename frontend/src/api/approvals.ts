/**
 * 审批流程相关API
 */
import request from './request'

// 审批请求接口类型定义
export interface ApprovalRequest {
  action: string  // APPROVE 或 REJECT
  comment?: string
}

export interface ApprovalResponse {
  success: boolean
  message: string
  new_status?: string
}

// 审批双选会
export const approveJobFair = async (jobFairId: string, data: ApprovalRequest): Promise<ApprovalResponse> => {
  return request.post(`/approvals/job-fairs/${jobFairId}/approve`, data)
}

// 审批宣讲会
export const approveInfoSession = async (sessionId: string, data: ApprovalRequest): Promise<ApprovalResponse> => {
  return request.post(`/approvals/info-sessions/${sessionId}/approve`, data)
}

