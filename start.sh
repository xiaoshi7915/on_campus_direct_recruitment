#!/bin/bash
# 校园直聘平台 - 前后端服务管理脚本
# 使用方法: ./start.sh [start|stop|restart|status|logs]

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 配置
BACKEND_PORT=6121
FRONTEND_PORT=8008
BACKEND_PID_FILE="$SCRIPT_DIR/.backend.pid"
FRONTEND_PID_FILE="$SCRIPT_DIR/.frontend.pid"
BACKEND_LOG_FILE="$SCRIPT_DIR/.backend.log"
FRONTEND_LOG_FILE="$SCRIPT_DIR/.frontend.log"

# 检查端口是否被占用
check_port() {
    local port=$1
    if command -v lsof > /dev/null 2>&1; then
        lsof -ti:$port 2>/dev/null
    elif command -v netstat > /dev/null 2>&1; then
        netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1
    elif command -v ss > /dev/null 2>&1; then
        ss -tlnp 2>/dev/null | grep ":$port " | grep -oP 'pid=\K\d+' | head -1
    fi
}

# 检查服务是否运行
is_running() {
    local pid_file=$1
    local port=$2
    
    if [ ! -f "$pid_file" ]; then
        return 1
    fi
    
    local pid=$(cat "$pid_file" 2>/dev/null)
    if [ -z "$pid" ]; then
        return 1
    fi
    
    # 检查进程是否存在
    if ! ps -p "$pid" > /dev/null 2>&1; then
        return 1
    fi
    
    # 检查端口是否被该进程占用
    if [ -n "$port" ]; then
        local port_pid=$(check_port "$port")
        if [ -n "$port_pid" ] && [ "$port_pid" = "$pid" ]; then
            return 0
        fi
    else
        return 0
    fi
    
    return 1
}

# 停止服务
stop_services() {
    echo -e "${YELLOW}正在停止服务...${NC}"
    
    local stopped=false
    
    # 停止后端
    if is_running "$BACKEND_PID_FILE" "$BACKEND_PORT"; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        echo -e "${YELLOW}停止后端服务 (PID: $BACKEND_PID)...${NC}"
        kill "$BACKEND_PID" 2>/dev/null
        sleep 2
        if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
            kill -9 "$BACKEND_PID" 2>/dev/null
        fi
        stopped=true
    fi
    
    # 清理后端端口
    local backend_port_pid=$(check_port "$BACKEND_PORT")
    if [ -n "$backend_port_pid" ]; then
        echo -e "${YELLOW}清理后端端口 $BACKEND_PORT (PID: $backend_port_pid)...${NC}"
        kill -9 "$backend_port_pid" 2>/dev/null
        stopped=true
    fi
    
    # 停止前端
    if is_running "$FRONTEND_PID_FILE" "$FRONTEND_PORT"; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        echo -e "${YELLOW}停止前端服务 (PID: $FRONTEND_PID)...${NC}"
        kill "$FRONTEND_PID" 2>/dev/null
        sleep 2
        if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
            kill -9 "$FRONTEND_PID" 2>/dev/null
        fi
        stopped=true
    fi
    
    # 清理前端端口
    local frontend_port_pid=$(check_port "$FRONTEND_PORT")
    if [ -n "$frontend_port_pid" ]; then
        echo -e "${YELLOW}清理前端端口 $FRONTEND_PORT (PID: $frontend_port_pid)...${NC}"
        kill -9 "$frontend_port_pid" 2>/dev/null
        stopped=true
    fi
    
    # 清理可能的残留进程
    pkill -f "uvicorn app.main:app.*6121" 2>/dev/null
    pkill -f "vite.*on_campus" 2>/dev/null
    
    # 删除PID文件
    rm -f "$BACKEND_PID_FILE" "$FRONTEND_PID_FILE"
    
    if [ "$stopped" = true ]; then
        echo -e "${GREEN}服务已停止${NC}"
    else
        echo -e "${YELLOW}没有运行中的服务${NC}"
    fi
}

