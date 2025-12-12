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

