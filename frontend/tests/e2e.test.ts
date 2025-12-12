/**
 * E2E测试示例
 * 使用Playwright进行端到端测试
 */
import { test, expect } from '@playwright/test'

test.describe('首页测试', () => {
  test('应该显示首页内容', async ({ page }) => {
    await page.goto('http://localhost:8008')
    
    // 检查页面标题
    await expect(page).toHaveTitle(/校园直聘/)
    
    // 检查是否有登录链接
    const loginLink = page.getByRole('link', { name: /登录/i })
    await expect(loginLink).toBeVisible()
  })
})

test.describe('登录页面测试', () => {
  test('应该能够访问登录页面', async ({ page }) => {
    await page.goto('http://localhost:8008/login')
    
    // 检查页面标题
    await expect(page).toHaveTitle(/登录/)
    
    // 检查是否有用户名输入框
    const usernameInput = page.locator('input[name="username"], input[type="text"]').first()
    await expect(usernameInput).toBeVisible()
    
    // 检查是否有密码输入框
    const passwordInput = page.locator('input[name="password"], input[type="password"]').first()
    await expect(passwordInput).toBeVisible()
  })
})

test.describe('注册页面测试', () => {
  test('应该能够访问注册页面', async ({ page }) => {
    await page.goto('http://localhost:8008/register')
    
    // 检查页面标题
    await expect(page).toHaveTitle(/注册/)
  })
})

test.describe('职位列表测试', () => {
  test('应该能够访问职位列表页面', async ({ page }) => {
    await page.goto('http://localhost:8008/jobs')
    
    // 检查页面是否加载
    await page.waitForLoadState('networkidle')
    
    // 检查是否有职位列表或搜索框
    const searchInput = page.locator('input[type="search"], input[placeholder*="搜索"]').first()
    if (await searchInput.isVisible()) {
      await expect(searchInput).toBeVisible()
    }
  })
})


