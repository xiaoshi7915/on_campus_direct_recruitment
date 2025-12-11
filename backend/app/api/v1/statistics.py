"""
数据统计相关API路由（教师和管理员）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_teacher, require_admin
from app.models.user import User
from app.models.profile import StudentProfile, TeacherProfile
from app.models.job import JobApplication, Resume
from app.models.activity import JobFair, InfoSession

router = APIRouter()


@router.get("/students/activity")
async def get_student_activity_statistics(
    start_date: Optional[str] = Query(None, description="开始日期（YYYY-MM-DD）"),
    end_date: Optional[str] = Query(None, description="结束日期（YYYY-MM-DD）"),
    department_id: Optional[str] = Query(None, description="院系ID"),
    current_user: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学生活跃度统计（仅教师）
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        department_id: 院系ID
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        dict: 学生活跃度统计数据
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
        # 如果没有部门信息，返回空数据
        return {
            "total_students": 0,
            "active_students": 0,
            "resume_count": 0,
            "application_count": 0,
            "by_department": []
        }
    
    # 日期过滤
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        # 可以添加基于学生活动时间的过滤
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    
    # 获取学生总数
    count_query = select(func.count(StudentProfile.id))
    if teacher.department_id:
        count_query = count_query.where(StudentProfile.department_id == teacher.department_id)
    elif teacher.school_id:
        count_query = count_query.where(StudentProfile.school_id == teacher.school_id)
    total_result = await db.execute(count_query)
    total_students = total_result.scalar() or 0
    
    # 获取有简历的学生数（活跃学生）
    students_result = await db.execute(query)
    students = students_result.scalars().all()
    student_profile_ids = [student.id for student in students]  # student_profiles.id
    student_user_ids = [student.user_id for student in students]  # users.id
    
    if student_profile_ids:
        # Resume.student_id 关联到 student_profiles.id
        resume_count_query = select(func.count(Resume.id)).where(
            Resume.student_id.in_(student_profile_ids)
        )
        resume_result = await db.execute(resume_count_query)
        resume_count = resume_result.scalar() or 0
    else:
        resume_count = 0
    
    if student_user_ids:
        # JobApplication.student_id 关联到 users.id
        application_count_query = select(func.count(JobApplication.id)).where(
            JobApplication.student_id.in_(student_user_ids)
        )
        application_result = await db.execute(application_count_query)
        application_count = application_result.scalar() or 0
    else:
        application_count = 0
    
    # 有简历或申请的学生视为活跃学生（去重）
    # 计算有简历的学生数
    if student_profile_ids:
        students_with_resume_query = select(func.count(func.distinct(Resume.student_id))).where(
            Resume.student_id.in_(student_profile_ids)
        )
        students_with_resume_result = await db.execute(students_with_resume_query)
        students_with_resume = students_with_resume_result.scalar() or 0
    else:
        students_with_resume = 0
    
    # 计算有申请的学生数
    if student_user_ids:
        students_with_application_query = select(func.count(func.distinct(JobApplication.student_id))).where(
            JobApplication.student_id.in_(student_user_ids)
        )
        students_with_application_result = await db.execute(students_with_application_query)
        students_with_application = students_with_application_result.scalar() or 0
    else:
        students_with_application = 0
    
    # 活跃学生数：有简历或申请的学生（需要去重）
    # 获取有简历的学生user_id集合
    students_with_resume_user_ids = set()
    if student_profile_ids:
        # 获取有简历的学生的user_id（通过子查询）
        resume_students_result = await db.execute(
            select(StudentProfile.user_id).where(
                StudentProfile.id.in_(
                    select(Resume.student_id).where(Resume.student_id.in_(student_profile_ids)).distinct()
                )
            ).distinct()
        )
        students_with_resume_user_ids = set(row[0] for row in resume_students_result.all() if row[0])
    
    # 获取有申请的学生user_id集合（JobApplication.student_id已经是user_id）
    students_with_application_user_ids = set()
    if student_user_ids:
        application_students_result = await db.execute(
            select(JobApplication.student_id).where(
                JobApplication.student_id.in_(student_user_ids)
            ).distinct()
        )
        students_with_application_user_ids = set(row[0] for row in application_students_result.all() if row[0])
    
    # 合并去重
    active_student_user_ids = students_with_resume_user_ids | students_with_application_user_ids
    active_students = len(active_student_user_ids)
    
    # 按部门统计
    by_department = []
    if teacher.department_id:
        # 如果教师有部门，统计该部门的学生
        dept_query = select(
            StudentProfile.department_id,
            func.count(StudentProfile.id).label("count")
        ).where(
            StudentProfile.department_id == teacher.department_id
        ).group_by(StudentProfile.department_id)
        
        dept_result = await db.execute(dept_query)
        by_department = [
            {"department_id": row[0], "count": row[1]}
            for row in dept_result.all()
        ]
    
    return {
        "total_students": total_students,
        "active_students": min(active_students, total_students),
        "resume_count": resume_count,
        "application_count": application_count,
        "by_department": by_department
    }


@router.get("/platform/overview")
async def get_platform_overview(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    获取平台概览统计（仅管理员）
    
    Args:
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        dict: 平台统计数据
    """
    # 统计用户数
    from app.models.user import User
    user_count_query = select(func.count(User.id))
    user_result = await db.execute(user_count_query)
    total_users = user_result.scalar() or 0
    
    # 统计学生数
    student_count_query = select(func.count(StudentProfile.id))
    student_result = await db.execute(student_count_query)
    total_students = student_result.scalar() or 0
    
    # 统计职位数（所有状态的职位）
    from app.models.job import Job
    job_count_query = select(func.count(Job.id))
    job_result = await db.execute(job_count_query)
    total_jobs = job_result.scalar() or 0
    
    # 统计申请数
    application_count_query = select(func.count(JobApplication.id))
    application_result = await db.execute(application_count_query)
    total_applications = application_result.scalar() or 0
    
    # 统计双选会数（所有状态的双选会）
    job_fair_count_query = select(func.count(JobFair.id))
    job_fair_result = await db.execute(job_fair_count_query)
    total_job_fairs = job_fair_result.scalar() or 0
    
    # 统计宣讲会数（所有状态的宣讲会）
    info_session_count_query = select(func.count(InfoSession.id))
    info_session_result = await db.execute(info_session_count_query)
    total_info_sessions = info_session_result.scalar() or 0
    
    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_job_fairs": total_job_fairs,
        "total_info_sessions": total_info_sessions
    }

