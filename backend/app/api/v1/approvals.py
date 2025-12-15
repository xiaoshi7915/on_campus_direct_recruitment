"""
审批流程相关API路由（管理员和教师）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_admin, require_teacher
from app.models.user import User
from app.models.profile import TeacherProfile
from app.models.activity import JobFair, InfoSession
from app.models.school import Class

router = APIRouter()


# ==================== Pydantic模式 ====================

class ApprovalRequest(BaseModel):
    """审批请求模式"""
    action: str = Field(..., description="审批操作（APPROVE-通过，REJECT-拒绝）")
    comment: Optional[str] = Field(None, description="审批意见")


class ApprovalResponse(BaseModel):
    """审批响应模式"""
    success: bool
    message: str
    new_status: Optional[str] = None


# ==================== 双选会审批 ====================

@router.post("/job-fairs/{job_fair_id}/approve", response_model=ApprovalResponse)
async def approve_job_fair(
    job_fair_id: str,
    approval_data: ApprovalRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    审批双选会（管理员或教师）
    
    Args:
        job_fair_id: 双选会ID
        approval_data: 审批数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ApprovalResponse: 审批结果
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "job_fair:approve", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员或教师才能审批双选会"
        )
    
    # 使用资源权限检查（教师只能审批自己学校的双选会）
    has_access = await check_resource_access("job_fair", job_fair_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权审批此双选会"
        )
    
    # 获取双选会
    job_fair_result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = job_fair_result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    # 执行审批
    if approval_data.action == "APPROVE":
        # 通过：将状态改为PUBLISHED
        if job_fair.status == "DRAFT" or job_fair.status == "PENDING":
            job_fair.status = "PUBLISHED"
            await db.commit()
            return {
                "success": True,
                "message": "双选会审批通过",
                "new_status": "PUBLISHED"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"当前状态为{job_fair.status}，无法审批"
            )
    elif approval_data.action == "REJECT":
        # 拒绝：将状态改为REJECTED（如果模型支持）或保持DRAFT
        if job_fair.status == "DRAFT" or job_fair.status == "PENDING":
            job_fair.status = "REJECTED"  # 假设支持REJECTED状态
            await db.commit()
            return {
                "success": True,
                "message": "双选会审批拒绝",
                "new_status": "REJECTED"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"当前状态为{job_fair.status}，无法拒绝"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的审批操作，必须是APPROVE或REJECT"
        )


# ==================== 宣讲会审批 ====================

@router.post("/info-sessions/{session_id}/approve", response_model=ApprovalResponse)
async def approve_info_session(
    session_id: str,
    approval_data: ApprovalRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    审批宣讲会（管理员或教师）
    
    Args:
        session_id: 宣讲会ID
        approval_data: 审批数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ApprovalResponse: 审批结果
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "info_session:approve", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员或教师才能审批宣讲会"
        )
    
    # 使用资源权限检查（教师只能审批自己学校的宣讲会）
    has_access = await check_resource_access("info_session", session_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权审批此宣讲会"
        )
    
    # 获取宣讲会
    session_result = await db.execute(select(InfoSession).where(InfoSession.id == session_id))
    info_session = session_result.scalar_one_or_none()
    
    if not info_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宣讲会不存在"
        )
    
    # 执行审批
    if approval_data.action == "APPROVE":
        # 通过：将状态改为PUBLISHED
        if info_session.status == "DRAFT" or info_session.status == "PENDING":
            info_session.status = "PUBLISHED"
            await db.commit()
            return {
                "success": True,
                "message": "宣讲会审批通过",
                "new_status": "PUBLISHED"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"当前状态为{info_session.status}，无法审批"
            )
    elif approval_data.action == "REJECT":
        # 拒绝：将状态改为REJECTED
        if info_session.status == "DRAFT" or info_session.status == "PENDING":
            info_session.status = "REJECTED"
            await db.commit()
            return {
                "success": True,
                "message": "宣讲会审批拒绝",
                "new_status": "REJECTED"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"当前状态为{info_session.status}，无法拒绝"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的审批操作，必须是APPROVE或REJECT"
        )

