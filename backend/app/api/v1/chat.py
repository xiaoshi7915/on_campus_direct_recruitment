"""
聊天相关API路由（WebSocket + REST）
"""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import Optional, Dict, List
from uuid import uuid4
import json

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.chat import ChatSession, Message
from app.schemas.chat import (
    MessageCreate, MessageResponse, MessageListResponse,
    ChatSessionResponse, ChatSessionListResponse
)

router = APIRouter()

# WebSocket连接管理器
class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储活跃的连接：{user_id: [websocket1, websocket2, ...]}
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """建立WebSocket连接"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        """断开WebSocket连接"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: str):
        """向特定用户发送消息"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"发送消息失败：{e}")
    
    async def broadcast(self, message: dict):
        """广播消息给所有连接"""
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"广播消息失败：{e}")


# 创建全局连接管理器
manager = ConnectionManager()


# ==================== WebSocket接口 ====================

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket连接端点
    
    Args:
        websocket: WebSocket连接
        user_id: 用户ID
    """
    await manager.connect(websocket, user_id)
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 处理不同类型的消息
            message_type = message_data.get("type", "message")
            
            if message_type == "ping":
                # 心跳检测
                await websocket.send_json({"type": "pong"})
            elif message_type == "message":
                # 普通消息（需要保存到数据库）
                # 这里可以添加消息保存逻辑
                receiver_id = message_data.get("receiver_id")
                content = message_data.get("content")
                
                if receiver_id and content:
                    # 发送给接收者
                    await manager.send_personal_message({
                        "type": "message",
                        "sender_id": user_id,
                        "content": content,
                        "timestamp": message_data.get("timestamp")
                    }, receiver_id)
                    
                    # 确认发送成功
                    await websocket.send_json({
                        "type": "message_sent",
                        "message_id": message_data.get("message_id")
                    })
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


# ==================== REST API接口 ====================

