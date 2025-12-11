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
from app.models.profile import EnterpriseProfile
from app.models.job import Job, JobApplication, Resume
from app.models.interview import Interview, Offer
from app.models.common import Favorite
from app.models.chat import ChatSession, Message

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
    
    # 检查是否是主账号
    if not enterprise.is_main_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有主账号才能创建子账号"
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
    sub_account = EnterpriseProfile(
        id=str(uuid4()),
        user_id=new_user.id,
        company_name=enterprise.company_name,  # 继承主账号的公司名称
        unified_code=enterprise.unified_code,  # 继承主账号的统一社会信用代码
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
    
    # 获取企业触达过的学生（通过申请、面试、Offer、收藏、聊天）
    from app.models.profile import StudentProfile
    
    # 1. 通过职位申请触达的学生（JobApplication.student_id是user_id，需要转换为student_profiles.id）
    applications_result = await db.execute(
        select(StudentProfile.id).join(
            JobApplication, StudentProfile.user_id == JobApplication.student_id
        ).where(
            JobApplication.job_id.in_(
                select(Job.id).where(Job.enterprise_id == enterprise.id)
            )
        ).distinct()
    )
    application_student_ids = set(row[0] for row in applications_result.all() if row[0])
    
    # 2. 通过面试触达的学生
    interviews_result = await db.execute(
        select(Interview.student_id).where(Interview.enterprise_id == enterprise.id).distinct()
    )
    interview_student_ids = set(row[0] for row in interviews_result.all() if row[0])
    
    # 3. 通过Offer触达的学生
    offers_result = await db.execute(
        select(Offer.student_id).where(Offer.enterprise_id == enterprise.id).distinct()
    )
    offer_student_ids = set(row[0] for row in offers_result.all() if row[0])
    
    # 4. 通过收藏触达的学生（收藏简历）
    favorites_result = await db.execute(
        select(Favorite.target_id).where(
            Favorite.user_id == current_user.id,
            Favorite.target_type == "RESUME"
        ).distinct()
    )
    favorite_resume_ids = set(row[0] for row in favorites_result.all() if row[0])
    # 通过简历ID获取学生ID
    favorite_student_ids = set()
    if favorite_resume_ids:
        resumes_result = await db.execute(
            select(Resume.student_id).where(Resume.id.in_(favorite_resume_ids)).distinct()
        )
        favorite_student_ids = set(row[0] for row in resumes_result.all() if row[0])
    
    # 5. 通过聊天触达的学生（ChatSession使用user1_id和user2_id）
    chat_sessions_result = await db.execute(
        select(ChatSession.user2_id).where(
            ChatSession.user1_id == current_user.id
        ).distinct()
    )
    chat_student_user_ids1 = set(row[0] for row in chat_sessions_result.all() if row[0])
    
    # 也查询user2_id为当前用户的会话
    chat_sessions_result2 = await db.execute(
        select(ChatSession.user1_id).where(
            ChatSession.user2_id == current_user.id
        ).distinct()
    )
    chat_student_user_ids2 = set(row[0] for row in chat_sessions_result2.all() if row[0])
    
    chat_student_user_ids = chat_student_user_ids1 | chat_student_user_ids2
    
    # 获取这些用户对应的学生档案ID
    chat_student_ids = set()
    if chat_student_user_ids:
        chat_students_result = await db.execute(
            select(StudentProfile.id).where(StudentProfile.user_id.in_(chat_student_user_ids)).distinct()
        )
        chat_student_ids = set(row[0] for row in chat_students_result.all() if row[0])
    
    # 合并所有触达的学生ID
    all_student_ids = application_student_ids | interview_student_ids | offer_student_ids | favorite_student_ids | chat_student_ids
    
    if not all_student_ids:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }
    
    # 获取学生信息
    students_result = await db.execute(
        select(StudentProfile).where(StudentProfile.id.in_(all_student_ids))
    )
    students = students_result.scalars().all()
    
    # 构建人才库项
    talents = []
    for student in students:
        student_user_result = await db.execute(select(User).where(User.id == student.user_id))
        student_user = student_user_result.scalar_one_or_none()
        
        # 获取最新简历
        resume_result = await db.execute(
            select(Resume).where(Resume.student_id == student.id).order_by(Resume.created_at.desc()).limit(1)
        )
        resume = resume_result.scalar_one_or_none()
        
        # 判断状态
        talent_status = "ALL"
        last_contact_time = None
        
        # 检查是否收藏
        if resume:
            favorite_check = await db.execute(
                select(Favorite).where(
                    Favorite.user_id == current_user.id,
                    Favorite.target_type == "RESUME",
                    Favorite.target_id == resume.id
                )
            )
            if favorite_check.scalar_one_or_none():
                talent_status = "FAVORITED"
        
        # 检查是否有聊天记录（ChatSession使用user1_id和user2_id）
        chat_check = await db.execute(
            select(ChatSession).where(
                or_(
                    and_(ChatSession.user1_id == current_user.id, ChatSession.user2_id == student.user_id),
                    and_(ChatSession.user1_id == student.user_id, ChatSession.user2_id == current_user.id)
                )
            ).order_by(ChatSession.last_message_at.desc()).limit(1)
        )
        chat_session = chat_check.scalar_one_or_none()
        if chat_session:
            talent_status = "COMMUNICATING"
            if chat_session.last_message_at:
                last_contact_time = chat_session.last_message_at.isoformat()
        
        # 检查是否有面试
        interview_check = await db.execute(
            select(Interview).where(
                Interview.enterprise_id == enterprise.id,
                Interview.student_id == student.id
            ).order_by(Interview.created_at.desc()).limit(1)
        )
        interview = interview_check.scalar_one_or_none()
        if interview:
            talent_status = "INTERVIEWED"
            if interview.created_at:
                last_contact_time = interview.created_at.isoformat()
        
        # 检查是否有Offer
        offer_check = await db.execute(
            select(Offer).where(
                Offer.enterprise_id == enterprise.id,
                Offer.student_id == student.id,
                Offer.status == "ACCEPTED"
            ).order_by(Offer.created_at.desc()).limit(1)
        )
        offer = offer_check.scalar_one_or_none()
        if offer:
            talent_status = "HIRED"
            if offer.created_at:
                last_contact_time = offer.created_at.isoformat()
        
        # 获取申请ID（JobApplication.student_id是user_id）
        application_check = await db.execute(
            select(JobApplication).where(
                JobApplication.student_id == student.user_id,
                JobApplication.job_id.in_(
                    select(Job.id).where(Job.enterprise_id == enterprise.id)
                )
            ).order_by(JobApplication.created_at.desc()).limit(1)
        )
        application = application_check.scalar_one_or_none()
        
        # 关键词过滤
        if keyword:
            keyword_lower = keyword.lower()
            student_name = (student.real_name or "").lower()
            student_phone = (student_user.phone or "").lower() if student_user and student_user.phone else ""
            student_email = (student_user.email or "").lower() if student_user and student_user.email else ""
            if not (keyword_lower in student_name or 
                   keyword_lower in student_phone or
                   keyword_lower in student_email):
                continue
        
        # 状态过滤
        if status_filter and status_filter != "ALL":
            if talent_status != status_filter:
                continue
        
        talents.append(TalentItem(
            student_id=student.id,
            student_name=student.real_name,
            student_phone=student_user.phone if student_user else None,
            student_email=student_user.email if student_user else None,
            resume_id=resume.id if resume else None,
            resume_title=resume.title if resume else None,
            status=talent_status,
            last_contact_time=last_contact_time,
            application_id=application.id if application else None,
            interview_id=interview.id if interview else None,
            offer_id=offer.id if offer else None
        ))
    
    # 排序（按最后联系时间倒序）
    talents.sort(key=lambda x: x.last_contact_time or "", reverse=True)
    
    # 分页
    total = len(talents)
    offset = (page - 1) * page_size
    paginated_talents = talents[offset:offset + page_size]
    
    return {
        "items": paginated_talents,
        "total": total,
        "page": page,
        "page_size": page_size
    }

