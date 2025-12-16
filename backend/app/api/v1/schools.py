"""
学校信息管理相关API路由（教师端和企业端）
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, case
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.api.v1.auth import get_current_user, get_current_user_optional
from app.core.permissions import require_teacher
from app.models.user import User
from app.models.profile import TeacherProfile, EnterpriseProfile
from app.models.school import School

router = APIRouter()


# ==================== Pydantic模式 ====================

class SchoolVerificationRequest(BaseModel):
    """学校实名认证请求模式"""
    verification_documents: Optional[str] = Field(None, description="认证材料（JSON字符串或描述）")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=100, description="联系邮箱")


class SchoolResponse(BaseModel):
    """学校响应模式"""
    id: str
    name: str
    code: Optional[str]
    province: Optional[str]
    city: Optional[str]
    address: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    description: Optional[str]
    is_verified: bool
    # 新增字段：主管部门、院系介绍、主要专业介绍
    charge_dep: Optional[str] = None  # 主管部门
    department: Optional[str] = None  # 院系介绍
    major: Optional[str] = None  # 主要专业介绍
    # 扩展字段：双一流、211/985、学校类型、办学性质、办学层次等
    dual_class: Optional[str] = None  # 双一流建设学科代码
    dual_class_name: Optional[str] = None  # 双一流建设学科名称
    f211: Optional[str] = None  # 是否211（是/否）
    f985: Optional[str] = None  # 是否985（是/否）
    school_type: Optional[str] = None  # 类型代码
    school_type_name: Optional[str] = None  # 类型名称
    nature: Optional[str] = None  # 办学性质代码
    nature_name: Optional[str] = None  # 办学性质（公办、民办、中外合作等）
    is_top: Optional[str] = None  # 是否顶尖高校（是/否）
    level: Optional[str] = None  # 办学层次代码
    level_name: Optional[str] = None  # 办学层次名称（本科、专科）
    created_at: str
    updated_at: str
    # 关联信息（可选，用于前端显示）
    student_count: Optional[int] = None  # 学生数量
    department_count: Optional[int] = None  # 院系数量
    
    class Config:
        from_attributes = True


class SchoolListResponse(BaseModel):
    """学校列表响应模式"""
    items: list[SchoolResponse]
    total: int
    page: int
    page_size: int


# ==================== API端点 ====================

# ==================== 企业端学校功能 ====================

@router.get("", response_model=SchoolListResponse)
async def get_schools(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索（学校名称、代码）"),
    province: Optional[str] = Query(None, description="省份过滤"),
    city: Optional[str] = Query(None, description="城市过滤"),
    is_verified: Optional[bool] = Query(None, description="是否认证过滤"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学校列表（企业端和公开访问）
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词搜索
        province: 省份过滤
        city: 城市过滤
        is_verified: 是否认证过滤
        current_user: 当前登录用户（可选）
        db: 数据库会话
        
    Returns:
        SchoolListResponse: 学校列表
    """
    # 构建查询
    query = select(School)
    
    # 关键词搜索
    if keyword:
        query = query.where(
            or_(
                School.name.contains(keyword),
                School.code.contains(keyword) if School.code else False
            )
        )
    
    # 省份过滤
    if province:
        query = query.where(School.province == province)
    
    # 城市过滤
    if city:
        query = query.where(School.city == city)
    
    # 认证状态过滤
    if is_verified is not None:
        query = query.where(School.is_verified == is_verified)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 构建排序逻辑
    # 优先级顺序：1. f985为1或2 -> 2. f211为1或2 -> 3. 北京市 -> 4. 上海市 -> 5. 其他按名称排序
    # 使用多个排序字段来实现优先级
    
    # 分页查询，按照优先级排序
    offset = (page - 1) * page_size
    
    # 构建排序：使用case语句为每个条件分配优先级值
    # f985优先级字段：f985为1或2时值为0，否则为1
    f985_priority = case(
        (or_(School.f985 == '1', School.f985 == '2'), 0),
        else_=1
    )
    
    # f211优先级字段：f211为1或2时值为0，否则为1（但只在f985不是1或2时生效）
    f211_priority = case(
        (or_(School.f211 == '1', School.f211 == '2'), 0),
        else_=1
    )
    
    # 城市优先级字段：北京市为0，上海市为1，其他为2
    city_priority = case(
        (School.city == '北京市', 0),
        (School.city == '上海市', 1),
        else_=2
    )
    
    # 排序逻辑：
    # 1. 首先按f985优先级排序（f985=1或2的排前面）
    # 2. 然后按f211优先级排序（f211=1或2的排前面，但f985优先的已经排好了）
    # 3. 然后按城市优先级排序（北京市、上海市优先）
    # 4. 最后按学校名称排序
    query = query.order_by(
        f985_priority.asc(),      # f985为1或2的优先（值为0）
        f211_priority.asc(),      # f211为1或2的优先（值为0）
        city_priority.asc(),      # 北京市(0)、上海市(1)优先
        School.name.asc()         # 同优先级按名称排序
    ).offset(offset).limit(page_size)
    result = await db.execute(query)
    schools = result.scalars().all()
    
    # 转换为响应格式并填充关联信息
    school_list = []
    for school in schools:
        # 统计学生数量
        from app.models.profile import StudentProfile
        student_count_result = await db.execute(
            select(func.count(StudentProfile.id)).where(StudentProfile.school_id == school.id)
        )
        student_count = student_count_result.scalar() or 0
        
        # 统计院系数量
        from app.models.school import Department
        dept_count_result = await db.execute(
            select(func.count(Department.id)).where(Department.school_id == school.id)
        )
        department_count = dept_count_result.scalar() or 0
        
        school_dict = {
            **school.__dict__,
            "created_at": school.created_at.isoformat() if school.created_at else "",
            "updated_at": school.updated_at.isoformat() if school.updated_at else "",
            "student_count": student_count,
            "department_count": department_count
        }
        school_list.append(SchoolResponse.model_validate(school_dict))
    
    return {
        "items": school_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


# ==================== 教师端学校功能 ====================
# 注意：这些路由必须在 /{school_id} 路由之前定义，避免路由冲突

@router.get("/my-school", response_model=SchoolResponse)
async def get_my_school(
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前教师所属的学校信息
    
    Args:
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        SchoolResponse: 学校信息
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
    
    if not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师尚未关联学校"
        )
    
    # 获取学校信息
    school_result = await db.execute(
        select(School).where(School.id == teacher.school_id)
    )
    school = school_result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校信息不存在"
        )
    
    # 转换为响应格式，确保 datetime 字段序列化为字符串
    return SchoolResponse.model_validate({
        **school.__dict__,
        "created_at": school.created_at.isoformat() if school.created_at else "",
        "updated_at": school.updated_at.isoformat() if school.updated_at else ""
    })


