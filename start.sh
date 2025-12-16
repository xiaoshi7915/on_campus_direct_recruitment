#!/bin/bash
# 一键启动前后端服务脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# PID 文件路径
BACKEND_PID_FILE="$SCRIPT_DIR/.backend.pid"
FRONTEND_PID_FILE="$SCRIPT_DIR/.frontend.pid"

# 停止函数
stop_services() {
    echo -e "${YELLOW}正在停止服务...${NC}"
    
    # 停止后端
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}停止后端服务 (PID: $BACKEND_PID)...${NC}"
            kill "$BACKEND_PID" 2>/dev/null
            sleep 1
            # 如果还在运行，强制杀死
            if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
                kill -9 "$BACKEND_PID" 2>/dev/null
            fi
        fi
        rm -f "$BACKEND_PID_FILE"
    fi
    
    # 停止前端
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}停止前端服务 (PID: $FRONTEND_PID)...${NC}"
            kill "$FRONTEND_PID" 2>/dev/null
            sleep 1
            # 如果还在运行，强制杀死
            if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
                kill -9 "$FRONTEND_PID" 2>/dev/null
            fi
        fi
        rm -f "$FRONTEND_PID_FILE"
    fi
    
    # 清理可能的残留进程
    pkill -f "uvicorn app.main:app" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    
    echo -e "${GREEN}服务已停止${NC}"
    exit 0
}

# 如果传入 stop 参数，则停止服务
if [ "$1" == "stop" ]; then
    stop_services
fi

# 检查是否已经在运行
if [ -f "$BACKEND_PID_FILE" ] || [ -f "$FRONTEND_PID_FILE" ]; then
    echo -e "${YELLOW}检测到服务可能正在运行，正在停止旧服务...${NC}"
    stop_services
    sleep 2
fi

# 设置退出时清理
trap stop_services EXIT INT TERM

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  启动校园直聘前后端服务${NC}"
echo -e "${GREEN}========================================${NC}"

# 启动后端服务
echo -e "${YELLOW}正在启动后端服务...${NC}"
cd "$SCRIPT_DIR/backend"
export PYTHONPATH="$PWD"
nohup python -m uvicorn app.main:app --reload --port 5011 --host 0.0.0.0 > "$SCRIPT_DIR/.backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$BACKEND_PID_FILE"
echo -e "${GREEN}后端服务已启动 (PID: $BACKEND_PID, 端口: 5011)${NC}"
echo -e "${YELLOW}后端日志: $SCRIPT_DIR/.backend.log${NC}"

# 等待后端启动
sleep 3

# 检查后端是否启动成功
if ! ps -p "$BACKEND_PID" > /dev/null 2>&1; then
    echo -e "${RED}后端服务启动失败，请查看日志: $SCRIPT_DIR/.backend.log${NC}"
    rm -f "$BACKEND_PID_FILE"
    exit 1
fi

# 启动前端服务
echo -e "${YELLOW}正在启动前端服务...${NC}"
cd "$SCRIPT_DIR/frontend"
nohup npm run dev > "$SCRIPT_DIR/.frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$FRONTEND_PID_FILE"
echo -e "${GREEN}前端服务已启动 (PID: $FRONTEND_PID)${NC}"
echo -e "${YELLOW}前端日志: $SCRIPT_DIR/.frontend.log${NC}"

# 等待前端启动
sleep 3

# 检查前端是否启动成功
if ! ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
    echo -e "${RED}前端服务启动失败，请查看日志: $SCRIPT_DIR/.frontend.log${NC}"
    rm -f "$FRONTEND_PID_FILE"
    stop_services
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  服务启动成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}后端服务: http://localhost:5011${NC}"
echo -e "${GREEN}前端服务: http://localhost:5173 (或查看前端日志获取实际端口)${NC}"
echo -e "${YELLOW}查看后端日志: tail -f $SCRIPT_DIR/.backend.log${NC}"
echo -e "${YELLOW}查看前端日志: tail -f $SCRIPT_DIR/.frontend.log${NC}"
echo -e "${YELLOW}停止服务: $0 stop 或 Ctrl+C${NC}"
echo ""

# 保持脚本运行，等待用户中断
echo -e "${YELLOW}按 Ctrl+C 停止所有服务...${NC}"
echo ""

# 持续监控服务状态
while true; do
    # 检查后端服务
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if ! ps -p "$BACKEND_PID" > /dev/null 2>&1; then
            echo -e "${RED}后端服务已停止 (PID: $BACKEND_PID)${NC}"
            rm -f "$BACKEND_PID_FILE"
        fi
    fi
    
    # 检查前端服务
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if ! ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
            echo -e "${RED}前端服务已停止 (PID: $FRONTEND_PID)${NC}"
            rm -f "$FRONTEND_PID_FILE"
        fi
    fi
    
    # 如果两个服务都停止了，退出
    if [ ! -f "$BACKEND_PID_FILE" ] && [ ! -f "$FRONTEND_PID_FILE" ]; then
        echo -e "${YELLOW}所有服务已停止${NC}"
        break
    fi
    
    sleep 5
done

