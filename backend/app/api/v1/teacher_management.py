"""
教师管理相关API路由（主账号管理、审批、权限移交等）
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Optional, List
from uuid import uuid4
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_admin, require_teacher
from app.models.user import User
from app.models.profile import TeacherProfile, StudentProfile
from app.models.school import Class, Department

router = APIRouter()


# ==================== Pydantic模式 ====================

class SubAccountCreate(BaseModel):
    """创建子账号请求模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    real_name: str = Field(..., min_length=1, max_length=50, description="真实姓名")
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    title: Optional[str] = Field(None, description="职称")
    position: Optional[str] = Field(None, description="职务名称")


class TeacherApprovalRequest(BaseModel):
    """教师审批请求模式"""
    action: str = Field(..., description="审批操作（APPROVE-通过，REJECT-拒绝）")
    comment: Optional[str] = Field(None, description="审批意见")


class PermissionTransferRequest(BaseModel):
    """权限移交请求模式"""
    target_teacher_id: str = Field(..., description="目标教师ID")
    transfer_students: Optional[List[str]] = Field(None, description="要移交的学生ID列表（可选）")


class ClassTransferRequest(BaseModel):
    """班级移交请求模式"""
    target_teacher_id: str = Field(..., description="目标教师ID")
    class_ids: List[str] = Field(..., description="要移交的班级ID列表")


class TeacherResponse(BaseModel):
    """教师响应模式"""
    id: str
    user_id: str
    real_name: str
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    school_id: Optional[str] = None
    department_id: Optional[str] = None
    title: Optional[str] = None
    position: Optional[str] = None
    is_main_account: bool
    main_account_id: Optional[str] = None
    status: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True


class TeacherListResponse(BaseModel):
    """教师列表响应模式"""
    items: List[TeacherResponse]
    total: int
    page: int
    page_size: int


# ==================== 主子账号管理 ====================

@router.get("/sub-accounts", response_model=TeacherListResponse)
async def get_sub_accounts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取子账号列表（仅主账号）
    
    Args:
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        TeacherListResponse: 子账号列表
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
    
    # 检查是否是主账号
    # 如果是子账号，允许查看（但只能看到自己的信息）
    if not teacher.is_main_account:
        # 子账号只能看到自己的信息
        query = select(TeacherProfile).where(TeacherProfile.id == teacher.id)
    else:
        # 主账号可以查看所有子账号
        query = select(TeacherProfile).where(TeacherProfile.main_account_id == teacher.id)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(TeacherProfile.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    sub_accounts = result.scalars().all()
    
    # 构建响应数据
    teacher_list = []
    for sub_account in sub_accounts:
        # 获取用户信息
        user_result = await db.execute(select(User).where(User.id == sub_account.user_id))
        user = user_result.scalar_one_or_none()
        
        teacher_list.append(TeacherResponse(
            id=sub_account.id,
            user_id=sub_account.user_id,
            real_name=sub_account.real_name,
            username=user.username if user else None,
            phone=user.phone if user else None,
            email=user.email if user else None,
            school_id=sub_account.school_id,
            department_id=sub_account.department_id,
            title=sub_account.title,
            position=sub_account.position,
            is_main_account=sub_account.is_main_account,
            main_account_id=sub_account.main_account_id,
            status=user.status if user else None,
            created_at=sub_account.created_at.isoformat() if sub_account.created_at else ""
        ))
    
    return {
        "items": teacher_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/sub-accounts", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_sub_account(
    account_data: SubAccountCreate,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    创建子账号（仅主账号）
    
    Args:
        account_data: 子账号数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        TeacherResponse: 创建的子账号
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "sub_account:create", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师主账号才能创建子账号"
        )
    
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
    
    # 检查用户名是否已存在
    existing_user_result = await db.execute(
        select(User).where(User.username == account_data.username)
    )
    if existing_user_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )
    
    # 创建用户
    from app.core.security import get_password_hash
    new_user = User(
        id=str(uuid4()),
        username=account_data.username,
        phone=account_data.phone,
        email=account_data.email,
        password_hash=get_password_hash(account_data.password),
        user_type="TEACHER",
        status="ACTIVE"
    )
    db.add(new_user)
    await db.flush()
    
    # 创建子账号教师档案
    sub_account = TeacherProfile(
        id=str(uuid4()),
        user_id=new_user.id,
        real_name=account_data.real_name,
        school_id=teacher.school_id,  # 继承主账号的学校
        department_id=teacher.department_id,  # 继承主账号的院系
        title=account_data.title,
        position=account_data.position,
        is_main_account=False,
        main_account_id=teacher.id
    )
    db.add(sub_account)
    await db.commit()
    await db.refresh(sub_account)
    
    return TeacherResponse(
        id=sub_account.id,
        user_id=sub_account.user_id,
        real_name=sub_account.real_name,
        username=new_user.username,
        phone=new_user.phone,
        email=new_user.email,
        school_id=sub_account.school_id,
        department_id=sub_account.department_id,
        title=sub_account.title,
        position=sub_account.position,
        is_main_account=sub_account.is_main_account,
        main_account_id=sub_account.main_account_id,
        status=new_user.status,
        created_at=sub_account.created_at.isoformat() if sub_account.created_at else ""
    )


