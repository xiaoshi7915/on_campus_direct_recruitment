# 密码管理功能实现总结

## 1. 账号密码信息

**小米科技（12分公司）账号信息：**
- **用户名**: `userb654fac1`
- **密码**: `123456`（默认测试密码）
- **用户ID**: `2452f751-ebc2-4a5f-a7d8-d2a37ee02824`
- **企业ID**: `005a2aaa-3451-404d-b2ba-3a15c43aab92`

> **注意**: 所有测试账号的默认密码都是 `123456`（从 `backend/scripts/seed_data.py` 可以看到）

## 2. 已实现的功能

### 2.1 后端API

#### 忘记密码 - 发送验证码
- **接口**: `POST /api/v1/auth/forgot-password`
- **请求参数**:
  ```json
  {
    "phone": "13800138000",  // 可选：手机号
    "email": "user@example.com",  // 可选：邮箱
    "username": "username"  // 可选：用户名
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "验证码已发送到手机",
    "phone": "138****8000",  // 脱敏的手机号
    "code": "123456"  // 仅开发环境返回验证码
  }
  ```

#### 重置密码
- **接口**: `POST /api/v1/auth/reset-password`
- **请求参数**:
  ```json
  {
    "phone": "13800138000",  // 可选：手机号
    "email": "user@example.com",  // 可选：邮箱
    "username": "username",  // 可选：用户名
    "verification_code": "123456",  // 必填：验证码
    "new_password": "newpassword123"  // 必填：新密码（至少6位）
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "密码重置成功"
  }
  ```

#### 修改密码（需要登录）
- **接口**: `POST /api/v1/auth/change-password`
- **请求头**: `Authorization: Bearer <token>`
- **请求参数**:
  ```json
  {
    "old_password": "oldpassword123",  // 必填：旧密码
    "new_password": "newpassword123"  // 必填：新密码（至少6位）
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "密码修改成功"
  }
  ```

### 2.2 前端页面

#### 忘记密码页面
- **路径**: `/forgot-password`
- **文件**: `frontend/src/views/ForgotPassword.vue`
- **功能**:
  1. 第一步：输入手机号/邮箱/用户名，发送验证码
  2. 第二步：输入验证码和新密码，重置密码
  3. 自动识别输入的是手机号、邮箱还是用户名
  4. 开发模式显示验证码（方便测试）

#### 修改密码页面
- **路径**: `/change-password`
- **文件**: `frontend/src/views/ChangePassword.vue`
- **功能**:
  1. 输入旧密码
  2. 输入新密码（至少6位）
  3. 确认新密码
  4. 修改成功后自动跳转到登录页

### 2.3 前端API

已更新 `frontend/src/api/auth.ts`，添加了以下函数：
- `forgotPassword(data: ForgotPasswordRequest)`: 忘记密码 - 发送验证码
- `resetPassword(data: ResetPasswordRequest)`: 重置密码
- `changePassword(data: ChangePasswordRequest)`: 修改密码

## 3. 使用流程

### 3.1 忘记密码流程

1. 用户访问 `/forgot-password` 页面
2. 输入手机号/邮箱/用户名
3. 点击"发送验证码"
4. 系统发送验证码到手机（开发模式会显示验证码）
5. 输入验证码和新密码
6. 点击"重置密码"
7. 密码重置成功后，自动跳转到登录页

### 3.2 修改密码流程

1. 用户登录后访问 `/change-password` 页面
2. 输入旧密码
3. 输入新密码（至少6位）
4. 确认新密码
5. 点击"修改密码"
6. 密码修改成功后，自动跳转到登录页（需要重新登录）

## 4. 安全特性

1. **验证码验证**: 重置密码需要验证码验证
2. **密码强度**: 新密码至少6位字符
3. **密码确认**: 修改/重置密码需要确认新密码
4. **旧密码验证**: 修改密码需要验证旧密码
5. **一次性验证码**: 验证码使用后自动失效
6. **验证码有效期**: 验证码5分钟内有效

## 5. 修复的问题

### 5.1 邀请学生时"宣讲会不存在"的错误

**问题**: 创建宣讲会后，点击"邀请学生"时提示"宣讲会不存在"

**原因**: 
- 搜索学生API不需要session_id，但前端在搜索时可能传递了错误的session_id
- 创建宣讲会后，前端没有正确刷新列表，导致session_id可能不正确

**修复**:
1. 修复了搜索学生功能，移除了对session_id的依赖
2. 修复了创建宣讲会后的列表刷新逻辑

## 6. 修改的文件

### 后端文件
1. `backend/app/api/v1/auth.py` - 添加了忘记密码、重置密码、修改密码API
2. `backend/app/api/v1/info_sessions.py` - 修复了搜索学生的逻辑

### 前端文件
1. `frontend/src/api/auth.ts` - 添加了密码管理相关的API函数
2. `frontend/src/views/ForgotPassword.vue` - **新建**，忘记密码页面
3. `frontend/src/views/ChangePassword.vue` - **新建**，修改密码页面
4. `frontend/src/views/enterprise/InfoSessions.vue` - 修复了创建宣讲会后的刷新逻辑

## 7. 路由配置

需要在 `frontend/src/router/index.ts` 中添加以下路由：

```typescript
{
  path: '/forgot-password',
  name: 'ForgotPassword',
  component: () => import('@/views/ForgotPassword.vue'),
  meta: { title: '忘记密码' }
},
{
  path: '/change-password',
  name: 'ChangePassword',
  component: () => import('@/views/ChangePassword.vue'),
  meta: { title: '修改密码', requiresAuth: true }
}
```

## 8. 测试建议

### 8.1 忘记密码测试
1. 访问 `/forgot-password` 页面
2. 输入手机号 `13800138000`（或用户名 `userb654fac1`）
3. 点击"发送验证码"
4. 查看控制台或响应中的验证码（开发模式）
5. 输入验证码和新密码
6. 点击"重置密码"
7. 使用新密码登录

### 8.2 修改密码测试
1. 登录账号
2. 访问 `/change-password` 页面
3. 输入旧密码 `123456`
4. 输入新密码（至少6位）
5. 确认新密码
6. 点击"修改密码"
7. 使用新密码重新登录

## 9. 注意事项

1. **开发模式**: 在开发模式下，发送验证码时会返回验证码，方便测试
2. **生产环境**: 在生产环境中，验证码不会返回，需要通过短信接收
3. **邮箱验证**: 邮箱验证码功能暂未实现，目前只支持手机号验证
4. **密码强度**: 目前只要求至少6位字符，可以根据需要增强密码强度要求


