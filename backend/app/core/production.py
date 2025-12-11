"""
生产环境配置
"""
import os
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def check_production_settings():
    """检查生产环境配置"""
    warnings = []
    
    # 检查密钥
    if settings.SECRET_KEY == "your-secret-key-here-change-in-production":
        warnings.append("⚠️ SECRET_KEY 使用默认值，生产环境必须修改！")
    
    # 检查调试模式
    if settings.DEBUG:
        warnings.append("⚠️ DEBUG 模式已开启，生产环境应关闭")
    
    # 检查数据库连接
    if "localhost" in settings.DATABASE_URL or "127.0.0.1" in settings.DATABASE_URL:
        warnings.append("⚠️ 数据库连接使用本地地址，生产环境应使用远程数据库")
    
    # 检查CORS配置
    if "*" in settings.CORS_ORIGINS or "localhost" in settings.CORS_ORIGINS:
        warnings.append("⚠️ CORS配置包含通配符或localhost，生产环境应限制具体域名")
    
    if warnings:
        logger.warning("生产环境配置检查发现以下问题：")
        for warning in warnings:
            logger.warning(warning)
    else:
        logger.info("生产环境配置检查通过")
    
    return warnings


def get_production_config():
    """获取生产环境配置建议"""
    return {
        "SECRET_KEY": "应使用强随机字符串（至少32字符）",
        "DEBUG": "False",
        "DATABASE_URL": "应使用远程数据库地址",
        "CORS_ORIGINS": "应限制为具体的前端域名",
        "REDIS_HOST": "应使用Redis服务器地址",
        "LOG_LEVEL": "INFO（生产环境）",
        "WORKERS": "根据CPU核心数设置（建议4-8）",
        "SSL": "应启用HTTPS",
        "RATE_LIMIT": "应根据实际情况调整限流策略"
    }


