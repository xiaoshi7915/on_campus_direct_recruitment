"""
用户档案相关API路由（企业、学生、教师信息管理）
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.profile import StudentProfile, TeacherProfile, EnterpriseProfile
from app.schemas.profile import (
    StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse,
    EnterpriseProfileCreate, EnterpriseProfileUpdate, EnterpriseProfileResponse,
    TeacherProfileCreate, TeacherProfileUpdate, TeacherProfileResponse
)

router = APIRouter()


# ==================== 学生档案 ====================

# 注意：GET路由必须在POST路由之前定义，避免路由冲突
@router.get("/student/me", response_model=StudentProfileResponse)
async def get_my_student_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的学生档案
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StudentProfileResponse: 学生档案
    """
    return await _get_student_profile_logic(current_user, db)


@router.get("/student", response_model=StudentProfileResponse)  # 添加别名，兼容前端调用
async def get_student_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的学生档案（兼容接口）
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StudentProfileResponse: 学生档案
    """
    return await _get_student_profile_logic(current_user, db)


@router.post("/student", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_student_profile(
    profile_data: StudentProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建学生档案（仅学生用户）
    
    Args:
        profile_data: 学生档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StudentProfileResponse: 创建的学生档案
    """
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能创建学生档案"
        )
    
    # 检查是否已存在档案
    existing = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="学生档案已存在，请使用更新接口"
        )
    
    # 创建学生档案
    profile = StudentProfile(
        id=str(uuid4()),
        user_id=current_user.id,
        real_name=profile_data.real_name,
        student_id=profile_data.student_id,
        school_id=profile_data.school_id,
        department_id=profile_data.department_id,
        class_id=profile_data.class_id,
        grade=profile_data.grade,
        major=profile_data.major,
        avatar_url=profile_data.avatar_url
    )
    
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    
    return profile


async def _get_student_profile_logic(
    current_user: User,
    db: AsyncSession
):
    """获取学生档案的通用逻辑"""
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能查看学生档案"
        )
    
    result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生档案不存在"
        )
    
    return profile


async def _update_student_profile_logic(
    profile_data: StudentProfileUpdate,
    current_user: User,
    db: AsyncSession
):
    """更新学生档案的通用逻辑"""
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能更新学生档案"
        )
    
    result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生档案不存在"
        )
    
    # 更新档案信息
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile


@router.put("/student/me", response_model=StudentProfileResponse)
async def update_my_student_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户的学生档案
    
    Args:
        profile_data: 更新的学生档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StudentProfileResponse: 更新后的学生档案
    """
    return await _update_student_profile_logic(profile_data, current_user, db)


@router.put("/student", response_model=StudentProfileResponse)  # 添加别名，兼容前端调用
async def update_student_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户的学生档案（兼容接口）
    
    Args:
        profile_data: 更新的学生档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StudentProfileResponse: 更新后的学生档案
    """
    return await _update_student_profile_logic(profile_data, current_user, db)


# ==================== 企业档案 ====================

async def _get_enterprise_profile_logic(
    current_user: User,
    db: AsyncSession
):
    """获取企业档案的通用逻辑"""
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看企业档案"
        )
    
    result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业档案不存在"
        )
    
    return profile


# 注意：更具体的路由（/enterprise/me）必须在通用路由（/enterprise）之前定义
@router.get("/enterprise/me", response_model=EnterpriseProfileResponse)
async def get_my_enterprise_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的企业档案
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseProfileResponse: 企业档案
    """
    return await _get_enterprise_profile_logic(current_user, db)


@router.get("/enterprise", response_model=EnterpriseProfileResponse)  # 兼容前端调用
async def get_enterprise_profile_alias(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的企业档案（兼容接口）
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseProfileResponse: 企业档案
    """
    return await _get_enterprise_profile_logic(current_user, db)