@router.get("/{school_id}/share-link", response_model=dict)
async def get_school_share_link(
    school_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学校分享链接
    
    Args:
        school_id: 学校ID
        current_user: 当前登录用户（可选）
        db: 数据库会话
        
    Returns:
        dict: 分享链接信息
    """
    # 检查学校是否存在
    school_result = await db.execute(select(School).where(School.id == school_id))
    school = school_result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在"
        )
    
    # 生成分享链接（前端URL）
    from app.core.config import settings
    # 如果没有配置FRONTEND_URL，使用默认值
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:8008')
    share_url = f"{frontend_url}/schools/{school_id}"
    
    return {
        "school_id": school_id,
        "school_name": school.name,
        "share_url": share_url,
        "share_text": f"推荐学校：{school.name}",
        "share_image": school.logo_url if school.logo_url else None
    }


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    获取学校详情（企业端和公开访问）
    
    Args:
        school_id: 学校ID
        current_user: 当前登录用户（可选）
        db: 数据库会话
        
    Returns:
        SchoolResponse: 学校详情
    """
    # 获取学校信息
    school_result = await db.execute(select(School).where(School.id == school_id))
    school = school_result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在"
        )
    
    # 统计学生数量
    from app.models.profile import StudentProfile
    student_count_result = await db.execute(
        select(func.count(StudentProfile.id)).where(StudentProfile.school_id == school.id)
    )
    student_count = student_count_result.scalar() or 0
    
    # 统计院系数量
    from app.models.school import Department
    dept_count_result = await db.execute(
        select(func.count(Department.id)).where(Department.school_id == school.id)
    )
    department_count = dept_count_result.scalar() or 0
    
    # 转换为响应格式
    school_dict = {
        **school.__dict__,
        "created_at": school.created_at.isoformat() if school.created_at else "",
        "updated_at": school.updated_at.isoformat() if school.updated_at else "",
        "student_count": student_count,
        "department_count": department_count
    }
    
    return SchoolResponse.model_validate(school_dict)


