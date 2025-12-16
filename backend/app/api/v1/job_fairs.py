"""
双选会相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.activity import JobFair, JobFairRegistration
from app.models.profile import EnterpriseProfile, TeacherProfile
from app.schemas.activity import (
    JobFairCreate, JobFairUpdate, JobFairResponse, JobFairListResponse,
    JobFairRegistrationCreate, JobFairRegistrationResponse
)

router = APIRouter()


@router.get("/my-created", response_model=JobFairListResponse)
async def get_my_created_job_fairs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业创建的双选会列表
    
    Args:
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        JobFairListResponse: 双选会列表
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看创建的双选会"
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
    
    # 获取企业创建的双选会
    query = select(JobFair).where(JobFair.created_by == enterprise.id)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页
    offset = (page - 1) * page_size
    query = query.order_by(JobFair.start_time.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    job_fairs = result.scalars().all()
    
    # 将ORM对象转换为响应模型
    job_fair_responses = [JobFairResponse.model_validate(jf) for jf in job_fairs]
    
    return {
        "items": job_fair_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/my-registrations", response_model=JobFairListResponse)
async def get_my_job_fair_registrations(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业报名的双选会列表
    
    Args:
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        JobFairListResponse: 双选会列表
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看报名的双选会"
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
    
    # 获取企业报名的双选会ID列表
    registrations_result = await db.execute(
        select(JobFairRegistration.job_fair_id).where(
            JobFairRegistration.enterprise_id == enterprise.id
        )
    )
    job_fair_ids = [row[0] for row in registrations_result.all()]
    
    if not job_fair_ids:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }
    
    # 获取双选会列表
    query = select(JobFair).where(JobFair.id.in_(job_fair_ids))
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页
    offset = (page - 1) * page_size
    query = query.order_by(JobFair.start_time.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    job_fairs = result.scalars().all()
    
    # 构建响应
    job_fair_list = []
    for job_fair in job_fairs:
        # 获取报名信息（包括签到时间）
        registration_result = await db.execute(
            select(JobFairRegistration).where(
                JobFairRegistration.job_fair_id == job_fair.id,
                JobFairRegistration.enterprise_id == enterprise.id
            )
        )
        registration = registration_result.scalar_one_or_none()
        
        # 构建响应（注意：JobFairResponse不包含registration相关字段，所以我们需要扩展）
        job_fair_dict = {
            "id": job_fair.id,
            "school_id": job_fair.school_id,
            "title": job_fair.title,
            "description": job_fair.description,
            "start_time": job_fair.start_time,
            "end_time": job_fair.end_time,
            "location": job_fair.location,
            "status": job_fair.status,
            "max_enterprises": job_fair.max_enterprises,
            "created_by": job_fair.created_by,
            "created_at": job_fair.created_at,
            "updated_at": job_fair.updated_at,
        }
        
        # 添加报名相关信息到字典中
        if registration:
            job_fair_dict["registration_id"] = registration.id
            job_fair_dict["registration_status"] = registration.status
            job_fair_dict["check_in_time"] = registration.check_in_time
        else:
            job_fair_dict["registration_id"] = None
            job_fair_dict["registration_status"] = None
            job_fair_dict["check_in_time"] = None
        
        # 创建响应对象
        job_fair_response = JobFairResponse(**job_fair_dict)
        job_fair_list.append(job_fair_response)
    
    return {
        "items": job_fair_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("", response_model=JobFairListResponse)
async def get_job_fairs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    school_id: Optional[str] = Query(None, description="学校ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    获取双选会列表
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词
        school_id: 学校ID
        status_filter: 状态过滤
        current_user: 当前登录用户（可选）
        db: 数据库会话
        
    Returns:
        JobFairListResponse: 双选会列表
    """
    # 构建查询
    query = select(JobFair)
    
    # 注意：企业用户调用此API时，应该通过"浏览双选会"模式来查看所有双选会
    # 而"我的双选会"应该通过/my-registrations接口来获取报名的双选会
    # 这里不再自动过滤企业创建的双选会，因为前端有专门的"浏览双选会"和"我的报名"按钮
    
    # 关键词搜索
    if keyword:
        query = query.where(
            or_(
                JobFair.title.contains(keyword),
                JobFair.description.contains(keyword)
            )
        )
    
    # 学校过滤
    if school_id:
        query = query.where(JobFair.school_id == school_id)
    
    # 状态过滤
    if status_filter:
        query = query.where(JobFair.status == status_filter)
    elif status_filter is None:
        # 如果未指定状态过滤，根据用户类型决定
        # 教师和企业用户可以看到所有状态，未登录用户和学生只能看到已发布的
        if current_user and current_user.user_type in ["TEACHER", "ENTERPRISE"]:
            # 教师和企业用户可以看到所有状态，不添加状态过滤
            pass
        else:
            # 未登录用户和学生只能看到已发布的双选会
            query = query.where(JobFair.status == "PUBLISHED")
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(JobFair.start_time.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    job_fairs = result.scalars().all()
    
    # 将ORM对象转换为响应模型
    job_fair_responses = [JobFairResponse.model_validate(jf) for jf in job_fairs]
    
    return {
        "items": job_fair_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{job_fair_id}", response_model=JobFairResponse)
async def get_job_fair(
    job_fair_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取双选会详情
    
    Args:
        job_fair_id: 双选会ID
        db: 数据库会话
        
    Returns:
        JobFairResponse: 双选会详情
        
    Raises:
        HTTPException: 如果双选会不存在
    """
    result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    return job_fair


@router.post("", response_model=JobFairResponse, status_code=status.HTTP_201_CREATED)
async def create_job_fair(
    job_fair_data: JobFairCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建双选会（仅教师用户）
    
    Args:
        job_fair_data: 双选会数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobFairResponse: 创建的双选会
        
    Raises:
        HTTPException: 如果用户类型不正确
    """
    # 只有教师可以创建双选会，企业不能创建
    if current_user.user_type != "TEACHER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师才能创建双选会，企业只能报名参加"
        )
    
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "job_fair:create", db)
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权创建双选会"
        )
    
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
    
    # 创建双选会（教师创建，状态设为PENDING等待审批）
    job_fair = JobFair(
        id=str(uuid4()),
        title=job_fair_data.title,
        description=job_fair_data.description,
        start_time=job_fair_data.start_time,
        end_time=job_fair_data.end_time,
        location=job_fair_data.location,
        school_id=teacher.school_id or job_fair_data.school_id,
        max_enterprises=job_fair_data.max_enterprises,
        status="PENDING"  # 教师创建的双选会需要审批
    )
    
    db.add(job_fair)
    await db.commit()
    await db.refresh(job_fair)
    
    return job_fair


