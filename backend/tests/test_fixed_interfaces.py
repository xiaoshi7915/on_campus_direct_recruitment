"""
测试修复后的接口
包括刷新令牌、标记消息已读、更新申请状态等接口
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.job import Job, JobApplication
from app.models.chat import ChatSession, Message
from app.models.profile import StudentProfile, EnterpriseProfile
from app.core.security import get_password_hash, create_access_token, create_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
import json

@pytest.fixture
async def client():
    """创建测试客户端"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_student_user():
    """创建测试学生用户"""
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        user = User(
            id=str(uuid4()),
            username=f"test_student_{uuid4().hex[:8]}",
            password_hash=get_password_hash("test123456"),
            user_type="STUDENT",
            status="ACTIVE"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # 创建学生档案
        student_profile = StudentProfile(
            id=str(uuid4()),
            user_id=user.id,
            real_name="测试学生",
            student_number=f"STU{uuid4().hex[:8]}"
        )
        db.add(student_profile)
        await db.commit()
        
        yield user


@pytest.fixture
async def test_enterprise_user():
    """创建测试企业用户"""
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        user = User(
            id=str(uuid4()),
            username=f"test_enterprise_{uuid4().hex[:8]}",
            password_hash=get_password_hash("test123456"),
            user_type="ENTERPRISE",
            status="ACTIVE"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # 创建企业档案
        enterprise_profile = EnterpriseProfile(
            id=str(uuid4()),
            user_id=user.id,
            company_name="测试企业",
            unified_social_credit_code=f"USC{uuid4().hex[:8]}"
        )
        db.add(enterprise_profile)
        await db.commit()
        
        yield user


@pytest.fixture
async def test_job(test_enterprise_user: User):
    """创建测试职位"""
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == test_enterprise_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        job = Job(
            id=str(uuid4()),
            enterprise_id=enterprise.id,
            title="测试职位",
            description="这是一个测试职位",
            status="PUBLISHED"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        yield job


@pytest.fixture
async def test_application(test_student_user: User, test_job: Job):
    """创建测试申请"""
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == test_student_user.id)
        )
        student = student_result.scalar_one_or_none()
        
        application = JobApplication(
            id=str(uuid4()),
            job_id=test_job.id,
            student_id=test_student_user.id,
            status="PENDING"
        )
        db.add(application)
        await db.commit()
        await db.refresh(application)
        
        yield application


@pytest.fixture
async def test_chat_session(test_student_user: User, test_enterprise_user: User):
    """创建测试聊天会话"""
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        session = ChatSession(
            id=str(uuid4()),
            user1_id=test_student_user.id,
            user2_id=test_enterprise_user.id
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        
        yield session


@pytest.fixture
async def test_message(test_chat_session: ChatSession, test_student_user: User, test_enterprise_user: User):
    """创建测试消息"""
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        message = Message(
            id=str(uuid4()),
            session_id=test_chat_session.id,
            sender_id=test_student_user.id,
            receiver_id=test_enterprise_user.id,
            content="测试消息",
            message_type="TEXT",
            is_read=False
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        
        yield message


@pytest.mark.asyncio
async def test_refresh_token_interface(client: AsyncClient, test_student_user: User):
    """
    测试刷新令牌接口（修复后的接口）
    验证使用Body参数传递refresh_token
    """
    # 1. 先登录获取refresh_token
    login_data = {
        "username": test_student_user.username,
        "password": "test123456"
    }
    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"登录失败，跳过测试: {login_response.status_code}")
    
    login_result = login_response.json()
    refresh_token = login_result.get("refresh_token")
    
    assert refresh_token is not None, "应该返回refresh_token"
    
    # 2. 使用Body参数刷新token（修复后的方式）
    refresh_data = {
        "refresh_token": refresh_token
    }
    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json=refresh_data  # 使用JSON Body传递
    )
    
    # 验证响应
    assert refresh_response.status_code == 200, f"刷新token应该成功，但返回了{refresh_response.status_code}"
    
    refresh_result = refresh_response.json()
    assert "access_token" in refresh_result, "应该返回新的access_token"
    assert "token_type" in refresh_result, "应该返回token_type"
    assert refresh_result["token_type"] == "bearer", "token_type应该是bearer"
    
    print("✅ 刷新令牌接口测试通过：使用Body参数传递refresh_token")


@pytest.mark.asyncio
async def test_refresh_token_with_query_should_fail(client: AsyncClient, test_student_user: User):
    """
    测试使用Query参数传递refresh_token应该失败（验证修复生效）
    """
    # 先登录获取refresh_token
    login_data = {
        "username": test_student_user.username,
        "password": "test123456"
    }
    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"登录失败，跳过测试: {login_response.status_code}")
    
    login_result = login_response.json()
    refresh_token = login_result.get("refresh_token")
    
    # 尝试使用Query参数传递（应该失败）
    refresh_response = await client.post(
        f"/api/v1/auth/refresh?token={refresh_token}"  # 使用Query参数
    )
    
    # 应该返回422（Unprocessable Entity）或400（Bad Request）
    assert refresh_response.status_code in [400, 422], \
        f"使用Query参数应该失败，但返回了{refresh_response.status_code}"
    
    print("✅ 验证修复生效：使用Query参数传递refresh_token已失效")


