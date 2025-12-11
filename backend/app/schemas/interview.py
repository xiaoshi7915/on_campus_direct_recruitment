"""
面试和Offer相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InterviewCreate(BaseModel):
    """创建面试请求模式"""
    application_id: str = Field(..., description="申请ID")
    interview_type: str = Field("VIDEO", description="面试类型：VIDEO, PHONE, ONSITE")
    scheduled_time: datetime = Field(..., description="安排时间")
    duration: Optional[int] = Field(None, ge=1, description="时长（分钟）")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    meeting_url: Optional[str] = Field(None, max_length=255, description="会议链接")


class InterviewUpdate(BaseModel):
    """更新面试请求模式"""
    interview_type: Optional[str] = Field(None, description="面试类型")
    scheduled_time: Optional[datetime] = Field(None, description="安排时间")
    duration: Optional[int] = Field(None, ge=1, description="时长（分钟）")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    meeting_url: Optional[str] = Field(None, max_length=255, description="会议链接")
    status: Optional[str] = Field(None, description="面试状态：SCHEDULED, CONFIRMED, COMPLETED, CANCELLED, NO_SHOW")
    feedback: Optional[str] = Field(None, description="反馈")


class InterviewResponse(BaseModel):
    """面试响应模式"""
    id: str
    application_id: str
    enterprise_id: str
    student_id: str
    interview_type: str
    scheduled_time: datetime
    duration: Optional[int]
    location: Optional[str]
    meeting_url: Optional[str]
    status: str
    feedback: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InterviewListResponse(BaseModel):
    """面试列表响应模式"""
    items: list[InterviewResponse]
    total: int
    page: int
    page_size: int


class OfferCreate(BaseModel):
    """创建Offer请求模式"""
    application_id: str = Field(..., description="申请ID")
    job_title: str = Field(..., min_length=1, max_length=100, description="职位名称")
    salary: Optional[int] = Field(None, ge=0, description="薪资")
    start_date: Optional[datetime] = Field(None, description="入职日期")
    content: str = Field(..., min_length=1, description="Offer内容")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class OfferUpdate(BaseModel):
    """更新Offer请求模式"""
    job_title: Optional[str] = Field(None, min_length=1, max_length=100, description="职位名称")
    salary: Optional[int] = Field(None, ge=0, description="薪资")
    start_date: Optional[datetime] = Field(None, description="入职日期")
    content: Optional[str] = Field(None, min_length=1, description="Offer内容")
    status: Optional[str] = Field(None, description="Offer状态：PENDING, ACCEPTED, REJECTED, EXPIRED")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class OfferResponse(BaseModel):
    """Offer响应模式"""
    id: str
    application_id: str
    enterprise_id: str
    student_id: str
    job_title: str
    salary: Optional[int]
    start_date: Optional[datetime]
    content: str
    status: str
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OfferListResponse(BaseModel):
    """Offer列表响应模式"""
    items: list[OfferResponse]
    total: int
    page: int
    page_size: int



