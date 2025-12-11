"""
聊天相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageCreate(BaseModel):
    """创建消息请求模式"""
    receiver_id: str = Field(..., description="接收者ID")
    content: str = Field(..., min_length=1, max_length=5000, description="消息内容")
    message_type: str = Field("TEXT", description="消息类型：TEXT, IMAGE, FILE, LOCATION")
    file_url: Optional[str] = Field(None, description="文件URL（如果是文件消息）")


class MessageResponse(BaseModel):
    """消息响应模式"""
    id: str
    session_id: str
    sender_id: str
    receiver_id: str
    content: str
    message_type: str
    file_url: Optional[str]
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    """消息列表响应模式"""
    items: list[MessageResponse]
    total: int
    page: int
    page_size: int


class ChatSessionResponse(BaseModel):
    """聊天会话响应模式"""
    id: str
    user1_id: str
    user2_id: str
    last_message_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatSessionListResponse(BaseModel):
    """聊天会话列表响应模式"""
    items: list[ChatSessionResponse]
    total: int

