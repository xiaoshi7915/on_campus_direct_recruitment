"""
企业端管理相关API路由（子账号管理、人才库等）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Optional, List
from uuid import uuid4
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.profile import EnterpriseProfile, StudentProfile
from app.models.job import Job, JobApplication, Resume
from app.models.interview import Interview, Offer
from app.models.common import Favorite
from app.models.chat import ChatSession, Message
from app.models.talent_pool import TalentPool

router = APIRouter()


# ==================== Pydantic模式 ====================

class SubAccountCreate(BaseModel):
    """创建子账号请求模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    real_name: str = Field(..., min_length=1, max_length=50, description="真实姓名")
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    position: Optional[str] = Field(None, description="职位")


class EnterpriseResponse(BaseModel):
    """企业响应模式"""
    id: str
    user_id: str
    company_name: str
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_main_account: bool
    main_account_id: Optional[str] = None
    status: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True


class EnterpriseListResponse(BaseModel):
    """企业列表响应模式"""
    items: List[EnterpriseResponse]
    total: int
    page: int
    page_size: int


class TalentItem(BaseModel):
    """人才库项"""
    student_id: str
    student_name: str
    student_phone: Optional[str] = None
    student_email: Optional[str] = None
    resume_id: Optional[str] = None
    resume_title: Optional[str] = None
    status: str  # ALL, FAVORITED, COMMUNICATING, INTERVIEWED, HIRED
    last_contact_time: Optional[str] = None
    application_id: Optional[str] = None
    interview_id: Optional[str] = None
    offer_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class TalentListResponse(BaseModel):
    """人才库列表响应"""
    items: List[TalentItem]
    total: int
    page: int
    page_size: int


# ==================== 子账号管理 ====================

