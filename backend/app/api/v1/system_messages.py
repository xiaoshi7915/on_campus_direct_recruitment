"""
系统消息相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.chat import Message, ChatSession
from app.models.enums import MessageType

router = APIRouter()


@router.get("")
async def get_system_messages(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    is_read: Optional[bool] = Query(None, description="是否已读过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取系统消息列表（学生端）
    
    Args:
        page: 页码
        page_size: 每页数量
        is_read: 是否已读过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        系统消息列表
    """
    # 查找系统消息会话（使用特殊的系统用户ID或通过消息类型筛选）
    # 这里我们通过message_type为SYSTEM来筛选系统消息
    # 系统消息需要有一个特殊的会话，如果没有则创建一个
    # 首先查找或创建系统消息会话
    system_session_query = select(ChatSession).where(
        and_(
            ChatSession.user1_id == current_user.id,
            ChatSession.user2_id.is_(None),
            ChatSession.school_id.is_(None)
        )
    )
    system_session_result = await db.execute(system_session_query)
    system_session = system_session_result.scalar_one_or_none()
    
    # 如果没有系统消息会话，创建一个（但这里我们不自动创建，而是直接查询消息）
    # 系统消息的session_id可以是None，或者使用一个特殊的系统会话
    # 为了简化，我们直接查询消息，不依赖会话
    
    # 查找系统消息（通过message_type为SYSTEM来筛选）
    query = select(Message).where(
        and_(
            Message.receiver_id == current_user.id,
            Message.message_type == MessageType.SYSTEM
        )
    )
    
    # 是否已读过滤
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
async def mark_message_read(
    message_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    标记系统消息为已读
    
    Args:
        message_id: 消息ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        成功消息
    """
    result = await db.execute(
        select(Message).where(
            and_(
                Message.id == message_id,
                Message.receiver_id == current_user.id,
                Message.message_type == MessageType.SYSTEM
            )
        )
    )
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )
    
    message.is_read = True
    await db.commit()
    
    return {"message": "标记成功"}


@router.post("/read-all")
async def mark_all_messages_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    标记所有系统消息为已读
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        成功消息
    """
    result = await db.execute(
        select(Message).where(
            and_(
                Message.receiver_id == current_user.id,
                Message.message_type == MessageType.SYSTEM,
                Message.is_read == False
            )
        )
    )
    messages = result.scalars().all()
    
    for message in messages:
        message.is_read = True
    
    await db.commit()
    
    return {"message": f"已标记{len(messages)}条消息为已读"}


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取未读系统消息数量
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        未读消息数量
    """
    result = await db.execute(
        select(func.count()).select_from(Message).where(
            and_(
                Message.receiver_id == current_user.id,
                Message.message_type == MessageType.SYSTEM,
                Message.is_read == False
            )
        )
    )
    count = result.scalar() or 0
    
    return {"unread_count": count}


@router.post("")
async def create_system_message(
    receiver_id: str = Query(..., description="接收者用户ID"),
    content: str = Query(..., description="消息内容"),
    title: Optional[str] = Query(None, description="消息标题"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建系统消息（仅管理员或系统可以调用）
    
    Args:
        receiver_id: 接收者用户ID
        content: 消息内容
        title: 消息标题（可选）
        current_user: 当前登录用户（必须是管理员）
        db: 数据库会话
        
    Returns:
        创建的系统消息
    """
    # 检查权限：只有管理员可以创建系统消息
    if current_user.user_type != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以创建系统消息"
        )
    
    # 检查接收者是否存在
    receiver_result = await db.execute(select(User).where(User.id == receiver_id))
    receiver = receiver_result.scalar_one_or_none()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="接收者不存在"
        )
    
    # 查找或创建系统消息会话
    # 系统消息使用一个特殊的会话，每个用户有一个系统消息会话
    system_session_query = select(ChatSession).where(
        and_(
            ChatSession.user1_id == receiver_id,
            ChatSession.user2_id.is_(None),
            ChatSession.school_id.is_(None)
        )
    )
    system_session_result = await db.execute(system_session_query)
    system_session = system_session_result.scalar_one_or_none()
    
    if not system_session:
        # 创建系统消息会话（使用系统用户ID作为sender_id，或者使用当前管理员ID）
        system_session = ChatSession(
            id=str(uuid4()),
            user1_id=receiver_id,
            user2_id=None,
            school_id=None
        )
        db.add(system_session)
        await db.flush()
    
    # 创建系统消息
    # 系统消息的sender_id可以是管理员ID，或者使用一个特殊的系统用户ID
    from datetime import datetime
    message = Message(
        id=str(uuid4()),
        session_id=system_session.id,
        sender_id=current_user.id,  # 使用管理员ID作为发送者
        receiver_id=receiver_id,
        content=content,
        message_type=MessageType.SYSTEM,
        is_read=False
    )
    
    db.add(message)
    
    # 更新会话的最后消息时间
    system_session.last_message_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(message)
    
    return message

