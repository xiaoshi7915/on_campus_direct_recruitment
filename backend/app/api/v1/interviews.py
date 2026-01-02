"""
面试相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.interview import Interview, Offer
from app.models.job import JobApplication, Job
from app.models.profile import EnterpriseProfile, StudentProfile
from app.schemas.interview import (
    InterviewCreate, InterviewUpdate, InterviewResponse, InterviewListResponse,
    OfferCreate, OfferUpdate, OfferResponse, OfferListResponse
)

router = APIRouter()


# ==================== Offer管理API（必须在/{interview_id}之前定义）====================

@router.get("/offers", response_model=OfferListResponse)
async def get_offers(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    enterprise_id: Optional[str] = Query(None, description="企业ID"),
    student_id: Optional[str] = Query(None, description="学生ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取Offer列表
    
    Args:
        page: 页码
        page_size: 每页数量
        enterprise_id: 企业ID
        student_id: 学生ID
        status_filter: 状态过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        OfferListResponse: Offer列表
    """
    # 构建查询
    query = select(Offer)
    
    # 根据用户类型过滤
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if enterprise:
            query = query.where(Offer.enterprise_id == enterprise.id)
        else:
            # 企业档案不存在，返回空列表
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
    elif current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if student:
            query = query.where(Offer.student_id == student.id)
        else:
            # 学生档案不存在，返回空列表
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
    
    # 企业ID过滤（管理员可查看所有）
    if enterprise_id and current_user.user_type == "ADMIN":
        query = query.where(Offer.enterprise_id == enterprise_id)
    
    # 学生ID过滤（管理员可查看所有）
    if student_id and current_user.user_type == "ADMIN":
        query = query.where(Offer.student_id == student_id)
    
    # 状态过滤
    if status_filter:
        query = query.where(Offer.status == status_filter)
    
    # 计算总数
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar()
    
    # 分页
    offset = (page - 1) * page_size
    query = query.order_by(Offer.created_at.desc()).offset(offset).limit(page_size)
    
    # 执行查询
    result = await db.execute(query)
    offers = result.scalars().all()
    
    return {
        "items": offers,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("", response_model=InterviewListResponse)
async def get_interviews(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    enterprise_id: Optional[str] = Query(None, description="企业ID"),
    student_id: Optional[str] = Query(None, description="学生ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取面试列表
    
    Args:
        page: 页码
        page_size: 每页数量
        enterprise_id: 企业ID
        student_id: 学生ID
        status_filter: 状态过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        InterviewListResponse: 面试列表
    """
    # 构建查询
    query = select(Interview)
    
    # 根据用户类型过滤
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if enterprise:
            query = query.where(Interview.enterprise_id == enterprise.id)
        else:
            # 企业档案不存在，返回空列表
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
    elif current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if student:
            query = query.where(Interview.student_id == student.id)
        else:
            # 学生档案不存在，返回空列表
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
    
    # 企业ID过滤（管理员可查看所有）
    if enterprise_id and current_user.user_type == "ADMIN":
        query = query.where(Interview.enterprise_id == enterprise_id)
    
    # 学生ID过滤（管理员可查看所有）
    if student_id and current_user.user_type == "ADMIN":
        query = query.where(Interview.student_id == student_id)
    
    # 状态过滤
    if status_filter:
        query = query.where(Interview.status == status_filter)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Interview.scheduled_time.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    interviews = result.scalars().all()
    
    return {
        "items": interviews,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取面试详情
    
    Args:
        interview_id: 面试ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        InterviewResponse: 面试详情
        
    Raises:
        HTTPException: 如果面试不存在或无权查看
    """
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试不存在"
        )
    
    # 使用资源权限检查
    from app.core.permissions import check_resource_access
    has_access = await check_resource_access("interview", interview_id, current_user, db, "read")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此面试"
        )
    
    return interview


@router.post("", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
async def create_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建面试（仅企业用户）
    
    Args:
        interview_data: 面试数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        InterviewResponse: 创建的面试
        
    Raises:
        HTTPException: 如果用户不是企业或申请不存在
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "interview:create", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能创建面试"
        )
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能创建面试"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在，请先完善企业信息"
        )
    
    # 检查申请是否存在
    application_result = await db.execute(
        select(JobApplication).where(JobApplication.id == interview_data.application_id)
    )
    application = application_result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位申请不存在"
        )
    
    # 检查是否已有面试
    existing_result = await db.execute(
        select(Interview).where(Interview.application_id == interview_data.application_id)
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="该申请已有面试记录"
        )
    
    # 检查权限（只能为申请自己企业职位的学生创建面试）
    # JobApplication没有enterprise_id字段，需要通过job获取
    job_result = await db.execute(select(Job).where(Job.id == application.job_id))
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    if job.enterprise_id != enterprise.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权为此申请创建面试"
        )
    
    # 获取学生档案ID（JobApplication.student_id关联的是users.id，需要转换为student_profiles.id）
    student_profile_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == application.student_id)
    )
    student_profile = student_profile_result.scalar_one_or_none()
    
    if not student_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生档案不存在"
        )
    
    # 创建面试
    interview = Interview(
        id=str(uuid4()),
        application_id=interview_data.application_id,
        enterprise_id=enterprise.id,
        student_id=student_profile.id,  # 使用student_profiles.id而不是users.id
        interview_type=interview_data.interview_type,
        scheduled_time=interview_data.scheduled_time,
        duration=interview_data.duration,
        location=interview_data.location,
        meeting_url=interview_data.meeting_url,
        status="SCHEDULED"
    )
    
    db.add(interview)
    await db.commit()
    await db.refresh(interview)
    
    return interview


