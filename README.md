# 校园直聘平台

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)](https://fastapi.tiangolo.com/)

> 一个面向高校、企业和学生的综合性招聘服务平台

## 📋 项目简介

校园直聘平台是一个连接高校人才与企业需求的综合性招聘服务平台，为高校教师、企业和学生提供便捷的招聘求职服务。

### 核心特性

- 🎯 **多角色支持**：学生、企业、教师、管理员四种角色
- 💬 **实时聊天**：支持文字、图片、文件等多种消息类型
- 📊 **数据统计**：多维度数据分析和报表
- 🔐 **安全可靠**：JWT认证、权限控制、数据加密
- 🚀 **高性能**：Redis缓存、数据库优化、OSS存储
- 📱 **响应式设计**：支持PC和移动端访问

## 🏗️ 技术架构

### 前端技术栈
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI框架**: TailwindCSS
- **状态管理**: Pinia
- **路由**: Vue Router

### 后端技术栈
- **框架**: FastAPI (Python 3.11+)
- **数据库**: MySQL 8.0
- **缓存**: Redis
- **ORM**: SQLAlchemy
- **认证**: JWT
- **文件存储**: 阿里云OSS

### DevOps
- **容器化**: Docker + Docker Compose
- **数据库迁移**: Alembic
- **CI/CD**: GitHub Actions (可选)

## 🚀 快速开始

### 前置要求

- Docker 20.10+ 和 Docker Compose 2.0+
- 或 Python 3.11+、Node.js 18+、MySQL 8.0+

### Docker部署（推荐）

#### 快速启动

```bash
# 1. 克隆项目
git clone https://github.com/xiaoshi7915/on_campus_direct_recruitment.git
cd on_campus_direct_recruitment

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入实际配置（数据库、OSS、JWT密钥等）

# 3. 启动所有服务（包括MySQL、Redis、后端、前端）
docker-compose up -d

# 4. 查看服务状态
docker-compose ps

# 5. 初始化数据库
docker-compose exec backend alembic upgrade head
```

#### 常用Docker命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f              # 查看所有日志
docker-compose logs -f backend      # 查看后端日志
docker-compose logs -f frontend     # 查看前端日志

# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷（谨慎使用）
docker-compose down -v

# 重新构建并启动
docker-compose up -d --build

# 进入容器
docker-compose exec backend bash     # 进入后端容器
docker-compose exec frontend sh     # 进入前端容器
docker-compose exec mysql mysql -u appuser -p college_zhaopin  # 进入数据库
```

#### 访问地址

启动成功后，访问以下地址：
- **前端**: http://localhost:8008
- **后端API**: http://localhost:6121
- **API文档**: http://localhost:6121/docs
- **ReDoc**: http://localhost:6121/redoc

### 服务管理脚本（本地开发）

项目提供了便捷的服务管理脚本 `start.sh`，用于管理前后端服务：

#### 快速开始

```bash
# 启动服务
./start.sh

# 查看状态
./start.sh status

# 停止服务
./start.sh stop

# 重启服务
./start.sh restart

# 查看日志
./start.sh logs
```

#### 详细命令

**1. 启动服务**
```bash
./start.sh          # 启动前后端服务（默认）
./start.sh start    # 启动前后端服务
```

**2. 停止服务**
```bash
./start.sh stop     # 停止所有服务
```

**3. 重启服务**
```bash
./start.sh restart  # 先停止，再启动
```

**4. 查看状态**
```bash
./start.sh status   # 显示服务运行状态、PID、端口、地址等信息
```

**5. 查看日志**
```bash
./start.sh logs              # 查看所有日志（最后20行）
./start.sh logs all          # 查看所有日志
./start.sh logs backend      # 查看后端日志（实时）
./start.sh logs b            # 查看后端日志（实时，简写）
./start.sh logs frontend     # 查看前端日志（实时）
./start.sh logs f            # 查看前端日志（实时，简写）
```

**6. 帮助信息**
```bash
./start.sh help     # 显示帮助信息
./start.sh --help    # 显示帮助信息
./start.sh -h        # 显示帮助信息
```

#### 服务配置

- **后端端口**: 6121
- **前端端口**: 8008
- **后端地址**: http://localhost:6121
- **后端API文档**: http://localhost:6121/docs
- **前端地址**: http://localhost:8008

#### PID和日志文件位置

- 后端PID: `.backend.pid`
- 前端PID: `.frontend.pid`
- 后端日志: `.backend.log`
- 前端日志: `.frontend.log`

#### 注意事项

1. 脚本会自动检测并使用正确的Python版本（优先使用py312/bin/python）
2. 启动前会自动清理端口占用
3. 停止服务时会先尝试优雅停止，然后强制终止
4. 状态检查会验证进程和端口是否匹配

> 📖 更多详细信息请参考 [服务管理文档](./SERVICE_MANAGEMENT.md)

### Linux一键部署

```bash
# 执行部署脚本
chmod +x deploy.sh
sudo ./deploy.sh
```

### 本地开发

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 6121

# 前端（新终端）
cd frontend
npm install
npm run dev
```

## 📚 文档

- [功能说明文档](./FEATURES.md) - 详细功能列表
- [部署文档](./DEPLOYMENT.md) - 部署指南和配置说明
- [服务管理文档](./SERVICE_MANAGEMENT.md) - 服务管理脚本使用说明
- [设计文档](./design.md) - 系统架构和数据模型
- [需求文档](./requirements.md) - 需求规格说明

## 🎯 核心功能

### 学生端
- ✅ 简历管理（创建、编辑、上传、预览）
- ✅ 职位搜索和申请
- ✅ 在线聊天（与企业、教师）
- ✅ 申请管理和面试安排
- ✅ 双选会和宣讲会参与
- ✅ 系统消息和待办事项

### 企业端
- ✅ 职位发布和管理
- ✅ 人才搜索和人才库管理
- ✅ 学校搜索和合作
- ✅ 在线聊天（与学生、教师、学校）
- ✅ 宣讲会和双选会管理
- ✅ 申请管理和面试安排
- ✅ 企业认证和个人认证

### 教师端
- ✅ 学生管理（查询、点评、推荐）
- ✅ 工作台（活跃度统计、数据分析）
- ✅ 院校管理（院系信息、认证）
- ✅ 活动管理（双选会、宣讲会）
- ✅ 在线聊天（与学生、企业）
- ✅ 主账号/子账号管理

### 管理端
- ✅ 用户管理
- ✅ 审批管理（教师、企业认证）
- ✅ 数据统计和分析
- ✅ 系统配置

## 📁 项目结构

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
│   ├── alembic/            # 数据库迁移
│   ├── scripts/            # 脚本工具
│   ├── tests/              # 测试文件
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── api/            # API调用
│   │   ├── components/      # 组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia状态管理
│   │   └── router/         # 路由配置
│   └── package.json        # Node依赖
├── docker-compose.yml      # Docker编排
├── deploy.sh              # Linux部署脚本
├── start.sh               # 服务管理脚本
├── .env.example           # 环境变量示例
├── FEATURES.md            # 功能说明文档
├── DEPLOYMENT.md          # 部署文档
├── SERVICE_MANAGEMENT.md  # 服务管理文档
└── README.md              # 项目说明
```

## 🔧 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并配置以下关键项：

- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT密钥（生产环境必须修改）
- `OSS_*`: 阿里云OSS配置
- `SMS_*`: 短信服务配置（可选）
- `CORS_ORIGINS`: 允许的跨域域名

详细配置说明请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🧪 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

## 📖 API文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:6121/docs
- ReDoc: http://localhost:6121/redoc

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 更新日志

### v1.0.0 (2024)
- ✅ 完成核心功能开发
- ✅ 支持学生、企业、教师、管理员四种角色
- ✅ 实现在线聊天功能
- ✅ 完成系统消息功能
- ✅ 支持Docker一键部署

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔗 相关链接

- 项目地址: https://github.com/xiaoshi7915/on_campus_direct_recruitment
- 问题反馈: https://github.com/xiaoshi7915/on_campus_direct_recruitment/issues

## 👥 作者

校园直聘平台开发团队

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
