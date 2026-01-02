"""
职位相关的Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class JobCreate(BaseModel):
    """创建职位请求模式"""
    title: str = Field(..., min_length=1, max_length=100, description="职位标题")
    department: Optional[str] = Field(None, max_length=50, description="部门")
    job_type: Optional[str] = Field(None, max_length=50, description="职位类型")
    salary_min: Optional[int] = Field(None, ge=0, description="最低薪资")
    salary_max: Optional[int] = Field(None, ge=0, description="最高薪资")
    work_location: Optional[str] = Field(None, max_length=100, description="工作地点")
    experience: Optional[str] = Field(None, max_length=50, description="工作经验要求")
    education: Optional[str] = Field(None, max_length=50, description="学历要求")
    description: str = Field(..., min_length=1, description="职位描述")
    requirements: Optional[str] = Field(None, description="职位要求")
    tags: Optional[str] = Field(None, max_length=255, description="标签（逗号分隔）")


class JobUpdate(BaseModel):
    """更新职位请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="职位标题")
    department: Optional[str] = Field(None, max_length=50, description="部门")
    job_type: Optional[str] = Field(None, max_length=50, description="职位类型")
    salary_min: Optional[int] = Field(None, ge=0, description="最低薪资")
    salary_max: Optional[int] = Field(None, ge=0, description="最高薪资")
    work_location: Optional[str] = Field(None, max_length=100, description="工作地点")
    experience: Optional[str] = Field(None, max_length=50, description="工作经验要求")
    education: Optional[str] = Field(None, max_length=50, description="学历要求")
    description: Optional[str] = Field(None, min_length=1, description="职位描述")
    requirements: Optional[str] = Field(None, description="职位要求")
    tags: Optional[str] = Field(None, max_length=255, description="标签")
    status: Optional[str] = Field(None, description="职位状态：DRAFT, PENDING, PUBLISHED, CLOSED")


class JobResponse(BaseModel):
    """职位响应模式"""
    id: str
    enterprise_id: str
    enterprise_name: Optional[str] = None  # 企业名称
    enterprise_logo: Optional[str] = None  # 企业Logo
    enterprise_industry: Optional[str] = None  # 企业行业
    enterprise_scale: Optional[str] = None  # 企业规模
    title: str
    department: Optional[str]
    job_type: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    work_location: Optional[str]
    experience: Optional[str]  # 工作经验要求
    education: Optional[str]
    description: str
    requirements: Optional[str]
    status: str
    view_count: int
    apply_count: int
    tags: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """职位列表响应模式"""
    items: list[JobResponse]
    total: int
    page: int
    page_size: int


# ==================== 求职意向相关Schema ====================

class JobIntentionCreate(BaseModel):
    """创建求职意向请求模式"""
    # 旧字段（保留兼容性）
    job_type: Optional[str] = Field(None, max_length=50, description="职位类型（旧字段，已废弃）")
    industry: Optional[str] = Field(None, max_length=100, description="行业（旧字段，已废弃）")
    salary_expect: Optional[int] = Field(None, ge=0, description="期望薪资（旧字段，已废弃）")
    work_location: Optional[str] = Field(None, max_length=100, description="工作地点（旧字段，已废弃）")
    
    # 新字段
    job_type_list: Optional[List[str]] = Field(None, description="职位类型列表")
    industry_list: Optional[List[str]] = Field(None, description="行业列表（包含一级和二级行业）")
    work_location_list: Optional[List[str]] = Field(None, description="工作地点列表")
    job_nature: Optional[str] = Field(None, description="求职类型：FULL_TIME（全职）、PART_TIME（兼职）")
    salary_min: Optional[int] = Field(None, ge=0, description="期望薪资最小值（单位：千元/月）")
    salary_max: Optional[int] = Field(None, ge=0, description="期望薪资最大值（单位：千元/月）")
    part_time_days: Optional[str] = Field(None, max_length=50, description="兼职每周工作天数")
    work_time_slot: Optional[str] = Field(None, max_length=50, description="兼职工作时间段")


class JobIntentionUpdate(BaseModel):
    """更新求职意向请求模式"""
    # 旧字段（保留兼容性）
    job_type: Optional[str] = Field(None, max_length=50, description="职位类型（旧字段，已废弃）")
    industry: Optional[str] = Field(None, max_length=100, description="行业（旧字段，已废弃）")
    salary_expect: Optional[int] = Field(None, ge=0, description="期望薪资（旧字段，已废弃）")
    work_location: Optional[str] = Field(None, max_length=100, description="工作地点（旧字段，已废弃）")
    
    # 新字段
    job_type_list: Optional[List[str]] = Field(None, description="职位类型列表")
    industry_list: Optional[List[str]] = Field(None, description="行业列表（包含一级和二级行业）")
    work_location_list: Optional[List[str]] = Field(None, description="工作地点列表")
    job_nature: Optional[str] = Field(None, description="求职类型：FULL_TIME（全职）、PART_TIME（兼职）")
    salary_min: Optional[int] = Field(None, ge=0, description="期望薪资最小值（单位：千元/月）")
    salary_max: Optional[int] = Field(None, ge=0, description="期望薪资最大值（单位：千元/月）")
    part_time_days: Optional[str] = Field(None, max_length=50, description="兼职每周工作天数")
    work_time_slot: Optional[str] = Field(None, max_length=50, description="兼职工作时间段")


class JobIntentionResponse(BaseModel):
    """求职意向响应模式"""
    id: str
    student_id: str
    # 旧字段（保留兼容性）
    job_type: Optional[str]
    industry: Optional[str]
    salary_expect: Optional[int]
    work_location: Optional[str]
    # 新字段
    job_type_list: Optional[str]  # JSON字符串
    industry_list: Optional[str]  # JSON字符串
    work_location_list: Optional[str]  # JSON字符串
    job_nature: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    part_time_days: Optional[str]
    work_time_slot: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobIntentionListResponse(BaseModel):
    """求职意向列表响应模式"""
    items: list[JobIntentionResponse]
    total: int
    page: int
    page_size: int



