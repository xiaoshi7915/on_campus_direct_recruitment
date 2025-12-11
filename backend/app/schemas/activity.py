"""
活动相关Pydantic模式（双选会、宣讲会）
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import json


# ==================== 双选会相关 ====================

class JobFairCreate(BaseModel):
    """创建双选会请求模式"""
    title: str = Field(..., min_length=1, max_length=100, description="双选会标题")
    description: Optional[str] = Field(None, description="描述")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    school_id: Optional[str] = Field(None, description="学校ID")
    max_enterprises: Optional[int] = Field(None, ge=1, description="最大企业数")


class JobFairUpdate(BaseModel):
    """更新双选会请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="双选会标题")
    description: Optional[str] = Field(None, description="描述")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    school_id: Optional[str] = Field(None, description="学校ID")
    max_enterprises: Optional[int] = Field(None, ge=1, description="最大企业数")
    status: Optional[str] = Field(None, description="状态：DRAFT, PUBLISHED, ONGOING, ENDED, CANCELLED")


class JobFairResponse(BaseModel):
    """双选会响应模式"""
    id: str
    school_id: Optional[str]
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    status: str
    max_enterprises: Optional[int]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobFairListResponse(BaseModel):
    """双选会列表响应模式"""
    items: list[JobFairResponse]
    total: int
    page: int
    page_size: int


class JobFairRegistrationCreate(BaseModel):
    """双选会报名请求模式"""
    job_fair_id: str = Field(..., description="双选会ID")


class JobFairRegistrationResponse(BaseModel):
    """双选会报名响应模式"""
    id: str
    job_fair_id: str
    enterprise_id: str
    enterprise_name: Optional[str] = None  # 企业名称
    enterprise_detail: Optional[dict] = None  # 企业详情
    status: str
    check_in_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 宣讲会相关 ====================

class InfoSessionCreate(BaseModel):
    """创建宣讲会请求模式"""
    title: str = Field(..., min_length=1, max_length=100, description="宣讲会标题")
    description: Optional[str] = Field(None, description="描述")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    session_type: str = Field("OFFLINE", description="宣讲会类型：OFFLINE, ONLINE, HYBRID")
    live_url: Optional[str] = Field(None, max_length=255, description="直播链接")
    school_id: Optional[str] = Field(None, description="学校ID")
    max_students: Optional[int] = Field(None, ge=1, description="最大学生数")
    materials: Optional[list[str]] = Field(None, description="宣讲会资料URLs（文件URL列表）")


class InfoSessionUpdate(BaseModel):
    """更新宣讲会请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="宣讲会标题")
    description: Optional[str] = Field(None, description="描述")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    location: Optional[str] = Field(None, max_length=255, description="地点")
    session_type: Optional[str] = Field(None, description="宣讲会类型")
    live_url: Optional[str] = Field(None, max_length=255, description="直播链接")
    school_id: Optional[str] = Field(None, description="学校ID")
    max_students: Optional[int] = Field(None, ge=1, description="最大学生数")
    materials: Optional[list[str]] = Field(None, description="宣讲会资料URLs（文件URL列表）")
    status: Optional[str] = Field(None, description="状态：DRAFT, PUBLISHED, ONGOING, ENDED, CANCELLED")


class InfoSessionResponse(BaseModel):
    """宣讲会响应模式"""
    id: str
    enterprise_id: str
    school_id: Optional[str]
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    session_type: str
    live_url: Optional[str]
    status: str
    max_students: Optional[int]
    check_in_count: int
    materials: Optional[list[str]]
    created_at: datetime
    updated_at: datetime
    
    @field_validator('materials', mode='before')
    @classmethod
    def parse_materials(cls, v):
        """解析materials字段（从JSON字符串转换为list）"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return None
        if isinstance(v, list):
            return v
        return None
    
    class Config:
        from_attributes = True


class InfoSessionListResponse(BaseModel):
    """宣讲会列表响应模式"""
    items: list[InfoSessionResponse]
    total: int
    page: int
    page_size: int


class InfoSessionRegistrationCreate(BaseModel):
    """宣讲会报名请求模式"""
    session_id: str = Field(..., description="宣讲会ID")


class InfoSessionRegistrationResponse(BaseModel):
    """宣讲会报名响应模式"""
    id: str
    session_id: str
    student_id: str
    student_name: Optional[str] = None  # 学生姓名
    student_detail: Optional[dict] = None  # 学生详情
    status: str
    check_in_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
