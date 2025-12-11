# 快速启动指南

## 前置要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0+（或使用Docker）
- Redis（或使用Docker）

## 方式一：使用Docker Compose（推荐）

### 1. 启动所有服务

```bash
docker-compose up -d
```

这将启动以下服务：
- MySQL数据库（端口3306）
- Redis缓存（端口6379）
- 后端API服务（端口5001）
- 前端开发服务器（端口5173）

### 2. 初始化数据库

```bash
# 进入后端容器
docker exec -it college_zhaopin_backend bash

# 运行数据库迁移（待实现）
# alembic upgrade head
```

### 3. 访问应用

- 前端：http://localhost:5173
- 后端API文档：http://localhost:5001/docs
- 后端ReDoc：http://localhost:5001/redoc

## 方式二：本地开发

### 后端启动

1. **创建虚拟环境**

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置环境变量**

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置数据库连接等信息。

4. **启动服务**

```bash
uvicorn app.main:app --reload --port 5001
```

### 前端启动

1. **安装依赖**

```bash
cd frontend
npm install
```

2. **启动开发服务器**

```bash
npm run dev
```

前端将在 http://localhost:5173 启动。

## 数据库配置

### 创建数据库

```sql
CREATE DATABASE college_zhaopin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 配置连接

在 `backend/.env` 中设置：

```
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/college_zhaopin
```

## 常见问题

### 1. 端口被占用

如果5001或5173端口被占用，可以修改：
- 后端：修改 `backend/app/core/config.py` 中的 `PORT`
- 前端：修改 `frontend/vite.config.ts` 中的 `server.port`

### 2. 数据库连接失败

- 检查MySQL服务是否启动
- 检查数据库用户名和密码是否正确
- 检查数据库是否已创建

### 3. 前端无法连接后端

- 检查后端服务是否正常启动
- 检查 `frontend/vite.config.ts` 中的代理配置
- 检查CORS配置是否正确

## 下一步

1. 查看 `requirements.md` 了解功能需求
2. 查看 `design.md` 了解系统设计
3. 开始开发具体功能模块



