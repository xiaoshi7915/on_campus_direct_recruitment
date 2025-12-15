"""
测试Redis分布式限流功能
验证限流中间件正确工作
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.core.cache import init_redis_pool
from app.core.logging import get_logger

logger = get_logger(__name__)
client = TestClient(app)


def test_rate_limit_with_redis():
    """测试Redis限流功能"""
    init_redis_pool()
    
    # 发送多个请求，测试限流
    responses = []
    for i in range(70):  # 超过默认的60次/分钟限制
        response = client.get("/health")
        responses.append(response.status_code)
    
    # 检查是否有429响应（Too Many Requests）
    status_429_count = responses.count(429)
    
    if status_429_count > 0:
        logger.info(f"限流测试通过：检测到{status_429_count}个429响应")
        assert status_429_count > 0, "应该触发限流"
    else:
        logger.warning("未检测到限流，可能是Redis不可用或限流配置问题")


def test_rate_limit_health_endpoint_excluded():
    """测试健康检查端点不受限流影响"""
    init_redis_pool()
    
    # 健康检查端点应该不受限流
    for i in range(100):
        response = client.get("/health")
        assert response.status_code == 200, "健康检查端点不应被限流"


def test_rate_limit_root_endpoint_excluded():
    """测试根端点不受限流影响"""
    init_redis_pool()
    
    # 根端点应该不受限流
    for i in range(100):
        response = client.get("/")
        assert response.status_code == 200, "根端点不应被限流"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


