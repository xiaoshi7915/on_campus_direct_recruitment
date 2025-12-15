"""
数据库连接和会话管理
"""
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# 将同步数据库URL转换为异步URL
# mysql+pymysql:// -> mysql+aiomysql://
# 如果URL已经是mysql+pymysql格式，则转换为aiomysql格式
database_url = settings.DATABASE_URL
if "mysql+pymysql://" in database_url:
    database_url = database_url.replace("mysql+pymysql://", "mysql+aiomysql://")
elif "mysql://" in database_url and "aiomysql" not in database_url:
    database_url = database_url.replace("mysql://", "mysql+aiomysql://")

# 添加utf8mb4字符集参数
if "?" not in database_url:
    database_url += "?charset=utf8mb4"
elif "charset=" not in database_url:
    database_url += "&charset=utf8mb4"
elif "charset=utf8" in database_url:
    database_url = database_url.replace("charset=utf8", "charset=utf8mb4")

# 创建异步数据库引擎
engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,  # 是否打印SQL语句
    future=True,
    pool_pre_ping=True,  # 连接前ping数据库
    pool_size=20,  # 连接池大小（从10增加到20，支持更高并发）
    max_overflow=40,  # 最大溢出连接数（从20增加到40）
    pool_recycle=3600,  # 连接回收时间（1小时），防止长时间连接失效
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
    } if "aiomysql" in database_url else {}
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 创建基础模型类
Base = declarative_base()


# 依赖注入：获取数据库会话
async def get_db() -> AsyncSession:
    """
    获取数据库会话的依赖函数
    用于FastAPI的依赖注入系统
    使用async with确保资源正确释放，即使发生异常也会自动关闭会话
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # 如果没有异常，提交事务
            await session.commit()
        except Exception as e:
            # 发生异常时回滚事务
            await session.rollback()
            logger.error(f"数据库操作失败，已回滚: {str(e)}", exc_info=True)
            raise
        # async with会自动处理session.close()，无需手动关闭

