# 使用 ARG 支持动态指定 Python 版本
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs /app/backup

# 暴露端口
EXPOSE 6121

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:6121/health || exit 1

# 启动命令（开发环境）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6121", "--reload"]

# 生产环境启动命令（使用 workers，需要时取消注释）
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6121", "--workers", "4", "--log-level", "info"]



