"""
待办事项相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoCreate(BaseModel):
    """创建待办事项请求模式"""
    title: str = Field(..., min_length=1, max_length=100, description="标题")
    content: Optional[str] = Field(None, description="内容")
    priority: str = Field("MEDIUM", description="优先级：LOW, MEDIUM, HIGH")
    due_date: Optional[datetime] = Field(None, description="截止日期")


class TodoUpdate(BaseModel):
    """更新待办事项请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="标题")
    content: Optional[str] = Field(None, description="内容")
    priority: Optional[str] = Field(None, description="优先级")
    due_date: Optional[datetime] = Field(None, description="截止日期")
    is_completed: Optional[bool] = Field(None, description="是否完成")


class TodoResponse(BaseModel):
    """待办事项响应模式"""
    id: str
    user_id: str
    title: str
    content: Optional[str]
    priority: str
    due_date: Optional[datetime]
    is_completed: bool
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """待办事项列表响应模式"""
    items: list[TodoResponse]
    total: int
    page: int
    page_size: int



