"""
用户档案模型（学生、教师、企业）
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.user_type import UserType


class StudentProfile(Base):
    """
    学生信息表模型
    """
    __tablename__ = "student_profiles"
    
    id = Column(String(36), primary_key=True, comment="学生ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, comment="用户ID")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    student_id = Column(String(50), unique=True, nullable=True, comment="学号")
    school_id = Column(String(36), ForeignKey("schools.id", ondelete="SET NULL"), nullable=True, index=True, comment="学校ID")
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True, index=True, comment="院系ID")
    class_id = Column(String(36), ForeignKey("classes.id", ondelete="SET NULL"), nullable=True, index=True, comment="班级ID")
    grade = Column(String(20), nullable=True, comment="年级")
    major = Column(String(100), nullable=True, comment="专业")
    avatar_url = Column(String(255), nullable=True, comment="头像URL")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="student_profile", uselist=False)
    school = relationship("School", back_populates="students")
    department = relationship("Department", back_populates="students")
    class_ = relationship("Class", back_populates="students")
    resumes = relationship("Resume", back_populates="student", cascade="all, delete-orphan")
    job_intentions = relationship("JobIntention", back_populates="student", cascade="all, delete-orphan")
    # job_applications通过user_id间接关联，不在这里定义
    info_session_registrations = relationship("InfoSessionRegistration", back_populates="student", cascade="all, delete-orphan", foreign_keys="InfoSessionRegistration.student_id")
    interviews = relationship("Interview", back_populates="student")
    offers = relationship("Offer", back_populates="student")


class TeacherProfile(Base):
    """
    教师信息表模型
    """
    __tablename__ = "teacher_profiles"
    
    id = Column(String(36), primary_key=True, comment="教师ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, comment="用户ID")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    school_id = Column(String(36), ForeignKey("schools.id", ondelete="SET NULL"), nullable=True, index=True, comment="学校ID")
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True, index=True, comment="院系ID")
    title = Column(String(50), nullable=True, comment="职称")
    position = Column(String(50), nullable=True, comment="职务名称")
    teaching_major = Column(String(100), nullable=True, comment="授课专业")
    teaching_grade = Column(String(50), nullable=True, comment="授课年级")
    avatar_url = Column(String(255), nullable=True, comment="头像URL")
    is_main_account = Column(Boolean, default=False, nullable=False, comment="是否主账号")
    main_account_id = Column(String(36), ForeignKey("teacher_profiles.id", ondelete="SET NULL"), nullable=True, index=True, comment="主账号ID")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="teacher_profile", uselist=False)
    school = relationship("School", back_populates="teachers")
    department = relationship("Department", back_populates="teachers")
    main_account = relationship("TeacherProfile", remote_side=[id], backref="sub_accounts")


class EnterpriseProfile(Base):
    """
    企业信息表模型
    """
    __tablename__ = "enterprise_profiles"
    
    id = Column(String(36), primary_key=True, comment="企业ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, comment="用户ID")
    company_name = Column(String(100), nullable=False, index=True, comment="公司名称")
    unified_code = Column(String(50), unique=True, nullable=True, comment="统一社会信用代码")
    legal_person = Column(String(50), nullable=True, comment="法人代表")
    industry = Column(String(100), nullable=True, comment="行业")
    scale = Column(String(50), nullable=True, comment="规模")
    address = Column(String(255), nullable=True, comment="地址")
    website = Column(String(255), nullable=True, comment="网站")
    logo_url = Column(String(255), nullable=True, comment="Logo URL")
    description = Column(Text, nullable=True, comment="描述")
    is_verified = Column(Boolean, default=False, nullable=False, index=True, comment="是否认证")
    is_main_account = Column(Boolean, default=False, nullable=False, comment="是否主账号")
    main_account_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="SET NULL"), nullable=True, index=True, comment="主账号ID")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="enterprise_profile", uselist=False)
    jobs = relationship("Job", back_populates="enterprise", cascade="all, delete-orphan")
    job_fairs = relationship("JobFair", back_populates="enterprise", foreign_keys="JobFair.created_by")
    info_sessions = relationship("InfoSession", back_populates="enterprise", cascade="all, delete-orphan")
    job_fair_registrations = relationship("JobFairRegistration", back_populates="enterprise", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="enterprise")
    offers = relationship("Offer", back_populates="enterprise")
    main_account = relationship("EnterpriseProfile", remote_side=[id], backref="sub_accounts")

