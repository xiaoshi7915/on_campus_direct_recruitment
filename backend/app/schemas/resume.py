"""
简历相关的Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ResumeCreate(BaseModel):
    """创建简历请求模式"""
    title: str = Field(..., min_length=1, max_length=100, description="简历标题")
    content: str = Field(..., min_length=1, description="简历内容")
    file_url: Optional[str] = Field(None, max_length=500, description="电子版简历文件URL")
    is_default: bool = Field(False, description="是否设为默认简历")


class ResumeUpdate(BaseModel):
    """更新简历请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="简历标题")
    content: Optional[str] = Field(None, min_length=1, description="简历内容")
    file_url: Optional[str] = Field(None, max_length=500, description="电子版简历文件URL")
    is_default: Optional[bool] = Field(None, description="是否设为默认简历")


class ResumeResponse(BaseModel):
    """简历响应模式"""
    id: str
    student_id: str
    title: str
    content: str
    file_url: Optional[str] = None
    is_default: bool
    view_count: int
    download_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ResumeListResponse(BaseModel):
    """简历列表响应模式"""
    items: list[ResumeResponse]
    total: int
    page: int
    page_size: int