@router.post("/my-school/verify", response_model=SchoolResponse)
async def request_school_verification(
    verification_data: SchoolVerificationRequest,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    申请学校实名认证
    
    Args:
        verification_data: 认证申请数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        SchoolResponse: 学校信息（认证状态可能仍为未认证，需要管理员审核）
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
    
    if not teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="教师尚未关联学校，无法申请认证"
        )
    
    # 获取学校信息
    school_result = await db.execute(
        select(School).where(School.id == teacher.school_id)
    )
    school = school_result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校信息不存在"
        )
    
    # 如果已经认证，直接返回
    if school.is_verified:
        return SchoolResponse.model_validate({
            **school.__dict__,
            "created_at": school.created_at.isoformat() if school.created_at else "",
            "updated_at": school.updated_at.isoformat() if school.updated_at else ""
        })
    
    # 这里可以添加认证申请记录到数据库的逻辑
    # 目前只是返回学校信息，实际认证需要管理员审核
    # 可以创建一个 school_verification_requests 表来记录申请
    
    # 返回学校信息（认证状态仍为未认证，等待管理员审核）
    return SchoolResponse.model_validate({
        **school.__dict__,
        "created_at": school.created_at.isoformat() if school.created_at else "",
        "updated_at": school.updated_at.isoformat() if school.updated_at else ""
    })


# ==================== 企业端申请线下宣讲会 ====================

class OfflineInfoSessionRequest(BaseModel):
    """申请线下宣讲会请求模式"""
    school_id: str = Field(..., description="学校ID")
    title: str = Field(..., min_length=1, max_length=100, description="宣讲会标题")
    description: Optional[str] = Field(None, description="描述")
    proposed_start_time: datetime = Field(..., description="建议开始时间")
    proposed_end_time: datetime = Field(..., description="建议结束时间")
    proposed_location: Optional[str] = Field(None, max_length=255, description="建议地点")
    max_students: Optional[int] = Field(None, ge=1, description="最大学生数")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=100, description="联系邮箱")
    message: Optional[str] = Field(None, description="申请留言")


@router.post("/{school_id}/request-info-session", response_model=dict, status_code=status.HTTP_201_CREATED)
async def request_offline_info_session(
    school_id: str,
    request_data: OfflineInfoSessionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    企业向学校申请线下宣讲会
    
    Args:
        school_id: 学校ID
        request_data: 申请数据
        current_user: 当前登录用户（企业）
        db: 数据库会话
        
    Returns:
        dict: 申请结果
    """
    # 检查用户类型
    if current_user.user_type != "ENTERPRISE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能申请线下宣讲会"
        )
    
    # 检查学校是否存在
    school_result = await db.execute(select(School).where(School.id == school_id))
    school = school_result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在"
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
    
    # 子账号创建时使用主账号ID
    from app.services.enterprise_service import get_effective_enterprise_id
    effective_enterprise_id = await get_effective_enterprise_id(db, enterprise)
    
    # 创建宣讲会（状态为PENDING，等待学校审批）
    from app.models.activity import InfoSession
    from uuid import uuid4
    
    info_session = InfoSession(
        id=str(uuid4()),
        enterprise_id=effective_enterprise_id,
        school_id=school_id,
        title=request_data.title,
        description=request_data.description,
        start_time=request_data.proposed_start_time,
        end_time=request_data.proposed_end_time,
        location=request_data.proposed_location,
        session_type="OFFLINE",
        status="PENDING",  # 等待学校审批
        max_students=request_data.max_students
    )
    
    db.add(info_session)
    await db.commit()
    await db.refresh(info_session)
    
    return {
        "message": "申请已提交，等待学校审批",
        "info_session_id": info_session.id,
        "status": "PENDING"
    }