@router.delete("/sub-accounts/{sub_account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_account(
    sub_account_id: str,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    删除子账号（仅主账号）
    
    Args:
        sub_account_id: 子账号ID
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
    
    # 检查是否是主账号
    if not teacher.is_main_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有主账号才能删除子账号"
        )
    
    # 获取子账号
    sub_account_result = await db.execute(
        select(TeacherProfile).where(
            TeacherProfile.id == sub_account_id,
            TeacherProfile.main_account_id == teacher.id
        )
    )
    sub_account = sub_account_result.scalar_one_or_none()
    
    if not sub_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="子账号不存在或不属于此主账号"
        )
    
    # 删除用户（级联删除教师档案）
    user_result = await db.execute(select(User).where(User.id == sub_account.user_id))
    user = user_result.scalar_one_or_none()
    if user:
        await db.delete(user)
    
    await db.commit()


# ==================== 教师注册审批 ====================

@router.get("/pending-approvals", response_model=TeacherListResponse)
async def get_pending_teacher_approvals(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取待审批的教师列表（仅管理员）
    
    Args:
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        TeacherListResponse: 待审批教师列表
    """
    # 获取状态为PENDING的教师用户
    query = select(TeacherProfile).join(User).where(User.status == "PENDING")
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(TeacherProfile.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    teachers = result.scalars().all()
    
    # 构建响应数据
    teacher_list = []
    for teacher in teachers:
        user_result = await db.execute(select(User).where(User.id == teacher.user_id))
        user = user_result.scalar_one_or_none()
        
        teacher_list.append(TeacherResponse(
            id=teacher.id,
            user_id=teacher.user_id,
            real_name=teacher.real_name,
            username=user.username if user else None,
            phone=user.phone if user else None,
            email=user.email if user else None,
            school_id=teacher.school_id,
            department_id=teacher.department_id,
            title=teacher.title,
            position=teacher.position,
            is_main_account=teacher.is_main_account,
            main_account_id=teacher.main_account_id,
            status=user.status if user else None,
            created_at=teacher.created_at.isoformat() if teacher.created_at else ""
        ))
    
    return {
        "items": teacher_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/{teacher_id}/approve", response_model=dict)
async def approve_teacher_registration(
    teacher_id: str,
    approval_data: TeacherApprovalRequest,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    审批教师注册（仅管理员）
    
    Args:
        teacher_id: 教师ID
        approval_data: 审批数据
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        dict: 审批结果
    """
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.id == teacher_id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师不存在"
        )
    
    # 获取用户信息
    user_result = await db.execute(select(User).where(User.id == teacher.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 执行审批
    if approval_data.action == "APPROVE":
        user.status = "ACTIVE"
        await db.commit()
        return {
            "success": True,
            "message": "教师注册审批通过"
        }
    elif approval_data.action == "REJECT":
        user.status = "REJECTED"
        await db.commit()
        return {
            "success": True,
            "message": "教师注册审批拒绝"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的审批操作，必须是APPROVE或REJECT"
        )


# ==================== 权限移交 ====================

@router.post("/permission-transfer", response_model=dict)
async def transfer_permission(
    transfer_data: PermissionTransferRequest,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    权限移交（主账号可以将部分学生的管理权限移交给其他教师）
    
    Args:
        transfer_data: 移交数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        dict: 移交结果
    """
    # 获取当前教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师信息不存在"
        )
    
    # 检查是否是主账号
    if not teacher.is_main_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有主账号才能进行权限移交"
        )
    
    # 获取目标教师
    target_teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.id == transfer_data.target_teacher_id)
    )
    target_teacher = target_teacher_result.scalar_one_or_none()
    
    if not target_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="目标教师不存在"
        )
    
    # 验证目标教师是否在同一学校/院系
    if teacher.school_id and target_teacher.school_id != teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="目标教师必须与主账号在同一学校"
        )
    
    if teacher.department_id and target_teacher.department_id != teacher.department_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="目标教师必须与主账号在同一院系"
        )
    
    # 移交学生权限
    transferred_count = 0
    if transfer_data.transfer_students:
        for student_id in transfer_data.transfer_students:
            student_result = await db.execute(
                select(StudentProfile).where(StudentProfile.id == student_id)
            )
            student = student_result.scalar_one_or_none()
            
            if student and student.department_id == teacher.department_id:
                # 将学生的department_id设置为目标教师的department_id
                # 或者保持原样，只是逻辑上移交权限
                # 这里我们假设通过修改学生的department_id来实现权限移交
                if target_teacher.department_id:
                    student.department_id = target_teacher.department_id
                transferred_count += 1
    
    await db.commit()
    
    return {
        "success": True,
        "message": f"权限移交成功，已移交{transferred_count}个学生的管理权限"
    }


# ==================== 班级移交 ====================

@router.post("/class-transfer", response_model=dict)
async def transfer_class(
    transfer_data: ClassTransferRequest,
    current_user: User = Depends(require_teacher()),
    db: AsyncSession = Depends(get_db)
):
    """
    班级移交（主账号可以将班级的管理权限移交给其他教师）
    
    Args:
        transfer_data: 移交数据
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        dict: 移交结果
    """
    # 获取当前教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="教师信息不存在"
        )
    
    # 检查是否是主账号
    if not teacher.is_main_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有主账号才能进行班级移交"
        )
    
    # 获取目标教师
    target_teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.id == transfer_data.target_teacher_id)
    )
    target_teacher = target_teacher_result.scalar_one_or_none()
    
    if not target_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="目标教师不存在"
        )
    
    # 验证目标教师是否在同一学校/院系
    if teacher.school_id and target_teacher.school_id != teacher.school_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="目标教师必须与主账号在同一学校"
        )
    
    # 移交班级权限：将班级下的学生移交给目标教师
    transferred_count = 0
    for class_id in transfer_data.class_ids:
        # 获取班级
        class_result = await db.execute(select(Class).where(Class.id == class_id))
        class_obj = class_result.scalar_one_or_none()
        
        if not class_obj:
            continue
        
        # 验证班级是否在权限范围内
        if teacher.department_id and class_obj.department_id != teacher.department_id:
            continue
        
        # 将班级下的学生移交给目标教师（通过修改学生的department_id）
        if target_teacher.department_id:
            students_result = await db.execute(
                select(StudentProfile).where(StudentProfile.class_id == class_id)
            )
            students = students_result.scalars().all()
            
            for student in students:
                student.department_id = target_teacher.department_id
                transferred_count += 1
    
    await db.commit()
    
    return {
        "success": True,
        "message": f"班级移交成功，已移交{transferred_count}个学生的管理权限"
    }