@router.get("/sessions", response_model=ChatSessionListResponse)
async def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取聊天会话列表
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ChatSessionListResponse: 聊天会话列表
    """
    from app.models.user import User
    
    # 查询当前用户参与的所有会话
    # 注意：MySQL中NULL值在降序排序时默认排在最后
    result = await db.execute(
        select(ChatSession).where(
            or_(
                ChatSession.user1_id == current_user.id,
                ChatSession.user2_id == current_user.id
            )
        ).order_by(ChatSession.last_message_at.desc())
    )
    sessions = result.scalars().all()
    
    # 为每个会话加载对方用户信息
    session_list = []
    # 收集所有需要查询的用户ID和学校ID
    all_user_ids = set()
    all_school_ids = set()
    for session in sessions:
        all_user_ids.add(session.user1_id)
        if session.user2_id:
            all_user_ids.add(session.user2_id)
        if session.school_id:
            all_school_ids.add(session.school_id)
    
    # 批量查询所有用户信息
    users = {}
    if all_user_ids:
        users_result = await db.execute(
            select(User).where(User.id.in_(all_user_ids))
        )
        users = {user.id: user for user in users_result.scalars().all()}
    
    # 批量查询所有学校信息
    schools = {}
    if all_school_ids:
        from app.models.school import School
        schools_result = await db.execute(
            select(School).where(School.id.in_(all_school_ids))
        )
        schools = {school.id: school for school in schools_result.scalars().all()}
    
    for session in sessions:
        # 获取用户1和用户2的信息
        user1 = users.get(session.user1_id)
        user2 = users.get(session.user2_id) if session.user2_id else None
        school = schools.get(session.school_id) if session.school_id else None
        
        # 构建响应对象
        session_dict = {
            "id": session.id,
            "user1_id": session.user1_id,
            "user2_id": session.user2_id,
            "school_id": session.school_id,
            "user1_name": user1.username if user1 else None,
            "user2_name": user2.username if user2 else None,
            "school_name": school.name if school else None,
            "user1_type": str(user1.user_type) if user1 else None,
            "user2_type": str(user2.user_type) if user2 else None,
            "last_message_at": session.last_message_at,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }
        
        session_list.append(session_dict)
    
    return {
        "items": session_list,
        "total": len(session_list)
    }


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取聊天会话详情
    
    Args:
        session_id: 会话ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ChatSessionResponse: 聊天会话详情
        
    Raises:
        HTTPException: 如果会话不存在或无权查看
    """
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            or_(
                ChatSession.user1_id == current_user.id,
                ChatSession.user2_id == current_user.id
            )
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="聊天会话不存在"
        )
    
    # 填充用户和学校信息
    from app.models.school import School
    user1_result = await db.execute(select(User).where(User.id == session.user1_id))
    user1 = user1_result.scalar_one_or_none()
    
    user2 = None
    if session.user2_id:
        user2_result = await db.execute(select(User).where(User.id == session.user2_id))
        user2 = user2_result.scalar_one_or_none()
    
    school = None
    if session.school_id:
        school_result = await db.execute(select(School).where(School.id == session.school_id))
        school = school_result.scalar_one_or_none()
    
    return {
        "id": session.id,
        "user1_id": session.user1_id,
        "user2_id": session.user2_id,
        "school_id": session.school_id,
        "user1_name": user1.username if user1 else None,
        "user2_name": user2.username if user2 else None,
        "school_name": school.name if school else None,
        "user1_type": str(user1.user_type.value) if user1 and hasattr(user1.user_type, 'value') else (str(user1.user_type) if user1 else None),
        "user2_type": str(user2.user_type.value) if user2 and hasattr(user2.user_type, 'value') else (str(user2.user_type) if user2 else None),
        "last_message_at": session.last_message_at,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    receiver_id: Optional[str] = Query(None, description="接收者ID（user_id）"),
    student_id: Optional[str] = Query(None, description="学生ID（如果提供，将转换为user_id）"),
    school_id: Optional[str] = Query(None, description="学校ID（如果与学校聊天）"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建或获取聊天会话
    支持用户-用户聊天和用户-学校聊天
    
    Args:
        receiver_id: 接收者ID（user_id，如果提供了student_id或school_id则可以为空）
        student_id: 学生ID（可选，如果提供将转换为user_id）
        school_id: 学校ID（可选，如果与学校聊天）
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ChatSessionResponse: 聊天会话
    """
    from app.models.profile import StudentProfile
    from app.models.user import User
    from app.models.school import School
    
    # 如果提供了school_id，创建企业-学校聊天会话
    if school_id:
        # 检查学校是否存在
        school_result = await db.execute(
            select(School).where(School.id == school_id)
        )
        school = school_result.scalar_one_or_none()
        if not school:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学校不存在"
            )
        
        # 检查是否已存在企业-学校会话
        existing_result = await db.execute(
            select(ChatSession).where(
                ChatSession.user1_id == current_user.id,
                ChatSession.school_id == school_id
            )
        )
        existing_session = existing_result.scalar_one_or_none()
        
        if existing_session:
            # 返回现有会话
            user1_result = await db.execute(select(User).where(User.id == existing_session.user1_id))
            user1 = user1_result.scalar_one_or_none()
            
            return {
                "id": existing_session.id,
                "user1_id": existing_session.user1_id,
                "user2_id": None,
                "school_id": existing_session.school_id,
                "user1_name": user1.username if user1 else None,
                "user2_name": None,
                "school_name": school.name,
                "user1_type": str(user1.user_type.value) if user1 and hasattr(user1.user_type, 'value') else (str(user1.user_type) if user1 else None),
                "user2_type": None,
                "last_message_at": existing_session.last_message_at,
                "created_at": existing_session.created_at,
                "updated_at": existing_session.updated_at,
            }
        
        # 创建新会话
        session = ChatSession(
            id=str(uuid4()),
            user1_id=current_user.id,
            user2_id=None,
            school_id=school_id
        )
        
        db.add(session)
        await db.commit()
        await db.refresh(session)
        
        user1_result = await db.execute(select(User).where(User.id == session.user1_id))
        user1 = user1_result.scalar_one_or_none()
        
        return {
            "id": session.id,
            "user1_id": session.user1_id,
            "user2_id": None,
            "school_id": session.school_id,
            "user1_name": user1.username if user1 else None,
            "user2_name": None,
            "school_name": school.name,
            "user1_type": str(user1.user_type.value) if user1 and hasattr(user1.user_type, 'value') else (str(user1.user_type) if user1 else None),
            "user2_type": None,
            "last_message_at": session.last_message_at,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }
    
    # 用户-用户聊天逻辑（原有逻辑）
    # 如果提供了student_id，转换为user_id
    actual_receiver_id = receiver_id
    if student_id:
        # 通过student_id查询user_id
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.id == student_id)
        )
        student = student_result.scalar_one_or_none()
        if student:
            actual_receiver_id = student.user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生不存在"
            )
    
    if not actual_receiver_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供receiver_id、student_id或school_id"
        )
    
    # 检查是否已存在会话
    result = await db.execute(
        select(ChatSession).where(
            or_(
                and_(
                    ChatSession.user1_id == current_user.id,
                    ChatSession.user2_id == actual_receiver_id,
                    ChatSession.school_id.is_(None)  # 确保是用户-用户聊天
                ),
                and_(
                    ChatSession.user1_id == actual_receiver_id,
                    ChatSession.user2_id == current_user.id,
                    ChatSession.school_id.is_(None)  # 确保是用户-用户聊天
                )
            )
        )
    )
    existing_session = result.scalar_one_or_none()
    
    if existing_session:
        # 返回现有会话，需要填充用户信息
        user1_result = await db.execute(select(User).where(User.id == existing_session.user1_id))
        user2_result = await db.execute(select(User).where(User.id == existing_session.user2_id))
        user1 = user1_result.scalar_one_or_none()
        user2 = user2_result.scalar_one_or_none()
        
        return {
            "id": existing_session.id,
            "user1_id": existing_session.user1_id,
            "user2_id": existing_session.user2_id,
            "school_id": None,
            "user1_name": user1.username if user1 else None,
            "user2_name": user2.username if user2 else None,
            "school_name": None,
            "user1_type": str(user1.user_type) if user1 else None,
            "user2_type": str(user2.user_type) if user2 else None,
            "last_message_at": existing_session.last_message_at,
            "created_at": existing_session.created_at,
            "updated_at": existing_session.updated_at,
        }
    
    # 创建新会话
    session = ChatSession(
        id=str(uuid4()),
        user1_id=current_user.id,
        user2_id=actual_receiver_id,
        school_id=None
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    # 填充用户信息
    user1_result = await db.execute(select(User).where(User.id == session.user1_id))
    user2_result = await db.execute(select(User).where(User.id == session.user2_id))
    user1 = user1_result.scalar_one_or_none()
    user2 = user2_result.scalar_one_or_none()
    
    return {
        "id": session.id,
        "user1_id": session.user1_id,
        "user2_id": session.user2_id,
        "school_id": None,
        "user1_name": user1.username if user1 else None,
        "user2_name": user2.username if user2 else None,
        "school_name": None,
        "user1_type": str(user1.user_type.value) if user1 and hasattr(user1.user_type, 'value') else (str(user1.user_type) if user1 else None),
        "user2_type": str(user2.user_type.value) if user2 and hasattr(user2.user_type, 'value') else (str(user2.user_type) if user2 else None),
        "last_message_at": session.last_message_at,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
    }


@router.get("/sessions/{session_id}/messages", response_model=MessageListResponse)
async def get_messages(
    session_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取会话消息列表
    
    Args:
        session_id: 会话ID
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MessageListResponse: 消息列表
        
    Raises:
        HTTPException: 如果会话不存在或无权查看
    """
    # 检查会话是否存在且用户有权访问
    session_result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            or_(
                ChatSession.user1_id == current_user.id,
                ChatSession.user2_id == current_user.id
            )
        )
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="聊天会话不存在"
        )
    
    # 查询消息
    query = select(Message).where(Message.session_id == session_id)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询（按时间倒序）
    offset = (page - 1) * page_size
    query = query.order_by(Message.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    messages = result.scalars().all()
    
    # 标记消息为已读
    unread_messages = [msg for msg in messages if not msg.is_read and msg.receiver_id == current_user.id]
    if unread_messages:
        for msg in unread_messages:
            msg.is_read = True
        
        # 更新会话的未读计数
        if session.user1_id == current_user.id:
            session.unread_count_user1 = 0
        else:
            session.unread_count_user2 = 0
        
        await db.commit()
    
    return {
        "items": messages,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    session_id: str,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发送消息
    
    Args:
        session_id: 会话ID
        message_data: 消息数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MessageResponse: 创建的消息
        
    Raises:
        HTTPException: 如果会话不存在或无权发送
    """
    # 检查会话是否存在且用户有权访问
    session_result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            or_(
                ChatSession.user1_id == current_user.id,
                ChatSession.user2_id == current_user.id
            )
        )
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="聊天会话不存在"
        )
    
    # 验证接收者
    if message_data.receiver_id != session.user1_id and message_data.receiver_id != session.user2_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="接收者不在该会话中"
        )
    
    # 创建消息
    from datetime import datetime
    message = Message(
        id=str(uuid4()),
        session_id=session_id,
        sender_id=current_user.id,
        receiver_id=message_data.receiver_id,
        content=message_data.content,
        message_type=message_data.message_type,
        file_url=message_data.file_url,
        is_read=False
    )
    
    # 使用当前时间作为创建时间
    from datetime import datetime
    current_time = datetime.utcnow()
    
    db.add(message)
    await db.flush()  # 刷新以获取created_at
    
    # 更新会话的最后消息时间（使用当前时间）
    session.last_message_at = current_time
    
    await db.commit()
    await db.refresh(message)
    
    # 确保message.created_at有值
    if not message.created_at:
        message.created_at = current_time
    
    # 通过WebSocket发送消息
    await manager.send_personal_message({
        "type": "message",
        "message_id": message.id,
        "session_id": session_id,
        "sender_id": current_user.id,
        "receiver_id": message_data.receiver_id,
        "content": message_data.content,
        "message_type": message_data.message_type,
        "file_url": message_data.file_url,
        "created_at": message.created_at.isoformat()
    }, message_data.receiver_id)
    
    return message


@router.put("/messages/{message_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_message_read(
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
        
    Raises:
        HTTPException: 如果消息不存在或无权操作
    """
    result = await db.execute(
        select(Message).where(
            Message.id == message_id,
            Message.receiver_id == current_user.id
        )
    )
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )
    
    if not message.is_read:
        message.is_read = True
        
        # 更新会话的未读计数
        session_result = await db.execute(
            select(ChatSession).where(ChatSession.id == message.session_id)
        )
        session = session_result.scalar_one_or_none()
        
        if session:
            if session.user1_id == current_user.id:
                session.unread_count_user1 = max(0, session.unread_count_user1 - 1)
            else:
                session.unread_count_user2 = max(0, session.unread_count_user2 - 1)
        
        await db.commit()

