"""
通用模型（收藏、日程、反馈）
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, UniqueConstraint, Index, and_
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import FavoriteType, ScheduleType, FeedbackStatus


class Favorite(Base):
    """
    收藏表模型
    """
    __tablename__ = "favorites"
    
    id = Column(String(36), primary_key=True, comment="收藏ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    target_type = Column(String(20), nullable=False, index=True, comment="收藏类型")
    target_id = Column(String(36), nullable=False, index=True, comment="目标ID")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    
    # 关联关系
    user = relationship("User", back_populates="favorites")
    # job和resume通过target_type和target_id动态关联，不在这里定义relationship
    
    __table_args__ = (
        UniqueConstraint('user_id', 'target_type', 'target_id', name='uq_favorite'),
        {"comment": "收藏表"},
    )


class Schedule(Base):
    """
    日程表模型
    """
    __tablename__ = "schedules"
    
    id = Column(String(36), primary_key=True, comment="日程ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    title = Column(String(100), nullable=False, comment="标题")
    content = Column(Text, nullable=True, comment="内容")
    start_time = Column(DateTime, nullable=False, index=True, comment="开始时间")
    end_time = Column(DateTime, nullable=True, comment="结束时间")
    schedule_type = Column(String(20), nullable=False, index=True, comment="日程类型")
    related_id = Column(String(36), nullable=True, index=True, comment="关联ID")
    reminder_time = Column(DateTime, nullable=True, comment="提醒时间")
    is_completed = Column(Boolean, default=False, nullable=False, comment="是否完成")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="schedules")
    # job_fair 和 info_session 通过 related_id 动态关联，使用 viewonly 避免外键检查
    job_fair = relationship(
        "JobFair", 
        back_populates="schedules",
        primaryjoin="and_(Schedule.related_id == JobFair.id, Schedule.schedule_type == 'JOB_FAIR')",
        foreign_keys="[Schedule.related_id]",
        viewonly=True,
        uselist=False
    )
    info_session = relationship(
        "InfoSession", 
        back_populates="schedules",
        primaryjoin="and_(Schedule.related_id == InfoSession.id, Schedule.schedule_type == 'INFO_SESSION')",
        foreign_keys="[Schedule.related_id]",
        viewonly=True,
        uselist=False
    )
    interview = relationship(
        "Interview", 
        back_populates="schedule",
        primaryjoin="and_(Schedule.related_id == Interview.id, Schedule.schedule_type == 'INTERVIEW')",
        foreign_keys="[Schedule.related_id]",
        viewonly=True,
        uselist=False
    )
    
    __table_args__ = (
        Index('idx_schedule_type_related', 'schedule_type', 'related_id'),
        {"comment": "日程表"},
    )


class Feedback(Base):
    """
    反馈建议表模型
    """
    __tablename__ = "feedbacks"
    
    id = Column(String(36), primary_key=True, comment="反馈ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    user_type = Column(String(20), nullable=False, comment="用户类型")
    title = Column(String(100), nullable=False, comment="标题")
    content = Column(Text, nullable=False, comment="内容")
    images = Column(String(500), nullable=True, comment="图片URLs（逗号分隔）")
    status = Column(String(20), default="PENDING", nullable=False, index=True, comment="状态")
    reply = Column(Text, nullable=True, comment="回复")
    replied_at = Column(DateTime, nullable=True, comment="回复时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="feedbacks")

