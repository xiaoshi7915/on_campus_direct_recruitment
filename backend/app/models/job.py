"""
职位相关模型（职位、简历、求职意向、职位申请）
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import JobStatus, ApplicationStatus


class Resume(Base):
    """
    简历表模型
    """
    __tablename__ = "resumes"
    
    id = Column(String(36), primary_key=True, comment="简历ID")
    student_id = Column(String(36), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    title = Column(String(100), nullable=False, comment="简历标题")
    content = Column(Text, nullable=False, comment="简历内容")
    file_url = Column(String(500), nullable=True, comment="电子版简历文件URL（PDF、Word等）")
    is_default = Column(Boolean, default=False, nullable=False, index=True, comment="是否默认简历")
    view_count = Column(Integer, default=0, nullable=False, comment="查看次数")
    download_count = Column(Integer, default=0, nullable=False, comment="下载次数")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    student = relationship("StudentProfile", back_populates="resumes")
    job_applications = relationship("JobApplication", back_populates="resume", cascade="all, delete-orphan")
    # favorites通过target_type和target_id动态关联


class Job(Base):
    """
    职位表模型
    """
    __tablename__ = "jobs"
    
    id = Column(String(36), primary_key=True, comment="职位ID")
    enterprise_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="企业ID")
    title = Column(String(100), nullable=False, comment="职位标题")
    department = Column(String(50), nullable=True, comment="部门")
    job_type = Column(String(50), nullable=True, comment="职位类型")
    salary_min = Column(Integer, nullable=True, comment="最低薪资")
    salary_max = Column(Integer, nullable=True, comment="最高薪资")
    work_location = Column(String(100), nullable=True, comment="工作地点")
    experience = Column(String(50), nullable=True, comment="工作经验要求")
    education = Column(String(50), nullable=True, comment="学历要求")
    description = Column(Text, nullable=False, comment="职位描述")
    requirements = Column(Text, nullable=True, comment="职位要求")
    status = Column(String(20), default="DRAFT", nullable=False, index=True, comment="职位状态")
    view_count = Column(Integer, default=0, nullable=False, comment="查看次数")
    apply_count = Column(Integer, default=0, nullable=False, comment="申请次数")
    tags = Column(String(255), nullable=True, comment="标签")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    enterprise = relationship("EnterpriseProfile", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    # favorites通过target_type和target_id动态关联


class JobIntention(Base):
    """
    求职意向表模型
    """
    __tablename__ = "job_intentions"
    
    id = Column(String(36), primary_key=True, comment="求职意向ID")
    student_id = Column(String(36), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    
    # 旧字段（保留兼容性）
    job_type = Column(String(50), nullable=True, comment="职位类型（旧字段，已废弃）")
    industry = Column(String(100), nullable=True, comment="行业（旧字段，已废弃）")
    salary_expect = Column(Integer, nullable=True, comment="期望薪资（旧字段，已废弃）")
    work_location = Column(String(100), nullable=True, comment="工作地点（旧字段，已废弃）")
    
    # 新字段
    job_type_list = Column(Text, nullable=True, comment="职位类型列表（JSON数组）")
    industry_list = Column(Text, nullable=True, comment="行业列表（JSON数组，包含一级和二级行业）")
    work_location_list = Column(Text, nullable=True, comment="工作地点列表（JSON数组）")
    job_nature = Column(String(20), nullable=True, comment="求职类型：FULL_TIME（全职）、PART_TIME（兼职）")
    salary_min = Column(Integer, nullable=True, comment="期望薪资最小值（单位：千元/月）")
    salary_max = Column(Integer, nullable=True, comment="期望薪资最大值（单位：千元/月）")
    part_time_days = Column(String(50), nullable=True, comment="兼职每周工作天数（如：1-2天、3-4天、5天）")
    work_time_slot = Column(String(50), nullable=True, comment="兼职工作时间段（如：工作日、周末、晚上、灵活）")
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    student = relationship("StudentProfile", back_populates="job_intentions")


class JobApplication(Base):
    """
    职位申请表模型
    """
    __tablename__ = "job_applications"
    
    id = Column(String(36), primary_key=True, comment="申请ID")
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True, comment="职位ID")
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, comment="简历ID")
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    status = Column(String(20), default="PENDING", nullable=False, index=True, comment="申请状态")
    message = Column(Text, nullable=True, comment="申请留言")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume", back_populates="job_applications")
    user = relationship("User", back_populates="job_applications", foreign_keys=[student_id])
    # 注意：student_id关联到users表，但我们也需要关联到student_profiles
    # 这里通过user_id间接关联
    interview = relationship("Interview", back_populates="application", uselist=False, cascade="all, delete-orphan")
    offer = relationship("Offer", back_populates="application", uselist=False, cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('job_id', 'student_id', name='uq_job_student'),
        {"comment": "职位申请表"},
    )

