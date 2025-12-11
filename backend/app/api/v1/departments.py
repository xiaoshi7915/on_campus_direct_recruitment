"""
院系信息管理相关API路由（教师端）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_teacher
from app.models.user import User
from app.models.profile import TeacherProfile
from app.models.school import Department, School
from pydantic import BaseModel, Field

router = APIRouter()


# ==================== Pydantic模式 ====================

class DepartmentCreate(BaseModel):
    """创建院系请求模式"""
    name: str = Field(..., min_length=1, max_length=100, description="院系名称")
    code: Optional[str] = Field(None, max_length=50, description="院系代码")
    description: Optional[str] = Field(None, description="描述")
    honors: Optional[str] = Field(None, description="资质荣誉")


class DepartmentUpdate(BaseModel):
    """更新院系请求模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="院系名称")
    code: Optional[str] = Field(None, max_length=50, description="院系代码")
    description: Optional[str] = Field(None, description="描述")
    honors: Optional[str] = Field(None, description="资质荣誉")


class DepartmentResponse(BaseModel):
    """院系响应模式"""
    id: str
    school_id: str
    name: str
    code: Optional[str]
    description: Optional[str]
    honors: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class DepartmentListResponse(BaseModel):
    """院系列表响应模式"""
    items: list[DepartmentResponse]
    total: int
    page: int
    page_size: int


# ==================== API端点 ====================

@router.get("", response_model=DepartmentListResponse)
async def get_departments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索（名称、代码）"),
    school_id: Optional[str] = Query(None, description="学校ID过滤"),
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取院系列表（仅教师，只能查看自己学校的院系）
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词搜索
        school_id: 学校ID过滤
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        DepartmentListResponse: 院系列表
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
    
    # 数据权限隔离：教师只能查看自己学校的院系
    if not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您还没有关联学校，无法查看院系信息"
        )
    
    # 构建查询条件
    query = select(Department).where(Department.school_id == teacher.school_id)
    
    # 如果指定了school_id，验证是否与教师的学校一致
    if school_id and school_id != teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看其他学校的院系信息"
        )
    
    # 关键词搜索
    if keyword:
        query = query.where(
            or_(
                Department.name.contains(keyword),
                Department.code.contains(keyword) if Department.code else False
            )
        )
    
    # 获取总数
    count_query = select(func.count(Department.id)).where(Department.school_id == teacher.school_id)
    if keyword:
        count_query = count_query.where(
            or_(
                Department.name.contains(keyword),
                Department.code.contains(keyword) if Department.code else False
            )
        )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Department.name.asc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    departments = result.scalars().all()
    
    # 转换为响应模型
    department_responses = []
    for dept in departments:
        dept_dict = {
            "id": dept.id,
            "school_id": dept.school_id,
            "name": dept.name,
            "code": dept.code,
            "description": dept.description,
            "honors": getattr(dept, 'honors', None),  # 如果模型中没有honors字段，返回None
            "created_at": dept.created_at.isoformat() if dept.created_at else "",
            "updated_at": dept.updated_at.isoformat() if dept.updated_at else "",
        }
        department_responses.append(DepartmentResponse(**dept_dict))
    
    return {
        "items": department_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: str,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取院系详情（仅教师）
    
    Args:
        department_id: 院系ID
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        DepartmentResponse: 院系详情
    """
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher or not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看院系信息"
        )
    
    # 获取院系信息
    dept_result = await db.execute(
        select(Department).where(
            Department.id == department_id,
            Department.school_id == teacher.school_id
        )
    )
    department = dept_result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院系不存在或无权查看"
        )
    
    dept_dict = {
        "id": department.id,
        "school_id": department.school_id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
        "honors": getattr(department, 'honors', None),
        "created_at": department.created_at.isoformat() if department.created_at else "",
        "updated_at": department.updated_at.isoformat() if department.updated_at else "",
    }
    return DepartmentResponse(**dept_dict)


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_data: DepartmentCreate,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    创建院系（仅教师）
    
    Args:
        department_data: 院系数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        DepartmentResponse: 创建的院系
    """
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher or not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您还没有关联学校，无法创建院系"
        )
    
    # 检查院系名称是否已存在（同一学校内）
    existing_dept_result = await db.execute(
        select(Department).where(
            Department.school_id == teacher.school_id,
            Department.name == department_data.name
        )
    )
    if existing_dept_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该院系名称已存在"
        )
    
    # 创建院系
    department = Department(
        id=str(uuid4()),
        school_id=teacher.school_id,
        name=department_data.name,
        code=department_data.code,
        description=department_data.description,
    )
    
    # 如果模型有honors字段，设置它
    if hasattr(department, 'honors'):
        department.honors = department_data.honors
    
    db.add(department)
    await db.commit()
    await db.refresh(department)
    
    dept_dict = {
        "id": department.id,
        "school_id": department.school_id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
        "honors": getattr(department, 'honors', None),
        "created_at": department.created_at.isoformat() if department.created_at else "",
        "updated_at": department.updated_at.isoformat() if department.updated_at else "",
    }
    return DepartmentResponse(**dept_dict)


@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: str,
    department_data: DepartmentUpdate,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    更新院系（仅教师）
    
    Args:
        department_id: 院系ID
        department_data: 院系更新数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        DepartmentResponse: 更新后的院系
    """
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher or not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权更新院系信息"
        )
    
    # 获取院系信息
    dept_result = await db.execute(
        select(Department).where(
            Department.id == department_id,
            Department.school_id == teacher.school_id
        )
    )
    department = dept_result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院系不存在或无权更新"
        )
    
    # 如果更新名称，检查是否与其他院系重名
    if department_data.name and department_data.name != department.name:
        existing_dept_result = await db.execute(
            select(Department).where(
                Department.school_id == teacher.school_id,
                Department.name == department_data.name,
                Department.id != department_id
            )
        )
        if existing_dept_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该院系名称已存在"
            )
    
    # 更新院系信息
    if department_data.name is not None:
        department.name = department_data.name
    if department_data.code is not None:
        department.code = department_data.code
    if department_data.description is not None:
        department.description = department_data.description
    if hasattr(department, 'honors') and department_data.honors is not None:
        department.honors = department_data.honors
    
    await db.commit()
    await db.refresh(department)
    
    dept_dict = {
        "id": department.id,
        "school_id": department.school_id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
        "honors": getattr(department, 'honors', None),
        "created_at": department.created_at.isoformat() if department.created_at else "",
        "updated_at": department.updated_at.isoformat() if department.updated_at else "",
    }
    return DepartmentResponse(**dept_dict)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: str,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    删除院系（仅教师）
    
    Args:
        department_id: 院系ID
        current_user: 当前登录用户（教师）
        db: 数据库会话
    """
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher or not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除院系"
        )
    
    # 获取院系信息
    dept_result = await db.execute(
        select(Department).where(
            Department.id == department_id,
            Department.school_id == teacher.school_id
        )
    )
    department = dept_result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院系不存在或无权删除"
        )
    
    # 检查是否有学生或教师关联该院系
    from app.models.profile import StudentProfile
    student_count_result = await db.execute(
        select(func.count(StudentProfile.id)).where(StudentProfile.department_id == department_id)
    )
    student_count = student_count_result.scalar() or 0
    
    teacher_count_result = await db.execute(
        select(func.count(TeacherProfile.id)).where(TeacherProfile.department_id == department_id)
    )
    teacher_count = teacher_count_result.scalar() or 0
    
    if student_count > 0 or teacher_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该院系下还有{student_count}个学生和{teacher_count}个教师，无法删除"
        )
    
    await db.delete(department)
    await db.commit()

