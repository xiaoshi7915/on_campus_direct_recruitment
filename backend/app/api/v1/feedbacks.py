"""
反馈建议相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.common import Feedback
from app.schemas.feedback import (
    FeedbackCreate, FeedbackUpdate, FeedbackResponse, FeedbackListResponse
)

router = APIRouter()


@router.get("", response_model=FeedbackListResponse)
async def get_feedbacks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取反馈列表
    
    Args:
        page: 页码
        page_size: 每页数量
        status_filter: 状态过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FeedbackListResponse: 反馈列表
    """
    # 构建查询
    query = select(Feedback)
    
    # 根据用户类型过滤
    if current_user.user_type != "ADMIN":
        # 非管理员只能查看自己的反馈
        query = query.where(Feedback.user_id == current_user.id)
    
    # 状态过滤
    if status_filter:
        query = query.where(Feedback.status == status_filter)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Feedback.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    feedbacks = result.scalars().all()
    
    return {
        "items": feedbacks,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取反馈详情
    
    Args:
        feedback_id: 反馈ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FeedbackResponse: 反馈详情
        
    Raises:
        HTTPException: 如果反馈不存在或无权查看
    """
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 检查权限（非管理员只能查看自己的反馈）
    if current_user.user_type != "ADMIN" and feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此反馈"
        )
    
    return feedback


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建反馈（所有用户）
    
    Args:
        feedback_data: 反馈数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FeedbackResponse: 创建的反馈
    """
    # 创建反馈
    feedback = Feedback(
        id=str(uuid4()),
        user_id=current_user.id,
        user_type=current_user.user_type,
        title=feedback_data.title,
        content=feedback_data.content,
        images=feedback_data.images,
        status="PENDING"
    )
    
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    
    return feedback


@router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: str,
    feedback_data: FeedbackUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新反馈（仅管理员）
    
    Args:
        feedback_id: 反馈ID
        feedback_data: 更新的反馈数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FeedbackResponse: 更新后的反馈
        
    Raises:
        HTTPException: 如果反馈不存在或无权修改
    """
    # 检查权限（仅管理员可以更新反馈）
    if current_user.user_type != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员才能更新反馈"
        )
    
    # 获取反馈
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 更新反馈信息
    update_data = feedback_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(feedback, field, value)
    
    # 如果有回复，更新回复时间
    if "reply" in update_data and update_data["reply"]:
        feedback.replied_at = datetime.now()
    
    await db.commit()
    await db.refresh(feedback)
    
    return feedback


