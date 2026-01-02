"""
职位相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.core.logging import get_logger
from app.core.cache import get_cache, set_cache
from app.api.v1.auth import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.job import Job
from app.models.profile import EnterpriseProfile
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from app.utils.search import fulltext_search_jobs, fallback_search_jobs

logger = get_logger(__name__)

router = APIRouter()


@router.get("", response_model=JobListResponse)
async def get_jobs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    location: Optional[str] = Query(None, description="工作地点"),
    status_filter: Optional[str] = Query(None, alias="status", description="职位状态过滤"),
    job_type: Optional[str] = Query(None, description="职位类型过滤"),
    education: Optional[str] = Query(None, description="学历要求过滤"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    获取职位列表
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词
        location: 工作地点
        status_filter: 职位状态过滤
        db: 数据库会话
        
    Returns:
        JobListResponse: 职位列表
    """
    # 如果有关键词，尝试使用全文搜索
    if keyword:
        try:
            offset = (page - 1) * page_size
            jobs, total = await fulltext_search_jobs(
                db, keyword, location, page_size, offset
            )
            # 如果全文搜索成功，直接返回
            if jobs and len(jobs) > 0:
                # 将ORM对象转换为响应模型，并获取企业信息
                job_responses = []
                for job in jobs:
                    # 获取企业信息
                    enterprise_result = await db.execute(
                        select(EnterpriseProfile).where(EnterpriseProfile.id == job.enterprise_id)
                    )
                    enterprise = enterprise_result.scalar_one_or_none()
                    
                    job_dict = {
                        "id": job.id,
                        "enterprise_id": job.enterprise_id,
                        "enterprise_name": enterprise.company_name if enterprise else None,
                        "enterprise_logo": enterprise.logo_url if enterprise else None,
                        "enterprise_industry": enterprise.industry if enterprise else None,
                        "enterprise_scale": enterprise.scale if enterprise else None,
                        "title": job.title,
                        "department": job.department,
                        "job_type": job.job_type,
                        "salary_min": job.salary_min,
                        "salary_max": job.salary_max,
                        "work_location": job.work_location,
                        "experience": job.experience,
                        "education": job.education,
                        "description": job.description,
                        "requirements": job.requirements,
                        "status": job.status,
                        "view_count": job.view_count,
                        "apply_count": job.apply_count,
                        "tags": job.tags,
                        "created_at": job.created_at,
                        "updated_at": job.updated_at,
                    }
                    job_responses.append(JobResponse.model_validate(job_dict))
                return {
                    "items": job_responses,
                    "total": total,
                    "page": page,
                    "page_size": page_size
                }
        except Exception as e:
            logger.warning(f"全文搜索失败，使用普通搜索: {str(e)}")
            logger.exception(e)  # 记录详细错误信息
    
    # 构建查询（普通搜索或全文搜索失败时的回退）
    query = select(Job)
    
    # 关键词搜索（搜索标题、描述和要求）
    if keyword:
        query = query.where(
            or_(
                Job.title.contains(keyword),
                Job.description.contains(keyword),
                Job.requirements.contains(keyword)
            )
        )
    
    # 工作地点过滤
    if location:
        query = query.where(Job.work_location.contains(location))
    
    # 职位类型过滤
    if job_type:
        query = query.where(Job.job_type == job_type)
    
    # 学历要求过滤
    if education:
        query = query.where(Job.education == education)
    
    # 状态过滤
    if status_filter:
        query = query.where(Job.status == status_filter)
    else:
        # 如果未指定状态过滤，根据用户类型决定
        # 企业用户可以看到自己的所有职位（包括草稿），其他用户只能看到已发布的
        if current_user and current_user.user_type == "ENTERPRISE":
            # 企业用户：显示主账号和所有子账号的职位
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                from app.services.enterprise_service import get_enterprise_ids_for_query
                enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                query = query.where(Job.enterprise_id.in_(enterprise_ids))
            else:
                # 如果企业信息不存在，返回空列表
                return {
                    "items": [],
                    "total": 0,
                    "page": page,
                    "page_size": page_size
                }
        else:
            # 其他用户（学生、未登录等）只能看到已发布的职位
            query = query.where(Job.status == "PUBLISHED")
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 构建缓存键（包含企业ID，如果是企业用户）
    enterprise_id_for_cache = None
    if current_user and current_user.user_type == "ENTERPRISE":
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if enterprise:
            enterprise_id_for_cache = enterprise.id
    
    cache_key = f"jobs:list:{page}:{page_size}:{keyword}:{location}:{status_filter}:{enterprise_id_for_cache}"
    cached_result = await get_cache(cache_key)
    if cached_result:
        logger.debug(f"从缓存获取职位列表: {cache_key}")
        return cached_result
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Job.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    jobs = result.scalars().all()
    
    # 将ORM对象转换为响应模型，并获取企业信息
    job_responses = []
    for job in jobs:
        # 获取企业信息
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.id == job.enterprise_id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        job_dict = {
            "id": job.id,
            "enterprise_id": job.enterprise_id,
            "enterprise_name": enterprise.company_name if enterprise else None,
            "enterprise_logo": enterprise.logo_url if enterprise else None,
            "enterprise_industry": enterprise.industry if enterprise else None,
            "enterprise_scale": enterprise.scale if enterprise else None,
            "title": job.title,
            "department": job.department,
            "job_type": job.job_type,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "work_location": job.work_location,
            "experience": job.experience,
            "education": job.education,
            "description": job.description,
            "requirements": job.requirements,
            "status": job.status,
            "view_count": job.view_count,
            "apply_count": job.apply_count,
            "tags": job.tags,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
        }
        job_responses.append(JobResponse.model_validate(job_dict))
    
    response_data = {
        "items": job_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    }
    
    # 缓存结果（5分钟）
    await set_cache(cache_key, response_data, expire=300)
    
    return response_data


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取职位详情
    
    Args:
        job_id: 职位ID
        db: 数据库会话
        
    Returns:
        JobResponse: 职位详情
        
    Raises:
        HTTPException: 如果职位不存在
    """
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    # 增加查看次数
    job.view_count += 1
    await db.commit()
    await db.refresh(job)
    
    # 获取企业信息
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.id == job.enterprise_id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    job_dict = {
        "id": job.id,
        "enterprise_id": job.enterprise_id,
        "enterprise_name": enterprise.company_name if enterprise else None,
        "enterprise_logo": enterprise.logo_url if enterprise else None,
        "enterprise_industry": enterprise.industry if enterprise else None,
        "enterprise_scale": enterprise.scale if enterprise else None,
        "title": job.title,
        "department": job.department,
        "job_type": job.job_type,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "work_location": job.work_location,
        "experience": job.experience,
        "education": job.education,
        "description": job.description,
        "requirements": job.requirements,
        "status": job.status,
        "view_count": job.view_count,
        "apply_count": job.apply_count,
        "tags": job.tags,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
    }
    
    return JobResponse.model_validate(job_dict)


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建职位（仅企业用户，主账号）
    
    Args:
        job_data: 职位数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobResponse: 创建的职位
        
    Raises:
        HTTPException: 如果用户不是企业用户或企业信息不存在
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "job:create", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业主账号才能创建职位"
        )
    
    # 获取企业信息
    result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = result.scalar_one_or_none()
    
    if not enterprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业信息不存在，请先完善企业信息"
        )
    
    # 创建职位
    job = Job(
        id=str(uuid4()),
        enterprise_id=enterprise.id,
        title=job_data.title,
        department=job_data.department,
        job_type=job_data.job_type,
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        work_location=job_data.work_location,
        experience=job_data.experience,
        education=job_data.education,
        description=job_data.description,
        requirements=job_data.requirements,
        tags=job_data.tags,
        status="DRAFT"  # 默认草稿状态
    )
    
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新职位（仅企业用户，只能更新自己的职位）
    
    Args:
        job_id: 职位ID
        job_data: 更新的职位数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        JobResponse: 更新后的职位
        
    Raises:
        HTTPException: 如果职位不存在或无权修改
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "job:update", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能更新职位"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("job", job_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权更新此职位"
        )
    
    # 获取职位
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise or job.enterprise_id != enterprise.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此职位"
        )
    
    # 更新职位信息
    update_data = job_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)
    
    await db.commit()
    await db.refresh(job)
    
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除职位（仅企业用户，只能删除自己的职位）
    
    Args:
        job_id: 职位ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果职位不存在或无权删除
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission, check_resource_access
    
    has_permission = await check_permission(current_user, "job:delete", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业主账号才能删除职位"
        )
    
    # 使用资源权限检查
    has_access = await check_resource_access("job", job_id, current_user, db, "delete")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此职位"
        )
    
    # 获取职位
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise or job.enterprise_id != enterprise.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此职位"
        )
    
    await db.delete(job)
    await db.commit()
    
    return None

