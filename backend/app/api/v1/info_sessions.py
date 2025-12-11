"""
宣讲会相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.activity import InfoSession, InfoSessionRegistration
from app.models.profile import EnterpriseProfile, StudentProfile
from app.schemas.activity import (
    InfoSessionCreate, InfoSessionUpdate, InfoSessionResponse, InfoSessionListResponse,
    InfoSessionRegistrationCreate, InfoSessionRegistrationResponse
)

router = APIRouter()


@router.get("", response_model=InfoSessionListResponse)
async def get_info_sessions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    school_id: Optional[str] = Query(None, description="学校ID"),
    enterprise_id: Optional[str] = Query(None, description="企业ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    获取宣讲会列表
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词
        school_id: 学校ID
        enterprise_id: 企业ID
        status_filter: 状态过滤
        current_user: 当前登录用户（可选）
        db: 数据库会话
        
    Returns:
        InfoSessionListResponse: 宣讲会列表
    """
    # 构建查询
    query = select(InfoSession)
    
    # 关键词搜索
    if keyword:
        query = query.where(
            or_(
                InfoSession.title.contains(keyword),
                InfoSession.description.contains(keyword)
            )
        )
    
    # 学校过滤
    if school_id:
        query = query.where(InfoSession.school_id == school_id)
    
    # 企业过滤
    if enterprise_id:
        query = query.where(InfoSession.enterprise_id == enterprise_id)
    
    # 状态过滤
    if status_filter:
        query = query.where(InfoSession.status == status_filter)
    elif status_filter is None:
        # 如果未指定状态过滤，根据用户类型决定
        # 教师和企业用户可以看到所有状态，未登录用户和学生只能看到已发布的
        if current_user and current_user.user_type in ["TEACHER", "ENTERPRISE"]:
            # 教师和企业用户可以看到所有状态，不添加状态过滤
            pass
        else:
            # 未登录用户和学生只能看到已发布的宣讲会
            query = query.where(InfoSession.status == "PUBLISHED")
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(InfoSession.start_time.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    info_sessions = result.scalars().all()
    
    # 将ORM对象转换为响应模型
    info_session_responses = [InfoSessionResponse.model_validate(session) for session in info_sessions]
    
    return {
        "items": info_session_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{session_id}", response_model=InfoSessionResponse)
async def get_info_session(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取宣讲会详情
    
    Args:
        session_id: 宣讲会ID
        db: 数据库会话
        
    Returns:
        InfoSessionResponse: 宣讲会详情
        
    Raises:
        HTTPException: 如果宣讲会不存在
    """
    result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = result.scalar_one_or_none()
    
    if not info_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宣讲会不存在"
        )
    
    return info_session


@router.post("", response_model=InfoSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_info_session(
    session_data: InfoSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建宣讲会（仅企业用户）
    
    Args:
        session_data: 宣讲会数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        InfoSessionResponse: 创建的宣讲会
        
    Raises:
        HTTPException: 如果用户不是企业
    """
    # 检查用户类型（教师或企业）
    if current_user.user_type not in ["TEACHER", "ENTERPRISE"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师或企业用户才能创建宣讲会"
        )
    
    # 如果是企业用户，获取企业信息
    enterprise_id = None
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="企业信息不存在，请先完善企业信息"
            )
        enterprise_id = enterprise.id
    
    # 创建宣讲会
    info_session = InfoSession(
        id=str(uuid4()),
        enterprise_id=enterprise_id,
        title=session_data.title,
        description=session_data.description,
        start_time=session_data.start_time,
        end_time=session_data.end_time,
        location=session_data.location,
        session_type=session_data.session_type,
        live_url=session_data.live_url,
        school_id=session_data.school_id,
        max_students=session_data.max_students,
        status="DRAFT"
    )
    
    db.add(info_session)
    await db.commit()
    await db.refresh(info_session)
    
    return info_session


@router.put("/{session_id}", response_model=InfoSessionResponse)
async def update_info_session(
    session_id: str,
    session_data: InfoSessionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新宣讲会（教师或企业用户）
    
    Args:
        session_id: 宣讲会ID
        session_data: 更新的宣讲会数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        InfoSessionResponse: 更新后的宣讲会
        
    Raises:
        HTTPException: 如果宣讲会不存在或无权修改
    """
    # 获取宣讲会
    result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = result.scalar_one_or_none()
    
    if not info_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宣讲会不存在"
        )
    
    # 检查权限
    if current_user.user_type == "TEACHER":
        # 教师可以修改所有宣讲会
        pass
    elif current_user.user_type == "ENTERPRISE":
        # 企业只能修改自己企业的宣讲会
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="企业信息不存在"
            )
        
        if info_session.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此宣讲会"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此宣讲会"
        )
    
    # 更新宣讲会信息
    update_data = session_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(info_session, field, value)
    
    await db.commit()
    await db.refresh(info_session)
    
    return info_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_info_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除宣讲会（教师或企业用户）
    
    Args:
        session_id: 宣讲会ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果宣讲会不存在或无权删除
    """
    # 获取宣讲会
    result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = result.scalar_one_or_none()
    
    if not info_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宣讲会不存在"
        )
    
    # 检查权限
    if current_user.user_type == "TEACHER":
        # 教师可以删除所有宣讲会
        pass
    elif current_user.user_type == "ENTERPRISE":
        # 企业只能删除自己企业的宣讲会
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="企业信息不存在"
            )
        
        if info_session.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此宣讲会"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此宣讲会"
        )
    
    await db.delete(info_session)
    await db.commit()


