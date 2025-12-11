"""
待办事项模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Todo(Base):
    """
    待办事项表模型
    """
    __tablename__ = "todos"
    
    id = Column(String(36), primary_key=True, comment="待办ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    title = Column(String(100), nullable=False, comment="标题")
    content = Column(Text, nullable=True, comment="内容")
    priority = Column(String(20), default="MEDIUM", nullable=False, comment="优先级：LOW, MEDIUM, HIGH")
    due_date = Column(DateTime, nullable=True, comment="截止日期")
    is_completed = Column(Boolean, default=False, nullable=False, index=True, comment="是否完成")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="todos")



