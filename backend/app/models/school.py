"""
学校、院系、班级模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class School(Base):
    """
    学校表模型
    """
    __tablename__ = "schools"
    
    id = Column(String(36), primary_key=True, comment="学校ID")
    name = Column(String(100), unique=True, nullable=False, index=True, comment="学校名称")
    code = Column(String(50), unique=True, nullable=True, comment="学校代码")
    province = Column(String(50), nullable=True, comment="省份")
    city = Column(String(50), nullable=True, comment="城市")
    address = Column(String(255), nullable=True, comment="地址")
    website = Column(String(255), nullable=True, comment="网站")
    logo_url = Column(String(255), nullable=True, comment="Logo URL")
    description = Column(Text, nullable=True, comment="描述")
    is_verified = Column(Boolean, default=False, nullable=False, comment="是否认证")
    # 新增字段：主管部门、院系介绍、主要专业介绍
    charge_dep = Column(String(255), nullable=True, comment="主管部门")
    department = Column(Text, nullable=True, comment="院系介绍")
    major = Column(Text, nullable=True, comment="主要专业介绍")
    # 扩展字段：双一流、211/985、学校类型、办学性质、办学层次等
    dual_class = Column(String(255), nullable=True, comment="双一流建设学科代码")
    dual_class_name = Column(String(255), nullable=True, comment="双一流建设学科名称")
    f211 = Column(String(255), nullable=True, comment="是否211（是/否）")
    f985 = Column(String(255), nullable=True, comment="是否985（是/否）")
    school_type = Column(String(255), nullable=True, comment="类型代码")
    school_type_name = Column(String(255), nullable=True, comment="类型名称")
    nature = Column(String(255), nullable=True, comment="办学性质代码")
    nature_name = Column(String(255), nullable=True, comment="办学性质（公办、民办、中外合作等）")
    is_top = Column(String(255), nullable=True, comment="是否顶尖高校（是/否）")
    level = Column(String(255), nullable=True, comment="办学层次代码")
    level_name = Column(String(255), nullable=True, comment="办学层次名称（本科、专科）")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    departments = relationship("Department", back_populates="school", cascade="all, delete-orphan")
    students = relationship("StudentProfile", back_populates="school")
    teachers = relationship("TeacherProfile", back_populates="school")
    chat_sessions = relationship("ChatSession", foreign_keys="ChatSession.school_id", back_populates="school")


class Department(Base):
    """
    院系表模型
    """
    __tablename__ = "departments"
    
    id = Column(String(36), primary_key=True, comment="院系ID")
    school_id = Column(String(36), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True, comment="学校ID")
    name = Column(String(100), nullable=False, comment="院系名称")
    code = Column(String(50), nullable=True, comment="院系代码")
    description = Column(Text, nullable=True, comment="描述")
    honors = Column(Text, nullable=True, comment="资质荣誉")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    school = relationship("School", back_populates="departments")
    classes = relationship("Class", back_populates="department", cascade="all, delete-orphan")
    students = relationship("StudentProfile", back_populates="department")
    teachers = relationship("TeacherProfile", back_populates="department")
    
    __table_args__ = (
        {"comment": "院系表"},
    )


class Class(Base):
    """
    班级表模型
    """
    __tablename__ = "classes"
    
    id = Column(String(36), primary_key=True, comment="班级ID")
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True, comment="院系ID")
    name = Column(String(100), nullable=False, comment="班级名称")
    grade = Column(String(20), nullable=True, comment="年级")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    department = relationship("Department", back_populates="classes")
    students = relationship("StudentProfile", back_populates="class_")
    
    __table_args__ = (
        {"comment": "班级表"},
    )



