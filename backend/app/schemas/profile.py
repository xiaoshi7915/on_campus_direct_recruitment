"""
用户档案相关的Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==================== 学生档案 ====================

class StudentProfileCreate(BaseModel):
    """创建学生档案请求模式"""
    real_name: str = Field(..., min_length=1, max_length=50, description="真实姓名")
    student_id: Optional[str] = Field(None, max_length=50, description="学号")
    school_id: Optional[str] = Field(None, description="学校ID")
    department_id: Optional[str] = Field(None, description="院系ID")
    class_id: Optional[str] = Field(None, description="班级ID")
    grade: Optional[str] = Field(None, max_length=20, description="年级")
    major: Optional[str] = Field(None, max_length=100, description="专业")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")


class StudentProfileUpdate(BaseModel):
    """更新学生档案请求模式"""
    real_name: Optional[str] = Field(None, min_length=1, max_length=50, description="真实姓名")
    student_id: Optional[str] = Field(None, max_length=50, description="学号")
    school_id: Optional[str] = Field(None, description="学校ID")
    department_id: Optional[str] = Field(None, description="院系ID")
    class_id: Optional[str] = Field(None, description="班级ID")
    grade: Optional[str] = Field(None, max_length=20, description="年级")
    major: Optional[str] = Field(None, max_length=100, description="专业")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")


class StudentProfileResponse(BaseModel):
    """学生档案响应模式"""
    id: str
    user_id: str
    real_name: str
    student_id: Optional[str]
    school_id: Optional[str]
    department_id: Optional[str]
    class_id: Optional[str]
    grade: Optional[str]
    major: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 企业档案 ====================

class EnterpriseProfileCreate(BaseModel):
    """创建企业档案请求模式"""
    company_name: str = Field(..., min_length=1, max_length=100, description="公司名称")
    unified_code: Optional[str] = Field(None, max_length=50, description="统一社会信用代码")
    legal_person: Optional[str] = Field(None, max_length=50, description="法人代表")
    industry: Optional[str] = Field(None, max_length=100, description="行业")
    scale: Optional[str] = Field(None, max_length=50, description="规模")
    address: Optional[str] = Field(None, max_length=255, description="地址")
    website: Optional[str] = Field(None, max_length=255, description="网站")
    logo_url: Optional[str] = Field(None, max_length=255, description="Logo URL")
    description: Optional[str] = Field(None, description="描述")


class EnterpriseProfileUpdate(BaseModel):
    """更新企业档案请求模式"""
    company_name: Optional[str] = Field(None, min_length=1, max_length=100, description="公司名称")
    unified_code: Optional[str] = Field(None, max_length=50, description="统一社会信用代码")
    legal_person: Optional[str] = Field(None, max_length=50, description="法人代表")
    industry: Optional[str] = Field(None, max_length=100, description="行业")
    scale: Optional[str] = Field(None, max_length=50, description="规模")
    address: Optional[str] = Field(None, max_length=255, description="地址")
    website: Optional[str] = Field(None, max_length=255, description="网站")
    logo_url: Optional[str] = Field(None, max_length=255, description="Logo URL")
    description: Optional[str] = Field(None, description="描述")


class EnterpriseProfileResponse(BaseModel):
    """企业档案响应模式"""
    id: str
    user_id: str
    company_name: str
    unified_code: Optional[str]
    legal_person: Optional[str]
    industry: Optional[str]
    scale: Optional[str]
    address: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    description: Optional[str]
    is_verified: bool
    is_main_account: bool
    main_account_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 教师档案 ====================

class TeacherProfileCreate(BaseModel):
    """创建教师档案请求模式"""
    real_name: str = Field(..., min_length=1, max_length=50, description="真实姓名")
    school_id: Optional[str] = Field(None, description="学校ID")
    department_id: Optional[str] = Field(None, description="院系ID")
    title: Optional[str] = Field(None, max_length=50, description="职称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")


class TeacherProfileUpdate(BaseModel):
    """更新教师档案请求模式"""
    real_name: Optional[str] = Field(None, min_length=1, max_length=50, description="真实姓名")
    school_id: Optional[str] = Field(None, description="学校ID")
    department_id: Optional[str] = Field(None, description="院系ID")
    title: Optional[str] = Field(None, max_length=50, description="职称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")


class TeacherProfileResponse(BaseModel):
    """教师档案响应模式"""
    id: str
    user_id: str
    real_name: str
    school_id: Optional[str]
    department_id: Optional[str]
    title: Optional[str]
    avatar_url: Optional[str]
    is_main_account: bool
    main_account_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True



