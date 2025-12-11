# 校园直聘平台

## 项目简介

校园直聘平台是一个面向高校、企业和学生的综合性招聘服务平台，旨在连接高校人才与企业需求，提供便捷的招聘求职服务。

## 项目架构

### 技术栈

- **前端**: Vue 3 + TypeScript + Vite + TailwindCSS + Pinia
- **后端**: Python 3.11 + FastAPI + MySQL 8.0
- **DevOps**: Docker + Docker-Compose + GitHub Actions
- **测试**: Pytest（后端）+ Vitest（前端）+ Playwright（E2E）

### 系统模块

#### 1. PC/APP端 - 教师端
- **工作台**: 学生活跃度分析、双选会分析、宣讲会分析、日程管理
- **我的院校**: 院系信息管理、院校实名认证
- **我的教师**: 主子账号管理、教师注册审批、权限移交
- **我的学生**: 班级移交、学生查询、学生点评、移除学生
- **推荐人才**: 为职位推荐管辖内的学生人才
- **宣讲会&双选会**: 发布双选会/宣讲会、查询报名企业/学生、邀请企业

#### 2. 企业端
- **注册登录**: 短信验证、企业认证、个人身份认证、多种登录方式
- **企业信息管理**: 企业信息编辑、宣传页预览和导出
- **账号管理**: 主子账号管理
- **消息中心**: 聊天消息、系统消息、日程表提醒消息
- **学校/学生搜索推荐**: 查看、收藏、标记、分享、申请宣讲会、发起聊天
- **职位管理**: 职位编辑、展示、搜索、标签管理
- **在线聊天**: 与学校/学生在线聊天，支持文字、图片、位置等
- **日程表**: 系统日程展示、手动输入、日程标记和提醒
- **人才管理**: 企业触达过的人才库管理
- **宣讲会管理**: 宣讲会信息编辑、资料上传、数据查看
- **双选会管理**: 查看、申请、签到、管理、数据统计
- **收藏夹**: 收藏学校/学生/简历
- **直播宣讲**: 在线直播宣讲、签到、播放资料、线上互动
- **视频/语音面试**: 双方在线面试
- **试题/测评管理**: 按岗位区分笔试题
- **反馈建议**: 提交意见反馈

#### 3. 学生端
- **个人中心**: 个人信息管理
- **消息中心**: 消息接收和管理
- **待办中心**: 待办事项管理
- **简历管理**: 简历创建、编辑、管理
- **求职意向管理**: 求职意向设置和管理
- **在线聊天**: 与企业/学校在线聊天
- **日程表**: 日程展示和管理
- **收藏**: 收藏企业/职位
- **面试管理**: 面试安排和管理
- **offer管理**: offer接收和管理
- **搜索/推荐**: 搜索/推荐宣讲会/双选会、企业/职位
- **参加活动**: 参加宣讲会、面试
- **数据报表**: 个人数据统计
- **注册登录**: 学生注册和登录
- **视频/语音面试**: 参与在线面试
- **在线笔试/测评**: 参与在线笔试和测评
- **扫码签到**: 活动签到
- **意见反馈**: 提交反馈

#### 4. 运营管理端
- **权益中心**: 权益配置、套餐配置、权益查询、权益管理、权益购买和消费
- **数据中心**: 用户数据分析、活跃分析、行为分析、权益收益分析
- **反馈建议**: 处理反馈建议
- **系统管理**: 系统配置和管理

## 项目结构

```
college_zhaopin/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── tests/              # 测试文件
│   ├── requirements.txt    # Python依赖
│   └── Dockerfile          # Docker配置
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── api/            # API调用
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia状态管理
│   │   ├── router/         # 路由配置
│   │   └── utils/          # 工具函数
│   ├── tests/              # 测试文件
│   └── Dockerfile          # Docker配置
├── docker-compose.yml      # Docker编排
├── requirements.md         # 需求文档
├── design.md              # 设计文档
└── README.md              # 项目说明
```

## 开发指南

### 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Docker & Docker Compose

### 快速开始

详细启动指南请查看 [QUICKSTART.md](./QUICKSTART.md)

**使用Docker Compose（推荐）**
```bash
docker-compose up -d
```

**本地开发**
```bash
# 后端
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 5001

# 前端（新终端）
cd frontend
npm install
npm run dev
```

### 数据库初始化

```bash
cd backend
alembic upgrade head
```

## API文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:5001/docs
- ReDoc: http://localhost:5001/redoc

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

### E2E测试
```bash
npm run test:e2e
```

## 部署

项目支持Docker部署，使用docker-compose.yml进行一键部署。

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

