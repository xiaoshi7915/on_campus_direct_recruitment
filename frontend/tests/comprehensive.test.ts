/**
 * 前端全面测试
 * 测试各个页面和API调用
 */
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'

// 测试API调用
describe('API调用测试', () => {
  it('应该能够调用健康检查接口', async () => {
    const response = await fetch('http://localhost:6121/health')
    expect(response.ok).toBe(true)
    const data = await response.json()
    expect(data.status).toBe('healthy')
  })

  it('应该能够发送短信验证码', async () => {
    const response = await fetch('http://localhost:6121/api/v1/sms/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone: '13800138000' }),
    })
    expect(response.ok).toBe(true)
    const data = await response.json()
    expect(data.success).toBe(true)
    if (data.code) {
      // 开发模式会返回验证码
      expect(data.code).toMatch(/^\d{6}$/)
    }
  })

  it('应该能够验证短信验证码', async () => {
    // 先发送验证码
    const sendResponse = await fetch('http://localhost:6121/api/v1/sms/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone: '13800138001' }),
    })
    const sendData = await sendResponse.json()
    
    if (sendData.code) {
      // 验证验证码
      const verifyResponse = await fetch('http://localhost:6121/api/v1/sms/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone: '13800138001',
          code: sendData.code,
        }),
      })
      expect(verifyResponse.ok).toBe(true)
      const verifyData = await verifyResponse.json()
      expect(verifyData.success).toBe(true)
    }
  })

  it('应该能够获取职位列表', async () => {
    const response = await fetch('http://localhost:6121/api/v1/jobs?page=1&page_size=10')
    expect(response.ok).toBe(true)
    const data = await response.json()
    expect(data).toHaveProperty('items')
    expect(data).toHaveProperty('total')
    expect(data).toHaveProperty('page')
    expect(data).toHaveProperty('page_size')
  })

  it('应该能够搜索职位', async () => {
    const response = await fetch('http://localhost:6121/api/v1/jobs?keyword=软件&page=1&page_size=10')
    expect(response.ok).toBe(true)
    const data = await response.json()
    expect(data).toHaveProperty('items')
    expect(Array.isArray(data.items)).toBe(true)
  })
})

// 测试路由
describe('路由测试', () => {
  it('应该能够访问首页', async () => {
    const response = await fetch('http://localhost:8008/')
    expect(response.ok).toBe(true)
  })

  it('应该能够访问登录页', async () => {
    const response = await fetch('http://localhost:8008/login')
    expect(response.ok).toBe(true)
  })

  it('应该能够访问注册页', async () => {
    const response = await fetch('http://localhost:8008/register')
    expect(response.ok).toBe(true)
  })
})

// 测试组件
describe('组件测试', () => {
  it('应该能够创建Pinia store', () => {
    const pinia = createPinia()
    expect(pinia).toBeDefined()
  })

  it('应该能够创建Vue Router', () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: [
        {
          path: '/',
          name: 'home',
          component: { template: '<div>Home</div>' },
        },
      ],
    })
    expect(router).toBeDefined()
  })
})


