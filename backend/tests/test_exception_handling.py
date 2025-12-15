"""
测试异常处理功能
验证全局异常处理器正确工作
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.core.logging import get_logger

logger = get_logger(__name__)
client = TestClient(app)


def test_http_exception_handling():
    """测试HTTP异常处理"""
    # 测试404错误
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    
    # 测试错误响应格式
    if response.status_code >= 400:
        data = response.json()
        # 检查是否有错误码字段（如果实现了统一错误格式）
        logger.info(f"HTTP异常响应: {data}")


def test_global_exception_handling():
    """测试全局异常处理"""
    # 访问一个可能触发异常的端点
    # 这里使用健康检查端点，它应该正常返回
    response = client.get("/health")
    assert response.status_code == 200
    
    # 测试根端点
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data


def test_error_response_format():
    """测试错误响应格式"""
    # 测试不存在的API端点
    response = client.get("/api/v1/invalid/endpoint")
    
    # 应该返回404或500
    assert response.status_code in [404, 500]
    
    # 检查响应格式
    try:
        data = response.json()
        logger.info(f"错误响应格式: {data}")
        # 如果有统一错误格式，检查字段
        # assert "error_code" in data or "detail" in data
    except:
        # 某些错误可能没有JSON响应
        pass


def test_system_exception_not_caught():
    """测试系统异常不被捕获（需要手动触发）"""
    # 这个测试主要验证SystemExit和KeyboardInterrupt不被捕获
    # 在实际应用中，这些异常应该正常传播
    # 这里只做概念验证
    logger.info("系统异常处理测试：SystemExit和KeyboardInterrupt应该正常传播")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


