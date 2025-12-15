# API权限说明文档

本文档说明各个API端点的权限要求。

## 权限格式

权限字符串格式：`资源:操作`

例如：
- `job:create` - 创建职位
- `job:read` - 查看职位
- `job:update` - 更新职位
- `job:delete` - 删除职位

## 职位管理 API

### POST /api/v1/jobs
**权限要求**：`job:create`
**角色限制**：仅企业主账号（企业子账号不能创建职位）

**说明**：
- 企业主账号可以创建职位
- 企业子账号不能创建职位（权限限制）
- 学生、教师、管理员不能创建职位

### PUT /api/v1/jobs/{job_id}
**权限要求**：`job:update` + 资源权限检查
**角色限制**：企业用户（主账号和子账号都可以）

**说明**：
- 企业用户只能更新自己企业的职位
- 使用 `check_resource_access("job", job_id, ...)` 检查资源权限

### DELETE /api/v1/jobs/{job_id}
**权限要求**：`job:delete`
**角色限制**：仅企业主账号（企业子账号不能删除职位）

## 简历管理 API

### POST /api/v1/resumes
**权限要求**：`resume:create`
**角色限制**：仅学生

**说明**：
- 只有学生可以创建简历
- 学生只能创建自己的简历

### GET /api/v1/resumes/{resume_id}
**权限要求**：`resume:read` + 资源权限检查
**角色限制**：学生、企业、教师、管理员

**说明**：
- 学生：只能查看自己的简历
- 企业：只能查看申请学生的简历
- 教师：只能查看管辖学生的简历
- 管理员：可以查看所有简历

### PUT /api/v1/resumes/{resume_id}
**权限要求**：`resume:update` + 资源权限检查
**角色限制**：仅学生

**说明**：
- 学生只能更新自己的简历

### DELETE /api/v1/resumes/{resume_id}
**权限要求**：`resume:delete` + 资源权限检查
**角色限制**：仅学生

**说明**：
- 学生只能删除自己的简历

## 申请管理 API

### POST /api/v1/applications
**权限要求**：`application:create`
**角色限制**：仅学生

**说明**：
- 只有学生可以创建申请
- 学生只能申请已发布的职位

### GET /api/v1/applications
**权限要求**：`application:read`
**角色限制**：学生、企业

**说明**：
- 学生：只能查看自己的申请
- 企业：只能查看自己职位的申请

### PUT /api/v1/applications/{application_id}
**权限要求**：`application:update` + 资源权限检查
**角色限制**：企业用户（主账号和子账号都可以）

**说明**：
- 企业用户只能更新自己职位的申请
- 使用 `check_resource_access("application", application_id, ...)` 检查资源权限

## 面试管理 API

### POST /api/v1/interviews
**权限要求**：`interview:create`
**角色限制**：企业用户（主账号和子账号都可以）

**说明**：
- 企业用户可以创建面试
- 只能为自己职位的申请创建面试

### GET /api/v1/interviews/{interview_id}
**权限要求**：`interview:read` + 资源权限检查
**角色限制**：学生、企业

**说明**：
- 学生：只能查看自己的面试
- 企业：只能查看自己企业的面试
- 使用 `check_resource_access("interview", interview_id, ...)` 检查资源权限

## 子账号管理 API

### POST /api/v1/enterprise-management/sub-accounts
**权限要求**：`sub_account:create`
**角色限制**：仅企业主账号

**说明**：
- 只有企业主账号可以创建子账号
- 企业子账号不能创建子账号（权限限制）

### POST /api/v1/teacher-management/sub-accounts
**权限要求**：`sub_account:create`
**角色限制**：仅教师主账号

**说明**：
- 只有教师主账号可以创建子账号
- 教师子账号不能创建子账号（权限限制）

## 权限检查机制

### 1. 权限检查函数

```python
from app.core.permissions import check_permission

has_permission = await check_permission(current_user, "job:create", db)
if not has_permission:
    raise HTTPException(status_code=403, detail="权限不足")
```

### 2. 资源权限检查

```python
from app.core.permissions import check_resource_access

has_access = await check_resource_access("job", job_id, current_user, db, "update")
if not has_access:
    raise HTTPException(status_code=403, detail="无权访问此资源")
```

### 3. 权限装饰器

