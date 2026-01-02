"""
认证相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.enums import VerificationStatus


# ==================== 企业认证 ====================

class EnterpriseVerificationCreate(BaseModel):
    """创建企业认证申请请求模式"""
    business_license_url: Optional[str] = Field(None, description="营业执照URL")
    legal_person_id_front_url: Optional[str] = Field(None, description="法人身份证正面URL")
    legal_person_id_back_url: Optional[str] = Field(None, description="法人身份证反面URL")
    authorization_letter_url: Optional[str] = Field(None, description="授权委托书URL")
    other_documents: Optional[List[str]] = Field(None, description="其他材料URLs")


class EnterpriseVerificationUpdate(BaseModel):
    """更新企业认证申请请求模式（审核用）"""
    status: VerificationStatus = Field(..., description="认证状态")
    review_comment: Optional[str] = Field(None, description="审核意见")


class EnterpriseVerificationResponse(BaseModel):
    """企业认证申请响应模式"""
    id: str
    enterprise_id: str
    enterprise_name: Optional[str] = None  # 企业名称
    status: str
    business_license_url: Optional[str]
    legal_person_id_front_url: Optional[str]
    legal_person_id_back_url: Optional[str]
    authorization_letter_url: Optional[str]
    other_documents: Optional[List[str]]
    reviewer_id: Optional[str]
    review_comment: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EnterpriseVerificationListResponse(BaseModel):
    """企业认证申请列表响应模式"""
    items: List[EnterpriseVerificationResponse]
    total: int
    page: int
    page_size: int


# ==================== 个人身份认证 ====================

class PersonalVerificationCreate(BaseModel):
    """创建个人身份认证申请请求模式"""
    id_card_front_url: Optional[str] = Field(None, description="身份证正面URL")
    id_card_back_url: Optional[str] = Field(None, description="身份证反面URL")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    id_card_number: Optional[str] = Field(None, max_length=18, description="身份证号")
    other_documents: Optional[List[str]] = Field(None, description="其他材料URLs")


class PersonalVerificationUpdate(BaseModel):
    """更新个人身份认证申请请求模式（审核用）"""
    status: VerificationStatus = Field(..., description="认证状态")
    review_comment: Optional[str] = Field(None, description="审核意见")


class PersonalVerificationResponse(BaseModel):
    """个人身份认证申请响应模式"""
    id: str
    user_id: str
    user_type: str
    status: str
    id_card_front_url: Optional[str]
    id_card_back_url: Optional[str]
    real_name: Optional[str]
    id_card_number: Optional[str]
    other_documents: Optional[List[str]]
    reviewer_id: Optional[str]
    review_comment: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PersonalVerificationListResponse(BaseModel):
    """个人身份认证申请列表响应模式"""
    items: List[PersonalVerificationResponse]
    total: int
    page: int
    page_size: int


# ==================== 学校认证 ====================

class SchoolVerificationCreate(BaseModel):
    """创建学校认证申请请求模式"""
    school_id: str = Field(..., description="学校ID")
    school_certificate_url: Optional[str] = Field(None, description="学校证明文件URL")
    teacher_id_card_front_url: Optional[str] = Field(None, description="教师身份证正面URL")
    teacher_id_card_back_url: Optional[str] = Field(None, description="教师身份证反面URL")
    teacher_work_certificate_url: Optional[str] = Field(None, description="教师工作证明URL")
    authorization_letter_url: Optional[str] = Field(None, description="授权委托书URL")
    other_documents: Optional[List[str]] = Field(None, description="其他材料URLs")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=100, description="联系邮箱")


class SchoolVerificationUpdate(BaseModel):
    """更新学校认证申请请求模式（审核用）"""
    status: VerificationStatus = Field(..., description="认证状态")
    review_comment: Optional[str] = Field(None, description="审核意见")


class SchoolVerificationResponse(BaseModel):
    """学校认证申请响应模式"""
    id: str
    teacher_id: str
    teacher_name: Optional[str] = None  # 教师名称
    school_id: str
    school_name: Optional[str] = None  # 学校名称
    status: str
    school_certificate_url: Optional[str]
    teacher_id_card_front_url: Optional[str]
    teacher_id_card_back_url: Optional[str]
    teacher_work_certificate_url: Optional[str]
    authorization_letter_url: Optional[str]
    other_documents: Optional[List[str]]
    contact_person: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    reviewer_id: Optional[str]
    review_comment: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SchoolVerificationListResponse(BaseModel):
    """学校认证申请列表响应模式"""
    items: List[SchoolVerificationResponse]
    total: int
    page: int
    page_size: int

