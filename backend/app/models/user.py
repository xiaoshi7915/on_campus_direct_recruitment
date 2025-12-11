"""
用户模型
"""
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.user_type import UserType
from app.models.enums import UserStatus


class User(Base):
    """
    用户表模型
    """
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    phone = Column(String(20), unique=True, nullable=True, index=True, comment="手机号")
    email = Column(String(100), unique=True, nullable=True, index=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    user_type = Column(SQLEnum(UserType), nullable=False, index=True, comment="用户类型")
    status = Column(String(20), default="ACTIVE", nullable=False, comment="用户状态")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher_profile = relationship("TeacherProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    enterprise_profile = relationship("EnterpriseProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # 消息和聊天
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    chat_sessions_user1 = relationship("ChatSession", foreign_keys="ChatSession.user1_id", back_populates="user1")
    chat_sessions_user2 = relationship("ChatSession", foreign_keys="ChatSession.user2_id", back_populates="user2")
    
    # 其他关联
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="user", cascade="all, delete-orphan")
    job_applications = relationship("JobApplication", back_populates="user", foreign_keys="JobApplication.student_id", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")

