# 校园直聘平台 - 部署文档

## 部署方式

本项目支持两种部署方式：
1. **Docker Compose部署**（推荐，适合生产环境）
2. **Linux一键部署脚本**（适合服务器直接部署）

## 前置要求

- Linux服务器（Ubuntu 20.04+ / CentOS 7+）
- Docker 20.10+ 和 Docker Compose 2.0+
- 或 Python 3.11+、Node.js 18+、MySQL 8.0+

## 方式一：Docker Compose部署（推荐）

### 1. 准备工作

```bash
# 克隆项目
git clone https://github.com/xiaoshi7915/on_campus_direct_recruitment.git
cd on_campus_direct_recruitment

# 创建环境变量文件
cp .env.example .env
```

### 2. 配置环境变量

编辑 `.env` 文件，配置以下关键信息：

```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@mysql:3306/college_zhaopin?charset=utf8mb4

# JWT密钥（生产环境必须修改）
SECRET_KEY=your-production-secret-key-here

# OSS配置（阿里云OSS）
OSS_ACCESS_KEY_ID=your-access-key-id
OSS_ACCESS_KEY_SECRET=your-access-key-secret
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=your-bucket-name
OSS_REGION=cn-hangzhou

# 短信服务配置（可选）
SMS_ACCESS_KEY_ID=your-sms-access-key-id
SMS_ACCESS_KEY_SECRET=your-sms-access-key-secret
SMS_SIGN_NAME=your-sign-name
SMS_TEMPLATE_CODE=your-template-code

# CORS配置
CORS_ORIGINS=http://your-domain.com,https://your-domain.com
```

### 3. 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 初始化数据库

```bash
# 执行数据库迁移
docker-compose exec backend alembic upgrade head

# 可选：初始化测试数据
docker-compose exec backend python scripts/seed_data.py
```

### 5. 访问服务

- 前端: http://your-server-ip:8008
- 后端API: http://your-server-ip:5001
- API文档: http://your-server-ip:5001/docs

### 6. 常用命令

```bash
# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷（谨慎使用）
docker-compose down -v

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec mysql mysql -u appuser -papppassword college_zhaopin
```

## 方式二：Linux一键部署脚本

### 1. 执行部署脚本

```bash
# 克隆项目
git clone https://github.com/xiaoshi7915/on_campus_direct_recruitment.git
cd on_campus_direct_recruitment

# 赋予执行权限
chmod +x deploy.sh

# 执行部署（会自动安装依赖、配置服务）
sudo ./deploy.sh
```

### 2. 配置环境变量

脚本执行完成后，编辑配置文件：

```bash
# 后端配置
nano backend/.env

# 前端配置（如需要）
nano frontend/.env
```

### 3. 启动服务

```bash
# 使用systemd管理服务
sudo systemctl start college-zhaopin-backend
sudo systemctl start college-zhaopin-frontend

# 设置开机自启
sudo systemctl enable college-zhaopin-backend
sudo systemctl enable college-zhaopin-frontend

# 查看服务状态
sudo systemctl status college-zhaopin-backend
sudo systemctl status college-zhaopin-frontend
```

## 生产环境配置

### 1. Nginx反向代理（推荐）

创建Nginx配置文件 `/etc/nginx/sites-available/college-zhaopin`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:8008;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端API
    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket支持（用于聊天）
    location /ws {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/college-zhaopin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. SSL证书配置（HTTPS）

使用Let's Encrypt免费SSL证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. 防火墙配置

```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 4. 数据库备份

创建备份脚本 `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backup/college_zhaopin"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T mysql mysqldump -u appuser -papppassword college_zhaopin > $BACKUP_DIR/db_$DATE.sql

# 保留最近7天的备份
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
```

设置定时任务：

```bash
# 每天凌晨2点备份
crontab -e
0 2 * * * /path/to/backup.sh
```

## 监控和日志

### 查看日志

```bash
# Docker方式
docker-compose logs -f backend
docker-compose logs -f frontend

# 系统服务方式
sudo journalctl -u college-zhaopin-backend -f
sudo journalctl -u college-zhaopin-frontend -f
```

### 性能监控

建议使用以下工具监控服务：
- Prometheus + Grafana（指标监控）
- ELK Stack（日志分析）
- 阿里云监控（云服务器监控）

## 故障排查

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 检查DATABASE_URL配置是否正确
   - 检查网络连接

2. **端口被占用**
   - 修改docker-compose.yml中的端口映射
   - 或停止占用端口的服务

3. **前端无法连接后端**
   - 检查CORS配置
   - 检查后端服务是否正常启动
   - 检查防火墙设置

4. **文件上传失败**
   - 检查OSS配置是否正确
   - 检查OSS权限设置
   - 检查网络连接

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 执行数据库迁移
docker-compose exec backend alembic upgrade head
```

## 安全建议

1. **修改默认密码**：生产环境必须修改所有默认密码
2. **使用HTTPS**：配置SSL证书启用HTTPS
3. **定期备份**：设置自动备份数据库
4. **更新依赖**：定期更新依赖包修复安全漏洞
5. **限制访问**：使用防火墙限制不必要的端口访问
6. **监控日志**：定期检查日志发现异常

## 技术支持

如遇到部署问题，请提交Issue到GitHub仓库：
https://github.com/xiaoshi7915/on_campus_direct_recruitment/issues

