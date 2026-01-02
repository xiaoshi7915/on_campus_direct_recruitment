"""
认证相关模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import VerificationStatus
from datetime import datetime


class EnterpriseVerification(Base):
    """
    企业认证申请表模型
    """
    __tablename__ = "enterprise_verifications"
    
    id = Column(String(36), primary_key=True, comment="认证ID")
    enterprise_id = Column(String(36), ForeignKey("enterprise_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="企业ID")
    status = Column(SQLEnum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False, index=True, comment="认证状态")
    
    # 认证材料
    business_license_url = Column(String(255), nullable=True, comment="营业执照URL")
    legal_person_id_front_url = Column(String(255), nullable=True, comment="法人身份证正面URL")
    legal_person_id_back_url = Column(String(255), nullable=True, comment="法人身份证反面URL")
    authorization_letter_url = Column(String(255), nullable=True, comment="授权委托书URL")
    other_documents = Column(Text, nullable=True, comment="其他材料URLs（JSON数组）")
    
    # 审核信息
    reviewer_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="审核人ID")
    review_comment = Column(Text, nullable=True, comment="审核意见")
    reviewed_at = Column(DateTime, nullable=True, comment="审核时间")
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    enterprise = relationship("EnterpriseProfile", back_populates="verifications")
    reviewer = relationship("User", foreign_keys=[reviewer_id])


class PersonalVerification(Base):
    """
    个人身份认证申请表模型
    """
    __tablename__ = "personal_verifications"
    
    id = Column(String(36), primary_key=True, comment="认证ID")
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    user_type = Column(String(20), nullable=False, comment="用户类型（ENTERPRISE, STUDENT等）")
    status = Column(SQLEnum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False, index=True, comment="认证状态")
    
    # 认证材料
    id_card_front_url = Column(String(255), nullable=True, comment="身份证正面URL")
    id_card_back_url = Column(String(255), nullable=True, comment="身份证反面URL")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card_number = Column(String(18), nullable=True, comment="身份证号")
    other_documents = Column(Text, nullable=True, comment="其他材料URLs（JSON数组）")
    
    # 审核信息
    reviewer_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="审核人ID")
    review_comment = Column(Text, nullable=True, comment="审核意见")
    reviewed_at = Column(DateTime, nullable=True, comment="审核时间")
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])


class SchoolVerification(Base):
    """
    学校认证申请表模型
    """
    __tablename__ = "school_verifications"
    
    id = Column(String(36), primary_key=True, comment="认证ID")
    teacher_id = Column(String(36), ForeignKey("teacher_profiles.id", ondelete="CASCADE"), nullable=False, index=True, comment="教师ID")
    school_id = Column(String(36), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True, comment="学校ID")
    status = Column(SQLEnum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False, index=True, comment="认证状态")
    
    # 认证材料
    school_certificate_url = Column(String(255), nullable=True, comment="学校证明文件URL")
    teacher_certificate_url = Column(String(255), nullable=True, comment="教师工作证明URL")
    id_card_front_url = Column(String(255), nullable=True, comment="身份证正面URL")
    id_card_back_url = Column(String(255), nullable=True, comment="身份证反面URL")
    authorization_letter_url = Column(String(255), nullable=True, comment="授权委托书URL")
    other_documents = Column(Text, nullable=True, comment="其他材料URLs（JSON数组）")
    
    # 联系信息
    contact_person = Column(String(50), nullable=True, comment="联系人")
    contact_phone = Column(String(20), nullable=True, comment="联系电话")
    contact_email = Column(String(100), nullable=True, comment="联系邮箱")
    
    # 审核信息
    reviewer_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="审核人ID")
    review_comment = Column(Text, nullable=True, comment="审核意见")
    reviewed_at = Column(DateTime, nullable=True, comment="审核时间")
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关联关系
    teacher = relationship("TeacherProfile", foreign_keys=[teacher_id])
    school = relationship("School", foreign_keys=[school_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])

