"""
职位申请相关的Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    """创建申请请求模式"""
    job_id: str = Field(..., description="职位ID")
    resume_id: Optional[str] = Field(None, description="简历ID（可选）")
    message: Optional[str] = Field(None, description="申请留言")


class ApplicationResponse(BaseModel):
    """申请响应模式"""
    id: str
    job_id: str
    resume_id: str
    student_id: str
    status: str
    message: Optional[str]
    created_at: datetime
    updated_at: datetime
    # 关联信息（可选，用于前端显示）
    job_title: Optional[str] = None
    student_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    """申请列表响应模式"""
    items: list[ApplicationResponse]
    total: int
    page: int
    page_size: int


