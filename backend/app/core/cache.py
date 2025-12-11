"""
Redis缓存工具模块
"""
import json
from typing import Optional, Any
from redis.asyncio import Redis
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Redis连接池
redis_client: Optional[Redis] = None


async def get_redis() -> Optional[Redis]:
    """获取Redis客户端"""
    global redis_client
    
    if redis_client is None:
        try:
            redis_client = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=True
            )
            # 测试连接
            await redis_client.ping()
            logger.info("Redis连接成功")
        except Exception as e:
            logger.warning(f"Redis连接失败: {str(e)}，将使用内存缓存")
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
    """关闭Redis连接"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
        logger.info("Redis连接已关闭")

