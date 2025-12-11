"""
学生点评相关API路由（教师端）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_teacher
from app.models.user import User
from app.models.profile import TeacherProfile, StudentProfile
from app.models.student_comment import StudentComment
from pydantic import BaseModel, Field

router = APIRouter()


# ==================== Pydantic模式 ====================

class StudentCommentCreate(BaseModel):
    """创建学生点评请求模式"""
    student_id: str = Field(..., description="学生ID")
    content: str = Field(..., min_length=1, description="点评内容")
    score: Optional[int] = Field(None, ge=1, le=5, description="评分（1-5分）")
    tags: Optional[str] = Field(None, max_length=255, description="标签（逗号分隔）")
    is_public: Optional[str] = Field("PRIVATE", description="是否公开（PRIVATE/PUBLIC）")


class StudentCommentUpdate(BaseModel):
    """更新学生点评请求模式"""
    content: Optional[str] = Field(None, min_length=1, description="点评内容")
    score: Optional[int] = Field(None, ge=1, le=5, description="评分（1-5分）")
    tags: Optional[str] = Field(None, max_length=255, description="标签（逗号分隔）")
    is_public: Optional[str] = Field(None, description="是否公开（PRIVATE/PUBLIC）")


class StudentCommentResponse(BaseModel):
    """学生点评响应模式"""
    id: str
    teacher_id: str
    student_id: str
    content: str
    score: Optional[int]
    tags: Optional[str]
    is_public: str
    created_at: str
    updated_at: str
    # 关联信息
    teacher_name: Optional[str] = None
    student_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class StudentCommentListResponse(BaseModel):
    """学生点评列表响应模式"""
    items: list[StudentCommentResponse]
    total: int
    page: int
    page_size: int


# ==================== API端点 ====================

@router.get("", response_model=StudentCommentListResponse)
async def get_student_comments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    student_id: Optional[str] = Query(None, description="学生ID过滤"),
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学生点评列表（仅教师，只能查看自己的点评）
    
    Args:
        page: 页码
        page_size: 每页数量
        student_id: 学生ID过滤
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        StudentCommentListResponse: 点评列表
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
    query = select(StudentComment).where(StudentComment.teacher_id == teacher.id)
    
    # 学生ID过滤
    if student_id:
        # 验证学生是否在教师管辖范围内
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
        if teacher.department_id and student.department_id != teacher.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看该学生的点评"
            )
        elif teacher.school_id and student.school_id != teacher.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权查看该学生的点评"
            )
        
        query = query.where(StudentComment.student_id == student_id)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(StudentComment.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    comments = result.scalars().all()
    
    # 构建响应数据
    comment_list = []
    for comment in comments:
        # 获取教师和学生名称
        teacher_name = teacher.real_name
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.id == comment.student_id)
        )
        student = student_result.scalar_one_or_none()
        student_name = student.real_name if student else None
        
        comment_list.append(StudentCommentResponse(
            id=comment.id,
            teacher_id=comment.teacher_id,
            student_id=comment.student_id,
            content=comment.content,
            score=comment.score,
            tags=comment.tags,
            is_public=comment.is_public,
            created_at=comment.created_at.isoformat(),
            updated_at=comment.updated_at.isoformat(),
            teacher_name=teacher_name,
            student_name=student_name
        ))
    
    return {
        "items": comment_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{comment_id}", response_model=StudentCommentResponse)
async def get_student_comment(
    comment_id: str,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学生点评详情
    
    Args:
        comment_id: 点评ID
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        StudentCommentResponse: 点评详情
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
    
    # 获取点评
    comment_result = await db.execute(
        select(StudentComment).where(StudentComment.id == comment_id)
    )
    comment = comment_result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="点评不存在"
        )
    
    # 权限检查：只能查看自己的点评
    if comment.teacher_id != teacher.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此点评"
        )
    
    # 获取学生名称
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.id == comment.student_id)
    )
    student = student_result.scalar_one_or_none()
    student_name = student.real_name if student else None
    
    return StudentCommentResponse(
        id=comment.id,
        teacher_id=comment.teacher_id,
        student_id=comment.student_id,
        content=comment.content,
        score=comment.score,
        tags=comment.tags,
        is_public=comment.is_public,
        created_at=comment.created_at.isoformat(),
        updated_at=comment.updated_at.isoformat(),
        teacher_name=teacher.real_name,
        student_name=student_name
    )


@router.post("", response_model=StudentCommentResponse, status_code=status.HTTP_201_CREATED)
async def create_student_comment(
    comment_data: StudentCommentCreate,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    创建学生点评
    
    Args:
        comment_data: 点评数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        StudentCommentResponse: 创建的点评
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
    
    # 验证学生是否存在且在教师管辖范围内
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.id == comment_data.student_id)
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
                detail="无权点评该学生"
            )
    elif teacher.school_id:
        if student.school_id != teacher.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权点评该学生"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="教师尚未关联学校或院系，无法点评学生"
        )
    
    # 检查是否已存在点评
    existing_result = await db.execute(
        select(StudentComment).where(
            StudentComment.teacher_id == teacher.id,
            StudentComment.student_id == comment_data.student_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="已存在该学生的点评，请使用更新接口"
        )
    
    # 创建点评
    comment = StudentComment(
        id=str(uuid4()),
        teacher_id=teacher.id,
        student_id=comment_data.student_id,
        content=comment_data.content,
        score=comment_data.score,
        tags=comment_data.tags,
        is_public=comment_data.is_public or "PRIVATE"
    )
    
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    
    return StudentCommentResponse(
        id=comment.id,
        teacher_id=comment.teacher_id,
        student_id=comment.student_id,
        content=comment.content,
        score=comment.score,
        tags=comment.tags,
        is_public=comment.is_public,
        created_at=comment.created_at.isoformat(),
        updated_at=comment.updated_at.isoformat(),
        teacher_name=teacher.real_name,
        student_name=student.real_name
    )


@router.put("/{comment_id}", response_model=StudentCommentResponse)
async def update_student_comment(
    comment_id: str,
    comment_data: StudentCommentUpdate,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    更新学生点评
    
    Args:
        comment_id: 点评ID
        comment_data: 更新的点评数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        StudentCommentResponse: 更新后的点评
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
    
    # 获取点评
    comment_result = await db.execute(
        select(StudentComment).where(StudentComment.id == comment_id)
    )
    comment = comment_result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="点评不存在"
        )
    
    # 权限检查：只能更新自己的点评
    if comment.teacher_id != teacher.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权更新此点评"
        )
    
    # 更新点评
    update_data = comment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    await db.commit()
    await db.refresh(comment)
    
    # 获取学生名称
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.id == comment.student_id)
    )
    student = student_result.scalar_one_or_none()
    student_name = student.real_name if student else None
    
    return StudentCommentResponse(
        id=comment.id,
        teacher_id=comment.teacher_id,
        student_id=comment.student_id,
        content=comment.content,
        score=comment.score,
        tags=comment.tags,
        is_public=comment.is_public,
        created_at=comment.created_at.isoformat(),
        updated_at=comment.updated_at.isoformat(),
        teacher_name=teacher.real_name,
        student_name=student_name
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_comment(
    comment_id: str,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    删除学生点评
    
    Args:
        comment_id: 点评ID
        current_user: 当前登录用户（教师）
        db: 数据库会话
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
    
    # 获取点评
    comment_result = await db.execute(
        select(StudentComment).where(StudentComment.id == comment_id)
    )
    comment = comment_result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="点评不存在"
        )
    
    # 权限检查：只能删除自己的点评
    if comment.teacher_id != teacher.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此点评"
        )
    
    await db.delete(comment)
    await db.commit()

