"""
日程相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ScheduleCreate(BaseModel):
    """创建日程请求模式"""
    title: str = Field(..., min_length=1, max_length=100, description="标题")
    content: Optional[str] = Field(None, description="内容")
    start_time: datetime = Field(..., description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    schedule_type: str = Field(..., description="日程类型：JOB_FAIR, INFO_SESSION, INTERVIEW, CUSTOM")
    related_id: Optional[str] = Field(None, description="关联ID")
    reminder_time: Optional[datetime] = Field(None, description="提醒时间")


class ScheduleUpdate(BaseModel):
    """更新日程请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="标题")
    content: Optional[str] = Field(None, description="内容")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    schedule_type: Optional[str] = Field(None, description="日程类型")
    related_id: Optional[str] = Field(None, description="关联ID")
    reminder_time: Optional[datetime] = Field(None, description="提醒时间")
    is_completed: Optional[bool] = Field(None, description="是否完成")


class ScheduleResponse(BaseModel):
    """日程响应模式"""
    id: str
    user_id: str
    title: str
    content: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    schedule_type: str
    related_id: Optional[str]
    reminder_time: Optional[datetime]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ScheduleListResponse(BaseModel):
    """日程列表响应模式"""
    items: list[ScheduleResponse]
    total: int
    page: int
    page_size: int



