# 后端服务说明

## 环境配置

### 1. 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

`.env` 文件已配置了数据库连接信息（使用utf8mb4字符集）：
- 数据库主机：47.118.250.53
- 数据库端口：3306
- 数据库名：college_zhaopin
- 用户名：cxs_rds
- 字符集：utf8mb4（支持emoji和特殊字符）

### 4. 测试数据库连接

```bash
python scripts/test_db.py
```

### 5. 初始化数据库

**方式一：使用Alembic（推荐）**

```bash
# 创建初始迁移
alembic revision --autogenerate -m "初始化数据库表"

# 应用迁移
alembic upgrade head
```

**方式二：直接创建表（开发环境，使用utf8mb4）**

```bash
python scripts/init_db.py
```

**设置数据库字符集为utf8mb4（如果数据库已存在）**

```bash
python scripts/set_charset.py
```

### 6. 启动服务

```bash
uvicorn app.main:app --reload --port 5001
```

## 数据库迁移

### 创建迁移脚本

```bash
alembic revision --autogenerate -m "描述信息"
```

### 应用迁移

```bash
alembic upgrade head
```

### 回退迁移

```bash
alembic downgrade -1
```

### 查看当前版本

```bash
alembic current
```

### 查看迁移历史

```bash
alembic history
```

## API文档

启动服务后，访问：
- Swagger UI: http://localhost:5001/docs
- ReDoc: http://localhost:5001/redoc

## 项目结构

```
backend/
├── app/
│   ├── api/v1/          # API路由
│   ├── core/            # 核心配置
│   ├── models/          # 数据模型
│   ├── schemas/         # Pydantic模式
│   ├── services/        # 业务逻辑
│   └── utils/           # 工具函数
├── alembic/             # 数据库迁移脚本
├── scripts/             # 工具脚本
├── tests/               # 测试文件
├── requirements.txt     # Python依赖
├── alembic.ini          # Alembic配置
└── .env                 # 环境变量
```

## 常用命令

使用Makefile（如果支持）：

```bash
make install      # 安装依赖
make test-db      # 测试数据库连接
make init-db      # 初始化数据库
make migrate      # 创建迁移脚本
make upgrade      # 应用迁移
make run          # 启动服务
```

## 注意事项

1. `.env` 文件包含敏感信息，不要提交到版本控制
2. 生产环境请修改 `SECRET_KEY`
3. 数据库迁移前请备份数据
4. 使用Alembic管理数据库结构变更
