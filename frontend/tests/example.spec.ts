/**
 * 前端E2E测试示例
 * 使用Playwright进行端到端测试
 */
import { test, expect } from '@playwright/test'

test.describe('首页测试', () => {
  test('应该显示首页内容', async ({ page }) => {
    await page.goto('http://localhost:5173')
    
    // 检查页面标题
    await expect(page).toHaveTitle(/校园直聘/)
    
    // 检查是否有登录链接
    const loginLink = page.getByRole('link', { name: /登录/i })
    await expect(loginLink).toBeVisible()
  })
})

test.describe('登录测试', () => {
  test('应该能够登录', async ({ page }) => {
    await page.goto('http://localhost:5173/login')
    
    // 填写登录表单
    await page.fill('input[name="username"]', 'test_student')
    await page.fill('input[name="password"]', '123456')
    
    // 点击登录按钮
    await page.click('button[type="submit"]')
    
    // 等待跳转
    await page.waitForURL('**/student/**', { timeout: 5000 })
    
    // 检查是否跳转到学生工作台
    await expect(page).toHaveURL(/\/student/)
  })
})


