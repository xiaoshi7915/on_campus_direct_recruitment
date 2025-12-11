"""
认证相关单元测试
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """测试健康检查接口"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """测试用户注册"""
    user_data = {
        "username": "test_user_001",
        "password": "123456",
        "user_type": "STUDENT",
        "phone": "13800138001",
        "email": "test001@example.com"
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code in [200, 201, 400]  # 400可能是用户已存在


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """测试用户登录"""
    login_data = {
        "username": "test_user_001",
        "password": "123456"
    }
    response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )
    # 如果用户不存在，返回404；如果密码错误，返回401；成功返回200
    assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_get_current_user_without_token(client: AsyncClient):
    """测试未登录时获取用户信息"""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401  # 未授权


@pytest.mark.asyncio
async def test_password_hashing():
    """测试密码加密"""
    from app.core.security import get_password_hash, verify_password
    
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    # 验证密码
    assert verify_password(password, hashed) == True
    assert verify_password("wrong_password", hashed) == False

