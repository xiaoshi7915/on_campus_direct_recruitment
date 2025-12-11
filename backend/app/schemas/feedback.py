"""
反馈建议相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FeedbackCreate(BaseModel):
    """创建反馈请求模式"""
    title: str = Field(..., min_length=1, max_length=100, description="标题")
    content: str = Field(..., min_length=1, description="内容")
    images: Optional[str] = Field(None, max_length=500, description="图片URLs（逗号分隔）")


class FeedbackUpdate(BaseModel):
    """更新反馈请求模式（管理员用）"""
    status: Optional[str] = Field(None, description="状态：PENDING, PROCESSING, RESOLVED, REJECTED")
    reply: Optional[str] = Field(None, description="回复内容")


class FeedbackResponse(BaseModel):
    """反馈响应模式"""
    id: str
    user_id: str
    user_type: str
    title: str
    content: str
    images: Optional[str]
    status: str
    reply: Optional[str]
    replied_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackListResponse(BaseModel):
    """反馈列表响应模式"""
    items: list[FeedbackResponse]
    total: int
    page: int
    page_size: int


