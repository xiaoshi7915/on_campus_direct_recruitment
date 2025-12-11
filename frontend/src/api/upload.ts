/**
 * 文件上传相关API
 */
import request from './request'

export interface UploadResponse {
  url: string
  filename: string
}

/**
 * 上传文档文件
 * @param file 文件对象
 * @param category 文件分类（resume, avatar, document等）
 */
export const uploadDocument = async (file: File, category: string = 'document'): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('category', category)
  
  return request.post('/upload/document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

/**
 * 上传图片
 * @param file 图片文件
 * @param category 图片分类（avatar, logo等）
 */
export const uploadImage = async (file: File, category: string = 'image'): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('category', category)
  
  return request.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}



