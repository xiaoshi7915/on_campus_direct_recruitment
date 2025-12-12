"""
收藏相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FavoriteCreate(BaseModel):
    """创建收藏请求模式"""
    target_type: str = Field(..., description="收藏类型：JOB, RESUME, ENTERPRISE, SCHOOL")
    target_id: str = Field(..., description="目标ID")


class FavoriteResponse(BaseModel):
    """收藏响应模式"""
    id: str
    user_id: str
    target_type: str
    target_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class FavoriteListResponse(BaseModel):
    """收藏列表响应模式"""
    items: list[FavoriteResponse]
    total: int
    page: int
    page_size: int



