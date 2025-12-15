"""
认证相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_admin
from app.models.user import User
from app.models.profile import EnterpriseProfile
from app.models.verification import EnterpriseVerification, PersonalVerification
from app.models.enums import VerificationStatus
from app.schemas.verification import (
    EnterpriseVerificationCreate,
    EnterpriseVerificationUpdate,
    EnterpriseVerificationResponse,
    EnterpriseVerificationListResponse,
    PersonalVerificationCreate,
    PersonalVerificationUpdate,
    PersonalVerificationResponse,
    PersonalVerificationListResponse,
)

router = APIRouter()


# ==================== 企业认证 ====================

@router.post("/enterprise", response_model=EnterpriseVerificationResponse, status_code=status.HTTP_201_CREATED)
async def create_enterprise_verification(
    verification_data: EnterpriseVerificationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建企业认证申请（仅企业用户）
    
    Args:
        verification_data: 认证申请数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseVerificationResponse: 创建的认证申请
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "verification:create:enterprise", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业主账号才能申请企业认证"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在，请先完善企业信息"
        )
    
    # 检查是否已有待审核的申请
    existing_result = await db.execute(
        select(EnterpriseVerification).where(
            EnterpriseVerification.enterprise_id == enterprise.id,
            EnterpriseVerification.status == VerificationStatus.PENDING
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已有待审核的认证申请，请等待审核结果"
        )
    
    # 创建认证申请
    import json
    verification = EnterpriseVerification(
        id=str(uuid4()),
        enterprise_id=enterprise.id,
        status=VerificationStatus.PENDING,
        business_license_url=verification_data.business_license_url,
        legal_person_id_front_url=verification_data.legal_person_id_front_url,
        legal_person_id_back_url=verification_data.legal_person_id_back_url,
        authorization_letter_url=verification_data.authorization_letter_url,
        other_documents=json.dumps(verification_data.other_documents) if verification_data.other_documents else None
    )
    
    db.add(verification)
    await db.commit()
    await db.refresh(verification)
    
    # 解析other_documents
    other_docs = json.loads(verification.other_documents) if verification.other_documents else None
    
    return {
        "id": verification.id,
        "enterprise_id": verification.enterprise_id,
        "status": verification.status.value,
        "business_license_url": verification.business_license_url,
        "legal_person_id_front_url": verification.legal_person_id_front_url,
        "legal_person_id_back_url": verification.legal_person_id_back_url,
        "authorization_letter_url": verification.authorization_letter_url,
        "other_documents": other_docs,
        "reviewer_id": verification.reviewer_id,
        "review_comment": verification.review_comment,
        "reviewed_at": verification.reviewed_at,
        "created_at": verification.created_at,
        "updated_at": verification.updated_at,
    }


@router.get("/enterprise", response_model=EnterpriseVerificationListResponse)
async def get_enterprise_verifications(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业认证申请列表
    
    Args:
        page: 页码
        page_size: 每页数量
        status_filter: 状态过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseVerificationListResponse: 认证申请列表
    """
    query = select(EnterpriseVerification)
    
    # 企业用户只能查看自己的申请
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        if not enterprise:
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
        
        query = query.where(EnterpriseVerification.enterprise_id == enterprise.id)
    elif current_user.user_type != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看认证申请列表"
        )
    
    # 状态过滤
    if status_filter:
        query = query.where(EnterpriseVerification.status == status_filter)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(EnterpriseVerification.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    verifications = result.scalars().all()
    
    # 解析other_documents
    import json
    verification_list = []
    for verification in verifications:
        other_docs = json.loads(verification.other_documents) if verification.other_documents else None
        verification_list.append({
            "id": verification.id,
            "enterprise_id": verification.enterprise_id,
            "status": verification.status.value,
            "business_license_url": verification.business_license_url,
            "legal_person_id_front_url": verification.legal_person_id_front_url,
            "legal_person_id_back_url": verification.legal_person_id_back_url,
            "authorization_letter_url": verification.authorization_letter_url,
            "other_documents": other_docs,
            "reviewer_id": verification.reviewer_id,
            "review_comment": verification.review_comment,
            "reviewed_at": verification.reviewed_at,
            "created_at": verification.created_at,
            "updated_at": verification.updated_at,
        })
    
    return {
        "items": verification_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/enterprise/{verification_id}", response_model=EnterpriseVerificationResponse)
async def get_enterprise_verification(
    verification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业认证申请详情
    
    Args:
        verification_id: 认证申请ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        EnterpriseVerificationResponse: 认证申请详情
    """
    result = await db.execute(
        select(EnterpriseVerification).where(EnterpriseVerification.id == verification_id)
    )
    verification = result.scalar_one_or_none()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="认证申请不存在"
        )
    
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    
    # 企业只能查看自己的认证申请，管理员可以查看所有
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        if not enterprise or verification.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此认证申请"
            )
    elif current_user.user_type != "ADMIN":
        has_permission = await check_permission(current_user, "verification:read", db)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此认证申请"
            )
    
    # 解析other_documents
    import json
    other_docs = json.loads(verification.other_documents) if verification.other_documents else None
    
    return {
        "id": verification.id,
        "enterprise_id": verification.enterprise_id,
        "status": verification.status.value,
        "business_license_url": verification.business_license_url,
        "legal_person_id_front_url": verification.legal_person_id_front_url,
        "legal_person_id_back_url": verification.legal_person_id_back_url,
        "authorization_letter_url": verification.authorization_letter_url,
        "other_documents": other_docs,
        "reviewer_id": verification.reviewer_id,
        "review_comment": verification.review_comment,
        "reviewed_at": verification.reviewed_at,
        "created_at": verification.created_at,
        "updated_at": verification.updated_at,
    }


@router.put("/enterprise/{verification_id}", response_model=EnterpriseVerificationResponse)
async def update_enterprise_verification(
    verification_id: str,
    verification_data: EnterpriseVerificationUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    审核企业认证申请（仅管理员）
    
    Args:
        verification_id: 认证申请ID
        verification_data: 审核数据
        current_user: 当前登录用户（必须是管理员）
        db: 数据库会话
        
    Returns:
        EnterpriseVerificationResponse: 更新后的认证申请
    """
    result = await db.execute(
        select(EnterpriseVerification).where(EnterpriseVerification.id == verification_id)
    )
    verification = result.scalar_one_or_none()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="认证申请不存在"
        )
    
    if verification.status != VerificationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该认证申请已审核，无法再次审核"
        )
    
    # 更新认证状态
    verification.status = verification_data.status
    verification.reviewer_id = current_user.id
    verification.review_comment = verification_data.review_comment
    verification.reviewed_at = datetime.utcnow()
    
    # 如果审核通过，更新企业的is_verified状态
    if verification_data.status == VerificationStatus.APPROVED:
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.id == verification.enterprise_id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if enterprise:
            enterprise.is_verified = True
    
    await db.commit()
    await db.refresh(verification)
    
    # 解析other_documents
    import json
    other_docs = json.loads(verification.other_documents) if verification.other_documents else None
    
    return {
        "id": verification.id,
        "enterprise_id": verification.enterprise_id,
        "status": verification.status.value,
        "business_license_url": verification.business_license_url,
        "legal_person_id_front_url": verification.legal_person_id_front_url,
        "legal_person_id_back_url": verification.legal_person_id_back_url,
        "authorization_letter_url": verification.authorization_letter_url,
        "other_documents": other_docs,
        "reviewer_id": verification.reviewer_id,
        "review_comment": verification.review_comment,
        "reviewed_at": verification.reviewed_at,
        "created_at": verification.created_at,
        "updated_at": verification.updated_at,
    }


# ==================== 个人身份认证 ====================

@router.post("/personal", response_model=PersonalVerificationResponse, status_code=status.HTTP_201_CREATED)
async def create_personal_verification(
    verification_data: PersonalVerificationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建个人身份认证申请
    
    Args:
        verification_data: 认证申请数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        PersonalVerificationResponse: 创建的认证申请
    """
    # 检查是否已有待审核的申请
    existing_result = await db.execute(
        select(PersonalVerification).where(
            PersonalVerification.user_id == current_user.id,
            PersonalVerification.status == VerificationStatus.PENDING
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已有待审核的认证申请，请等待审核结果"
        )
    
    # 创建认证申请
    import json
    verification = PersonalVerification(
        id=str(uuid4()),
        user_id=current_user.id,
        user_type=current_user.user_type.value if hasattr(current_user.user_type, 'value') else str(current_user.user_type),
        status=VerificationStatus.PENDING,
        id_card_front_url=verification_data.id_card_front_url,
        id_card_back_url=verification_data.id_card_back_url,
        real_name=verification_data.real_name,
        id_card_number=verification_data.id_card_number,
        other_documents=json.dumps(verification_data.other_documents) if verification_data.other_documents else None
    )
    
    db.add(verification)
    await db.commit()
    await db.refresh(verification)
    
    # 解析other_documents
    other_docs = json.loads(verification.other_documents) if verification.other_documents else None
    
    return {
        "id": verification.id,
        "user_id": verification.user_id,
        "user_type": verification.user_type,
        "status": verification.status.value,
        "id_card_front_url": verification.id_card_front_url,
        "id_card_back_url": verification.id_card_back_url,
        "real_name": verification.real_name,
        "id_card_number": verification.id_card_number,
        "other_documents": other_docs,
        "reviewer_id": verification.reviewer_id,
        "review_comment": verification.review_comment,
        "reviewed_at": verification.reviewed_at,
        "created_at": verification.created_at,
        "updated_at": verification.updated_at,
    }


@router.get("/personal", response_model=PersonalVerificationListResponse)
async def get_personal_verifications(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取个人身份认证申请列表
    
    Args:
        page: 页码
        page_size: 每页数量
        status_filter: 状态过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        PersonalVerificationListResponse: 认证申请列表
    """
    query = select(PersonalVerification)
    
    # 普通用户只能查看自己的申请
    if current_user.user_type != "ADMIN":
        query = query.where(PersonalVerification.user_id == current_user.id)
    
    # 状态过滤
    if status_filter:
        query = query.where(PersonalVerification.status == status_filter)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(PersonalVerification.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    verifications = result.scalars().all()
    
    # 解析other_documents
    import json
    verification_list = []
    for verification in verifications:
        other_docs = json.loads(verification.other_documents) if verification.other_documents else None
        verification_list.append({
            "id": verification.id,
            "user_id": verification.user_id,
            "user_type": verification.user_type,
            "status": verification.status.value,
            "id_card_front_url": verification.id_card_front_url,
            "id_card_back_url": verification.id_card_back_url,
            "real_name": verification.real_name,
            "id_card_number": verification.id_card_number,
            "other_documents": other_docs,
            "reviewer_id": verification.reviewer_id,
            "review_comment": verification.review_comment,
            "reviewed_at": verification.reviewed_at,
            "created_at": verification.created_at,
            "updated_at": verification.updated_at,
        })
    
    return {
        "items": verification_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.put("/personal/{verification_id}", response_model=PersonalVerificationResponse)
async def update_personal_verification(
    verification_id: str,
    verification_data: PersonalVerificationUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    审核个人身份认证申请（仅管理员）
    
    Args:
        verification_id: 认证申请ID
        verification_data: 审核数据
        current_user: 当前登录用户（必须是管理员）
        db: 数据库会话
        
    Returns:
        PersonalVerificationResponse: 更新后的认证申请
    """
    result = await db.execute(
        select(PersonalVerification).where(PersonalVerification.id == verification_id)
    )
    verification = result.scalar_one_or_none()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="认证申请不存在"
        )
    
    if verification.status != VerificationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该认证申请已审核，无法再次审核"
        )
    
    # 更新认证状态
    verification.status = verification_data.status
    verification.reviewer_id = current_user.id
    verification.review_comment = verification_data.review_comment
    verification.reviewed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(verification)
    
    # 解析other_documents
    import json
    other_docs = json.loads(verification.other_documents) if verification.other_documents else None
    
    return {
        "id": verification.id,
        "user_id": verification.user_id,
        "user_type": verification.user_type,
        "status": verification.status.value,
        "id_card_front_url": verification.id_card_front_url,
        "id_card_back_url": verification.id_card_back_url,
        "real_name": verification.real_name,
        "id_card_number": verification.id_card_number,
        "other_documents": other_docs,
        "reviewer_id": verification.reviewer_id,
        "review_comment": verification.review_comment,
        "reviewed_at": verification.reviewed_at,
        "created_at": verification.created_at,
        "updated_at": verification.updated_at,
    }

