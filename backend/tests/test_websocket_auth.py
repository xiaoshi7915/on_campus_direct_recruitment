"""
测试WebSocket认证功能
验证token验证和用户身份验证
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from app.main import app
from app.core.security import create_access_token
from app.models.user import User
from app.core.database import get_db
from sqlalchemy import select

client = TestClient(app)


@pytest.mark.asyncio
async def test_websocket_without_token():
    """测试没有token的WebSocket连接应该被拒绝"""
    with client.websocket_connect("/api/v1/chat/ws") as websocket:
        # 应该立即关闭
        try:
            websocket.receive_text()
        except Exception as e:
            # 应该收到关闭消息
            assert "缺少认证令牌" in str(e) or "1008" in str(e)


@pytest.mark.asyncio
async def test_websocket_with_invalid_token():
    """测试无效token的WebSocket连接应该被拒绝"""
    invalid_token = "invalid_token_here"
    with client.websocket_connect(f"/api/v1/chat/ws?token={invalid_token}") as websocket:
        try:
            websocket.receive_text()
        except Exception as e:
            # 应该收到关闭消息
            assert "无效的认证令牌" in str(e) or "1008" in str(e)


@pytest.mark.asyncio
async def test_websocket_with_valid_token():
    """测试有效token的WebSocket连接"""
    # 首先需要创建一个测试用户并获取token
    user = None
    async for db in get_db():
        # 查找或创建测试用户
        result = await db.execute(
            select(User).where(User.username == "test_websocket_user")
        )
        user = result.scalar_one_or_none()
        break
    
    if not user:
        pytest.skip("需要先创建测试用户")
    
    # 创建token
    from datetime import timedelta
    from app.core.config import settings
    token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "user_type": user.user_type},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # 测试WebSocket连接
    with client.websocket_connect(f"/api/v1/chat/ws?token={token}") as websocket:
        # 发送ping消息
        websocket.send_json({"type": "ping"})
        response = websocket.receive_json()
        assert response["type"] == "pong"


@pytest.mark.asyncio
async def test_websocket_heartbeat():
    """测试WebSocket心跳机制"""
    user = None
    async for db in get_db():
        result = await db.execute(
            select(User).where(User.username == "test_websocket_user")
        )
        user = result.scalar_one_or_none()
        break
    
    if not user:
        pytest.skip("需要先创建测试用户")
    
    from datetime import timedelta
    from app.core.config import settings
    token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "user_type": user.user_type},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    with client.websocket_connect(f"/api/v1/chat/ws?token={token}") as websocket:
        # 发送多个ping消息
        for i in range(5):
            websocket.send_json({"type": "ping"})
            response = websocket.receive_json()
            assert response["type"] == "pong"
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

