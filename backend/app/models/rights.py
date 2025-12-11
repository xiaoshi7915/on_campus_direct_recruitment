"""
权益相关模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean, Numeric, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import RightsType, PurchaseStatus


class Rights(Base):
    """
    权益表模型
    """
    __tablename__ = "rights"
    
    id = Column(String(36), primary_key=True, comment="权益ID")
    name = Column(String(100), unique=True, nullable=False, comment="权益名称")
    code = Column(String(50), unique=True, nullable=False, index=True, comment="权益代码")
    description = Column(Text, nullable=True, comment="描述")
    type = Column(String(20), nullable=False, index=True, comment="权益类型")
    value = Column(Integer, nullable=True, comment="权益值")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    package_items = relationship("RightsPackageItem", back_populates="rights", cascade="all, delete-orphan")
    user_rights = relationship("UserRights", back_populates="rights", cascade="all, delete-orphan")


class RightsPackage(Base):
    """
    权益套餐表模型
    """
    __tablename__ = "rights_packages"
    
    id = Column(String(36), primary_key=True, comment="套餐ID")
    name = Column(String(100), unique=True, nullable=False, comment="套餐名称")
    description = Column(Text, nullable=True, comment="描述")
    price = Column(Numeric(10, 2), nullable=False, comment="价格")
    duration_days = Column(Integer, nullable=True, comment="时长（天）")
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="是否激活")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    items = relationship("RightsPackageItem", back_populates="package", cascade="all, delete-orphan")
    purchases = relationship("RightsPurchase", back_populates="package")


class RightsPackageItem(Base):
    """
    权益套餐项表模型
    """
    __tablename__ = "rights_package_items"
    
    id = Column(String(36), primary_key=True, comment="套餐项ID")
    package_id = Column(String(36), ForeignKey("rights_packages.id", ondelete="CASCADE"), nullable=False, index=True, comment="套餐ID")
    rights_id = Column(String(36), ForeignKey("rights.id", ondelete="CASCADE"), nullable=False, comment="权益ID")
    quantity = Column(Integer, default=1, nullable=False, comment="数量")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    
    # 关联关系
    package = relationship("RightsPackage", back_populates="items")
    rights = relationship("Rights", back_populates="package_items")
    
    __table_args__ = (
        UniqueConstraint('package_id', 'rights_id', name='uq_package_rights'),
        {"comment": "权益套餐项表"},
    )


class UserRights(Base):
    """
    用户权益表模型
    """
    __tablename__ = "user_rights"
    
    id = Column(String(36), primary_key=True, comment="用户权益ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    rights_id = Column(String(36), ForeignKey("rights.id", ondelete="CASCADE"), nullable=False, comment="权益ID")
    quantity = Column(Integer, default=0, nullable=False, comment="数量")
    expires_at = Column(DateTime, nullable=True, index=True, comment="过期时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", backref="user_rights")
    rights = relationship("Rights", back_populates="user_rights")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'rights_id', name='uq_user_rights'),
        {"comment": "用户权益表"},
    )


class RightsPurchase(Base):
    """
    权益购买表模型
    """
    __tablename__ = "rights_purchases"
    
    id = Column(String(36), primary_key=True, comment="购买ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    package_id = Column(String(36), ForeignKey("rights_packages.id", ondelete="CASCADE"), nullable=False, comment="套餐ID")
    amount = Column(Numeric(10, 2), nullable=False, comment="金额")
    status = Column(String(20), default="PENDING", nullable=False, index=True, comment="购买状态")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", backref="rights_purchases")
    package = relationship("RightsPackage", back_populates="purchases")

