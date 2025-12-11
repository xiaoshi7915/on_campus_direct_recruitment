"""
学生管理相关API路由（教师端）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_teacher
from app.models.user import User
from app.models.profile import StudentProfile, TeacherProfile
from app.models.job import Resume, JobApplication

router = APIRouter()


@router.get("")
async def get_students(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索（姓名、学号）"),
    grade: Optional[str] = Query(None, description="年级过滤"),
    major: Optional[str] = Query(None, description="专业过滤"),
    department_id: Optional[str] = Query(None, description="院系ID过滤"),
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学生列表（仅教师，带数据权限隔离）
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词搜索
        grade: 年级过滤
        major: 专业过滤
        department_id: 院系ID过滤
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        dict: 学生列表
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
    
    # 构建查询条件
    query = select(StudentProfile)
    
    # 数据权限隔离：教师只能查看管辖范围内的学生
    if teacher.department_id:
        query = query.where(StudentProfile.department_id == teacher.department_id)
    elif teacher.school_id:
        query = query.where(StudentProfile.school_id == teacher.school_id)
    else:
        # 如果没有部门信息，返回空列表
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }
    
    # 关键词搜索
    if keyword:
        query = query.where(
            or_(
                StudentProfile.real_name.contains(keyword),
                StudentProfile.student_id.contains(keyword)
            )
        )
    
    # 年级过滤
    if grade:
        query = query.where(StudentProfile.grade == grade)
    
    # 专业过滤
    if major:
        query = query.where(StudentProfile.major.contains(major))
    
    # 院系过滤
    if department_id:
        query = query.where(StudentProfile.department_id == department_id)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(StudentProfile.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    students = result.scalars().all()
    
    # 获取每个学生的简历数和申请数
    student_list = []
    for student in students:
        # 获取简历数
        resume_count_result = await db.execute(
            select(func.count()).select_from(
                select(Resume).where(Resume.student_id == student.id).subquery()
            )
        )
        resume_count = resume_count_result.scalar() or 0
        
        # 获取申请数
        application_count_result = await db.execute(
            select(func.count()).select_from(
                select(JobApplication).where(JobApplication.student_id == student.user_id).subquery()
            )
        )
        application_count = application_count_result.scalar() or 0
        
        student_list.append({
            "id": student.id,
            "user_id": student.user_id,
            "real_name": student.real_name,
            "student_id": student.student_id,
            "grade": student.grade,
            "major": student.major,
            "school_id": student.school_id,
            "department_id": student.department_id,
            "resume_count": resume_count,
            "application_count": application_count,
            "created_at": student.created_at.isoformat() if student.created_at else None,
            "updated_at": student.updated_at.isoformat() if student.updated_at else None
        })
    
    return {
        "items": student_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{student_id}")
async def get_student_detail(
    student_id: str,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学生详情（仅教师，带数据权限隔离）
    
    Args:
        student_id: 学生ID（student_profiles.id）
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        dict: 学生详情
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
    
    # 获取学生信息
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.id == student_id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    # 数据权限检查
    if teacher.department_id and student.department_id:
        if teacher.department_id != student.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此学生信息"
            )
    elif teacher.school_id and student.school_id:
        if teacher.school_id != student.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看此学生信息"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此学生信息"
        )
    
    # 获取简历数和申请数
    resume_count_result = await db.execute(
        select(func.count()).select_from(
            select(Resume).where(Resume.student_id == student.id).subquery()
        )
    )
    resume_count = resume_count_result.scalar() or 0
    
    application_count_result = await db.execute(
        select(func.count()).select_from(
            select(JobApplication).where(JobApplication.student_id == student.user_id).subquery()
        )
    )
    application_count = application_count_result.scalar() or 0
    
    return {
        "id": student.id,
        "user_id": student.user_id,
        "real_name": student.real_name,
        "student_id": student.student_id,
        "grade": student.grade,
        "major": student.major,
        "school_id": student.school_id,
        "department_id": student.department_id,
        "class_id": student.class_id,
        "avatar_url": student.avatar_url,
        "resume_count": resume_count,
        "application_count": application_count,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "updated_at": student.updated_at.isoformat() if student.updated_at else None
    }

