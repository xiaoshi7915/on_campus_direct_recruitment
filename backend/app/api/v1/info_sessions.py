"""
宣讲会相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from uuid import uuid4
import json

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
    # 注意：企业用户调用此API时，应该通过"浏览宣讲会"模式来查看所有宣讲会
    # 而"我的报名"应该通过/my-registrations接口来获取报名的宣讲会
    # 这里不再自动过滤企业创建的宣讲会，因为前端有专门的"浏览宣讲会"和"我的报名"按钮
    if enterprise_id:
        query = query.where(InfoSession.enterprise_id == enterprise_id)
    
    # 状态过滤
    if status_filter:
        query = query.where(InfoSession.status == status_filter)
    elif status_filter is None:
        # 如果未指定状态过滤，根据用户类型决定
        # 教师可以看到所有状态，企业用户和学生只能看到已发布的
        if current_user and current_user.user_type == "TEACHER":
            # 教师可以看到所有状态，不添加状态过滤
            pass
        else:
            # 企业用户、未登录用户和学生只能看到已发布的宣讲会
            # 企业用户可以通过/my-created接口查看自己创建的所有状态的宣讲会
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


@router.get("/my-registrations", response_model=InfoSessionListResponse)
async def get_my_info_session_registrations(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业报名的宣讲会列表（仅企业用户）
    
    Args:
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        InfoSessionListResponse: 宣讲会列表
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看报名的宣讲会"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 获取企业报名的宣讲会ID列表（通过InfoSessionRegistration查找企业邀请的宣讲会）
    # 注意：企业报名的宣讲会实际上是企业被邀请参加的宣讲会
    # 这里需要查找企业作为参与者（通过enterprise_id字段）的宣讲会
    # 但InfoSessionRegistration只有student_id，没有enterprise_id
    # 所以企业报名的宣讲会应该是企业创建的宣讲会
    # 根据需求，企业只能查看自己报名的宣讲会，这里理解为企业创建的宣讲会
    
    # 获取企业创建的宣讲会ID列表（主账号和子账号）
    from app.services.enterprise_service import get_enterprise_ids_for_query
    enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
    
    query = select(InfoSession).where(InfoSession.enterprise_id.in_(enterprise_ids))
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页
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


@router.get("/my-created", response_model=InfoSessionListResponse)
async def get_my_created_info_sessions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业创建的宣讲会列表（仅企业用户）
    
    Args:
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        InfoSessionListResponse: 宣讲会列表
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看创建的宣讲会"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 获取企业创建的宣讲会ID列表（主账号和子账号）
    from app.services.enterprise_service import get_enterprise_ids_for_query
    enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
    
    query = select(InfoSession).where(InfoSession.enterprise_id.in_(enterprise_ids))
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页
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


@router.get("/search-students", response_model=dict)
async def search_students_for_invite(
    keyword: Optional[str] = Query(None, description="关键词搜索（姓名、学号）"),
    department_id: Optional[str] = Query(None, description="院系ID"),
    grade: Optional[str] = Query(None, description="年级"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    搜索学生（供企业邀请宣讲会使用）
    
    Args:
        keyword: 关键词搜索
        department_id: 院系ID
        grade: 年级
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        dict: 学生列表
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能搜索学生"
        )
    
    from app.models.profile import StudentProfile
    
    # 构建查询
    query = select(StudentProfile)
    
    # 关键词搜索
    if keyword:
        query = query.where(
            or_(
                StudentProfile.real_name.contains(keyword),
                StudentProfile.student_id.contains(keyword)
            )
        )
    
    # 院系过滤
    if department_id:
        query = query.where(StudentProfile.department_id == department_id)
    
    # 年级过滤
    if grade:
        query = query.where(StudentProfile.grade == grade)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页
    offset = (page - 1) * page_size
    query = query.order_by(StudentProfile.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    students = result.scalars().all()
    
    # 构建响应
    student_list = []
    for student in students:
        student_list.append({
            "id": student.id,
            "real_name": student.real_name,
            "student_id": student.student_id,
            "grade": student.grade,
            "major": student.major,
            "department_id": student.department_id,
        })
    
    return {
        "items": student_list,
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
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    
    # 教师和企业都可以创建宣讲会，但教师子账号不能创建
    if current_user.user_type == "TEACHER":
        has_permission = await check_permission(current_user, "info_session:create", db)
    elif current_user.user_type == "ENTERPRISE":
        has_permission = await check_permission(current_user, "info_session:create", db)
    else:
        has_permission = False
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师主账号或企业用户才能创建宣讲会"
        )
    
    # 如果是企业用户，获取企业信息（子账号创建时使用主账号ID）
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
        # 子账号创建时使用主账号ID，主账号使用自己的ID
        from app.services.enterprise_service import get_effective_enterprise_id
        enterprise_id = await get_effective_enterprise_id(db, enterprise)
    
    # 创建宣讲会
    # 如果是教师创建，状态设为PENDING等待审批；如果是企业创建，状态设为DRAFT
    initial_status = "PENDING" if current_user.user_type == "TEACHER" else "DRAFT"
    
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
        status=initial_status
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
    
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "info_session:update", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此宣讲会"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("info_session", session_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此宣讲会"
        )
    
    # 更新宣讲会信息
    update_data = session_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "materials":
            # 处理materials字段（将list转换为JSON字符串）
            if value is not None:
                setattr(info_session, field, json.dumps(value, ensure_ascii=False))
            else:
                setattr(info_session, field, None)
        else:
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
    
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "info_session:delete", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此宣讲会"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("info_session", session_id, current_user, db, "delete")
    if not has_access:
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
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="企业信息不存在"
            )
        # 检查权限（主账号和子账号都可以查看主账号创建的宣讲会报名）
        from app.services.enterprise_service import get_effective_enterprise_id
        effective_enterprise_id = await get_effective_enterprise_id(db, enterprise)
        if info_session.enterprise_id != effective_enterprise_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此宣讲会的报名信息"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此宣讲会的报名信息"
        )
    
    # 获取报名列表，并关联学生信息
    result = await db.execute(
        select(InfoSessionRegistration, StudentProfile)
        .join(StudentProfile, InfoSessionRegistration.student_id == StudentProfile.id)
        .where(InfoSessionRegistration.session_id == session_id)
    )
    rows = result.all()
    
    # 构建响应列表
    registration_list = []
    for registration, student in rows:
        registration_dict = {
            "id": registration.id,
            "session_id": registration.session_id,
            "student_id": registration.student_id,
            "student_name": student.real_name if student else None,
            "student_detail": {
                "id": student.id if student else None,
                "name": student.real_name if student else None,
                "student_id": student.student_id if student else None,
                "major": student.major if student else None,
                "grade": student.grade if student else None,
            } if student else None,
            "status": registration.status,
            "check_in_time": registration.check_in_time,
            "created_at": registration.created_at,
        }
        registration_list.append(InfoSessionRegistrationResponse(**registration_dict))
    
    return registration_list


@router.post("/{session_id}/invite-student", response_model=InfoSessionRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def invite_student_to_info_session(
    session_id: str,
    student_id: Optional[str] = Query(None, description="学生ID"),
    user_id: Optional[str] = Query(None, description="用户ID（如果提供，将转换为student_id）"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    邀请学生参加宣讲会（企业用户）
    
    Args:
        session_id: 宣讲会ID
        student_id: 学生ID（可选）
        user_id: 用户ID（可选，如果提供将转换为student_id）
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        InfoSessionRegistrationResponse: 创建的报名记录
        
    Raises:
        HTTPException: 如果宣讲会不存在、无权邀请或学生已报名
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能邀请学生"
        )
    
    # 如果提供了user_id，转换为student_id
    actual_student_id = student_id
    if user_id and not student_id:
        from app.models.profile import StudentProfile
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == user_id)
        )
        student_profile = student_result.scalar_one_or_none()
        if student_profile:
            actual_student_id = student_profile.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="该用户不是学生或学生档案不存在"
            )
    
    if not actual_student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供student_id或user_id"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 检查宣讲会是否存在
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"邀请学生 - session_id: {session_id}, student_id: {actual_student_id}, enterprise_id: {enterprise.id}, is_main_account: {enterprise.is_main_account}, main_account_id: {enterprise.main_account_id}")
    
    session_result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = session_result.scalar_one_or_none()
    
    if not info_session:
        # 尝试查询所有宣讲会，看看是否有ID匹配的问题
        all_sessions_result = await db.execute(select(InfoSession).limit(10))
        all_sessions = all_sessions_result.scalars().all()
        logger.warning(f"宣讲会不存在 - session_id: {session_id}, 数据库中前10个宣讲会IDs: {[s.id for s in all_sessions]}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"宣讲会不存在（session_id: {session_id}）"
        )
    
    logger.info(f"找到宣讲会 - session_id: {session_id}, enterprise_id: {info_session.enterprise_id}")
    
    # 检查权限（主账号和子账号都可以邀请主账号创建的宣讲会）
    from app.services.enterprise_service import get_effective_enterprise_id
    effective_enterprise_id = await get_effective_enterprise_id(db, enterprise)
    logger.info(f"权限检查 - 宣讲会企业ID: {info_session.enterprise_id}, 当前企业有效ID: {effective_enterprise_id}")
    
    if info_session.enterprise_id != effective_enterprise_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"无权邀请学生参加此宣讲会（宣讲会企业ID: {info_session.enterprise_id}, 当前企业有效ID: {effective_enterprise_id}）"
        )
    
    # 检查学生是否存在
    student_result = await db.execute(select(StudentProfile).where(StudentProfile.id == actual_student_id))
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    # 检查是否已报名
    existing_result = await db.execute(
        select(InfoSessionRegistration).where(
            InfoSessionRegistration.session_id == session_id,
            InfoSessionRegistration.student_id == actual_student_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该学生已报名此宣讲会"
        )
    
    # 创建报名记录（邀请状态为ACCEPTED）
    registration = InfoSessionRegistration(
        id=str(uuid4()),
        session_id=session_id,
        student_id=actual_student_id,
        status="ACCEPTED"  # 邀请自动接受
    )
    
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    
    # 构建响应
    registration_dict = {
        "id": registration.id,
        "session_id": registration.session_id,
        "student_id": registration.student_id,
        "student_name": student.real_name if student else None,
        "student_detail": {
            "id": student.id if student else None,
            "real_name": student.real_name if student else None,
            "major": student.major if student else None,
            "education": student.education if student else None,
            "graduation_year": student.graduation_year if student else None,
        } if student else None,
        "status": registration.status,
        "check_in_time": registration.check_in_time,
        "created_at": registration.created_at,
    }
    
    return InfoSessionRegistrationResponse(**registration_dict)


class BatchInviteRequest(BaseModel):
    student_ids: list[str]


@router.post("/{session_id}/invite-students-batch", response_model=dict)
async def invite_students_batch(
    session_id: str,
    request_data: BatchInviteRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    批量邀请学生参加宣讲会
    
    Args:
        session_id: 宣讲会ID
        student_ids: 学生ID列表
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        dict: 邀请结果
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能邀请学生"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 检查宣讲会是否存在
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"批量邀请学生 - session_id: {session_id}, enterprise_id: {enterprise.id}, is_main_account: {enterprise.is_main_account}, main_account_id: {enterprise.main_account_id}, student_ids: {request_data.student_ids}")
    
    session_result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = session_result.scalar_one_or_none()
    
    if not info_session:
        # 尝试查询所有宣讲会，看看是否有ID匹配的问题
        all_sessions_result = await db.execute(select(InfoSession).limit(10))
        all_sessions = all_sessions_result.scalars().all()
        logger.warning(f"宣讲会不存在 - session_id: {session_id}, 数据库中前10个宣讲会IDs: {[s.id for s in all_sessions]}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"宣讲会不存在（session_id: {session_id}）"
        )
    
    logger.info(f"找到宣讲会 - session_id: {session_id}, enterprise_id: {info_session.enterprise_id}")
    
    # 检查权限（主账号和子账号都可以邀请主账号创建的宣讲会）
    from app.services.enterprise_service import get_effective_enterprise_id
    effective_enterprise_id = await get_effective_enterprise_id(db, enterprise)
    logger.info(f"权限检查 - 宣讲会企业ID: {info_session.enterprise_id}, 当前企业有效ID: {effective_enterprise_id}")
    
    if info_session.enterprise_id != effective_enterprise_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"无权邀请学生参加此宣讲会（宣讲会企业ID: {info_session.enterprise_id}, 当前企业有效ID: {effective_enterprise_id}）"
        )
    
    success_count = 0
    failed_count = 0
    failed_reasons = []
    
    for student_id in request_data.student_ids:
        try:
            # 检查学生是否存在
            student_result = await db.execute(select(StudentProfile).where(StudentProfile.id == student_id))
            student = student_result.scalar_one_or_none()
            
            if not student:
                failed_count += 1
                failed_reasons.append(f"学生ID {student_id} 不存在")
                continue
            
            # 检查是否已报名
            existing_result = await db.execute(
                select(InfoSessionRegistration).where(
                    InfoSessionRegistration.session_id == session_id,
                    InfoSessionRegistration.student_id == student_id
                )
            )
            existing = existing_result.scalar_one_or_none()
            
            if existing:
                failed_count += 1
                failed_reasons.append(f"学生 {student.real_name} 已报名")
                continue
            
            # 创建报名记录
            registration = InfoSessionRegistration(
                id=str(uuid4()),
                session_id=session_id,
                student_id=student_id,
                status="ACCEPTED"
            )
            
            db.add(registration)
            success_count += 1
        except Exception as e:
            failed_count += 1
            failed_reasons.append(f"学生ID {student_id}: {str(e)}")
    
    await db.commit()
    
    return {
        "success_count": success_count,
        "failed_count": failed_count,
        "failed_reasons": failed_reasons
    }