@router.get("/sub-accounts", response_model=EnterpriseListResponse)
async def get_sub_accounts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取子账号列表（仅主账号）
    
    Args:
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        EnterpriseListResponse: 子账号列表
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看子账号列表"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 检查是否是主账号
    if not enterprise.is_main_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有主账号才能查看子账号列表"
        )
    
    # 获取子账号列表
    query = select(EnterpriseProfile).where(EnterpriseProfile.main_account_id == enterprise.id)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(EnterpriseProfile.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    sub_accounts = result.scalars().all()
    
    # 构建响应数据
    enterprise_list = []
    for sub_account in sub_accounts:
        # 获取用户信息
        user_result = await db.execute(select(User).where(User.id == sub_account.user_id))
        user = user_result.scalar_one_or_none()
        
        enterprise_list.append(EnterpriseResponse(
            id=sub_account.id,
            user_id=sub_account.user_id,
            company_name=sub_account.company_name,
            username=user.username if user else None,
            phone=user.phone if user else None,
            email=user.email if user else None,
            is_main_account=sub_account.is_main_account,
            main_account_id=sub_account.main_account_id,
            status=user.status if user else None,
            created_at=sub_account.created_at.isoformat() if sub_account.created_at else ""
        ))
    
    return {
        "items": enterprise_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/sub-accounts", response_model=EnterpriseResponse, status_code=status.HTTP_201_CREATED)
async def create_sub_account(
    account_data: SubAccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建子账号（仅企业主账号）
    
    使用新的权限检查机制，确保只有主账号可以创建子账号
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "sub_account:create", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业主账号才能创建子账号"
        )
    """
    创建子账号（仅主账号）
    
    Args:
        account_data: 子账号数据
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        EnterpriseResponse: 创建的子账号
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能创建子账号"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 确保是主账号（一个企业只能有一个主账号）
    if not enterprise.is_main_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有主账号才能创建子账号"
        )
    
    # 验证主账号唯一性：通过unified_code检查该企业是否已有主账号
    # 注意：由于unified_code是unique的，主账号创建时应该已经验证过唯一性
    # 这里主要确保当前账号确实是主账号
    if enterprise.unified_code:
        main_account_result = await db.execute(
            select(EnterpriseProfile).where(
                EnterpriseProfile.unified_code == enterprise.unified_code,
                EnterpriseProfile.is_main_account == True,
                EnterpriseProfile.id != enterprise.id
            )
        )
        existing_main = main_account_result.scalar_one_or_none()
        if existing_main:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="该企业已存在主账号，一个企业只能有一个主账号"
            )
    
    # 检查用户名是否已存在
    existing_user_result = await db.execute(
        select(User).where(User.username == account_data.username)
    )
    if existing_user_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )
    
    # 创建用户
    from app.core.security import get_password_hash
    new_user = User(
        id=str(uuid4()),
        username=account_data.username,
        phone=account_data.phone,
        email=account_data.email,
        password_hash=get_password_hash(account_data.password),
        user_type="ENTERPRISE",
        status="ACTIVE"
    )
    db.add(new_user)
    await db.flush()
    
    # 创建子账号企业档案
    # 注意：unified_code是unique的，子账号不能继承主账号的unified_code，应该设置为None
    sub_account = EnterpriseProfile(
        id=str(uuid4()),
        user_id=new_user.id,
        company_name=enterprise.company_name,  # 继承主账号的公司名称
        unified_code=None,  # 子账号不继承统一社会信用代码（因为unique约束）
        industry=enterprise.industry,
        scale=enterprise.scale,
        address=enterprise.address,
        website=enterprise.website,
        logo_url=enterprise.logo_url,
        description=enterprise.description,
        is_verified=enterprise.is_verified,  # 继承主账号的认证状态
        is_main_account=False,
        main_account_id=enterprise.id
    )
    db.add(sub_account)
    await db.commit()
    await db.refresh(sub_account)
    
    return EnterpriseResponse(
        id=sub_account.id,
        user_id=sub_account.user_id,
        company_name=sub_account.company_name,
        username=new_user.username,
        phone=new_user.phone,
        email=new_user.email,
        is_main_account=sub_account.is_main_account,
        main_account_id=sub_account.main_account_id,
        status=new_user.status,
        created_at=sub_account.created_at.isoformat() if sub_account.created_at else ""
    )


@router.delete("/sub-accounts/{sub_account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_account(
    sub_account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除子账号（仅主账号）
    
    Args:
        sub_account_id: 子账号ID
        current_user: 当前登录用户（企业）
        db: 数据库会话
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能删除子账号"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 检查是否是主账号
    if not enterprise.is_main_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有主账号才能删除子账号"
        )
    
    # 获取子账号
    sub_account_result = await db.execute(
        select(EnterpriseProfile).where(
            EnterpriseProfile.id == sub_account_id,
            EnterpriseProfile.main_account_id == enterprise.id
        )
    )
    sub_account = sub_account_result.scalar_one_or_none()
    
    if not sub_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="子账号不存在或不属于此主账号"
        )
    
    # 删除用户（级联删除企业档案）
    user_result = await db.execute(select(User).where(User.id == sub_account.user_id))
    user = user_result.scalar_one_or_none()
    if user:
        await db.delete(user)
    
    await db.commit()


# ==================== 人才库管理 ====================

@router.get("/talents", response_model=TalentListResponse)
async def get_talents(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status_filter: Optional[str] = Query(None, description="状态过滤：ALL, FAVORITED, COMMUNICATING, INTERVIEWED, HIRED"),
    keyword: Optional[str] = Query(None, description="关键词搜索（姓名、手机号）"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业触达过的人才库
    
    Args:
        page: 页码
        page_size: 每页数量
        status_filter: 状态过滤
        keyword: 关键词搜索
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        TalentListResponse: 人才库列表
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看人才库"
        )
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在"
        )
    
    # 从人才库表读取数据（主账号和子账号都可以查看主账号的人才库）
    from app.services.enterprise_service import get_enterprise_ids_for_query
    enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
    query = select(TalentPool).where(TalentPool.enterprise_id.in_(enterprise_ids))
    
    # 状态过滤
    if status_filter and status_filter != "ALL":
        query = query.where(TalentPool.status == status_filter)
    
    # 关键词搜索
    if keyword:
        keyword_lower = keyword.lower()
        # 通过学生姓名和手机号搜索
        query = query.join(StudentProfile, TalentPool.student_id == StudentProfile.id)
        query = query.join(User, StudentProfile.user_id == User.id)
        query = query.where(
            or_(
                StudentProfile.real_name.like(f"%{keyword}%"),
                User.phone.like(f"%{keyword}%"),
                User.email.like(f"%{keyword}%")
            )
        )
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 排序和分页
    # MySQL在降序排序时，NULL值默认排在最后，无需特殊处理
    offset = (page - 1) * page_size
    query = query.order_by(TalentPool.last_contact_time.desc(), TalentPool.created_at.desc())
    query = query.offset(offset).limit(page_size)
    
    result = await db.execute(query)
    talent_pools = result.scalars().all()
    
    # 构建响应数据
    talents = []
    for talent_pool in talent_pools:
        # 获取学生信息
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.id == talent_pool.student_id)
        )
        student = student_result.scalar_one_or_none()
        
        if not student:
            continue
        
        student_user_result = await db.execute(select(User).where(User.id == student.user_id))
        student_user = student_user_result.scalar_one_or_none()
        
        # 获取简历信息
        resume = None
        if talent_pool.resume_id:
            resume_result = await db.execute(
                select(Resume).where(Resume.id == talent_pool.resume_id)
            )
            resume = resume_result.scalar_one_or_none()
        
        # 如果没有简历ID，获取最新简历
        if not resume:
            resume_query = select(Resume).where(Resume.student_id == student.id).order_by(Resume.created_at.desc()).limit(1)
            resume_result = await db.execute(resume_query)
            resume = resume_result.scalar_one_or_none()
        
        talents.append(TalentItem(
            student_id=student.id,
            student_name=student.real_name,
            student_phone=student_user.phone if student_user else None,
            student_email=student_user.email if student_user else None,
            resume_id=resume.id if resume else None,
            resume_title=resume.title if resume else None,
            status=talent_pool.status,
            last_contact_time=talent_pool.last_contact_time.isoformat() if talent_pool.last_contact_time else None,
            application_id=talent_pool.application_id,
            interview_id=talent_pool.interview_id,
            offer_id=talent_pool.offer_id
        ))
    
    return {
        "items": talents,
        "total": total,
        "page": page,
        "page_size": page_size
    }

