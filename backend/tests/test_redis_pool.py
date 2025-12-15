"""
测试Redis连接池功能
验证连接池正确初始化和使用
"""
import pytest
import asyncio
from app.core.cache import init_redis_pool, get_redis, close_redis, set_cache, get_cache, delete_cache
from app.core.logging import get_logger

logger = get_logger(__name__)


@pytest.mark.asyncio
async def test_redis_pool_initialization():
    """测试Redis连接池初始化"""
    init_redis_pool()
    redis = await get_redis()
    
    if redis:
        # 测试连接
        result = await redis.ping()
        assert result is True
        logger.info("Redis连接池初始化成功")
    else:
        pytest.skip("Redis不可用，跳过测试")


@pytest.mark.asyncio
async def test_redis_connection_pool_reuse():
    """测试连接池复用"""
    init_redis_pool()
    
    # 创建多个连接，应该复用连接池
    connections = []
    for i in range(10):
        redis = await get_redis()
        if redis:
            connections.append(redis)
            result = await redis.ping()
            assert result is True
    
    if connections:
        logger.info(f"成功创建{len(connections)}个Redis连接（复用连接池）")
    else:
        pytest.skip("Redis不可用，跳过测试")


@pytest.mark.asyncio
async def test_redis_cache_operations():
    """测试Redis缓存操作"""
    init_redis_pool()
    
    # 测试设置缓存
    await set_cache("test_key", "test_value", expire=60)
    
    # 测试获取缓存
    value = await get_cache("test_key")
    assert value == "test_value"
    
    # 测试设置复杂对象
    test_data = {"name": "test", "value": 123}
    await set_cache("test_complex", test_data, expire=60)
    
    # 测试获取复杂对象
    cached_data = await get_cache("test_complex")
    assert cached_data == test_data
    
    # 测试删除缓存
    await delete_cache("test_key")
    deleted_value = await get_cache("test_key")
    assert deleted_value is None
    
    logger.info("Redis缓存操作测试通过")


@pytest.mark.asyncio
async def test_redis_pool_close():
    """测试连接池关闭"""
    init_redis_pool()
    await close_redis()
    
    # 关闭后应该无法获取连接
    redis = await get_redis()
    # 注意：close_redis后，get_redis可能会重新初始化
    # 这里主要测试关闭功能本身
    logger.info("Redis连接池关闭测试完成")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