# 查看服务状态
show_status() {
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}  服务状态${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""
    
    # 后端状态（优先通过端口检查，然后更新PID文件）
    local backend_pid=$(ps aux | grep "uvicorn.*$BACKEND_PORT" | grep -v grep | awk '{print $2}' | head -1)
    if [ -z "$backend_pid" ]; then
        backend_pid=$(check_port "$BACKEND_PORT")
    fi
    
    if [ -n "$backend_pid" ] && ps -p "$backend_pid" > /dev/null 2>&1 && (netstat -tlnp 2>/dev/null | grep -q ":$BACKEND_PORT" || ss -tlnp 2>/dev/null | grep -q ":$BACKEND_PORT"); then
        echo "$backend_pid" > "$BACKEND_PID_FILE"
        echo -e "${GREEN}✅ 后端服务: 运行中${NC}"
        echo -e "   PID: $backend_pid"
        echo -e "   端口: $BACKEND_PORT"
        echo -e "   地址: ${BLUE}http://localhost:$BACKEND_PORT${NC}"
        echo -e "   API文档: ${BLUE}http://localhost:$BACKEND_PORT/docs${NC}"
        
        # 健康检查
        local health=$(curl -s http://localhost:$BACKEND_PORT/health 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$health" ]; then
            echo -e "   健康状态: ${GREEN}$health${NC}"
        else
            echo -e "   健康状态: ${YELLOW}检查中...${NC}"
        fi
    else
        echo -e "${RED}❌ 后端服务: 未运行${NC}"
        rm -f "$BACKEND_PID_FILE"
    fi
    
    echo ""
    
    # 前端状态（优先通过端口检查，然后更新PID文件）
    local frontend_pid=$(lsof -ti:$FRONTEND_PORT 2>/dev/null | head -1)
    if [ -z "$frontend_pid" ]; then
        frontend_pid=$(ps aux | grep "vite.*on_campus\|node.*vite" | grep -v grep | awk '{print $2}' | head -1)
    fi
    
    if [ -n "$frontend_pid" ] && ps -p "$frontend_pid" > /dev/null 2>&1 && (netstat -tlnp 2>/dev/null | grep -q ":$FRONTEND_PORT" || ss -tlnp 2>/dev/null | grep -q ":$FRONTEND_PORT"); then
        echo "$frontend_pid" > "$FRONTEND_PID_FILE"
        echo -e "${GREEN}✅ 前端服务: 运行中${NC}"
        echo -e "   PID: $frontend_pid"
        echo -e "   端口: $FRONTEND_PORT"
        echo -e "   地址: ${BLUE}http://localhost:$FRONTEND_PORT${NC}"
    else
        echo -e "${RED}❌ 前端服务: 未运行${NC}"
        rm -f "$FRONTEND_PID_FILE"
    fi
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
}

# 查看日志
show_logs() {
    local service=${1:-"all"}
    
    case $service in
        backend|b)
            if [ -f "$BACKEND_LOG_FILE" ]; then
                echo -e "${CYAN}后端日志 (按 Ctrl+C 退出):${NC}"
                tail -f "$BACKEND_LOG_FILE"
            else
                echo -e "${RED}后端日志文件不存在: $BACKEND_LOG_FILE${NC}"
            fi
            ;;
        frontend|f)
            if [ -f "$FRONTEND_LOG_FILE" ]; then
                echo -e "${CYAN}前端日志 (按 Ctrl+C 退出):${NC}"
                tail -f "$FRONTEND_LOG_FILE"
            else
                echo -e "${RED}前端日志文件不存在: $FRONTEND_LOG_FILE${NC}"
            fi
            ;;
        all|*)
            if [ -f "$BACKEND_LOG_FILE" ] || [ -f "$FRONTEND_LOG_FILE" ]; then
                echo -e "${CYAN}查看所有日志 (最后20行):${NC}"
                echo ""
                if [ -f "$BACKEND_LOG_FILE" ]; then
                    echo -e "${YELLOW}=== 后端日志 ===${NC}"
                    tail -20 "$BACKEND_LOG_FILE"
                    echo ""
                fi
                if [ -f "$FRONTEND_LOG_FILE" ]; then
                    echo -e "${YELLOW}=== 前端日志 ===${NC}"
                    tail -20 "$FRONTEND_LOG_FILE"
                fi
            else
                echo -e "${RED}日志文件不存在${NC}"
            fi
            ;;
    esac
}

