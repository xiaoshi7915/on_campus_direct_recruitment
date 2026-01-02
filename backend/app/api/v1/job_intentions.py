"""
求职意向相关API路由
"""
import json
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.job import JobIntention
from app.models.profile import StudentProfile
from app.schemas.job import (
    JobIntentionCreate, JobIntentionUpdate, JobIntentionResponse, JobIntentionListResponse
)

router = APIRouter()


@router.get("", response_model=JobIntentionListResponse)
async def get_job_intentions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    student_id: Optional[str] = Query(None, description="学生ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取求职意向列表
    
    Args:
        page: 页码
        page_size: 每页数量
        student_id: 学生ID（管理员可查看所有）
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobIntentionListResponse: 求职意向列表
    """
    # 构建查询
    query = select(JobIntention)
    
    # 根据用户类型过滤
    if current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if student:
            query = query.where(JobIntention.student_id == student.id)
        else:
            # 学生档案不存在，返回空列表
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
    elif current_user.user_type == "ADMIN":
        # 管理员可以查看所有
        if student_id:
            query = query.where(JobIntention.student_id == student_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看求职意向"
        )
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(JobIntention.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    intentions = result.scalars().all()
    
    return {
        "items": intentions,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{intention_id}", response_model=JobIntentionResponse)
async def get_job_intention(
    intention_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取求职意向详情
    
    Args:
        intention_id: 求职意向ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobIntentionResponse: 求职意向详情
        
    Raises:
        HTTPException: 如果求职意向不存在或无权查看
    """
    result = await db.execute(select(JobIntention).where(JobIntention.id == intention_id))
    intention = result.scalar_one_or_none()
    
    if not intention:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="求职意向不存在"
        )
    
    # 检查权限
    if current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if not student or intention.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此求职意向"
            )
    elif current_user.user_type != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此求职意向"
        )
    
    return intention


@router.post("", response_model=JobIntentionResponse, status_code=status.HTTP_201_CREATED)
async def create_job_intention(
    intention_data: JobIntentionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建求职意向（仅学生用户）
    
    Args:
        intention_data: 求职意向数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobIntentionResponse: 创建的求职意向
        
    Raises:
        HTTPException: 如果用户不是学生或学生信息不存在
    """
    # 检查用户类型
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能创建求职意向"
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
    
    # 创建求职意向
    intention = JobIntention(
        id=str(uuid4()),
        student_id=student.id,
        # 旧字段（保留兼容性）
        job_type=intention_data.job_type,
        industry=intention_data.industry,
        salary_expect=intention_data.salary_expect,
        work_location=intention_data.work_location,
        # 新字段
        job_type_list=json.dumps(intention_data.job_type_list) if intention_data.job_type_list else None,
        industry_list=json.dumps(intention_data.industry_list) if intention_data.industry_list else None,
        work_location_list=json.dumps(intention_data.work_location_list) if intention_data.work_location_list else None,
        job_nature=intention_data.job_nature,
        salary_min=intention_data.salary_min,
        salary_max=intention_data.salary_max,
        part_time_days=intention_data.part_time_days,
        work_time_slot=intention_data.work_time_slot
    )
    
    db.add(intention)
    await db.commit()
    await db.refresh(intention)
    
    return intention


@router.put("/{intention_id}", response_model=JobIntentionResponse)
async def update_job_intention(
    intention_id: str,
    intention_data: JobIntentionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新求职意向（仅学生用户）
    
    Args:
        intention_id: 求职意向ID
        intention_data: 更新的求职意向数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobIntentionResponse: 更新后的求职意向
        
    Raises:
        HTTPException: 如果求职意向不存在或无权修改
    """
    # 获取求职意向
    result = await db.execute(select(JobIntention).where(JobIntention.id == intention_id))
    intention = result.scalar_one_or_none()
    
    if not intention:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="求职意向不存在"
        )
    
    # 检查权限
    if current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if not student or intention.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此求职意向"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此求职意向"
        )
    
    # 更新求职意向信息
    update_data = intention_data.model_dump(exclude_unset=True)
    
    # 处理JSON字段
    if 'job_type_list' in update_data and update_data['job_type_list'] is not None:
        update_data['job_type_list'] = json.dumps(update_data['job_type_list']) if update_data['job_type_list'] else None
    if 'industry_list' in update_data and update_data['industry_list'] is not None:
        update_data['industry_list'] = json.dumps(update_data['industry_list']) if update_data['industry_list'] else None
    if 'work_location_list' in update_data and update_data['work_location_list'] is not None:
        update_data['work_location_list'] = json.dumps(update_data['work_location_list']) if update_data['work_location_list'] else None
    
    for field, value in update_data.items():
        setattr(intention, field, value)
    
    await db.commit()
    await db.refresh(intention)
    
    return intention


@router.delete("/{intention_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_intention(
    intention_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除求职意向（仅学生用户）
    
    Args:
        intention_id: 求职意向ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果求职意向不存在或无权删除
    """
    # 获取求职意向
    result = await db.execute(select(JobIntention).where(JobIntention.id == intention_id))
    intention = result.scalar_one_or_none()
    
    if not intention:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="求职意向不存在"
        )
    
    # 检查权限
    if current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if not student or intention.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此求职意向"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此求职意向"
        )
    
    await db.delete(intention)
    await db.commit()
    
    return None



