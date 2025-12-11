"""
企业人才库表模型
用于保存企业触达过的学生信息
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TalentPool(Base):
    """
    企业人才库表模型
    用于保存企业触达过的学生信息，方便快速查询和管理
    """
    __tablename__ = "talent_pools"
    
    id = Column(String(36), primary_key=True, comment="人才库ID")
    enterprise_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="企业ID")
    student_id = Column(String(36), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="学生ID")
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True, comment="简历ID")
    
    # 状态信息
    status = Column(String(20), default="ALL", nullable=False, index=True, comment="状态：ALL, FAVORITED, COMMUNICATING, INTERVIEWED, HIRED")
    
    # 关联信息
    application_id = Column(String(36), ForeignKey("job_applications.id", ondelete="SET NULL"), nullable=True, comment="申请ID")
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="SET NULL"), nullable=True, comment="面试ID")
    offer_id = Column(String(36), ForeignKey("offers.id", ondelete="SET NULL"), nullable=True, comment="Offer ID")
    
    # 备注信息
    notes = Column(Text, nullable=True, comment="备注")
    tags = Column(String(255), nullable=True, comment="标签（逗号分隔）")
    
    # 时间信息
    first_contact_time = Column(DateTime, nullable=True, comment="首次接触时间")
    last_contact_time = Column(DateTime, nullable=True, index=True, comment="最后联系时间")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系（不使用外键约束，避免字符集问题）
    enterprise = relationship("EnterpriseProfile", foreign_keys=[enterprise_id], back_populates="talent_pools")
    student = relationship("StudentProfile", foreign_keys=[student_id], back_populates="talent_pools")
    resume = relationship("Resume", foreign_keys=[resume_id])
    application = relationship("JobApplication", foreign_keys=[application_id])
    interview = relationship("Interview", foreign_keys=[interview_id])
    offer = relationship("Offer", foreign_keys=[offer_id])
    
    __table_args__ = (
        UniqueConstraint('enterprise_id', 'student_id', name='uq_enterprise_student'),
        Index('idx_enterprise_status', 'enterprise_id', 'status'),
        Index('idx_last_contact_time', 'last_contact_time'),
        {"comment": "企业人才库表"},
    )

