"""
活动相关模型（双选会、宣讲会）
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import JobFairStatus, SessionType, SessionStatus, RegistrationStatus


class JobFair(Base):
    """
    双选会表模型
    """
    __tablename__ = "job_fairs"
    
    id = Column(String(36), primary_key=True, comment="双选会ID")
    school_id = Column(String(36), ForeignKey("schools.id", ondelete="SET NULL"), nullable=True, index=True, comment="学校ID")
    title = Column(String(100), nullable=False, comment="双选会标题")
    description = Column(Text, nullable=True, comment="描述")
    start_time = Column(DateTime, nullable=False, index=True, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    location = Column(String(255), nullable=True, comment="地点")
    status = Column(String(20), default="DRAFT", nullable=False, index=True, comment="状态")
    max_enterprises = Column(Integer, nullable=True, comment="最大企业数")
    created_by = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="SET NULL"), nullable=True, comment="创建者ID")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    school = relationship("School", backref="job_fairs")
    enterprise = relationship("EnterpriseProfile", back_populates="job_fairs", foreign_keys=[created_by])
    registrations = relationship("JobFairRegistration", back_populates="job_fair", cascade="all, delete-orphan")
    schedules = relationship(
        "Schedule", 
        back_populates="job_fair", 
        primaryjoin="and_(Schedule.related_id == JobFair.id, Schedule.schedule_type == 'JOB_FAIR')",
        foreign_keys="[Schedule.related_id]",
        viewonly=False,
        cascade="all, delete-orphan"
    )


class JobFairRegistration(Base):
    """
    双选会报名表模型
    """
    __tablename__ = "job_fair_registrations"
    
    id = Column(String(36), primary_key=True, comment="报名ID")
    job_fair_id = Column(String(36), ForeignKey("job_fairs.id", ondelete="CASCADE"), nullable=False, index=True, comment="双选会ID")
    enterprise_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="企业ID")
    status = Column(String(20), default="PENDING", nullable=False, comment="报名状态")
    check_in_time = Column(DateTime, nullable=True, comment="签到时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    
    # 关联关系
    job_fair = relationship("JobFair", back_populates="registrations")
    enterprise = relationship("EnterpriseProfile", back_populates="job_fair_registrations")
    
    __table_args__ = (
        UniqueConstraint('job_fair_id', 'enterprise_id', name='uq_job_fair_enterprise'),
        {"comment": "双选会报名表"},
    )


class InfoSession(Base):
    """
    宣讲会表模型
    """
    __tablename__ = "info_sessions"
    
    id = Column(String(36), primary_key=True, comment="宣讲会ID")
    enterprise_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="企业ID")
    school_id = Column(String(36), ForeignKey("schools.id", ondelete="SET NULL"), nullable=True, index=True, comment="学校ID")
    title = Column(String(100), nullable=False, comment="宣讲会标题")
    description = Column(Text, nullable=True, comment="描述")
    start_time = Column(DateTime, nullable=False, index=True, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    location = Column(String(255), nullable=True, comment="地点")
    session_type = Column(String(20), default="OFFLINE", nullable=False, comment="宣讲会类型")
    live_url = Column(String(255), nullable=True, comment="直播链接")
    status = Column(String(20), default="DRAFT", nullable=False, index=True, comment="状态")
    max_students = Column(Integer, nullable=True, comment="最大学生数")
    check_in_count = Column(Integer, default=0, nullable=False, comment="签到人数")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    enterprise = relationship("EnterpriseProfile", back_populates="info_sessions")
    school = relationship("School", backref="info_sessions")
    registrations = relationship("InfoSessionRegistration", back_populates="session", cascade="all, delete-orphan")
    schedules = relationship(
        "Schedule", 
        back_populates="info_session", 
        primaryjoin="and_(Schedule.related_id == InfoSession.id, Schedule.schedule_type == 'INFO_SESSION')",
        foreign_keys="[Schedule.related_id]",
        viewonly=False,
        cascade="all, delete-orphan"
    )


class InfoSessionRegistration(Base):
    """
    宣讲会报名表模型
    """
    __tablename__ = "info_session_registrations"
    
    id = Column(String(36), primary_key=True, comment="报名ID")
    session_id = Column(String(36), ForeignKey("info_sessions.id", ondelete="CASCADE"), nullable=False, index=True, comment="宣讲会ID")
    student_id = Column(String(36), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    status = Column(String(20), default="PENDING", nullable=False, comment="报名状态")
    check_in_time = Column(DateTime, nullable=True, comment="签到时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    
    # 关联关系
    session = relationship("InfoSession", back_populates="registrations")
    student = relationship("StudentProfile", back_populates="info_session_registrations")
    
    __table_args__ = (
        UniqueConstraint('session_id', 'student_id', name='uq_session_student'),
        {"comment": "宣讲会报名表"},
    )

