"""
面试和Offer相关模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import InterviewType, InterviewStatus, OfferStatus


class Interview(Base):
    """
    面试表模型
    """
    __tablename__ = "interviews"
    
    id = Column(String(36), primary_key=True, comment="面试ID")
    application_id = Column(String(36), ForeignKey("job_applications.id", ondelete="CASCADE"), unique=True, nullable=False, comment="申请ID")
    enterprise_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="企业ID")
    student_id = Column(String(36), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    interview_type = Column(String(20), default="VIDEO", nullable=False, comment="面试类型")
    scheduled_time = Column(DateTime, nullable=False, index=True, comment="安排时间")
    duration = Column(Integer, nullable=True, comment="时长（分钟）")
    location = Column(String(255), nullable=True, comment="地点")
    meeting_url = Column(String(255), nullable=True, comment="会议链接")
    status = Column(String(20), default="SCHEDULED", nullable=False, index=True, comment="面试状态")
    feedback = Column(Text, nullable=True, comment="反馈")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    application = relationship("JobApplication", back_populates="interview")
    enterprise = relationship("EnterpriseProfile", back_populates="interviews")
    student = relationship("StudentProfile", back_populates="interviews")
    schedule = relationship(
        "Schedule", 
        back_populates="interview", 
        primaryjoin="and_(Schedule.related_id == Interview.id, Schedule.schedule_type == 'INTERVIEW')",
        foreign_keys="[Schedule.related_id]",
        viewonly=False,
        uselist=False, 
        cascade="all, delete-orphan"
    )


class Offer(Base):
    """
    Offer表模型
    """
    __tablename__ = "offers"
    
    id = Column(String(36), primary_key=True, comment="Offer ID")
    application_id = Column(String(36), ForeignKey("job_applications.id", ondelete="CASCADE"), unique=True, nullable=False, comment="申请ID")
    enterprise_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="企业ID")
    student_id = Column(String(36), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    job_title = Column(String(100), nullable=False, comment="职位名称")
    salary = Column(Integer, nullable=True, comment="薪资")
    start_date = Column(DateTime, nullable=True, comment="入职日期")
    content = Column(Text, nullable=False, comment="Offer内容")
    status = Column(String(20), default="PENDING", nullable=False, index=True, comment="Offer状态")
    expires_at = Column(DateTime, nullable=True, comment="过期时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    application = relationship("JobApplication", back_populates="offer")
    enterprise = relationship("EnterpriseProfile", back_populates="offers")
    student = relationship("StudentProfile", back_populates="offers")

