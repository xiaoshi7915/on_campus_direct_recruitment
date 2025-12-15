"""
Redis缓存工具模块
使用连接池管理Redis连接
"""
import json
from typing import Optional, Any
from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Redis连接池
redis_pool: Optional[ConnectionPool] = None
redis_client: Optional[Redis] = None


def init_redis_pool():
    """初始化Redis连接池"""
    global redis_pool, redis_client
    
    if redis_pool is None:
        try:
            redis_pool = ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=True,
                max_connections=50,  # 最大连接数
                retry_on_timeout=True,
                health_check_interval=30  # 健康检查间隔（秒）
            )
            redis_client = Redis(connection_pool=redis_pool)
            logger.info("Redis连接池初始化成功")
        except Exception as e:
            logger.warning(f"Redis连接池初始化失败: {str(e)}，将使用内存缓存")
            redis_pool = None
            redis_client = None


async def get_redis() -> Optional[Redis]:
    """获取Redis客户端（使用连接池）"""
    global redis_client
    
    if redis_pool is None:
        init_redis_pool()
    
    if redis_client is None:
        return None
    
    # 测试连接
    try:
        await redis_client.ping()
    except Exception as e:
        logger.warning(f"Redis连接测试失败: {str(e)}")
        # 尝试重新初始化
        init_redis_pool()
        if redis_client:
            try:
                await redis_client.ping()
            except Exception:
                redis_client = None
    
    return redis_client


async def set_cache(key: str, value: Any, expire: int = 3600):
    """
    设置缓存
    
    Args:
        key: 缓存键
        value: 缓存值
        expire: 过期时间（秒）
    """
    redis = await get_redis()
    if redis:
        try:
            # 如果value是字符串，直接存储；否则序列化为JSON
            if isinstance(value, str):
                await redis.setex(key, expire, value)
            else:
                await redis.setex(
                    key,
                    expire,
                    json.dumps(value, ensure_ascii=False)
                )
        except Exception as e:
            logger.error(f"设置缓存失败: {str(e)}")
    else:
        # 如果Redis不可用，使用内存缓存（简单实现）
        logger.debug(f"[内存缓存] 设置 {key}")


async def get_cache(key: str) -> Optional[Any]:
    """
    获取缓存
    
    Args:
        key: 缓存键
        
    Returns:
        缓存值，如果不存在返回None
    """
    redis = await get_redis()
    if redis:
        try:
            value = await redis.get(key)
            if value:
                # 尝试解析为JSON，如果失败则返回原始字符串
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
        except Exception as e:
            logger.error(f"获取缓存失败: {str(e)}")
    
    return None


async def delete_cache(key: str):
    """
    删除缓存
    
    Args:
        key: 缓存键
    """
    redis = await get_redis()
    if redis:
        try:
            await redis.delete(key)
        except Exception as e:
            logger.error(f"删除缓存失败: {str(e)}")


async def close_redis():
    """关闭Redis连接和连接池"""
    global redis_client, redis_pool
    if redis_client:
        await redis_client.close()
        redis_client = None
    if redis_pool:
        await redis_pool.disconnect()
        redis_pool = None
        logger.info("Redis连接池已关闭")

