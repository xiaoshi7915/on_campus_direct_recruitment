"""
聊天相关API路由（WebSocket + REST）
"""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional, Dict, List, Set
from uuid import uuid4
import json
import asyncio
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.datetime_utils import utc_now
from app.api.v1.auth import get_current_user
from app.core.security import verify_token
from app.models.user import User
from app.models.chat import ChatSession, Message
from app.schemas.chat import (
    MessageCreate, MessageResponse, MessageListResponse,
    ChatSessionResponse, ChatSessionListResponse
)
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

# WebSocket连接管理器
class ConnectionManager:
    """WebSocket连接管理器，支持心跳检测和自动清理失效连接"""
    
    def __init__(self):
        # 存储活跃的连接：{user_id: [websocket1, websocket2, ...]}
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # 存储连接的最后心跳时间：{websocket: last_ping_time}
        self.connection_heartbeat: Dict[WebSocket, datetime] = {}
        # 心跳超时时间（秒）
        self.heartbeat_timeout = 60
        # 启动心跳检测任务
        self._heartbeat_task: Optional[asyncio.Task] = None
    
    async def start_heartbeat_check(self):
        """启动心跳检测任务"""
        if self._heartbeat_task is None or self._heartbeat_task.done():
            self._heartbeat_task = asyncio.create_task(self._check_heartbeat())
    
    async def _check_heartbeat(self):
        """定期检查连接心跳，清理超时连接"""
        while True:
            try:
                await asyncio.sleep(30)  # 每30秒检查一次
                current_time = utc_now()
                timeout_connections: Set[WebSocket] = set()
                
                # 检查所有连接的心跳时间
                for websocket, last_ping in list(self.connection_heartbeat.items()):
                    if (current_time - last_ping).total_seconds() > self.heartbeat_timeout:
                        timeout_connections.add(websocket)
                
                # 清理超时连接
                for websocket in timeout_connections:
                    await self._remove_connection(websocket, reason="心跳超时")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"心跳检测任务出错: {str(e)}", exc_info=True)
    
    async def _remove_connection(self, websocket: WebSocket, reason: str = "未知原因"):
        """移除连接（内部方法）"""
        try:
            # 关闭WebSocket连接
            await websocket.close(code=1000, reason=reason)
        except Exception as e:
            logger.debug(f"关闭WebSocket连接时出错: {str(e)}")
        
        # 从心跳记录中移除
        if websocket in self.connection_heartbeat:
            del self.connection_heartbeat[websocket]
        
        # 从活跃连接中移除
        for user_id, connections in list(self.active_connections.items()):
            if websocket in connections:
                connections.remove(websocket)
                if not connections:
                    del self.active_connections[user_id]
                break
        
        logger.info(f"WebSocket连接已移除: {reason}")
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """建立WebSocket连接"""
        try:
            await websocket.accept()
            if user_id not in self.active_connections:
                self.active_connections[user_id] = []
            self.active_connections[user_id].append(websocket)
            # 记录连接时间作为初始心跳
            self.connection_heartbeat[websocket] = utc_now()
            
            # 确保心跳检测任务运行
            await self.start_heartbeat_check()
            
            logger.info(f"WebSocket连接已建立: user_id={user_id}")
        except Exception as e:
            logger.error(f"建立WebSocket连接失败: {str(e)}", exc_info=True)
            raise
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        """断开WebSocket连接"""
        asyncio.create_task(self._remove_connection(websocket, "主动断开"))
    
    async def update_heartbeat(self, websocket: WebSocket):
        """更新连接心跳时间"""
        self.connection_heartbeat[websocket] = datetime.utcnow()
    
    async def send_personal_message(self, message: dict, user_id: str):
        """向特定用户发送消息"""
        if user_id not in self.active_connections:
            return
        
        # 收集需要移除的失效连接
        invalid_connections: List[WebSocket] = []
        
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_json(message)
                # 发送成功，更新心跳
                await self.update_heartbeat(connection)
            except Exception as e:
                logger.warning(f"发送消息失败，连接可能已断开: {str(e)}")
                # 记录失效连接，稍后移除
                invalid_connections.append(connection)
        
        # 移除失效连接
        for connection in invalid_connections:
            await self._remove_connection(connection, "发送消息失败")
    
    async def broadcast(self, message: dict):
        """广播消息给所有连接"""
        invalid_connections: List[WebSocket] = []
        
        for user_id, connections in list(self.active_connections.items()):
            for connection in connections:
                try:
                    await connection.send_json(message)
                    await self.update_heartbeat(connection)
                except Exception as e:
                    logger.warning(f"广播消息失败: {str(e)}")
                    invalid_connections.append(connection)
        
        # 移除失效连接
        for connection in invalid_connections:
            await self._remove_connection(connection, "广播消息失败")


