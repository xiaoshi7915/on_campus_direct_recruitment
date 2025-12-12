"""
职位申请相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.job import Job, JobApplication, Resume
from app.models.profile import StudentProfile
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationListResponse

router = APIRouter()


# 注意：GET路由必须在POST路由之前定义，避免路由冲突
@router.get("", response_model=ApplicationListResponse)
async def get_applications(
    job_id: Optional[str] = Query(None, description="职位ID（企业用户查看某个职位的申请）"),
    status_filter: Optional[str] = Query(None, alias="status", description="申请状态过滤"),
    user_id: Optional[str] = Query(None, description="用户ID（可选，如果提供将转换为student_id查询）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取职位申请列表
    
    Args:
        job_id: 职位ID（可选）
        status_filter: 申请状态过滤
        user_id: 用户ID（可选，如果提供将转换为student_id查询）
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ApplicationListResponse: 申请列表
    """
    query = select(JobApplication)
    
    # 如果提供了user_id，转换为student_id查询（仅企业用户）
    if user_id and current_user.user_type == "ENTERPRISE":
        student_profile_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == user_id)
        )
        student_profile = student_profile_result.scalar_one_or_none()
        if student_profile:
            # 通过student_id查询申请（JobApplication.student_id是user_id，需要转换）
            # 注意：JobApplication.student_id 实际上是 users.id，所以可以直接使用 user_id
            query = query.where(JobApplication.student_id == user_id)
        else:
            # 如果找不到学生档案，返回空列表
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
    
    # 学生用户只能查看自己的申请
    if current_user.user_type == "STUDENT":
        query = query.where(JobApplication.student_id == current_user.id)
    # 企业用户只能查看自己职位的申请
    elif current_user.user_type == "ENTERPRISE":
        # 获取企业信息
        from app.models.profile import EnterpriseProfile
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        if not enterprise:
            # 如果企业信息不存在，返回空列表而不是404
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
        
        # 如果指定了job_id，只查看该职位的申请
        if job_id:
            # 检查职位是否属于当前企业
            job_result = await db.execute(
                select(Job).where(Job.id == job_id)
            )
            job = job_result.scalar_one_or_none()
            
            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="职位不存在"
                )
            
            # 检查企业权限
            if job.enterprise_id != enterprise.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权查看该职位的申请"
                )
            
            query = query.where(JobApplication.job_id == job_id)
        else:
            # 如果没有指定job_id，查看企业所有职位的申请
            # 先获取企业的所有职位
            jobs_result = await db.execute(
                select(Job).where(Job.enterprise_id == enterprise.id)
            )
            jobs = jobs_result.scalars().all()
            job_ids = [job.id for job in jobs]
            
            if job_ids:
                query = query.where(JobApplication.job_id.in_(job_ids))
            else:
                # 如果企业没有职位，返回空列表
                return {
                    "items": [],
                    "total": 0,
                    "page": page,
                    "page_size": page_size
                }
    # 管理员可以查看所有申请
    elif current_user.user_type != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看申请列表"
        )
    
    # 状态过滤
    if status_filter:
        query = query.where(JobApplication.status == status_filter)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(JobApplication.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    applications = result.scalars().all()
    
    # 填充关联信息用于前端显示（职位名称和学生姓名）
    application_list = []
    for application in applications:
        # 获取职位信息
        job_result = await db.execute(select(Job).where(Job.id == application.job_id))
        job = job_result.scalar_one_or_none()
        if job:
            application.job_title = job.title  # type: ignore
        
        # 获取学生姓名
        student_profile_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == application.student_id)
        )
        student_profile = student_profile_result.scalar_one_or_none()
        if student_profile:
            application.student_name = student_profile.real_name  # type: ignore
        
        application_list.append(application)
    
    return {
        "items": application_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    申请职位（仅学生用户）
    
    Args:
        application_data: 申请数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ApplicationResponse: 创建的申请
        
    Raises:
        HTTPException: 如果用户不是学生、职位不存在或已申请
    """
    # 检查用户类型
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能申请职位"
        )
    
    # 获取学生信息
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生信息不存在，请先完善学生信息"
        )
    
    # 检查职位是否存在
    job_result = await db.execute(select(Job).where(Job.id == application_data.job_id))
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    # 检查职位状态
    if job.status != "PUBLISHED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该职位未发布，无法申请"
        )
    
    # 检查是否已申请
    # 注意：JobApplication.student_id 关联到 users.id，不是 student_profiles.id
    existing_result = await db.execute(
        select(JobApplication).where(
            JobApplication.job_id == application_data.job_id,
            JobApplication.student_id == current_user.id  # 使用current_user.id
        )
    )
    if existing_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="您已申请过该职位"
        )
    
    # 检查简历是否存在且属于当前学生（如果提供了resume_id）
    resume_id = application_data.resume_id
    if resume_id:
        resume_result = await db.execute(
            select(Resume).where(
                Resume.id == resume_id,
                Resume.student_id == student.id
            )
        )
        resume = resume_result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="简历不存在或不属于您"
            )
    else:
        # 如果没有提供resume_id，尝试获取学生的默认简历
        default_resume_result = await db.execute(
            select(Resume).where(
                Resume.student_id == student.id,
                Resume.is_default == True
            )
        )
        default_resume = default_resume_result.scalar_one_or_none()
        if default_resume:
            resume_id = default_resume.id
        else:
            # 如果没有默认简历，获取第一个简历
            any_resume_result = await db.execute(
                select(Resume).where(
                    Resume.student_id == student.id
                ).limit(1)
            )
            any_resume = any_resume_result.scalar_one_or_none()
            if any_resume:
                resume_id = any_resume.id
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="请先创建简历再申请职位"
                )
    
    # 创建申请
    # 注意：JobApplication.student_id 关联到 users.id，不是 student_profiles.id
    application = JobApplication(
        id=str(uuid4()),
        job_id=application_data.job_id,
        resume_id=resume_id,  # 必须提供，不能为None
        student_id=current_user.id,  # 使用current_user.id（users表）
        status="PENDING",
        message=application_data.message
    )
    
    # 增加职位申请次数
    job.apply_count += 1
    
    db.add(application)
    await db.commit()
    await db.refresh(application)
    
    return application


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取申请详情
    
    Args:
        application_id: 申请ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ApplicationResponse: 申请详情
        
    Raises:
        HTTPException: 如果申请不存在或无权查看
    """
    # 获取申请
    result = await db.execute(select(JobApplication).where(JobApplication.id == application_id))
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申请不存在"
        )
    
    # 检查权限
    if current_user.user_type == "STUDENT":
        # 学生只能查看自己的申请
        if application.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此申请"
            )
    elif current_user.user_type == "ENTERPRISE":
        # 企业只能查看自己职位的申请
        job_result = await db.execute(select(Job).where(Job.id == application.job_id))
        job = job_result.scalar_one_or_none()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="职位不存在"
            )
        
        from app.models.profile import EnterpriseProfile
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        
        if not enterprise or job.enterprise_id != enterprise.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此申请"
            )
    elif current_user.user_type != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此申请"
        )
    
    # 填充关联信息用于前端显示
    job_result = await db.execute(select(Job).where(Job.id == application.job_id))
    job = job_result.scalar_one_or_none()
    if job:
        application.job_title = job.title  # type: ignore
    
    # 获取学生姓名
    student_profile_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == application.student_id)
    )
    student_profile = student_profile_result.scalar_one_or_none()
    if student_profile:
        application.student_name = student_profile.real_name  # type: ignore
    
    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application_status(
    application_id: str,
    status: str = Query(..., description="新的申请状态：VIEWED, INTERVIEWED, ACCEPTED, REJECTED"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新申请状态（企业用户）
    
    Args:
        application_id: 申请ID
        status: 新的申请状态
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ApplicationResponse: 更新后的申请
        
    Raises:
        HTTPException: 如果申请不存在或无权修改
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能更新申请状态"
        )
    
    # 获取申请
    result = await db.execute(select(JobApplication).where(JobApplication.id == application_id))
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申请不存在"
        )
    
    # 检查权限：企业只能更新自己职位的申请
    job_result = await db.execute(select(Job).where(Job.id == application.job_id))
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    from app.models.profile import EnterpriseProfile
    enterprise_result = await db.execute(
        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
    )
    enterprise = enterprise_result.scalar_one_or_none()
    
    if not enterprise or job.enterprise_id != enterprise.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此申请"
        )
    
    # 验证状态值
    valid_statuses = ["VIEWED", "INTERVIEWED", "ACCEPTED", "REJECTED"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的状态值，必须是: {', '.join(valid_statuses)}"
        )
    
    # 更新状态
    application.status = status
    await db.commit()
    await db.refresh(application)
    
    # 填充关联信息用于前端显示
    job_result = await db.execute(select(Job).where(Job.id == application.job_id))
    job = job_result.scalar_one_or_none()
    if job:
        application.job_title = job.title  # type: ignore
    
    # 获取学生姓名
    student_profile_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == application.student_id)
    )
    student_profile = student_profile_result.scalar_one_or_none()
    if student_profile:
        application.student_name = student_profile.real_name  # type: ignore
    
    return application