```python
from app.core.permissions import require_permission

@router.post("/jobs")
@require_permission("job:create")
async def create_job(...):
    ...
```

## 子账号权限限制

### 企业子账号限制

企业子账号不能执行以下操作：
- `job:create` - 创建职位
- `job:delete` - 删除职位
- `sub_account:create` - 创建子账号
- `sub_account:delete` - 删除子账号
- `verification:create:enterprise` - 申请企业认证
- `verification:create:personal` - 申请个人认证
- `job_fair:create` - 创建双选会

### 教师子账号限制

教师子账号不能执行以下操作：
- `job_fair:create` - 创建双选会
- `info_session:create` - 创建宣讲会
- `sub_account:create` - 创建子账号
- `sub_account:delete` - 删除子账号
- `permission:transfer` - 移交权限
- `class:transfer` - 移交班级
- `school:verify` - 申请学校认证

## 数据权限隔离

### 学生数据权限

- 学生只能操作自己的数据（简历、申请、面试、Offer等）
- 教师可以查看管辖范围内学生的数据（院系级别或学校级别）
- 企业可以查看申请学生的简历

### 企业数据权限

- 企业只能操作自己企业的数据（职位、申请、面试、Offer等）
- 企业主账号和子账号共享企业数据（但子账号有操作限制）

### 教师数据权限

- 教师只能操作自己学校的活动（双选会、宣讲会）
- 教师只能查看管辖范围内学生的数据

## 收藏管理 API

### POST /api/v1/favorites
**权限要求**：`favorite:write`
**角色限制**：所有角色

**说明**：
- 所有用户都可以创建收藏
- 用户只能创建自己的收藏

### DELETE /api/v1/favorites/{favorite_id}
**权限要求**：`favorite:delete` + 资源权限检查
**角色限制**：所有角色

**说明**：
- 用户只能删除自己的收藏
- 使用 `check_resource_access("favorite", favorite_id, ...)` 检查资源权限

## 待办事项管理 API

### POST /api/v1/todos
**权限要求**：`todo:write`
**角色限制**：所有角色

**说明**：
- 所有用户都可以创建待办事项
- 用户只能创建自己的待办事项

### PUT /api/v1/todos/{todo_id}
**权限要求**：`todo:write` + 资源权限检查
**角色限制**：所有角色

**说明**：
- 用户只能更新自己的待办事项
- 使用 `check_resource_access("todo", todo_id, ...)` 检查资源权限

### DELETE /api/v1/todos/{todo_id}
**权限要求**：`todo:delete` + 资源权限检查
**角色限制**：所有角色

**说明**：
- 用户只能删除自己的待办事项
- 使用 `check_resource_access("todo", todo_id, ...)` 检查资源权限

## 标记管理 API

### POST /api/v1/marks
**权限要求**：`talent:mark`
**角色限制**：仅企业用户

**说明**：
- 只有企业用户可以创建标记
- 企业用户只能创建自己的标记

### PUT /api/v1/marks/{mark_id}
**权限要求**：`talent:mark` + 资源权限检查
**角色限制**：仅企业用户

**说明**：
- 企业用户只能更新自己的标记
- 使用 `check_resource_access("mark", mark_id, ...)` 检查资源权限

### DELETE /api/v1/marks/{mark_id}
**权限要求**：`talent:mark` + 资源权限检查
**角色限制**：仅企业用户

**说明**：
- 企业用户只能删除自己的标记
- 使用 `check_resource_access("mark", mark_id, ...)` 检查资源权限

## 权限审计

所有权限检查操作都会记录日志，包括：
- 用户ID和用户类型
- 权限字符串
- 资源类型和资源ID（如果有）
- 检查结果（通过/失败）
- 失败原因（如果有）

日志级别：
- 权限检查通过：DEBUG级别
- 权限检查失败：WARNING级别

## 资源权限检查支持列表

`check_resource_access` 函数现在支持以下资源类型：

1. **resume** - 简历
2. **application** - 申请
3. **job** - 职位
4. **interview** - 面试
5. **offer** - Offer
6. **job_fair** - 双选会
7. **info_session** - 宣讲会
8. **talent_pool** - 人才库
9. **schedule** - 日程
10. **favorite** - 收藏
11. **todo** - 待办事项
12. **mark** - 标记