# ==================== 宣讲会报名相关 ====================

@router.post("/{session_id}/register", response_model=InfoSessionRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_info_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    学生报名参加宣讲会
    
    Args:
        session_id: 宣讲会ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        InfoSessionRegistrationResponse: 报名信息
        
    Raises:
        HTTPException: 如果用户不是学生、宣讲会不存在或已报名
    """
    # 检查用户类型
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能报名宣讲会"
        )
    
    # 获取学生信息
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生信息不存在，请先完善学生信息"
        )
    
    # 检查宣讲会是否存在
    session_result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = session_result.scalar_one_or_none()
    
    if not info_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宣讲会不存在"
        )
    
    # 检查是否已报名
    existing_result = await db.execute(
        select(InfoSessionRegistration).where(
            InfoSessionRegistration.session_id == session_id,
            InfoSessionRegistration.student_id == student.id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="已报名此宣讲会"
        )
    
    # 检查人数限制
    if info_session.max_students:
        registration_count_result = await db.execute(
            select(func.count()).select_from(
                select(InfoSessionRegistration).where(
                    InfoSessionRegistration.session_id == session_id,
                    InfoSessionRegistration.status == "CONFIRMED"
                ).subquery()
            )
        )
        registration_count = registration_count_result.scalar() or 0
        if registration_count >= info_session.max_students:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="宣讲会报名人数已满"
            )
    
    # 创建报名记录
    registration = InfoSessionRegistration(
        id=str(uuid4()),
        session_id=session_id,
        student_id=student.id,
        status="PENDING"
    )
    
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    
    return registration


@router.get("/{session_id}/registrations", response_model=list[InfoSessionRegistrationResponse])
async def get_info_session_registrations(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取宣讲会报名列表（仅企业可查看自己创建的宣讲会报名）
    
    Args:
        session_id: 宣讲会ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        list[InfoSessionRegistrationResponse]: 报名列表
    """
    # 检查宣讲会是否存在
    session_result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = session_result.scalar_one_or_none()
    
    if not info_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宣讲会不存在"
        )
    
    # 检查权限（企业可查看自己创建的宣讲会报名，教师可查看所有）
    if current_user.user_type == "TEACHER":
        # 教师可以查看所有宣讲会的报名
        pass
    elif current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if not enterprise or info_session.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此宣讲会的报名信息"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此宣讲会的报名信息"
        )
    
    # 获取报名列表
    result = await db.execute(
        select(InfoSessionRegistration).where(InfoSessionRegistration.session_id == session_id)
    )
    registrations = result.scalars().all()
    
    return registrations