# 启动服务
start_services() {
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  启动校园直聘前后端服务${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo ""
    
    # 检查是否已经在运行
    if is_running "$BACKEND_PID_FILE" "$BACKEND_PORT" || is_running "$FRONTEND_PID_FILE" "$FRONTEND_PORT"; then
        echo -e "${YELLOW}检测到服务正在运行，请先停止服务: $0 stop${NC}"
        show_status
        exit 1
    fi
    
    # 启动后端服务
    echo -e "${YELLOW}正在启动后端服务...${NC}"
    cd "$SCRIPT_DIR/backend"
    export PYTHONPATH="$PWD"
    
    # 检测并使用正确的Python解释器
    if [ -f "$SCRIPT_DIR/py312/bin/python" ]; then
        PYTHON_CMD="$SCRIPT_DIR/py312/bin/python"
        echo -e "${YELLOW}使用 py312/bin/python 启动后端${NC}"
    elif command -v python3.12 > /dev/null 2>&1; then
        PYTHON_CMD="python3.12"
        echo -e "${YELLOW}使用 python3.12 启动后端${NC}"
    elif command -v python3.11 > /dev/null 2>&1; then
        PYTHON_CMD="python3.11"
        echo -e "${YELLOW}使用 python3.11 启动后端${NC}"
    else
        PYTHON_CMD="python"
        echo -e "${YELLOW}使用系统 python 启动后端${NC}"
    fi
    
    # 清理端口
    local backend_port_pid=$(check_port "$BACKEND_PORT")
    if [ -n "$backend_port_pid" ]; then
        echo -e "${YELLOW}清理端口 $BACKEND_PORT (PID: $backend_port_pid)...${NC}"
        kill -9 "$backend_port_pid" 2>/dev/null
        sleep 1
    fi
    
    # 启动后端
    nohup $PYTHON_CMD -m uvicorn app.main:app --reload --port $BACKEND_PORT --host 0.0.0.0 > "$BACKEND_LOG_FILE" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$BACKEND_PID_FILE"
    echo -e "${GREEN}后端服务已启动 (PID: $BACKEND_PID, 端口: $BACKEND_PORT)${NC}"
    
    # 等待后端启动
    sleep 5
    
    # 检查后端是否启动成功（通过端口和进程双重检查）
    local backend_check=false
    if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
        local port_pid=$(check_port "$BACKEND_PORT")
        if [ -n "$port_pid" ] && [ "$port_pid" = "$BACKEND_PID" ]; then
            backend_check=true
        fi
    fi
    
    if [ "$backend_check" = false ]; then
        echo -e "${YELLOW}后端服务可能正在启动中，继续检查...${NC}"
        sleep 3
        # 再次检查
        local actual_pid=$(ps aux | grep "uvicorn.*$BACKEND_PORT" | grep -v grep | awk '{print $2}' | head -1)
        if [ -n "$actual_pid" ] && (netstat -tlnp 2>/dev/null | grep -q ":$BACKEND_PORT" || ss -tlnp 2>/dev/null | grep -q ":$BACKEND_PORT"); then
            echo "$actual_pid" > "$BACKEND_PID_FILE"
            backend_check=true
        fi
    fi
    
    if [ "$backend_check" = false ]; then
        echo -e "${RED}后端服务启动失败，请查看日志: $BACKEND_LOG_FILE${NC}"
        tail -30 "$BACKEND_LOG_FILE"
        rm -f "$BACKEND_PID_FILE"
        exit 1
    fi
    
    # 启动前端服务
    echo -e "${YELLOW}正在启动前端服务...${NC}"
    cd "$SCRIPT_DIR/frontend"
    
    # 清理端口
    local frontend_port_pid=$(check_port "$FRONTEND_PORT")
    if [ -n "$frontend_port_pid" ]; then
        echo -e "${YELLOW}清理端口 $FRONTEND_PORT (PID: $frontend_port_pid)...${NC}"
        kill -9 "$frontend_port_pid" 2>/dev/null
        sleep 1
    fi
    
    # 启动前端
    PORT=$FRONTEND_PORT nohup npm run dev > "$FRONTEND_LOG_FILE" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$FRONTEND_PID_FILE"
    echo -e "${GREEN}前端服务已启动 (PID: $FRONTEND_PID, 端口: $FRONTEND_PORT)${NC}"
    
    # 等待前端启动
    sleep 5
    
    # 检查前端是否启动成功（通过端口和进程双重检查）
    local frontend_check=false
    if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
        local port_pid=$(check_port "$FRONTEND_PORT")
        if [ -n "$port_pid" ]; then
            echo "$port_pid" > "$FRONTEND_PID_FILE"
            frontend_check=true
        fi
    fi
    
    if [ "$frontend_check" = false ]; then
        echo -e "${YELLOW}前端服务可能正在启动中，继续检查...${NC}"
        sleep 3
        # 再次检查
        local actual_pid=$(lsof -ti:$FRONTEND_PORT 2>/dev/null | head -1)
        if [ -n "$actual_pid" ] && (netstat -tlnp 2>/dev/null | grep -q ":$FRONTEND_PORT" || ss -tlnp 2>/dev/null | grep -q ":$FRONTEND_PORT"); then
            echo "$actual_pid" > "$FRONTEND_PID_FILE"
            frontend_check=true
        fi
    fi
    
    if [ "$frontend_check" = false ]; then
        echo -e "${RED}前端服务启动失败，请查看日志: $FRONTEND_LOG_FILE${NC}"
        tail -30 "$FRONTEND_LOG_FILE"
        rm -f "$FRONTEND_PID_FILE"
        stop_services
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  服务启动成功！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo ""
    show_status
    echo ""
    echo -e "${YELLOW}查看日志:${NC}"
    echo -e "  后端: ${CYAN}tail -f $BACKEND_LOG_FILE${NC}"
    echo -e "  前端: ${CYAN}tail -f $FRONTEND_LOG_FILE${NC}"
    echo -e "  或使用: ${CYAN}$0 logs${NC}"
    echo ""
    echo -e "${YELLOW}停止服务: ${CYAN}$0 stop${NC}"
    echo ""
}

# 重启服务
restart_services() {
    echo -e "${YELLOW}重启服务...${NC}"
    stop_services
    sleep 2
    start_services
}

# 显示帮助信息
show_help() {
    echo -e "${CYAN}校园直聘平台 - 服务管理脚本${NC}"
    echo ""
    echo -e "${YELLOW}使用方法:${NC}"
    echo -e "  $0 [命令]"
    echo ""
    echo -e "${YELLOW}命令:${NC}"
    echo -e "  ${GREEN}start${NC}     启动前后端服务 (默认)"
    echo -e "  ${GREEN}stop${NC}      停止前后端服务"
    echo -e "  ${GREEN}restart${NC}   重启前后端服务"
    echo -e "  ${GREEN}status${NC}    查看服务状态"
    echo -e "  ${GREEN}logs${NC}      查看服务日志"
    echo -e "    ${CYAN}logs backend${NC}  或 ${CYAN}logs b${NC}  - 查看后端日志"
    echo -e "    ${CYAN}logs frontend${NC} 或 ${CYAN}logs f${NC}  - 查看前端日志"
    echo -e "    ${CYAN}logs all${NC}      或 ${CYAN}logs${NC}    - 查看所有日志"
    echo -e "  ${GREEN}help${NC}      显示帮助信息"
    echo ""
    echo -e "${YELLOW}示例:${NC}"
    echo -e "  $0              # 启动服务"
    echo -e "  $0 start       # 启动服务"
    echo -e "  $0 stop        # 停止服务"
    echo -e "  $0 status      # 查看状态"
    echo -e "  $0 logs        # 查看所有日志"
    echo -e "  $0 logs backend # 查看后端日志"
    echo ""
}

# 主逻辑
case "${1:-start}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "${2:-all}"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