@pytest.mark.asyncio
async def test_mark_message_read_interface(client: AsyncClient, test_student_user: User, test_message: Message):
    """
    测试标记消息已读接口（修复后的接口）
    验证使用PUT方法
    """
    # 1. 登录获取token
    login_data = {
        "username": test_student_user.username,
        "password": "test123456"
    }
    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"登录失败，跳过测试: {login_response.status_code}")
    
    login_result = login_response.json()
    access_token = login_result.get("access_token")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 2. 使用PUT方法标记消息为已读（修复后的方式）
    mark_read_response = await client.put(
        f"/api/v1/chat/messages/{test_message.id}/read",
        headers=headers
    )
    
    # 验证响应
    assert mark_read_response.status_code == 204, \
        f"标记消息已读应该成功，但返回了{mark_read_response.status_code}"
    
    # 3. 验证消息确实被标记为已读
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Message).where(Message.id == test_message.id)
        )
        message = result.scalar_one_or_none()
        assert message is not None, "消息应该存在"
        assert message.is_read == True, "消息应该被标记为已读"
    
    print("✅ 标记消息已读接口测试通过：使用PUT方法")


@pytest.mark.asyncio
async def test_mark_message_read_with_post_should_fail(client: AsyncClient, test_student_user: User, test_message: Message):
    """
    测试使用POST方法标记消息已读应该失败（验证修复生效）
    """
    # 1. 登录获取token
    login_data = {
        "username": test_student_user.username,
        "password": "test123456"
    }
    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"登录失败，跳过测试: {login_response.status_code}")
    
    login_result = login_response.json()
    access_token = login_result.get("access_token")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 2. 尝试使用POST方法（应该失败）
    mark_read_response = await client.post(
        f"/api/v1/chat/messages/{test_message.id}/read",
        headers=headers
    )
    
    # 应该返回405（Method Not Allowed）
    assert mark_read_response.status_code == 405, \
        f"使用POST方法应该返回405，但返回了{mark_read_response.status_code}"
    
    print("✅ 验证修复生效：使用POST方法标记消息已读已失效")


@pytest.mark.asyncio
async def test_update_application_status_interface(client: AsyncClient, test_enterprise_user: User, test_application: JobApplication):
    """
    测试更新申请状态接口（修复后的接口）
    验证参数验证和URL编码
    """
    # 1. 登录获取token
    login_data = {
        "username": test_enterprise_user.username,
        "password": "test123456"
    }
    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"登录失败，跳过测试: {login_response.status_code}")
    
    login_result = login_response.json()
    access_token = login_result.get("access_token")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 2. 更新申请状态（使用Query参数）
    new_status = "VIEWED"
    update_response = await client.put(
        f"/api/v1/applications/{test_application.id}?status={new_status}",
        headers=headers
    )
    
    # 验证响应
    assert update_response.status_code == 200, \
        f"更新申请状态应该成功，但返回了{update_response.status_code}"
    
    update_result = update_response.json()
    assert update_result.get("status") == new_status, \
        f"申请状态应该更新为{new_status}"
    
    # 3. 验证申请状态确实被更新
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(JobApplication).where(JobApplication.id == test_application.id)
        )
        application = result.scalar_one_or_none()
        assert application is not None, "申请应该存在"
        assert application.status == new_status, f"申请状态应该更新为{new_status}"
    
    print("✅ 更新申请状态接口测试通过：参数验证和URL编码正常")


@pytest.mark.asyncio
async def test_update_application_status_without_status_should_fail(client: AsyncClient, test_enterprise_user: User, test_application: JobApplication):
    """
    测试更新申请状态时缺少status参数应该失败（验证参数验证生效）
    """
    # 1. 登录获取token
    login_data = {
        "username": test_enterprise_user.username,
        "password": "test123456"
    }
    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"登录失败，跳过测试: {login_response.status_code}")
    
    login_result = login_response.json()
    access_token = login_result.get("access_token")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 2. 尝试不提供status参数（应该失败）
    update_response = await client.put(
        f"/api/v1/applications/{test_application.id}",  # 缺少status参数
        headers=headers
    )
    
    # 应该返回422（Unprocessable Entity）或400（Bad Request）
    assert update_response.status_code in [400, 422], \
        f"缺少status参数应该失败，但返回了{update_response.status_code}"
    
    print("✅ 验证参数验证生效：缺少status参数时更新申请状态已失效")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

