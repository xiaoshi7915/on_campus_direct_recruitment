"""
标记相关模型（用于标记简历、学校等）
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Mark(Base):
    """
    标记表模型
    """
    __tablename__ = "marks"
    
    id = Column(String(36), primary_key=True, comment="标记ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    target_type = Column(String(20), nullable=False, index=True, comment="标记类型：RESUME, SCHOOL等")
    target_id = Column(String(36), nullable=False, index=True, comment="目标ID")
    note = Column(Text, nullable=True, comment="备注")
    color = Column(String(20), nullable=True, default="blue", comment="标记颜色")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="marks")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'target_type', 'target_id', name='uq_mark'),
        Index('idx_mark_target', 'target_type', 'target_id'),
        {"comment": "标记表"},
    )



