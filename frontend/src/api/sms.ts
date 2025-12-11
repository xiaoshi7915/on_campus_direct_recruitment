/**
 * 短信验证码API
 */
import request from './request'

export interface SendSMSRequest {
  phone: string
}

export interface VerifySMSRequest {
  phone: string
  code: string
}

export interface SMSResponse {
  success: boolean
  message: string
  code?: string  // 仅开发环境返回
}

/**
 * 发送短信验证码
 */
export async function sendSMS(data: SendSMSRequest): Promise<SMSResponse> {
  return request.post('/sms/send', data)
}

/**
 * 验证短信验证码
 */
export async function verifySMS(data: VerifySMSRequest): Promise<SMSResponse> {
  return request.post('/sms/verify', data)
}


