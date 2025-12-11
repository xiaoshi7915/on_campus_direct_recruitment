/**
 * 简历相关API
 */
import request from './request'

// 简历接口类型定义
export interface Resume {
  id: string
  student_id: string
  title: string
  content: string
  file_url?: string
  is_default: boolean
  view_count: number
  download_count: number
  created_at: string
  updated_at: string
}

export interface ResumeListResponse {
  items: Resume[]
  total: number
  page: number
  page_size: number
}

export interface ResumeCreateRequest {
  title: string
  content: string
  file_url?: string
  is_default?: boolean
}

export interface ResumeUpdateRequest {
  title?: string
  content?: string
  file_url?: string
  is_default?: boolean
}

// 获取简历列表
export const getResumes = async (params?: {
  page?: number
  page_size?: number
  student_id?: string
}): Promise<ResumeListResponse> => {
  return request.get('/resumes', { params })
}

// 获取简历详情
export const getResume = async (id: string): Promise<Resume> => {
  return request.get(`/resumes/${id}`)
}

// 创建简历
export const createResume = async (data: ResumeCreateRequest): Promise<Resume> => {
  return request.post('/resumes', data)
}

// 更新简历
export const updateResume = async (id: string, data: ResumeUpdateRequest): Promise<Resume> => {
  return request.put(`/resumes/${id}`, data)
}

// 删除简历
export const deleteResume = async (id: string): Promise<void> => {
  return request.delete(`/resumes/${id}`)
}

// 获取简历预览URL
export const getResumePreviewUrl = async (id: string): Promise<string> => {
  const response = await request.get(`/resumes/${id}/preview_url`)
  return response.preview_url
}

// 下载简历文件
export const downloadResume = async (id: string): Promise<void> => {
  // 使用fetch来下载，携带token
  const token = localStorage.getItem('access_token')
  // 使用相对路径，通过vite代理
  const url = `/api/v1/resumes/${id}/download`
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      redirect: 'follow'
    })
    
    if (response.status === 307 || response.status === 302 || response.redirected) {
      // 如果是重定向，获取Location头或最终URL
      const redirectUrl = response.headers.get('Location') || response.url
      if (redirectUrl) {
        // 直接打开重定向后的URL（签名URL）
        window.open(redirectUrl, '_blank')
        return
      }
    }
    
    if (response.ok) {
      // 如果不是重定向，尝试下载blob
      const blob = await response.blob()
      const blobUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = `resume-${id}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(blobUrl)
    } else {
      const errorText = await response.text()
      throw new Error(`下载失败: ${response.status} - ${errorText}`)
    }
  } catch (error: any) {
    console.error('下载失败:', error)
    alert('下载失败: ' + (error.message || '未知错误'))
  }
}

