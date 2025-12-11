@echo off
REM 启动前端服务
echo 正在启动前端服务...
cd frontend
if not exist node_modules (
    echo 正在安装前端依赖...
    call npm install
)
call npm run dev


