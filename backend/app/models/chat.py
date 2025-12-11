"""
聊天相关模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import MessageType


class ChatSession(Base):
    """
    聊天会话表模型
    """
    __tablename__ = "chat_sessions"
    
    id = Column(String(36), primary_key=True, comment="会话ID")
    user1_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户1 ID")
    user2_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户2 ID")
    last_message_at = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="最后消息时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user1 = relationship("User", foreign_keys=[user1_id], back_populates="chat_sessions_user1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="chat_sessions_user2")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan", order_by="Message.created_at")
    
    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='uq_chat_users'),
        {"comment": "聊天会话表"},
    )


class Message(Base):
    """
    消息表模型
    """
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, comment="消息ID")
    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True, comment="会话ID")
    sender_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="发送者ID")
    receiver_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="接收者ID")
    content = Column(Text, nullable=False, comment="消息内容")
    message_type = Column(String(20), default="TEXT", nullable=False, comment="消息类型")
    file_url = Column(String(255), nullable=True, comment="文件URL")
    is_read = Column(Boolean, default=False, nullable=False, comment="是否已读")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="创建时间")
    
    # 关联关系
    session = relationship("ChatSession", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")



