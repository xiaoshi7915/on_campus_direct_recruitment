"""
行业职位类型维表模型
用于存储行业和职位类型的关联关系
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class IndustryCategory(Base):
    """
    行业分类表（一级行业）
    """
    __tablename__ = "industry_categories"
    
    id = Column(String(36), primary_key=True, comment="行业分类ID")
    name = Column(String(100), nullable=False, unique=True, comment="行业分类名称")
    code = Column(String(50), nullable=True, unique=True, comment="行业分类代码")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
    # 关联关系
    sub_industries = relationship("SubIndustry", back_populates="category", cascade="all, delete-orphan")
    job_types = relationship("JobType", back_populates="industry_category", cascade="all, delete-orphan")


class SubIndustry(Base):
    """
    细分行业表（二级行业）
    """
    __tablename__ = "sub_industries"
    
    id = Column(String(36), primary_key=True, comment="细分行业ID")
    category_id = Column(String(36), ForeignKey("industry_categories.id", ondelete="CASCADE"), nullable=False, index=True, comment="行业分类ID")
    name = Column(String(100), nullable=False, comment="细分行业名称")
    code = Column(String(50), nullable=True, comment="细分行业代码")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
    # 关联关系
    category = relationship("IndustryCategory", back_populates="sub_industries")
    job_types = relationship("JobType", back_populates="sub_industry", cascade="all, delete-orphan")
    
    # 索引
    __table_args__ = (
        Index('idx_category_id', 'category_id'),
    )


class JobType(Base):
    """
    职位类型表
    """
    __tablename__ = "job_types"
    
    id = Column(String(36), primary_key=True, comment="职位类型ID")
    category_id = Column(String(36), ForeignKey("industry_categories.id", ondelete="CASCADE"), nullable=True, index=True, comment="行业分类ID（可为空，表示通用职位）")
    sub_industry_id = Column(String(36), ForeignKey("sub_industries.id", ondelete="CASCADE"), nullable=True, index=True, comment="细分行业ID（可为空）")
    name = Column(String(100), nullable=False, comment="职位类型名称")
    code = Column(String(50), nullable=True, comment="职位类型代码")
    description = Column(Text, nullable=True, comment="职位类型描述")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
    # 关联关系
    industry_category = relationship("IndustryCategory", back_populates="job_types")
    sub_industry = relationship("SubIndustry", back_populates="job_types")
    
    # 索引
    __table_args__ = (
        Index('idx_category_id', 'category_id'),
        Index('idx_sub_industry_id', 'sub_industry_id'),
    )

