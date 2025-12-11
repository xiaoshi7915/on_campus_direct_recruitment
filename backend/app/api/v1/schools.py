"""
学校信息管理相关API路由（教师端）
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_teacher
from app.models.user import User
from app.models.profile import TeacherProfile
from app.models.school import School

router = APIRouter()


# ==================== Pydantic模式 ====================

class SchoolVerificationRequest(BaseModel):
    """学校实名认证请求模式"""
    verification_documents: Optional[str] = Field(None, description="认证材料（JSON字符串或描述）")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=100, description="联系邮箱")


class SchoolResponse(BaseModel):
    """学校响应模式"""
    id: str
    name: str
    code: Optional[str]
    province: Optional[str]
    city: Optional[str]
    address: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    description: Optional[str]
    is_verified: bool
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


# ==================== API端点 ====================

@router.get("/my-school", response_model=SchoolResponse)
async def get_my_school(
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前教师所属的学校信息
    
    Args:
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        SchoolResponse: 学校信息
    """
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师信息不存在"
        )
    
    if not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师尚未关联学校"
        )
    
    # 获取学校信息
    school_result = await db.execute(
        select(School).where(School.id == teacher.school_id)
    )
    school = school_result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校信息不存在"
        )
    
    return school


@router.post("/my-school/verify", response_model=SchoolResponse)
async def request_school_verification(
    verification_data: SchoolVerificationRequest,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    申请学校实名认证
    
    Args:
        verification_data: 认证申请数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        SchoolResponse: 学校信息（认证状态可能仍为未认证，需要管理员审核）
    """
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师信息不存在"
        )
    
    if not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="教师尚未关联学校，无法申请认证"
        )
    
    # 获取学校信息
    school_result = await db.execute(
        select(School).where(School.id == teacher.school_id)
    )
    school = school_result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校信息不存在"
        )
    
    # 如果已经认证，直接返回
    if school.is_verified:
        return school
    
    # 这里可以添加认证申请记录到数据库的逻辑
    # 目前只是返回学校信息，实际认证需要管理员审核
    # 可以创建一个 school_verification_requests 表来记录申请
    
    # 返回学校信息（认证状态仍为未认证，等待管理员审核）
    return school

