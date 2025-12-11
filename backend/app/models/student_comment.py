"""
学生点评相关模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class StudentComment(Base):
    """
    学生点评表模型
    """
    __tablename__ = "student_comments"
    
    id = Column(String(36), primary_key=True, comment="点评ID")
    teacher_id = Column(String(36), ForeignKey("teacher_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="教师ID")
    student_id = Column(String(36), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    content = Column(Text, nullable=False, comment="点评内容")
    score = Column(Integer, nullable=True, comment="评分（1-5分）")
    tags = Column(String(255), nullable=True, comment="标签（逗号分隔，如：学习能力强,团队合作好）")
    is_public = Column(String(20), default="PRIVATE", nullable=False, comment="是否公开（PRIVATE-仅教师可见，PUBLIC-公开）")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    teacher = relationship("TeacherProfile", backref="student_comments")
    student = relationship("StudentProfile", backref="comments")
    
    __table_args__ = (
        {"comment": "学生点评表"},
    )



