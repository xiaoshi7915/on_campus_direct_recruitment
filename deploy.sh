#!/bin/bash

# 校园直聘平台 - Linux一键部署脚本
# 适用于 Ubuntu 20.04+ / CentOS 7+

set -e

echo "=========================================="
echo "校园直聘平台 - Linux一键部署脚本"
echo "=========================================="

# 检测操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "无法检测操作系统类型"
    exit 1
fi

echo "检测到操作系统: $OS"

# 安装Docker和Docker Compose
install_docker() {
    echo "正在安装Docker..."
    
    if command -v docker &> /dev/null; then
        echo "Docker已安装"
    else
        if [ "$OS" == "ubuntu" ] || [ "$OS" == "debian" ]; then
            sudo apt-get update
            sudo apt-get install -y \
                ca-certificates \
                curl \
                gnupg \
                lsb-release
            sudo mkdir -p /etc/apt/keyrings
            curl -fsSL https://download.docker.com/linux/$OS/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
            echo \
                "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$OS \
                $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
            sudo apt-get update
            sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        elif [ "$OS" == "centos" ] || [ "$OS" == "rhel" ]; then
            sudo yum install -y yum-utils
            sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
            sudo systemctl start docker
            sudo systemctl enable docker
        fi
    fi
    
    echo "Docker安装完成"
}

# 配置环境变量
setup_env() {
    echo "正在配置环境变量..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            echo "已创建 .env 文件，请编辑并填入实际配置"
        else
            echo "警告: .env.example 文件不存在"
        fi
    else
        echo ".env 文件已存在"
    fi
}

# 启动服务
start_services() {
    echo "正在启动服务..."
    
    # 检查docker-compose是否可用
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    elif docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        echo "错误: 未找到docker-compose命令"
        exit 1
    fi
    
    # 启动服务
    $COMPOSE_CMD up -d
    
    echo "等待服务启动..."
    sleep 10
    
    # 检查服务状态
    $COMPOSE_CMD ps
}

# 初始化数据库
init_database() {
    echo "正在初始化数据库..."
    
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
    
    # 等待数据库就绪
    echo "等待数据库就绪..."
    sleep 15
    
    # 执行数据库迁移
    $COMPOSE_CMD exec -T backend alembic upgrade head || echo "数据库迁移失败，请手动执行: docker-compose exec backend alembic upgrade head"
}

# 主函数
main() {
    echo "开始部署..."
    
    # 检查是否为root用户
    if [ "$EUID" -ne 0 ]; then 
        echo "请使用sudo运行此脚本"
        exit 1
    fi
    
    # 安装Docker
    install_docker
    
    # 配置环境变量
    setup_env
    
    # 启动服务
    start_services
    
    # 初始化数据库
    init_database
    
    echo ""
    echo "=========================================="
    echo "部署完成！"
    echo "=========================================="
    echo ""
    echo "服务访问地址:"
    echo "  前端: http://$(hostname -I | awk '{print $1}'):8008"
    echo "  后端API: http://$(hostname -I | awk '{print $1}'):6121"
    echo "  API文档: http://$(hostname -I | awk '{print $1}'):6121/docs"
    echo ""
    echo "常用命令:"
    echo "  查看服务状态: docker-compose ps"
    echo "  查看日志: docker-compose logs -f"
    echo "  停止服务: docker-compose stop"
    echo "  重启服务: docker-compose restart"
    echo ""
    echo "重要提示:"
    echo "  1. 请编辑 .env 文件，配置数据库、OSS等关键信息"
    echo "  2. 生产环境请修改SECRET_KEY为强随机密钥"
    echo "  3. 建议配置Nginx反向代理和SSL证书"
    echo ""
}

# 执行主函数
main