@router.post("/enterprise", response_model=EnterpriseProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_enterprise_profile(
    profile_data: EnterpriseProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建企业档案（仅企业用户）
    
    Args:
        profile_data: 企业档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseProfileResponse: 创建的企业档案
    """
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能创建企业档案"
        )
    
    # 检查是否已存在档案
    existing = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="企业档案已存在，请使用更新接口"
        )
    
    # 创建企业档案
    profile = EnterpriseProfile(
        id=str(uuid4()),
        user_id=current_user.id,
        company_name=profile_data.company_name,
        unified_code=profile_data.unified_code,
        legal_person=profile_data.legal_person,
        industry=profile_data.industry,
        scale=profile_data.scale,
        address=profile_data.address,
        website=profile_data.website,
        logo_url=profile_data.logo_url,
        description=profile_data.description
    )
    
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    
    return profile


async def _update_enterprise_profile_logic(
    profile_data: EnterpriseProfileUpdate,
    current_user: User,
    db: AsyncSession
):
    """更新企业档案的通用逻辑"""
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能更新企业档案"
        )
    
    result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业档案不存在"
        )
    
    # 更新档案信息
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile


@router.put("/enterprise/me", response_model=EnterpriseProfileResponse)
async def update_my_enterprise_profile(
    profile_data: EnterpriseProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户的企业档案
    
    Args:
        profile_data: 更新的企业档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseProfileResponse: 更新后的企业档案
    """
    return await _update_enterprise_profile_logic(profile_data, current_user, db)


@router.put("/enterprise", response_model=EnterpriseProfileResponse)  # 添加兼容接口
async def update_enterprise_profile(
    profile_data: EnterpriseProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户的企业档案（兼容接口）
    
    Args:
        profile_data: 更新的企业档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseProfileResponse: 更新后的企业档案
    """
    return await _update_enterprise_profile_logic(profile_data, current_user, db)


# ==================== 教师档案 ====================

@router.post("/teacher", response_model=TeacherProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher_profile(
    profile_data: TeacherProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建教师档案（仅教师用户）
    
    Args:
        profile_data: 教师档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        TeacherProfileResponse: 创建的教师档案
    """
    if current_user.user_type != "TEACHER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师用户才能创建教师档案"
        )
    
    # 检查是否已存在档案
    existing = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="教师档案已存在，请使用更新接口"
        )
    
    # 创建教师档案
    # 将空字符串转换为None，避免外键约束错误
    school_id = profile_data.school_id if profile_data.school_id and profile_data.school_id.strip() else None
    department_id = profile_data.department_id if profile_data.department_id and profile_data.department_id.strip() else None
    
    profile = TeacherProfile(
        id=str(uuid4()),
        user_id=current_user.id,
        real_name=profile_data.real_name,
        school_id=school_id,
        department_id=department_id,
        title=profile_data.title,
        avatar_url=profile_data.avatar_url
    )
    
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    
    return profile


@router.get("/teacher", response_model=TeacherProfileResponse)  # 兼容前端调用，放在最前面
async def get_teacher_profile_alias(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的教师档案（兼容接口）
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        TeacherProfileResponse: 教师档案
    """
    return await get_my_teacher_profile(current_user, db)


@router.get("/teacher/me", response_model=TeacherProfileResponse)
async def get_my_teacher_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的教师档案
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        TeacherProfileResponse: 教师档案
    """
    if current_user.user_type != "TEACHER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师用户才能查看教师档案"
        )
    
    result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师档案不存在"
        )
    
    return profile


@router.put("/teacher/me", response_model=TeacherProfileResponse)
async def update_my_teacher_profile(
    profile_data: TeacherProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户的教师档案
    
    Args:
        profile_data: 更新的教师档案数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        TeacherProfileResponse: 更新后的教师档案
    """
    if current_user.user_type != "TEACHER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师用户才能更新教师档案"
        )
    
    result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师档案不存在"
        )
    
    # 更新档案信息
    update_data = profile_data.model_dump(exclude_unset=True)
    # 将空字符串转换为None，避免外键约束错误
    if 'school_id' in update_data:
        school_id_val = update_data['school_id']
        if not school_id_val or (isinstance(school_id_val, str) and not school_id_val.strip()):
            update_data['school_id'] = None
    if 'department_id' in update_data:
        dept_id_val = update_data['department_id']
        if not dept_id_val or (isinstance(dept_id_val, str) and not dept_id_val.strip()):
            update_data['department_id'] = None
    
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile


