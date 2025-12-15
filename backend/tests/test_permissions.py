"""
权限测试用例
测试权限检查机制、子账号权限限制、数据权限隔离等
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.job import Job, JobApplication, Resume
from app.models.profile import StudentProfile, EnterpriseProfile, TeacherProfile
from app.models.interview import Interview, Offer
from app.core.security import get_password_hash, create_access_token
from app.core.permissions import (
    check_permission,
    check_resource_access,
    ROLE_PERMISSIONS,
    ENTERPRISE_SUB_ACCOUNT_RESTRICTIONS,
    TEACHER_SUB_ACCOUNT_RESTRICTIONS
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from app.models.user_type import UserType


@pytest.fixture
async def client():
    """创建测试客户端"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def db():
    """数据库会话"""
    async for session in get_db():
        yield session


@pytest.fixture
async def test_student_user(db: AsyncSession):
    """创建测试学生用户"""
    user = User(
        id=str(uuid4()),
        username=f"test_student_{uuid4().hex[:8]}",
        password_hash=get_password_hash("test123456"),
        user_type=UserType.STUDENT,
        status="ACTIVE"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    student = StudentProfile(
        id=str(uuid4()),
        user_id=user.id,
        real_name="测试学生",
        student_id="2021001"
    )
    db.add(student)
    await db.commit()
    
    return user


@pytest.fixture
async def test_enterprise_main_user(db: AsyncSession):
    """创建测试企业主账号"""
    user = User(
        id=str(uuid4()),
        username=f"test_enterprise_main_{uuid4().hex[:8]}",
        password_hash=get_password_hash("test123456"),
        user_type=UserType.ENTERPRISE,
        status="ACTIVE"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    enterprise = EnterpriseProfile(
        id=str(uuid4()),
        user_id=user.id,
        company_name="测试企业",
        is_main_account=True
    )
    db.add(enterprise)
    await db.commit()
    
    return user


@pytest.fixture
async def test_enterprise_sub_user(db: AsyncSession, test_enterprise_main_user: User):
    """创建测试企业子账号"""
    main_enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == test_enterprise_main_user.id)
    )
    main_enterprise = main_enterprise_result.scalar_one_or_none()
    
    user = User(
        id=str(uuid4()),
        username=f"test_enterprise_sub_{uuid4().hex[:8]}",
        password_hash=get_password_hash("test123456"),
        user_type=UserType.ENTERPRISE,
        status="ACTIVE"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    enterprise = EnterpriseProfile(
        id=str(uuid4()),
        user_id=user.id,
        company_name=main_enterprise.company_name,
        is_main_account=False,
        main_account_id=main_enterprise.id
    )
    db.add(enterprise)
    await db.commit()
    
    return user


@pytest.fixture
async def test_teacher_main_user(db: AsyncSession):
    """创建测试教师主账号"""
    user = User(
        id=str(uuid4()),
        username=f"test_teacher_main_{uuid4().hex[:8]}",
        password_hash=get_password_hash("test123456"),
        user_type=UserType.TEACHER,
        status="ACTIVE"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    teacher = TeacherProfile(
        id=str(uuid4()),
        user_id=user.id,
        real_name="测试教师",
        is_main_account=True
    )
    db.add(teacher)
    await db.commit()
    
    return user


@pytest.fixture
async def test_admin_user(db: AsyncSession):
    """创建测试管理员用户"""
    user = User(
        id=str(uuid4()),
        username=f"test_admin_{uuid4().hex[:8]}",
        password_hash=get_password_hash("test123456"),
        user_type=UserType.ADMIN,
        status="ACTIVE"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@pytest.fixture
async def test_job(db: AsyncSession, test_enterprise_main_user: User):
    """创建测试职位"""
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == test_enterprise_main_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    job = Job(
        id=str(uuid4()),
        enterprise_id=enterprise.id,
        title="测试职位",
        status="PUBLISHED"
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    return job


@pytest.fixture
async def test_resume(db: AsyncSession, test_student_user: User):
    """创建测试简历"""
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == test_student_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    resume = Resume(
        id=str(uuid4()),
        student_id=student.id,
        title="测试简历"
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    
    return resume


# ==================== 权限检查测试 ====================

@pytest.mark.asyncio
async def test_student_permissions(db: AsyncSession, test_student_user: User):
    """测试学生权限"""
    # 学生应该有的权限
    assert await check_permission(test_student_user, "resume:create", db) == True
    assert await check_permission(test_student_user, "job:read", db) == True
    assert await check_permission(test_student_user, "job:apply", db) == True
    
    # 学生不应该有的权限
    assert await check_permission(test_student_user, "job:create", db) == False
    assert await check_permission(test_student_user, "job:delete", db) == False
    assert await check_permission(test_student_user, "student:read", db) == False


@pytest.mark.asyncio
async def test_enterprise_main_account_permissions(db: AsyncSession, test_enterprise_main_user: User):
    """测试企业主账号权限"""
    # 企业主账号应该有的权限
    assert await check_permission(test_enterprise_main_user, "job:create", db) == True
    assert await check_permission(test_enterprise_main_user, "job:delete", db) == True
    assert await check_permission(test_enterprise_main_user, "sub_account:create", db) == True
    
    # 企业主账号不应该有的权限
    assert await check_permission(test_enterprise_main_user, "student:read", db) == False
    assert await check_permission(test_enterprise_main_user, "job_fair:approve", db) == False


@pytest.mark.asyncio
async def test_enterprise_sub_account_restrictions(db: AsyncSession, test_enterprise_sub_user: User):
    """测试企业子账号权限限制"""
    # 企业子账号被限制的权限
    assert await check_permission(test_enterprise_sub_user, "job:create", db) == False
    assert await check_permission(test_enterprise_sub_user, "job:delete", db) == False
    assert await check_permission(test_enterprise_sub_user, "sub_account:create", db) == False
    
    # 企业子账号应该有的权限
    assert await check_permission(test_enterprise_sub_user, "job:read", db) == True
    assert await check_permission(test_enterprise_sub_user, "job:update", db) == True
    assert await check_permission(test_enterprise_sub_user, "application:read", db) == True


@pytest.mark.asyncio
async def test_teacher_sub_account_restrictions(db: AsyncSession, test_teacher_main_user: User):
    """测试教师子账号权限限制"""
    # 创建教师子账号
    main_teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == test_teacher_main_user.id)
    )
    main_teacher = main_teacher_result.scalar_one_or_none()
    
    sub_user = User(
        id=str(uuid4()),
        username=f"test_teacher_sub_{uuid4().hex[:8]}",
        password_hash=get_password_hash("test123456"),
        user_type=UserType.TEACHER,
        status="ACTIVE"
    )
    db.add(sub_user)
    await db.commit()
    await db.refresh(sub_user)
    
    sub_teacher = TeacherProfile(
        id=str(uuid4()),
        user_id=sub_user.id,
        real_name="测试教师子账号",
        is_main_account=False,
        main_account_id=main_teacher.id
    )
    db.add(sub_teacher)
    await db.commit()
    
    # 教师子账号被限制的权限
    assert await check_permission(sub_user, "job_fair:create", db) == False
    assert await check_permission(sub_user, "info_session:create", db) == False
    assert await check_permission(sub_user, "sub_account:create", db) == False
    assert await check_permission(sub_user, "permission:transfer", db) == False
    
    # 教师子账号应该有的权限
    assert await check_permission(sub_user, "student:read", db) == True
    assert await check_permission(sub_user, "student:comment", db) == True
    assert await check_permission(sub_user, "job_fair:approve", db) == True


@pytest.mark.asyncio
async def test_admin_permissions(db: AsyncSession, test_admin_user: User):
    """测试管理员权限"""
    # 管理员拥有所有权限
    assert await check_permission(test_admin_user, "job:create", db) == True
    assert await check_permission(test_admin_user, "student:read", db) == True
    assert await check_permission(test_admin_user, "job_fair:approve", db) == True
    assert await check_permission(test_admin_user, "any:permission", db) == True


# ==================== 资源权限检查测试 ====================

@pytest.mark.asyncio
async def test_resource_access_job(db: AsyncSession, test_student_user: User, test_enterprise_main_user: User, test_job: Job):
    """测试职位资源权限"""
    # 学生：只能查看已发布的职位
    assert await check_resource_access("job", test_job.id, test_student_user, db, "read") == True
    
    # 企业：可以操作自己的职位
    assert await check_resource_access("job", test_job.id, test_enterprise_main_user, db, "update") == True
    assert await check_resource_access("job", test_job.id, test_enterprise_main_user, db, "delete") == True


@pytest.mark.asyncio
async def test_resource_access_resume(db: AsyncSession, test_student_user: User, test_resume: Resume):
    """测试简历资源权限"""
    # 学生：只能操作自己的简历
    assert await check_resource_access("resume", test_resume.id, test_student_user, db, "read") == True
    assert await check_resource_access("resume", test_resume.id, test_student_user, db, "update") == True


@pytest.mark.asyncio
async def test_resource_access_application(
    db: AsyncSession,
    test_student_user: User,
    test_enterprise_main_user: User,
    test_job: Job
):
    """测试申请资源权限"""
    # 创建申请
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == test_student_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    application = JobApplication(
        id=str(uuid4()),
        job_id=test_job.id,
        student_id=test_student_user.id,
        resume_id=None,
        status="PENDING"
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    
    # 学生：只能操作自己的申请
    assert await check_resource_access("application", application.id, test_student_user, db, "read") == True
    
    # 企业：可以操作自己职位的申请
    assert await check_resource_access("application", application.id, test_enterprise_main_user, db, "read") == True
    assert await check_resource_access("application", application.id, test_enterprise_main_user, db, "update") == True


# ==================== API端点权限测试 ====================

@pytest.mark.asyncio
async def test_create_job_permission(client: AsyncClient, test_student_user: User, test_enterprise_main_user: User):
    """测试创建职位API权限"""
    # 学生不能创建职位
    student_token = create_access_token({"sub": test_student_user.username, "user_id": test_student_user.id})
    response = await client.post(
        "/api/v1/jobs",
        json={"title": "测试职位", "department": "技术部"},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 403
    
    # 企业主账号可以创建职位
    enterprise_token = create_access_token({"sub": test_enterprise_main_user.username, "user_id": test_enterprise_main_user.id})
    response = await client.post(
        "/api/v1/jobs",
        json={"title": "测试职位", "department": "技术部"},
        headers={"Authorization": f"Bearer {enterprise_token}"}
    )
    # 注意：这里可能会因为缺少企业信息而返回404，但权限检查应该通过
    assert response.status_code in [201, 404]  # 201成功，404可能是缺少企业信息


@pytest.mark.asyncio
async def test_create_resume_permission(client: AsyncClient, test_student_user: User, test_enterprise_main_user: User):
    """测试创建简历API权限"""
    # 企业不能创建简历
    enterprise_token = create_access_token({"sub": test_enterprise_main_user.username, "user_id": test_enterprise_main_user.id})
    response = await client.post(
        "/api/v1/resumes",
        json={"title": "测试简历"},
        headers={"Authorization": f"Bearer {enterprise_token}"}
    )
    assert response.status_code == 403
    
    # 学生可以创建简历
    student_token = create_access_token({"sub": test_student_user.username, "user_id": test_student_user.id})
    response = await client.post(
        "/api/v1/resumes",
        json={"title": "测试简历"},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    # 注意：这里可能会因为缺少学生信息而返回404，但权限检查应该通过
    assert response.status_code in [201, 404]  # 201成功，404可能是缺少学生信息


# ==================== 资源权限检查扩展测试 ====================

@pytest.mark.asyncio
async def test_resource_access_job_fair(
    db: AsyncSession,
    test_student_user: User,
    test_enterprise_main_user: User,
    test_teacher_main_user: User
):
    """测试双选会资源权限"""
    from app.models.activity import JobFair
    from app.models.profile import EnterpriseProfile, TeacherProfile
    
    # 创建企业档案
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == test_enterprise_main_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    # 创建双选会
    job_fair = JobFair(
        id=str(uuid4()),
        title="测试双选会",
        status="PUBLISHED",
        created_by=enterprise.id if enterprise else None
    )
    db.add(job_fair)
    await db.commit()
    await db.refresh(job_fair)
    
    # 学生：只能查看已发布的双选会
    assert await check_resource_access("job_fair", job_fair.id, test_student_user, db, "read") == True
    
    # 企业：可以操作自己创建的双选会
    if enterprise:
        assert await check_resource_access("job_fair", job_fair.id, test_enterprise_main_user, db, "update") == True


@pytest.mark.asyncio
async def test_resource_access_schedule(
    db: AsyncSession,
    test_student_user: User,
    test_enterprise_main_user: User
):
    """测试日程资源权限"""
    from app.models.common import Schedule
    
    # 创建学生日程
    schedule = Schedule(
        id=str(uuid4()),
        user_id=test_student_user.id,
        title="测试日程",
        start_time=datetime.now(),
        schedule_type="OTHER"
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    
    # 学生：可以操作自己的日程
    assert await check_resource_access("schedule", schedule.id, test_student_user, db, "read") == True
    assert await check_resource_access("schedule", schedule.id, test_student_user, db, "update") == True
    
    # 企业：不能操作学生的日程
    assert await check_resource_access("schedule", schedule.id, test_enterprise_main_user, db, "read") == False


@pytest.mark.asyncio
async def test_resource_access_info_session(
    db: AsyncSession,
    test_student_user: User,
    test_enterprise_main_user: User
):
    """测试宣讲会资源权限"""
    from app.models.activity import InfoSession
    from app.models.profile import EnterpriseProfile
    
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == test_enterprise_main_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    # 创建宣讲会
    info_session = InfoSession(
        id=str(uuid4()),
        enterprise_id=enterprise.id if enterprise else None,
        title="测试宣讲会",
        status="PUBLISHED"
    )
    db.add(info_session)
    await db.commit()
    await db.refresh(info_session)
    
    # 学生：只能查看已发布的宣讲会
    assert await check_resource_access("info_session", info_session.id, test_student_user, db, "read") == True
    
    # 企业：可以操作自己创建的宣讲会
    if enterprise:
        assert await check_resource_access("info_session", info_session.id, test_enterprise_main_user, db, "update") == True


@pytest.mark.asyncio
async def test_resource_access_favorite(
    db: AsyncSession,
    test_student_user: User,
    test_enterprise_main_user: User
):
    """测试收藏资源权限"""
    from app.models.common import Favorite
    
    # 创建学生收藏
    favorite = Favorite(
        id=str(uuid4()),
        user_id=test_student_user.id,
        target_type="JOB",
        target_id=str(uuid4())
    )
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    
    # 学生：可以操作自己的收藏
    assert await check_resource_access("favorite", favorite.id, test_student_user, db, "read") == True
    assert await check_resource_access("favorite", favorite.id, test_student_user, db, "delete") == True
    
    # 企业：不能操作学生的收藏
    assert await check_resource_access("favorite", favorite.id, test_enterprise_main_user, db, "read") == False


@pytest.mark.asyncio
async def test_resource_access_todo(
    db: AsyncSession,
    test_student_user: User,
    test_enterprise_main_user: User
):
    """测试待办事项资源权限"""
    from app.models.todo import Todo
    
    # 创建学生待办事项
    todo = Todo(
        id=str(uuid4()),
        user_id=test_student_user.id,
        title="测试待办",
        priority="MEDIUM"
    )
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    
    # 学生：可以操作自己的待办事项
    assert await check_resource_access("todo", todo.id, test_student_user, db, "read") == True
    assert await check_resource_access("todo", todo.id, test_student_user, db, "update") == True
    
    # 企业：不能操作学生的待办事项
    assert await check_resource_access("todo", todo.id, test_enterprise_main_user, db, "read") == False


@pytest.mark.asyncio
async def test_resource_access_mark(
    db: AsyncSession,
    test_enterprise_main_user: User,
    test_student_user: User
):
    """测试标记资源权限"""
    from app.models.mark import Mark
    
    # 创建企业标记
    mark = Mark(
        id=str(uuid4()),
        user_id=test_enterprise_main_user.id,
        target_type="RESUME",
        target_id=str(uuid4()),
        color="blue"
    )
    db.add(mark)
    await db.commit()
    await db.refresh(mark)
    
    # 企业：可以操作自己的标记
    assert await check_resource_access("mark", mark.id, test_enterprise_main_user, db, "read") == True
    assert await check_resource_access("mark", mark.id, test_enterprise_main_user, db, "update") == True
    
    # 学生：不能操作企业的标记
    assert await check_resource_access("mark", mark.id, test_student_user, db, "read") == False

