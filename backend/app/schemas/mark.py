"""
标记相关的Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MarkCreate(BaseModel):
    """创建标记请求模式"""
    target_type: str = Field(..., description="标记类型：RESUME, SCHOOL等")
    target_id: str = Field(..., description="目标ID")
    note: Optional[str] = Field(None, description="备注")
    color: Optional[str] = Field("blue", description="标记颜色：blue, red, green, yellow, purple")


class MarkUpdate(BaseModel):
    """更新标记请求模式"""
    note: Optional[str] = Field(None, description="备注")
    color: Optional[str] = Field(None, description="标记颜色")


class MarkResponse(BaseModel):
    """标记响应模式"""
    id: str
    user_id: str
    target_type: str
    target_id: str
    note: Optional[str]
    color: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MarkListResponse(BaseModel):
    """标记列表响应模式"""
    items: list[MarkResponse]
    total: int
    page: int
    page_size: int



