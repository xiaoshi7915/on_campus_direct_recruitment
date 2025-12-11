"""
日志配置模块
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# 创建logs目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 配置根日志记录器
def setup_logging():
    """设置日志配置"""
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器 - 应用日志
    app_log_file = LOG_DIR / "app.log"
    app_file_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    app_file_handler.setLevel(logging.DEBUG)
    app_file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    app_file_handler.setFormatter(app_file_formatter)
    root_logger.addHandler(app_file_handler)
    
    # 文件处理器 - 错误日志
    error_log_file = LOG_DIR / "error.log"
    error_file_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    error_file_handler.setFormatter(error_file_formatter)
    root_logger.addHandler(error_file_handler)
    
    # 文件处理器 - 访问日志
    access_log_file = LOG_DIR / "access.log"
    access_file_handler = RotatingFileHandler(
        access_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    access_file_handler.setLevel(logging.INFO)
    access_file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    access_file_handler.setFormatter(access_file_formatter)
    
    # 创建访问日志记录器
    access_logger = logging.getLogger("access")
    access_logger.addHandler(access_file_handler)
    access_logger.setLevel(logging.INFO)
    access_logger.propagate = False
    
    return root_logger


# 初始化日志
logger = setup_logging()

# 获取不同模块的日志记录器
def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志记录器"""
    return logging.getLogger(name)


