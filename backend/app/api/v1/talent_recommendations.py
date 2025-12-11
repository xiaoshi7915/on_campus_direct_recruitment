"""
人才推荐相关API路由（教师端）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_teacher
from app.models.user import User
from app.models.profile import TeacherProfile, StudentProfile
from app.models.job import Job, Resume, JobApplication
from pydantic import BaseModel, Field

router = APIRouter()


# ==================== Pydantic模式 ====================

class TalentRecommendationCreate(BaseModel):
    """创建人才推荐请求模式"""
    job_id: str = Field(..., description="职位ID")
    student_id: str = Field(..., description="学生ID")
    resume_id: Optional[str] = Field(None, description="简历ID（可选）")
    recommendation_note: Optional[str] = Field(None, description="推荐说明")


class TalentRecommendationResponse(BaseModel):
    """人才推荐响应模式"""
    id: str
    job_id: str
    student_id: str
    resume_id: Optional[str]
    recommendation_note: Optional[str]
    status: str
    created_at: str
    updated_at: str
    # 关联信息
    job_title: Optional[str] = None
    student_name: Optional[str] = None
    enterprise_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class TalentRecommendationListResponse(BaseModel):
    """人才推荐列表响应模式"""
    items: list[TalentRecommendationResponse]
    total: int
    page: int
    page_size: int


# ==================== 数据模型（临时使用，后续可创建独立表） ====================
# 注意：这里使用JobApplication表来存储推荐信息，通过status字段区分
# 实际应用中可以创建独立的talent_recommendations表


# ==================== API端点 ====================

@router.post("", response_model=TalentRecommendationResponse, status_code=status.HTTP_201_CREATED)
async def recommend_talent(
    recommendation_data: TalentRecommendationCreate,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    为某个职位推荐管辖内的学生人才
    
    Args:
        recommendation_data: 推荐数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        TalentRecommendationResponse: 推荐信息
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
    
    # 验证职位是否存在
    job_result = await db.execute(
        select(Job).where(Job.id == recommendation_data.job_id)
    )
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="职位不存在"
        )
    
    # 验证学生是否存在且在教师管辖范围内
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.id == recommendation_data.student_id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    # 数据权限检查
    if teacher.department_id:
        if student.department_id != teacher.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权推荐该学生"
            )
    elif teacher.school_id:
        if student.school_id != teacher.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权推荐该学生"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="教师尚未关联学校或院系，无法推荐学生"
        )
    
    # 获取或创建简历
    resume_id = recommendation_data.resume_id
    if not resume_id:
        # 如果没有指定简历，尝试获取学生的默认简历或第一个简历
        resume_result = await db.execute(
            select(Resume).where(Resume.student_id == student.id).limit(1)
        )
        resume = resume_result.scalar_one_or_none()
        if resume:
            resume_id = resume.id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学生没有简历，无法推荐"
            )
    
    # 检查是否已存在推荐或申请
    existing_result = await db.execute(
        select(JobApplication).where(
            JobApplication.job_id == recommendation_data.job_id,
            JobApplication.student_id == student.user_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        # 如果已存在，更新为推荐状态
        existing.status = "RECOMMENDED"
        if recommendation_data.recommendation_note:
            # 可以将推荐说明存储在某个字段中，这里暂时忽略
            pass
        await db.commit()
        await db.refresh(existing)
        
        return TalentRecommendationResponse(
            id=existing.id,
            job_id=existing.job_id,
            student_id=recommendation_data.student_id,
            resume_id=resume_id,
            recommendation_note=recommendation_data.recommendation_note,
            status=existing.status,
            created_at=existing.created_at.isoformat() if existing.created_at else datetime.now().isoformat(),
            updated_at=existing.updated_at.isoformat() if existing.updated_at else datetime.now().isoformat(),
            job_title=job.title,
            student_name=student.real_name
        )
    
    # 创建新的推荐（通过JobApplication表，status设为RECOMMENDED）
    recommendation = JobApplication(
        id=str(uuid4()),
        job_id=recommendation_data.job_id,
        student_id=student.user_id,
        resume_id=resume_id,
        status="RECOMMENDED"  # 使用特殊状态表示推荐
    )
    
    db.add(recommendation)
    await db.commit()
    await db.refresh(recommendation)
    
    # 获取企业名称
    enterprise_name = None
    if job.enterprise_id:
        from app.models.profile import EnterpriseProfile
        enterprise_result = await db.execute(
            select(EnterpriseProfile).where(EnterpriseProfile.id == job.enterprise_id)
        )
        enterprise = enterprise_result.scalar_one_or_none()
        if enterprise:
            enterprise_name = enterprise.company_name
    
    return TalentRecommendationResponse(
        id=recommendation.id,
        job_id=recommendation.job_id,
        student_id=recommendation_data.student_id,
        resume_id=resume_id,
        recommendation_note=recommendation_data.recommendation_note,
        status=recommendation.status,
        created_at=recommendation.created_at.isoformat() if recommendation.created_at else datetime.now().isoformat(),
        updated_at=recommendation.updated_at.isoformat() if recommendation.updated_at else datetime.now().isoformat(),
        job_title=job.title,
        student_name=student.real_name,
        enterprise_name=enterprise_name
    )


@router.get("", response_model=TalentRecommendationListResponse)
async def get_talent_recommendations(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    job_id: Optional[str] = Query(None, description="职位ID过滤"),
    student_id: Optional[str] = Query(None, description="学生ID过滤"),
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取人才推荐列表（仅教师，只能查看自己的推荐）
    
    Args:
        page: 页码
        page_size: 每页数量
        job_id: 职位ID过滤
        student_id: 学生ID过滤
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        TalentRecommendationListResponse: 推荐列表
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
    
    # 获取教师管辖范围内的学生user_id列表
    student_query = select(StudentProfile)
    if teacher.department_id:
        student_query = student_query.where(StudentProfile.department_id == teacher.department_id)
    elif teacher.school_id:
        student_query = student_query.where(StudentProfile.school_id == teacher.school_id)
    else:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }
    
    students_result = await db.execute(student_query)
    students = students_result.scalars().all()
    student_user_ids = [student.user_id for student in students]
    
    if not student_user_ids:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }
    
    # 构建查询条件（查找状态为RECOMMENDED的JobApplication）
    query = select(JobApplication).where(
        JobApplication.student_id.in_(student_user_ids),
        JobApplication.status == "RECOMMENDED"
    )
    
    # 职位ID过滤
    if job_id:
        query = query.where(JobApplication.job_id == job_id)
    
    # 学生ID过滤
    if student_id:
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.id == student_id)
        )
        student = student_result.scalar_one_or_none()
        if student and student.user_id in student_user_ids:
            query = query.where(JobApplication.student_id == student.user_id)
        else:
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(JobApplication.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    recommendations = result.scalars().all()
    
    # 构建响应数据
    recommendation_list = []
    for rec in recommendations:
        # 获取职位信息
        job_result = await db.execute(select(Job).where(Job.id == rec.job_id))
        job = job_result.scalar_one_or_none()
        job_title = job.title if job else None
        
        # 获取企业名称
        enterprise_name = None
        if job and job.enterprise_id:
            from app.models.profile import EnterpriseProfile
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.id == job.enterprise_id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                enterprise_name = enterprise.company_name
        
        # 获取学生信息
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == rec.student_id)
        )
        student = student_result.scalar_one_or_none()
        student_name = student.real_name if student else None
        student_profile_id = student.id if student else None
        
        recommendation_list.append(TalentRecommendationResponse(
            id=rec.id,
            job_id=rec.job_id,
            student_id=student_profile_id or "",
            resume_id=rec.resume_id,
            recommendation_note=None,  # 推荐说明需要存储在独立表中
            status=rec.status,
            created_at=rec.created_at.isoformat() if rec.created_at else datetime.now().isoformat(),
            updated_at=rec.updated_at.isoformat() if rec.updated_at else datetime.now().isoformat(),
            job_title=job_title,
            student_name=student_name,
            enterprise_name=enterprise_name
        ))
    
    return {
        "items": recommendation_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }




