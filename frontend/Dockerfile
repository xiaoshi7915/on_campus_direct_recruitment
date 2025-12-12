FROM node:18-alpine

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8008

# 启动命令（开发环境）
CMD ["npm", "run", "dev", "--", "--host"]

# 生产环境构建命令（可选）
# RUN npm run build
# CMD ["npm", "run", "preview", "--", "--host"]



