# 使用 ARG 支持动态指定 Node 版本
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=development \
    HOST=0.0.0.0 \
    PORT=8008

# 安装 curl 用于健康检查
RUN apk add --no-cache curl

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production=false && \
    npm cache clean --force

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8008

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8008 || exit 1

# 启动命令（开发环境）
CMD ["npm", "run", "dev", "--", "--host"]

# 生产环境构建命令（需要时取消注释）
# RUN npm run build
# CMD ["npm", "run", "preview", "--", "--host"]



