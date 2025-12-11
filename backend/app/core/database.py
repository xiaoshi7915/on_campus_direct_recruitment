"""
数据库连接和会话管理
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

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
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大溢出连接数
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
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

