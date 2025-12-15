/**
 * 统一错误处理工具
 * 提供用户友好的错误提示
 * 
 * 注意：如果项目未使用element-plus，请替换为其他UI库的提示组件
 * 或者使用原生的alert/console.error
 */

export interface ErrorInfo {
  code?: number | string
  message: string
  detail?: string
}

// 临时使用console，如果项目有UI库请替换
function showMessage(message: string, type: 'error' | 'warning' | 'success' | 'info' = 'info'): void {
  const consoleMethod = type === 'error' ? 'error' : type === 'warning' ? 'warn' : 'log'
  console[consoleMethod](message)
  // 如果有UI库，可以在这里调用UI库的提示组件
  // 例如：ElMessage[type](message)
}

function showNotification(title: string, message: string, type: 'error' | 'warning' | 'success' | 'info' = 'info'): void {
  const consoleMethod = type === 'error' ? 'error' : type === 'warning' ? 'warn' : 'log'
  console[consoleMethod](`${title}: ${message}`)
  // 如果有UI库，可以在这里调用UI库的通知组件
  // 例如：ElNotification[type]({ title, message })
}

/**
 * 处理API错误
 */
export function handleApiError(error: any): void {
  let errorInfo: ErrorInfo = {
    message: '操作失败，请稍后重试'
  }

  if (error.response) {
    const response = error.response
    const data = response.data || {}

    // 从响应中提取错误信息
    if (data.error_message) {
      errorInfo.message = data.error_message
    } else if (data.detail) {
      errorInfo.message = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)
    } else if (data.message) {
      errorInfo.message = data.message
    }

    errorInfo.code = data.error_code || response.status
    errorInfo.detail = data.detail

    // 根据状态码处理
    switch (response.status) {
      case 400:
        errorInfo.message = errorInfo.message || '请求参数错误'
        showMessage(errorInfo.message, 'error')
        break
      case 401:
        errorInfo.message = '登录已过期，请重新登录'
        showMessage(errorInfo.message, 'warning')
        // 延迟跳转，让用户看到提示
        setTimeout(() => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }, 1500)
        break
      case 403:
        errorInfo.message = errorInfo.message || '权限不足，无法执行此操作'
        showMessage(errorInfo.message, 'error')
        break
      case 404:
        errorInfo.message = errorInfo.message || '请求的资源不存在'
        showMessage(errorInfo.message, 'warning')
        break
      case 429:
        errorInfo.message = '请求过于频繁，请稍后再试'
        showMessage(errorInfo.message, 'warning')
        break
      case 500:
        errorInfo.message = '服务器内部错误，请稍后重试'
        showNotification('服务器错误', errorInfo.message, 'error')
        break
      default:
        showMessage(errorInfo.message, 'error')
    }
  } else if (error.request) {
    // 网络错误
    errorInfo.message = '网络连接失败，请检查网络设置'
    showNotification('网络错误', errorInfo.message, 'error')
  } else {
    // 其他错误
    errorInfo.message = error.message || '发生未知错误'
    showMessage(errorInfo.message, 'error')
  }

  // 开发环境下输出详细错误信息
  // @ts-ignore - Vite环境变量
  try {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    if (import.meta && import.meta.env && import.meta.env.DEV) {
      console.error('API错误详情:', {
        error,
        errorInfo,
        url: error.config?.url,
        method: error.config?.method
      })
    }
  } catch {
    // 忽略环境变量检查错误
  }
}

/**
 * 处理业务错误（非HTTP错误）
 */
export function handleBusinessError(message: string, type: 'error' | 'warning' | 'info' = 'error'): void {
  showMessage(message, type)
}

/**
 * 显示成功消息
 */
export function showSuccess(message: string): void {
  showMessage(message, 'success')
}