@router.put("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: str,
    interview_data: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新面试（企业或学生）
    
    Args:
        interview_id: 面试ID
        interview_data: 更新的面试数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        InterviewResponse: 更新后的面试
        
    Raises:
        HTTPException: 如果面试不存在或无权修改
    """
    # 获取面试
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试不存在"
        )
    
    # 检查权限
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if not enterprise or interview.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此面试"
            )
    elif current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if not student or interview.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此面试"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此面试"
        )
    
    # 更新面试信息
    update_data = interview_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(interview, field, value)
    
    await db.commit()
    await db.refresh(interview)
    
    return interview


# ==================== Offer管理API（续）====================

@router.get("/offers/{offer_id}", response_model=OfferResponse)
async def get_offer(
    offer_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取Offer详情
    
    Args:
        offer_id: Offer ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        OfferResponse: Offer详情
        
    Raises:
        HTTPException: 如果Offer不存在或无权查看
    """
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer不存在"
        )
    
    # 检查权限
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if not enterprise or offer.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此Offer"
            )
    elif current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if not student or offer.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此Offer"
            )
    
    return offer


@router.post("/offers", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
async def create_offer(
    offer_data: OfferCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建Offer（仅企业用户）
    
    Args:
        offer_data: Offer数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        OfferResponse: 创建的Offer
        
    Raises:
        HTTPException: 如果用户不是企业或申请不存在
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "offer:create", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能创建Offer"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在，请先完善企业信息"
        )
    
    # 检查申请是否存在
    application_result = await db.execute(
        select(JobApplication).where(JobApplication.id == offer_data.application_id)
    )
    application = application_result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位申请不存在"
        )
    
    # 检查是否已有Offer
    existing_result = await db.execute(
        select(Offer).where(Offer.application_id == offer_data.application_id)
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="该申请已有Offer记录"
        )
    
    # 检查权限（只能为申请自己企业职位的学生创建Offer）
    # JobApplication没有enterprise_id字段，需要通过job获取
    job_result = await db.execute(select(Job).where(Job.id == application.job_id))
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    if job.enterprise_id != enterprise.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权为此申请创建Offer"
        )
    
    # 获取学生档案ID（JobApplication.student_id关联的是users.id，需要转换为student_profiles.id）
    student_profile_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == application.student_id)
    )
    student_profile = student_profile_result.scalar_one_or_none()
    
    if not student_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生档案不存在"
        )
    
    # 创建Offer
    offer = Offer(
        id=str(uuid4()),
        application_id=offer_data.application_id,
        enterprise_id=enterprise.id,
        student_id=student_profile.id,  # 使用student_profiles.id而不是users.id
        job_title=offer_data.job_title,
        salary=offer_data.salary,
        start_date=offer_data.start_date,
        content=offer_data.content,
        status="PENDING",
        expires_at=offer_data.expires_at
    )
    
    db.add(offer)
    await db.commit()
    await db.refresh(offer)
    
    return offer


@router.put("/offers/{offer_id}", response_model=OfferResponse)
async def update_offer(
    offer_id: str,
    offer_data: OfferUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新Offer（企业或学生）
    
    Args:
        offer_id: Offer ID
        offer_data: 更新的Offer数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        OfferResponse: 更新后的Offer
        
    Raises:
        HTTPException: 如果Offer不存在或无权修改
    """
    # 获取Offer
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer不存在"
        )
    
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    # 企业可以更新，学生也可以更新（接受/拒绝）
    if current_user.user_type == "ENTERPRISE":
        has_permission = await check_permission(current_user, "offer:update", db)
    elif current_user.user_type == "STUDENT":
        has_permission = await check_permission(current_user, "offer:update", db)
    else:
        has_permission = False
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此Offer"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("offer", offer_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此Offer"
        )
    
    # 更新Offer信息
    update_data = offer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(offer, field, value)
    
    await db.commit()
    await db.refresh(offer)
    
    return offer


@router.post("/offers/{offer_id}/accept", response_model=OfferResponse)
async def accept_offer(
    offer_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    接受Offer（仅学生用户）
    
    Args:
        offer_id: Offer ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        OfferResponse: 更新后的Offer
        
    Raises:
        HTTPException: 如果Offer不存在或无权操作
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "offer:update", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能接受Offer"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("offer", offer_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此Offer"
        )
    
    # 获取学生信息
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生信息不存在"
        )
    
    # 获取Offer
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer不存在"
        )
    
    # 检查权限
    if offer.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此Offer"
        )
    
    # 检查状态
    if offer.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Offer状态为{offer.status}，无法接受"
        )
    
    # 检查是否过期
    from datetime import datetime
    if offer.expires_at and offer.expires_at < datetime.now():
        offer.status = "EXPIRED"
        await db.commit()
        await db.refresh(offer)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offer已过期"
        )
    
    # 更新状态为已接受
    offer.status = "ACCEPTED"
    await db.commit()
    await db.refresh(offer)
    
    return offer


@router.post("/offers/{offer_id}/reject", response_model=OfferResponse)
async def reject_offer(
    offer_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    拒绝Offer（仅学生用户）
    
    Args:
        offer_id: Offer ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        OfferResponse: 更新后的Offer
        
    Raises:
        HTTPException: 如果Offer不存在或无权操作
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "offer:update", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能拒绝Offer"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("offer", offer_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此Offer"
        )
    
    # 获取学生信息
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生信息不存在"
        )
    
    # 获取Offer
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer不存在"
        )
    
    # 检查权限
    if offer.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此Offer"
        )
    
    # 检查状态
    if offer.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Offer状态为{offer.status}，无法拒绝"
        )
    
    # 更新状态为已拒绝
    offer.status = "REJECTED"
    await db.commit()
    await db.refresh(offer)
    
    return offer

