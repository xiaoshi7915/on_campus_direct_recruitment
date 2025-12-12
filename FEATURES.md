# 校园直聘平台 - 功能说明文档

## 项目概述

校园直聘平台是一个面向高校、企业和学生的综合性招聘服务平台，旨在连接高校人才与企业需求，提供便捷的招聘求职服务。

## 技术架构

- **前端**: Vue 3 + TypeScript + Vite + TailwindCSS + Pinia
- **后端**: Python 3.11 + FastAPI + MySQL 8.0
- **DevOps**: Docker + Docker-Compose
- **测试**: Pytest（后端）+ Vitest（前端）

## 核心功能模块

### 1. 教师端功能

#### 1.1 工作台
- ✅ 学生活跃度统计（按时间、院系筛选）
- ✅ 双选会统计分析（按时间、学校、状态筛选）
- ✅ 宣讲会统计分析
- ✅ 日程管理

#### 1.2 学生管理
- ✅ 学生信息查询和管理
- ✅ 学生点评功能
- ✅ 班级移交
- ✅ 学生推荐给企业

#### 1.3 院校管理
- ✅ 院系信息管理（基本信息、资质荣誉）
- ✅ 院校实名认证申请

#### 1.4 账号管理
- ✅ 主账号/子账号管理
- ✅ 子账号创建和管理
- ✅ 权限管理

#### 1.5 活动管理
- ✅ 双选会创建和管理
- ✅ 宣讲会创建和管理
- ✅ 企业邀请和管理
- ✅ 报名统计

#### 1.6 其他功能
- ✅ 在线聊天（与学生、企业）
- ✅ 系统消息接收
- ✅ 数据统计报表

### 2. 企业端功能

#### 2.1 账号管理
- ✅ 企业注册和登录
- ✅ 短信验证码登录
- ✅ 忘记密码/修改密码
- ✅ 主账号/子账号管理
- ✅ 企业认证
- ✅ 个人身份认证

#### 2.2 企业信息管理
- ✅ 企业信息编辑
- ✅ 宣传页预览和导出
- ✅ Logo和头像上传

#### 2.3 职位管理
- ✅ 职位发布和编辑
- ✅ 职位搜索和筛选
- ✅ 职位标签管理
- ✅ 职位状态管理

#### 2.4 人才管理
- ✅ 人才搜索（按条件筛选）
- ✅ 人才库管理（企业触达过的人才）
- ✅ 简历查看和下载
- ✅ 人才标记和收藏

#### 2.5 申请管理
- ✅ 职位申请查看
- ✅ 申请状态管理（查看、面试、通过、拒绝）
- ✅ 面试安排和管理
- ✅ Offer发送和管理

#### 2.6 学校搜索
- ✅ 学校列表和搜索
- ✅ 学校详情查看
- ✅ 学校收藏和标记
- ✅ 学校分享
- ✅ 申请线下宣讲会
- ✅ 与学校发起聊天

#### 2.7 活动管理
- ✅ 宣讲会创建和管理
- ✅ 宣讲会资料上传
- ✅ 学生邀请（单个/批量）
- ✅ 双选会浏览和报名
- ✅ 双选会签到
- ✅ 我的报名列表

#### 2.8 在线聊天
- ✅ 与学生/教师/学校聊天
- ✅ 消息发送和接收
- ✅ 文件传输
- ✅ 快捷操作（查看简历、邀请宣讲会、邀请面试等）

#### 2.9 其他功能
- ✅ 系统消息接收
- ✅ 日程管理
- ✅ 收藏夹管理
- ✅ 数据统计报表
- ✅ 意见反馈

### 3. 学生端功能

#### 3.1 账号管理
- ✅ 学生注册和登录
- ✅ 短信验证码登录
- ✅ 忘记密码/修改密码

#### 3.2 个人信息管理
- ✅ 个人资料编辑
- ✅ 头像上传

#### 3.3 简历管理
- ✅ 简历创建和编辑
- ✅ 简历文件上传（支持OSS存储）
- ✅ 简历预览和下载
- ✅ 多份简历管理

#### 3.4 求职意向
- ✅ 求职意向设置
- ✅ 意向职位类型管理

#### 3.5 职位搜索
- ✅ 职位列表和搜索
- ✅ 职位详情查看
- ✅ 职位申请
- ✅ 职位收藏

#### 3.6 申请管理
- ✅ 我的申请列表
- ✅ 申请状态查看
- ✅ 面试安排查看
- ✅ Offer接收和管理

#### 3.7 活动参与
- ✅ 双选会浏览和报名
- ✅ 宣讲会浏览和报名
- ✅ 活动签到

#### 3.8 在线聊天
- ✅ 与企业/教师聊天
- ✅ 消息发送和接收
- ✅ 快捷操作（查看企业、查看职位、查看宣讲会等）

#### 3.9 其他功能
- ✅ 系统消息接收
- ✅ 待办事项管理
- ✅ 收藏夹管理
- ✅ 意见反馈
- ✅ 数据统计

### 4. 运营管理端功能

#### 4.1 用户管理
- ✅ 用户列表和查询
- ✅ 用户权限管理

#### 4.2 审批管理
- ✅ 教师注册审批
- ✅ 企业认证审批
- ✅ 个人身份认证审批

#### 4.3 数据统计
- ✅ 用户数据分析
- ✅ 活跃度分析
- ✅ 行为分析

#### 4.4 系统管理
- ✅ 系统配置
- ✅ 反馈建议处理

## 技术特性

### 安全性
- JWT Token认证
- 密码加密存储
- 权限控制（RBAC）
- CORS配置
- SQL注入防护

### 性能优化
- Redis缓存
- 数据库索引优化
- 文件OSS存储
- 分页查询

### 可扩展性
- 微服务架构设计
- Docker容器化部署
- 数据库迁移（Alembic）
- API版本管理

## 数据库设计

主要数据表：
- users（用户表）
- student_profiles（学生档案）
- teacher_profiles（教师档案）
- enterprise_profiles（企业档案）
- jobs（职位表）
- resumes（简历表）
- applications（申请表）
- interviews（面试表）
- offers（Offer表）
- job_fairs（双选会表）
- info_sessions（宣讲会表）
- chat_sessions（聊天会话表）
- messages（消息表）
- schools（学校表）
- departments（院系表）
- talent_pools（人才库表）
- favorites（收藏表）
- schedules（日程表）
- todos（待办事项表）
- feedbacks（反馈表）
- marks（标记表）
- verifications（认证表）

详细数据模型请参考 `design.md`。

## API文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:5001/docs
- ReDoc: http://localhost:5001/redoc

## 部署说明

### Docker部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/xiaoshi7915/on_campus_direct_recruitment.git
cd on_campus_direct_recruitment

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入实际配置

# 3. 启动服务
docker-compose up -d

# 4. 初始化数据库
docker-compose exec backend alembic upgrade head
```

### Linux一键部署

```bash
# 执行部署脚本
chmod +x deploy.sh
./deploy.sh
```

详细部署说明请参考 `DEPLOYMENT.md`。

## 开发指南

### 环境要求
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Docker & Docker Compose

### 本地开发

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 5001

# 前端
cd frontend
npm install
npm run dev
```

### 数据库迁移

```bash
cd backend
alembic upgrade head
```

## 测试

### 后端测试
```bash
cd backend
pytest
```

### 前端测试
```bash
cd frontend
npm run test
```

## 许可证

MIT License

## 联系方式

项目地址: https://github.com/xiaoshi7915/on_campus_direct_recruitment