# 创建全局连接管理器
manager = ConnectionManager()


# ==================== WebSocket接口 ====================

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    """
    WebSocket连接端点（需要认证）
    
    Args:
        websocket: WebSocket连接
        token: JWT令牌（通过查询参数传递，例如：ws://host/ws?token=xxx）
    """
    # 验证token
    if not token:
        await websocket.close(code=1008, reason="缺少认证令牌")
        return
    
    # 验证token并获取用户信息
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=1008, reason="无效的认证令牌")
        return
    
    username = payload.get("sub")
    user_id_from_token = payload.get("user_id")
    
    if not username or not user_id_from_token:
        await websocket.close(code=1008, reason="令牌信息不完整")
        return
    
    # 从数据库验证用户存在且状态正常
    # 注意：WebSocket不能使用Depends，需要手动创建数据库会话
    async for db in get_db():
        try:
            result = await db.execute(
                select(User).where(User.id == user_id_from_token, User.username == username)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                await websocket.close(code=1008, reason="用户不存在")
                return
            
            if user.status != "ACTIVE":
                await websocket.close(code=1008, reason="账户已被禁用")
                return
            
            # 认证通过，建立连接
            await manager.connect(websocket, user_id_from_token)
            logger.info(f"WebSocket连接已建立（已认证）: user_id={user_id_from_token}, username={username}")
            
            # 保存user_id供后续使用
            current_user_id = user_id_from_token
            
            try:
                while True:
                    # 接收消息
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    
                    # 处理不同类型的消息
                    message_type = message_data.get("type", "message")
                    
                    if message_type == "ping":
                        # 心跳检测
                        await manager.update_heartbeat(websocket)
                        await websocket.send_json({"type": "pong"})
                    elif message_type == "message":
                        # 普通消息（需要保存到数据库）
                        receiver_id = message_data.get("receiver_id")
                        content = message_data.get("content")
                        
                        if receiver_id and content:
                            # 发送给接收者
                            await manager.send_personal_message({
                                "type": "message",
                                "sender_id": current_user_id,
                                "content": content,
                                "timestamp": message_data.get("timestamp")
                            }, receiver_id)
                            
                            # 确认发送成功
                            await websocket.send_json({
                                "type": "message_sent",
                                "message_id": message_data.get("message_id")
                            })
                            # 更新心跳
                            await manager.update_heartbeat(websocket)
            except WebSocketDisconnect:
                logger.info(f"WebSocket连接断开: user_id={current_user_id}")
                manager.disconnect(websocket, current_user_id)
            except Exception as e:
                logger.error(f"WebSocket处理出错: {str(e)}", exc_info=True)
                manager.disconnect(websocket, current_user_id)
            break
        except Exception as e:
            logger.error(f"WebSocket认证失败: {str(e)}", exc_info=True)
            await websocket.close(code=1011, reason="服务器内部错误")
            break
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 处理不同类型的消息
            message_type = message_data.get("type", "message")
            
            if message_type == "ping":
                # 心跳检测
                await manager.update_heartbeat(websocket)
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
                        "sender_id": user_id_from_token,
                        "content": content,
                        "timestamp": message_data.get("timestamp")
                    }, receiver_id)
                    
                    # 确认发送成功
                    await websocket.send_json({
                        "type": "message_sent",
                        "message_id": message_data.get("message_id")
                    })
                    # 更新心跳
                    await manager.update_heartbeat(websocket)
    except WebSocketDisconnect:
        logger.info(f"WebSocket连接断开: user_id={user_id_from_token}")
        manager.disconnect(websocket, user_id_from_token)
    except Exception as e:
        logger.error(f"WebSocket处理出错: {str(e)}", exc_info=True)
        manager.disconnect(websocket, user_id_from_token)


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
    # 使用selectinload预加载关联数据，避免N+1查询问题
    # 注意：MySQL中NULL值在降序排序时默认排在最后
    result = await db.execute(
        select(ChatSession)
        .options(
            selectinload(ChatSession.user1),
            selectinload(ChatSession.user2),
            selectinload(ChatSession.school)
        )
        .where(
            or_(
                ChatSession.user1_id == current_user.id,
                ChatSession.user2_id == current_user.id
            )
        )
        .order_by(ChatSession.last_message_at.desc())
    )
    sessions = result.scalars().all()
    
    # 为每个会话构建响应对象
    session_list = []
    
    for session in sessions:
        # 获取用户1和用户2的信息（已通过selectinload预加载）
        user1 = session.user1
        user2 = session.user2 if session.user2_id else None
        school = session.school if session.school_id else None
        
        # 构建响应对象
        # 处理用户类型：确保返回的是枚举值（如 'ENTERPRISE'）而不是字符串表示（如 'UserType.ENTERPRISE'）
        user1_type_value = None
        if user1 and user1.user_type:
            if hasattr(user1.user_type, 'value'):
                user1_type_value = user1.user_type.value
            else:
                # 如果直接转换为字符串，提取实际值
                user1_type_str = str(user1.user_type)
                user1_type_value = user1_type_str.split('.')[-1] if '.' in user1_type_str else user1_type_str
        
        user2_type_value = None
        if user2 and user2.user_type:
            if hasattr(user2.user_type, 'value'):
                user2_type_value = user2.user_type.value
            else:
                # 如果直接转换为字符串，提取实际值
                user2_type_str = str(user2.user_type)
                user2_type_value = user2_type_str.split('.')[-1] if '.' in user2_type_str else user2_type_str
        
        session_dict = {
            "id": session.id,
            "user1_id": session.user1_id,
            "user2_id": session.user2_id,
            "school_id": session.school_id,
            "user1_name": user1.username if user1 else None,
            "user2_name": user2.username if user2 else None,
            "school_name": school.name if school else None,
            "user1_type": user1_type_value,
            "user2_type": user2_type_value,
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
    
    # 处理用户类型：确保返回枚举值
    user1_type_value = None
    if user1 and user1.user_type:
        if hasattr(user1.user_type, 'value'):
            user1_type_value = user1.user_type.value
        else:
            user1_type_str = str(user1.user_type)
            user1_type_value = user1_type_str.split('.')[-1] if '.' in user1_type_str else user1_type_str
    
    user2_type_value = None
    if user2 and user2.user_type:
        if hasattr(user2.user_type, 'value'):
            user2_type_value = user2.user_type.value
        else:
            user2_type_str = str(user2.user_type)
            user2_type_value = user2_type_str.split('.')[-1] if '.' in user2_type_str else user2_type_str
    
    return {
        "id": session.id,
        "user1_id": session.user1_id,
        "user2_id": session.user2_id,
        "school_id": session.school_id,
        "user1_name": user1.username if user1 else None,
        "user2_name": user2.username if user2 else None,
        "school_name": school.name if school else None,
        "user1_type": user1_type_value,
        "user2_type": user2_type_value,
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
                # 处理用户类型：确保返回枚举值
                "user1_type": user1.user_type.value if user1 and user1.user_type and hasattr(user1.user_type, 'value') else (str(user1.user_type).split('.')[-1] if user1 and user1.user_type and '.' in str(user1.user_type) else (str(user1.user_type) if user1 and user1.user_type else None)),
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
                # 处理用户类型：确保返回枚举值
                "user1_type": user1.user_type.value if user1 and user1.user_type and hasattr(user1.user_type, 'value') else (str(user1.user_type).split('.')[-1] if user1 and user1.user_type and '.' in str(user1.user_type) else (str(user1.user_type) if user1 and user1.user_type else None)),
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
            # 处理用户类型：确保返回枚举值
            "user1_type": user1.user_type.value if user1 and user1.user_type and hasattr(user1.user_type, 'value') else (str(user1.user_type).split('.')[-1] if user1 and user1.user_type and '.' in str(user1.user_type) else (str(user1.user_type) if user1 and user1.user_type else None)),
            "user2_type": user2.user_type.value if user2 and user2.user_type and hasattr(user2.user_type, 'value') else (str(user2.user_type).split('.')[-1] if user2 and user2.user_type and '.' in str(user2.user_type) else (str(user2.user_type) if user2 and user2.user_type else None)),
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
                # 处理用户类型：确保返回枚举值
                "user1_type": user1.user_type.value if user1 and user1.user_type and hasattr(user1.user_type, 'value') else (str(user1.user_type).split('.')[-1] if user1 and user1.user_type and '.' in str(user1.user_type) else (str(user1.user_type) if user1 and user1.user_type else None)),
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
    
    db.add(message)
    await db.flush()  # 刷新以获取created_at
    
    # 更新会话的最后消息时间（使用当前时间）
    current_time = utc_now()
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

