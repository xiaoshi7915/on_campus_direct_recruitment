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
from app.models.interview import Interview
from app.models.job import JobApplication
from app.models.profile import EnterpriseProfile, StudentProfile
from app.schemas.interview import InterviewCreate, InterviewUpdate, InterviewResponse, InterviewListResponse

router = APIRouter()


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
    elif current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if student:
            query = query.where(Interview.student_id == student.id)
    
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
    
    # 检查权限
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if not enterprise or interview.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此面试"
            )
    elif current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if not student or interview.student_id != student.id:
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
    if application.enterprise_id != enterprise.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权为此申请创建面试"
        )
    
    # 创建面试
    interview = Interview(
        id=str(uuid4()),
        application_id=interview_data.application_id,
        enterprise_id=enterprise.id,
        student_id=application.student_id,
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



