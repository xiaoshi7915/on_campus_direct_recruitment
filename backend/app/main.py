"""
FastAPI应用主入口文件
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import setup_logging, get_logger
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware
from app.api.v1 import api_router

# 初始化日志
setup_logging()
logger = get_logger(__name__)


# 应用启动和关闭时的生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    - 启动时：初始化数据库表
    - 关闭时：清理资源
    """
    # 启动时执行
    logger.info(f"启动 {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"调试模式: {settings.DEBUG}")
    
    # 检查生产环境配置
    from app.core.production import check_production_settings
    check_production_settings()
    
    async with engine.begin() as conn:
        # 创建数据库表（生产环境应使用Alembic迁移）
        # await conn.run_sync(Base.metadata.create_all)
        pass
    
    yield
    
    # 关闭时执行
    logger.info("应用正在关闭...")
    
    # 关闭时执行
    pass


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="校园直聘平台API服务",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加日志中间件
app.add_middleware(LoggingMiddleware)

# 添加限流中间件（每分钟60次请求）
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# 注册API路由
app.include_router(api_router, prefix="/api/v1")


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    全局异常处理器
    捕获所有未处理的异常并返回统一格式的错误响应
    """
    return JSONResponse(
        status_code=500,
        content={
            "error_code": 5000,
            "error_message": "服务器内部错误",
            "detail": str(exc) if settings.DEBUG else "服务器处理请求时发生错误"
        }
    )


# 根路径
@app.get("/")
async def root():
    """
    根路径，返回API基本信息
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


# 健康检查
@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy"}