@router.put("/{job_fair_id}", response_model=JobFairResponse)
async def update_job_fair(
    job_fair_id: str,
    job_fair_data: JobFairUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新双选会（仅创建者或教师）
    
    Args:
        job_fair_id: 双选会ID
        job_fair_data: 更新的双选会数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobFairResponse: 更新后的双选会
        
    Raises:
        HTTPException: 如果双选会不存在或无权修改
    """
    # 获取双选会
    result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "job_fair:update", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此双选会"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("job_fair", job_fair_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此双选会"
        )
    
    # 更新双选会信息
    update_data = job_fair_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job_fair, field, value)
    
    await db.commit()
    await db.refresh(job_fair)
    
    return job_fair


@router.delete("/{job_fair_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_fair(
    job_fair_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除双选会（仅创建者或教师）
    
    Args:
        job_fair_id: 双选会ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果双选会不存在或无权删除
    """
    # 获取双选会
    result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "job_fair:delete", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此双选会"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("job_fair", job_fair_id, current_user, db, "delete")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此双选会"
        )
    
    await db.delete(job_fair)
    await db.commit()


# ==================== 双选会报名相关 ====================

@router.post("/{job_fair_id}/register", response_model=JobFairRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_job_fair(
    job_fair_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    企业报名参加双选会
    
    Args:
        job_fair_id: 双选会ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobFairRegistrationResponse: 报名信息
        
    Raises:
        HTTPException: 如果用户不是企业、双选会不存在或已报名
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能报名双选会"
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
    
    # 检查双选会是否存在
    job_fair_result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = job_fair_result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    # 检查是否已报名
    existing_result = await db.execute(
        select(JobFairRegistration).where(
            JobFairRegistration.job_fair_id == job_fair_id,
            JobFairRegistration.enterprise_id == enterprise.id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="已报名此双选会"
        )
    
    # 创建报名记录
    registration = JobFairRegistration(
        id=str(uuid4()),
        job_fair_id=job_fair_id,
        enterprise_id=enterprise.id,
        status="PENDING"
    )
    
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    
    return registration


@router.get("/{job_fair_id}/registrations", response_model=list[JobFairRegistrationResponse])
async def get_job_fair_registrations(
    job_fair_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取双选会报名列表（仅创建者或教师可查看）
    
    Args:
        job_fair_id: 双选会ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        list[JobFairRegistrationResponse]: 报名列表
    """
    # 检查双选会是否存在
    job_fair_result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = job_fair_result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    # 检查权限（创建者或教师可查看）
    if current_user.user_type == "TEACHER":
        # 教师可以查看所有双选会的报名
        pass
    elif current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        # 企业可以查看自己创建的双选会的报名，或者自己报名的双选会的报名
        if enterprise:
            # 检查是否是创建者
            if job_fair.created_by and job_fair.created_by == enterprise.id:
                pass  # 是创建者，可以查看
            else:
                # 检查是否已报名
                registration_result = await db.execute(
                    select(JobFairRegistration).where(
                        JobFairRegistration.job_fair_id == job_fair_id,
                        JobFairRegistration.enterprise_id == enterprise.id
                    )
                )
                if not registration_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="无权查看此双选会的报名信息"
                    )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="企业信息不存在"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此双选会的报名信息"
        )
    
    # 获取报名列表，并关联企业信息
    result = await db.execute(
        select(JobFairRegistration, EnterpriseProfile)
        .join(EnterpriseProfile, JobFairRegistration.enterprise_id == EnterpriseProfile.id)
        .where(JobFairRegistration.job_fair_id == job_fair_id)
    )
    rows = result.all()
    
    # 构建响应列表
    registration_list = []
    for registration, enterprise in rows:
        registration_dict = {
            "id": registration.id,
            "job_fair_id": registration.job_fair_id,
            "enterprise_id": registration.enterprise_id,
            "enterprise_name": enterprise.company_name if enterprise else None,
            "enterprise_detail": {
                "id": enterprise.id if enterprise else None,
                "company_name": enterprise.company_name if enterprise else None,
                "industry": enterprise.industry if enterprise else None,
                "scale": enterprise.scale if enterprise else None,
                "address": enterprise.address if enterprise else None,
                "website": enterprise.website if enterprise else None,
                "description": enterprise.description if enterprise else None,
            } if enterprise else None,
            "status": registration.status,
            "check_in_time": registration.check_in_time,
            "created_at": registration.created_at,
        }
        registration_list.append(JobFairRegistrationResponse(**registration_dict))
    
    return registration_list


@router.post("/{job_fair_id}/check-in", response_model=JobFairRegistrationResponse)
async def check_in_job_fair(
    job_fair_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    企业双选会签到
    
    Args:
        job_fair_id: 双选会ID
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        JobFairRegistrationResponse: 签到后的报名信息
        
    Raises:
        HTTPException: 如果企业未报名或已签到
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能签到"
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
    
    # 检查双选会是否存在
    job_fair_result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = job_fair_result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    # 查找报名记录
    registration_result = await db.execute(
        select(JobFairRegistration).where(
            JobFairRegistration.job_fair_id == job_fair_id,
            JobFairRegistration.enterprise_id == enterprise.id
        )
    )
    registration = registration_result.scalar_one_or_none()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="您尚未报名此双选会"
        )
    
    # 检查是否已签到
    if registration.check_in_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已经签到过了"
        )
    
    # 执行签到
    registration.check_in_time = datetime.now()
    await db.commit()
    await db.refresh(registration)
    
    # 构建响应
    registration_dict = {
        "id": registration.id,
        "job_fair_id": registration.job_fair_id,
        "enterprise_id": registration.enterprise_id,
        "enterprise_name": enterprise.company_name if enterprise else None,
        "enterprise_detail": {
            "id": enterprise.id if enterprise else None,
            "company_name": enterprise.company_name if enterprise else None,
            "industry": enterprise.industry if enterprise else None,
            "scale": enterprise.scale if enterprise else None,
            "address": enterprise.address if enterprise else None,
            "website": enterprise.website if enterprise else None,
            "description": enterprise.description if enterprise else None,
        } if enterprise else None,
        "status": registration.status,
        "check_in_time": registration.check_in_time,
        "created_at": registration.created_at,
    }
    
    return JobFairRegistrationResponse(**registration_dict)


@router.post("/{job_fair_id}/invite", response_model=JobFairRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def invite_enterprise_to_job_fair(
    job_fair_id: str,
    enterprise_id: str = Query(..., description="企业ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    邀请企业参加双选会（教师或创建者）
    
    Args:
        job_fair_id: 双选会ID
        enterprise_id: 企业ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobFairRegistrationResponse: 邀请/报名信息
    """
    # 检查用户类型（教师或企业创建者）
    if current_user.user_type not in ["TEACHER", "ENTERPRISE"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师或企业创建者才能邀请企业"
        )
    
    # 获取双选会信息
    job_fair_result = await db.execute(select(JobFair).where(JobFair.id == job_fair_id))
    job_fair = job_fair_result.scalar_one_or_none()
    
    if not job_fair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="双选会不存在"
        )
    
    # 权限检查
    if current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if not enterprise or job_fair.created_by != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有创建者才能邀请企业"
            )
    elif current_user.user_type == "TEACHER":
        # 教师可以邀请企业
        teacher_result = await db.execute(
            select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
        )
        teacher = teacher_result.scalar_one_or_none()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="教师信息不存在"
            )
        # 验证双选会是否属于教师的学校
        if teacher.school_id and job_fair.school_id != teacher.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权邀请企业参加此双选会"
            )
    
    # 验证企业是否存在
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.id == enterprise_id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业不存在"
        )
    
    # 检查是否已存在报名或邀请
    existing_result = await db.execute(
        select(JobFairRegistration).where(
            JobFairRegistration.job_fair_id == job_fair_id,
            JobFairRegistration.enterprise_id == enterprise_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        # 如果已存在，更新状态为INVITED（如果当前是PENDING）
        if existing.status == "PENDING":
            existing.status = "INVITED"
            await db.commit()
            await db.refresh(existing)
        return existing
    
    # 创建邀请记录（状态为INVITED）
    invitation = JobFairRegistration(
        id=str(uuid4()),
        job_fair_id=job_fair_id,
        enterprise_id=enterprise_id,
        status="INVITED"  # 邀请状态
    )
    
    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)
    
    return invitation

