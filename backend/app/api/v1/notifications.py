"""
系统消息相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.chat import Message

router = APIRouter()


@router.get("")
async def get_notifications(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    is_read: Optional[bool] = Query(None, description="是否已读过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取系统消息列表（只能查看自己的消息）
    
    Args:
        page: 页码
        page_size: 每页数量
        is_read: 是否已读过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 消息列表
    """
    # 构建查询（系统消息，且接收者是当前用户）
    query = select(Message).where(
        Message.receiver_id == current_user.id,
        Message.message_type == "SYSTEM"
    )
    
    # 已读状态过滤
    if is_read is not None:
        query = query.where(Message.is_read == is_read)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Message.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return {
        "items": messages,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/{message_id}/read")
async def mark_as_read(
    message_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    标记消息为已读
    
    Args:
        message_id: 消息ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 成功消息
    """
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message or message.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在或无权操作"
        )
    
    message.is_read = True
    await db.commit()
    
    return {"message": "标记成功"}


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取未读消息数量
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 未读消息数量
    """
    result = await db.execute(
        select(func.count()).where(
            Message.receiver_id == current_user.id,
            Message.message_type == "SYSTEM",
            Message.is_read == False
        )
    )
    count = result.scalar()
    
    return {"count": count}

