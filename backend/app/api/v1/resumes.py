"""
简历相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.job import Resume
from app.models.profile import StudentProfile
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse, ResumeListResponse

router = APIRouter()


@router.get("", response_model=ResumeListResponse)
async def get_resumes(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    student_id: Optional[str] = Query(None, description="学生ID（可选，管理员可查看所有）"),
    user_id: Optional[str] = Query(None, description="用户ID（可选，如果提供将转换为student_id）"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取简历列表
    
    Args:
        student_id: 学生ID（可选）
        user_id: 用户ID（可选，如果提供将转换为student_id）
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ResumeListResponse: 简历列表
    """
    # 如果提供了user_id，转换为student_id
    actual_student_id = student_id
    if user_id and not student_id:
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == user_id)
        )
        student_profile = student_result.scalar_one_or_none()
        if student_profile:
            actual_student_id = student_profile.id
    
    # 构建查询
    query = select(Resume)
    
    # 如果是学生用户，只能查看自己的简历
    if current_user.user_type == "STUDENT":
        # 获取学生信息
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        
        if not student:
            return {"items": [], "total": 0, "page": page, "page_size": page_size}
        
        query = query.where(Resume.student_id == student.id)
    # 企业用户可以查看所有简历（用于人才搜索）
    elif current_user.user_type == "ENTERPRISE":
        # 如果指定了student_id，只查看该学生的简历
        if actual_student_id:
            query = query.where(Resume.student_id == actual_student_id)
        # 否则查看所有简历
        pass
    # 如果指定了student_id，且用户有权限查看（企业或管理员）
    elif actual_student_id:
        query = query.where(Resume.student_id == actual_student_id)
    # 管理员可以查看所有简历
    elif current_user.user_type == "ADMIN":
        pass
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看简历列表"
        )
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Resume.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    resumes = result.scalars().all()
    
    # 将ORM对象转换为响应模型，并为file_url生成签名URL
    from app.core.oss import oss_service
    resume_responses = []
    for resume in resumes:
        resume_dict = ResumeResponse.model_validate(resume).model_dump()
        # 如果file_url存在，生成签名URL（有效期24小时）
        if resume_dict.get('file_url'):
            resume_dict['file_url'] = oss_service.get_file_url(resume_dict['file_url'], signed=True, expires=86400)  # 24小时
        resume_responses.append(ResumeResponse(**resume_dict))
    
    return {
        "items": resume_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取简历详情
    
    Args:
        resume_id: 简历ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ResumeResponse: 简历详情
        
    Raises:
        HTTPException: 如果简历不存在或无权查看
    """
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 检查权限：学生只能查看自己的简历，企业和管理员可以查看
    if current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        
        if not student or resume.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此简历"
            )
    
    # 增加查看次数
    resume.view_count += 1
    await db.commit()
    await db.refresh(resume)
    
    # 如果file_url存在，生成签名URL用于预览（有效期24小时）
    if resume.file_url:
        from app.core.oss import oss_service
        resume.file_url = oss_service.get_file_url(resume.file_url, signed=True, expires=86400)  # 24小时
    # 如果没有file_url，也要正常返回简历信息（不报错）
    
    return resume


@router.get("/{resume_id}/download")
async def download_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    下载简历文件（电子版）
    
    Args:
        resume_id: 简历ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        RedirectResponse: 重定向到文件URL
        
    Raises:
        HTTPException: 如果简历不存在或无权下载
    """
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 检查权限：学生只能下载自己的简历，企业和管理员可以下载
    if current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        
        if not student or resume.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权下载此简历"
            )
    
    if not resume.file_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该简历没有电子版文件"
        )
    
    # 增加下载次数
    resume.download_count += 1
    await db.commit()
    
    # 生成签名URL用于下载（有效期24小时，避免用户点击时过期）
    from app.core.oss import oss_service
    signed_url = oss_service.get_file_url(resume.file_url, signed=True, expires=86400)  # 24小时 = 86400秒
    
    # 重定向到签名URL
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=signed_url)


@router.get("/{resume_id}/preview_url", response_model=dict)
async def get_resume_preview_url(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取简历文件预览的签名URL
    
    Args:
        resume_id: 简历ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 包含签名URL的字典
        
    Raises:
        HTTPException: 如果简历不存在或无权查看
    """
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 检查权限：学生只能查看自己的简历，企业和管理员可以查看
    if current_user.user_type == "STUDENT":
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == current_user.id)
        )
        student = student_result.scalar_one_or_none()
        
        if not student or resume.student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此简历"
            )
    
    if not resume.file_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该简历没有电子版文件"
        )
    
    # 生成签名URL用于预览（有效期24小时，避免用户点击时过期）
    from app.core.oss import oss_service
    signed_url = oss_service.get_file_url(resume.file_url, signed=True, expires=86400)  # 24小时 = 86400秒
    
    return {"preview_url": signed_url}


@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建简历（仅学生用户）
    
    Args:
        resume_data: 简历数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ResumeResponse: 创建的简历
        
    Raises:
        HTTPException: 如果用户不是学生或学生信息不存在
    """
    # 检查用户类型
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能创建简历"
        )
    
    # 获取学生信息
    result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生信息不存在，请先完善学生信息"
        )
    
    # 如果设置为默认简历，需要先取消其他默认简历
    if resume_data.is_default:
        await db.execute(
            select(Resume).where(
                Resume.student_id == student.id,
                Resume.is_default == True
            )
        )
        existing_defaults = await db.execute(
            select(Resume).where(
                Resume.student_id == student.id,
                Resume.is_default == True
            )
        )
        for existing in existing_defaults.scalars().all():
            existing.is_default = False
    
    # 创建简历
    resume = Resume(
        id=str(uuid4()),
        student_id=student.id,
        title=resume_data.title,
        content=resume_data.content,
        file_url=getattr(resume_data, 'file_url', None),
        is_default=resume_data.is_default
    )
    
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    
    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: str,
    resume_data: ResumeUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新简历（仅学生用户，只能更新自己的简历）
    
    Args:
        resume_id: 简历ID
        resume_data: 更新的简历数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ResumeResponse: 更新后的简历
        
    Raises:
        HTTPException: 如果简历不存在或无权修改
    """
    # 检查用户类型
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能更新简历"
        )
    
    # 获取简历
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 检查权限
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student or resume.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此简历"
        )
    
    # 如果设置为默认简历，需要先取消其他默认简历
    if resume_data.is_default is True:
        existing_defaults_result = await db.execute(
            select(Resume).where(
                Resume.student_id == student.id,
                Resume.is_default == True,
                Resume.id != resume_id
            )
        )
        for existing in existing_defaults_result.scalars().all():
            existing.is_default = False
    
    # 更新简历信息
    update_data = resume_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resume, field, value)
    
    await db.commit()
    await db.refresh(resume)
    
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除简历（仅学生用户，只能删除自己的简历）
    
    Args:
        resume_id: 简历ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果简历不存在或无权删除
    """
    # 检查用户类型
    if current_user.user_type != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能删除简历"
        )
    
    # 获取简历
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 检查权限
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student or resume.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此简历"
        )
    
    await db.delete(resume)
    await db.commit()
    
    return None

