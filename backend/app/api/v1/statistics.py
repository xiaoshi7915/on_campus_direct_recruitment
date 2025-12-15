"""
数据统计相关API路由（教师和管理员）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_teacher, require_admin
from app.models.profile import EnterpriseProfile
from app.models.user import User
from app.models.profile import StudentProfile, TeacherProfile
from app.models.job import JobApplication, Resume, Job
from app.models.interview import Interview, Offer
from app.models.activity import JobFair, InfoSession, JobFairRegistration, InfoSessionRegistration
from app.models.school import School, Department
from app.models.chat import ChatSession
from app.models.common import Favorite

router = APIRouter()


# ==================== 学生个人数据统计 ====================

@router.get("/student/personal")
async def get_student_personal_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学生个人数据统计
    
    Args:
        current_user: 当前登录用户（学生）
        db: 数据库会话
        
    Returns:
        dict: 个人统计数据
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "statistics:read:personal", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生用户才能查看个人统计"
        )
    
    # 获取学生信息
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生信息不存在"
        )
    
    # 统计职位申请
    applications_result = await db.execute(
        select(func.count()).where(JobApplication.student_id == student.id)
    )
    total_applications = applications_result.scalar() or 0
    
    # 统计已通过的申请
    accepted_applications_result = await db.execute(
        select(func.count()).where(
            JobApplication.student_id == student.id,
            JobApplication.status == "ACCEPTED"
        )
    )
    accepted_applications = accepted_applications_result.scalar() or 0
    
    # 统计面试
    from app.models.interview import Interview
    interviews_result = await db.execute(
        select(func.count()).where(Interview.student_id == student.id)
    )
    total_interviews = interviews_result.scalar() or 0
    
    # 统计Offer
    from app.models.interview import Offer
    offers_result = await db.execute(
        select(func.count()).where(Offer.student_id == student.id)
    )
    total_offers = offers_result.scalar() or 0
    
    # 统计已接受的Offer
    accepted_offers_result = await db.execute(
        select(func.count()).where(
            Offer.student_id == student.id,
            Offer.status == "ACCEPTED"
        )
    )
    accepted_offers = accepted_offers_result.scalar() or 0
    
    # 统计收藏
    from app.models.common import Favorite
    favorites_result = await db.execute(
        select(func.count()).where(Favorite.user_id == current_user.id)
    )
    total_favorites = favorites_result.scalar() or 0
    
    # 统计简历
    from app.models.job import Resume
    resumes_result = await db.execute(
        select(func.count()).where(Resume.student_id == student.id)
    )
    total_resumes = resumes_result.scalar() or 0
    
    # 统计待办事项
    from app.models.common import Schedule
    todos_result = await db.execute(
        select(func.count()).where(
            Schedule.user_id == current_user.id,
            Schedule.is_completed == False
        )
    )
    total_todos = todos_result.scalar() or 0
    
    return {
        "total_applications": total_applications,
        "accepted_applications": accepted_applications,
        "total_interviews": total_interviews,
        "total_offers": total_offers,
        "accepted_offers": accepted_offers,
        "total_favorites": total_favorites,
        "total_resumes": total_resumes,
        "total_todos": total_todos
    }


@router.get("/students/activity")
async def get_student_activity_statistics(
    start_date: Optional[str] = Query(None, description="开始日期（YYYY-MM-DD）"),
    end_date: Optional[str] = Query(None, description="结束日期（YYYY-MM-DD）"),
    department_id: Optional[str] = Query(None, description="院系ID"),
    current_user: User = Depends(require_teacher()),
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


@router.get("/job-fairs/analysis")
async def get_job_fair_analysis(
    start_date: Optional[str] = Query(None, description="开始日期（YYYY-MM-DD）"),
    end_date: Optional[str] = Query(None, description="结束日期（YYYY-MM-DD）"),
    school_id: Optional[str] = Query(None, description="学校ID"),
    department_id: Optional[str] = Query(None, description="院系ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取双选会统计分析（仅教师）
    支持多条件过滤：时间、学校、院系、状态
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        school_id: 学校ID
        department_id: 院系ID
        status_filter: 状态过滤
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        dict: 双选会统计数据
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
    query = select(JobFair)
    
    # 数据权限隔离：教师只能查看管辖范围内的双选会
    if teacher.school_id:
        query = query.where(JobFair.school_id == teacher.school_id)
    
    # 学校过滤
    if school_id:
        query = query.where(JobFair.school_id == school_id)
    
    # 状态过滤
    if status_filter:
        query = query.where(JobFair.status == status_filter)
    
    # 时间过滤
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.where(JobFair.start_time >= start_datetime)
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        # 结束日期应该包含整天，所以加一天
        end_datetime = end_datetime + timedelta(days=1)
        query = query.where(JobFair.start_time < end_datetime)
    
    # 获取双选会总数
    count_query = select(func.count(JobFair.id))
    if teacher.school_id:
        count_query = count_query.where(JobFair.school_id == teacher.school_id)
    if school_id:
        count_query = count_query.where(JobFair.school_id == school_id)
    if status_filter:
        count_query = count_query.where(JobFair.status == status_filter)
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        count_query = count_query.where(JobFair.start_time >= start_datetime)
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        count_query = count_query.where(JobFair.start_time < end_datetime)
    
    total_result = await db.execute(count_query)
    total_job_fairs = total_result.scalar() or 0
    
    # 获取符合条件的双选会ID列表
    job_fairs_result = await db.execute(query)
    job_fairs = job_fairs_result.scalars().all()
    job_fair_ids = [jf.id for jf in job_fairs]
    
    # 统计报名企业数
    registered_enterprises = 0
    if job_fair_ids:
        enterprise_count_query = select(func.count(func.distinct(JobFairRegistration.enterprise_id))).where(
            JobFairRegistration.job_fair_id.in_(job_fair_ids)
        )
        enterprise_result = await db.execute(enterprise_count_query)
        registered_enterprises = enterprise_result.scalar() or 0
    
    # 统计报名学生数（通过院系过滤）
    registered_students = 0
    if job_fair_ids and department_id:
        # 如果指定了院系，统计该院系的学生报名数
        from app.models.profile import StudentProfile
        student_ids_query = select(StudentProfile.user_id).where(
            StudentProfile.department_id == department_id
        )
        student_ids_result = await db.execute(student_ids_query)
        student_user_ids = [row[0] for row in student_ids_result.all() if row[0]]
        
        # 这里需要根据实际的报名表结构来统计
        # 假设有学生报名表，如果没有则需要通过其他方式统计
        registered_students = len(student_user_ids)  # 临时实现
    elif job_fair_ids and teacher.department_id:
        # 如果教师有部门，统计该部门的学生
        from app.models.profile import StudentProfile
        student_ids_query = select(StudentProfile.user_id).where(
            StudentProfile.department_id == teacher.department_id
        )
        student_ids_result = await db.execute(student_ids_query)
        student_user_ids = [row[0] for row in student_ids_result.all() if row[0]]
        registered_students = len(student_user_ids)  # 临时实现
    
    # 按状态统计
    by_status = []
    if job_fair_ids:
        status_query = select(
            JobFair.status,
            func.count(JobFair.id).label("count")
        ).where(
            JobFair.id.in_(job_fair_ids)
        ).group_by(JobFair.status)
        
        status_result = await db.execute(status_query)
        by_status = [
            {"status": row[0], "count": row[1]}
            for row in status_result.all()
        ]
    
    # 按学校统计
    by_school = []
    if job_fair_ids:
        school_query = select(
            JobFair.school_id,
            func.count(JobFair.id).label("count")
        ).where(
            JobFair.id.in_(job_fair_ids)
        ).group_by(JobFair.school_id)
        
        school_result = await db.execute(school_query)
        by_school = [
            {"school_id": row[0], "count": row[1]}
            for row in school_result.all()
        ]
    
    return {
        "total_job_fairs": total_job_fairs,
        "registered_enterprises": registered_enterprises,
        "registered_students": registered_students,
        "by_status": by_status,
        "by_school": by_school
    }


@router.get("/info-sessions/analysis")
async def get_info_session_analysis(
    start_date: Optional[str] = Query(None, description="开始日期（YYYY-MM-DD）"),
    end_date: Optional[str] = Query(None, description="结束日期（YYYY-MM-DD）"),
    school_id: Optional[str] = Query(None, description="学校ID"),
    department_id: Optional[str] = Query(None, description="院系ID"),
    enterprise_id: Optional[str] = Query(None, description="企业ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取宣讲会统计分析（仅教师）
    支持多条件过滤：时间、学校、院系、企业、状态
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        school_id: 学校ID
        department_id: 院系ID
        enterprise_id: 企业ID
        status_filter: 状态过滤
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        dict: 宣讲会统计数据
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
    query = select(InfoSession)
    
    # 数据权限隔离：教师只能查看管辖范围内的宣讲会
    if teacher.school_id:
        query = query.where(InfoSession.school_id == teacher.school_id)
    
    # 学校过滤
    if school_id:
        query = query.where(InfoSession.school_id == school_id)
    
    # 企业过滤
    if enterprise_id:
        query = query.where(InfoSession.enterprise_id == enterprise_id)
    
    # 状态过滤
    if status_filter:
        query = query.where(InfoSession.status == status_filter)
    
    # 时间过滤
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.where(InfoSession.start_time >= start_datetime)
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = end_datetime + timedelta(days=1)
        query = query.where(InfoSession.start_time < end_datetime)
    
    # 获取宣讲会总数
    count_query = select(func.count(InfoSession.id))
    if teacher.school_id:
        count_query = count_query.where(InfoSession.school_id == teacher.school_id)
    if school_id:
        count_query = count_query.where(InfoSession.school_id == school_id)
    if enterprise_id:
        count_query = count_query.where(InfoSession.enterprise_id == enterprise_id)
    if status_filter:
        count_query = count_query.where(InfoSession.status == status_filter)
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        count_query = count_query.where(InfoSession.start_time >= start_datetime)
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        count_query = count_query.where(InfoSession.start_time < end_datetime)
    
    total_result = await db.execute(count_query)
    total_info_sessions = total_result.scalar() or 0
    
    # 获取符合条件的宣讲会ID列表
    info_sessions_result = await db.execute(query)
    info_sessions = info_sessions_result.scalars().all()
    info_session_ids = [is_obj.id for is_obj in info_sessions]
    
    # 统计报名学生数
    registered_students = 0
    if info_session_ids:
        student_count_query = select(func.count(func.distinct(InfoSessionRegistration.student_id))).where(
            InfoSessionRegistration.session_id.in_(info_session_ids)
        )
        student_result = await db.execute(student_count_query)
        registered_students = student_result.scalar() or 0
    
    # 按状态统计
    by_status = []
    if info_session_ids:
        status_query = select(
            InfoSession.status,
            func.count(InfoSession.id).label("count")
        ).where(
            InfoSession.id.in_(info_session_ids)
        ).group_by(InfoSession.status)
        
        status_result = await db.execute(status_query)
        by_status = [
            {"status": row[0], "count": row[1]}
            for row in status_result.all()
        ]
    
    # 按企业统计
    by_enterprise = []
    if info_session_ids:
        enterprise_query = select(
            InfoSession.enterprise_id,
            func.count(InfoSession.id).label("count")
        ).where(
            InfoSession.id.in_(info_session_ids)
        ).group_by(InfoSession.enterprise_id)
        
        enterprise_result = await db.execute(enterprise_query)
        by_enterprise = [
            {"enterprise_id": row[0], "count": row[1]}
            for row in enterprise_result.all()
        ]
    
    return {
        "total_info_sessions": total_info_sessions,
        "registered_students": registered_students,
        "by_status": by_status,
        "by_enterprise": by_enterprise
    }


# ==================== 企业端数据统计 ====================

@router.get("/enterprise/personal")
async def get_enterprise_personal_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业个人数据统计
    
    Args:
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        dict: 企业统计数据
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "statistics:read:personal", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能查看企业统计"
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
    
    # 统计职位数
    from app.models.job import Job
    jobs_result = await db.execute(
        select(func.count(Job.id)).where(Job.enterprise_id == enterprise.id)
    )
    total_jobs = jobs_result.scalar() or 0
    
    # 统计已发布职位数
    published_jobs_result = await db.execute(
        select(func.count(Job.id)).where(
            Job.enterprise_id == enterprise.id,
            Job.status == "PUBLISHED"
        )
    )
    published_jobs = published_jobs_result.scalar() or 0
    
    # 统计职位申请数
    applications_result = await db.execute(
        select(func.count(JobApplication.id)).where(
            JobApplication.job_id.in_(
                select(Job.id).where(Job.enterprise_id == enterprise.id)
            )
        )
    )
    total_applications = applications_result.scalar() or 0
    
    # 统计已通过申请数
    accepted_applications_result = await db.execute(
        select(func.count(JobApplication.id)).where(
            JobApplication.job_id.in_(
                select(Job.id).where(Job.enterprise_id == enterprise.id)
            ),
            JobApplication.status == "ACCEPTED"
        )
    )
    accepted_applications = accepted_applications_result.scalar() or 0
    
    # 统计面试数
    interviews_result = await db.execute(
        select(func.count(Interview.id)).where(Interview.enterprise_id == enterprise.id)
    )
    total_interviews = interviews_result.scalar() or 0
    
    # 统计Offer数
    offers_result = await db.execute(
        select(func.count(Offer.id)).where(Offer.enterprise_id == enterprise.id)
    )
    total_offers = offers_result.scalar() or 0
    
    # 统计已接受Offer数
    accepted_offers_result = await db.execute(
        select(func.count(Offer.id)).where(
            Offer.enterprise_id == enterprise.id,
            Offer.status == "ACCEPTED"
        )
    )
    accepted_offers = accepted_offers_result.scalar() or 0
    
    # 统计收藏数（收藏的简历）
    favorites_result = await db.execute(
        select(func.count(Favorite.id)).where(
            Favorite.user_id == current_user.id,
            Favorite.target_type == "RESUME"
        )
    )
    total_favorites = favorites_result.scalar() or 0
    
    # 统计宣讲会数
    info_sessions_result = await db.execute(
        select(func.count(InfoSession.id)).where(InfoSession.enterprise_id == enterprise.id)
    )
    total_info_sessions = info_sessions_result.scalar() or 0
    
    # 统计双选会报名数
    job_fair_registrations_result = await db.execute(
        select(func.count(JobFairRegistration.id)).where(
            JobFairRegistration.enterprise_id == enterprise.id
        )
    )
    total_job_fair_registrations = job_fair_registrations_result.scalar() or 0
    
    # 统计聊天会话数（ChatSession使用user1_id和user2_id）
    chat_sessions_result = await db.execute(
        select(func.count(ChatSession.id)).where(
            or_(
                ChatSession.user1_id == current_user.id,
                ChatSession.user2_id == current_user.id
            )
        )
    )
    total_chat_sessions = chat_sessions_result.scalar() or 0
    
    # 统计触达人才数（通过申请、面试、Offer、收藏、聊天）
    from app.models.profile import StudentProfile
    
    # 通过申请触达的学生（JobApplication.student_id是user_id，需要转换为student_profiles.id）
    application_student_ids = set()
    if total_applications > 0:
        app_students_result = await db.execute(
            select(StudentProfile.id).join(
                JobApplication, StudentProfile.user_id == JobApplication.student_id
            ).where(
                JobApplication.job_id.in_(
                    select(Job.id).where(Job.enterprise_id == enterprise.id)
                )
            ).distinct()
        )
        application_student_ids = set(row[0] for row in app_students_result.all() if row[0])
    
    # 通过面试触达的学生
    interview_student_ids = set()
    if total_interviews > 0:
        interview_students_result = await db.execute(
            select(Interview.student_id).where(Interview.enterprise_id == enterprise.id).distinct()
        )
        interview_student_ids = set(row[0] for row in interview_students_result.all() if row[0])
    
    # 通过Offer触达的学生
    offer_student_ids = set()
    if total_offers > 0:
        offer_students_result = await db.execute(
            select(Offer.student_id).where(Offer.enterprise_id == enterprise.id).distinct()
        )
        offer_student_ids = set(row[0] for row in offer_students_result.all() if row[0])
    
    # 通过收藏触达的学生
    favorite_student_ids = set()
    if total_favorites > 0:
        favorite_resume_ids_result = await db.execute(
            select(Favorite.target_id).where(
                Favorite.user_id == current_user.id,
                Favorite.target_type == "RESUME"
            ).distinct()
        )
        favorite_resume_ids = set(row[0] for row in favorite_resume_ids_result.all() if row[0])
        if favorite_resume_ids:
            favorite_students_result = await db.execute(
                select(Resume.student_id).where(Resume.id.in_(favorite_resume_ids)).distinct()
            )
            favorite_student_ids = set(row[0] for row in favorite_students_result.all() if row[0])
    
    # 通过聊天触达的学生（ChatSession使用user1_id和user2_id）
    chat_student_ids = set()
    if total_chat_sessions > 0:
        # 查询user1_id为当前用户的会话
        chat_user_ids_result1 = await db.execute(
            select(ChatSession.user2_id).where(
                ChatSession.user1_id == current_user.id
            ).distinct()
        )
        chat_user_ids1 = set(row[0] for row in chat_user_ids_result1.all() if row[0])
        
        # 查询user2_id为当前用户的会话
        chat_user_ids_result2 = await db.execute(
            select(ChatSession.user1_id).where(
                ChatSession.user2_id == current_user.id
            ).distinct()
        )
        chat_user_ids2 = set(row[0] for row in chat_user_ids_result2.all() if row[0])
        
        chat_user_ids = chat_user_ids1 | chat_user_ids2
        if chat_user_ids:
            chat_students_result = await db.execute(
                select(StudentProfile.id).where(StudentProfile.user_id.in_(chat_user_ids)).distinct()
            )
            chat_student_ids = set(row[0] for row in chat_students_result.all() if row[0])
    
    # 合并去重
    all_talent_ids = application_student_ids | interview_student_ids | offer_student_ids | favorite_student_ids | chat_student_ids
    total_talents = len(all_talent_ids)
    
    # 按职位统计申请数
    applications_by_job = []
    if total_applications > 0:
        job_applications_result = await db.execute(
            select(
                JobApplication.job_id,
                func.count(JobApplication.id).label("count")
            ).where(
                JobApplication.job_id.in_(
                    select(Job.id).where(Job.enterprise_id == enterprise.id)
                )
            ).group_by(JobApplication.job_id)
        )
        applications_by_job = [
            {"job_id": row[0], "count": row[1]}
            for row in job_applications_result.all()
        ]
    
    return {
        "total_jobs": total_jobs,
        "published_jobs": published_jobs,
        "total_applications": total_applications,
        "accepted_applications": accepted_applications,
        "total_interviews": total_interviews,
        "total_offers": total_offers,
        "accepted_offers": accepted_offers,
        "total_favorites": total_favorites,
        "total_info_sessions": total_info_sessions,
        "total_job_fair_registrations": total_job_fair_registrations,
        "total_chat_sessions": total_chat_sessions,
        "total_talents": total_talents,
        "applications_by_job": applications_by_job
    }

