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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取简历列表
    
    Args:
        student_id: 学生ID（可选）
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ResumeListResponse: 简历列表
    """
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
        # 企业用户可以查看所有简历，不需要student_id
        pass
    # 如果指定了student_id，且用户有权限查看（企业或管理员）
    elif student_id:
        query = query.where(Resume.student_id == student_id)
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
    
    # 将ORM对象转换为响应模型
    resume_responses = [ResumeResponse.model_validate(resume) for resume in resumes]
    
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
    
    return resume


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

