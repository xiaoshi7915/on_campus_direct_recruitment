"""
增强的权限管理模块
实现统一的权限检查机制和数据权限隔离
"""
from fastapi import Depends, HTTPException, status
from typing import List, Optional, Callable, Dict, Set
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.user_type import UserType
from app.models.profile import TeacherProfile, StudentProfile, EnterpriseProfile
from app.core.database import get_db


# ==================== 完善的权限定义 ====================

# 权限操作类型
PERMISSION_ACTIONS = {
    "create": "创建",
    "read": "查看",
    "update": "更新",
    "delete": "删除",
    "approve": "审批",
    "apply": "申请",
    "register": "报名",
    "invite": "邀请",
    "recommend": "推荐",
    "comment": "点评",
    "transfer": "移交"
}

# 完善的角色权限映射
ENHANCED_ROLE_PERMISSIONS: Dict[UserType, Set[str]] = {
    UserType.STUDENT: {
        # 简历管理
        "resume:create", "resume:read", "resume:update", "resume:delete",
        # 职位管理
        "job:read", "job:apply",
        # 申请管理
        "application:read", "application:create", "application:cancel",
        # 面试管理
        "interview:read", "interview:update",
        # Offer管理
        "offer:read", "offer:update",
        # 活动管理
        "job_fair:read", "job_fair:register",
        "info_session:read", "info_session:register",
        # 聊天
        "chat:read", "chat:write",
        # 其他
        "profile:read", "profile:update",
        "schedule:read", "schedule:write", "schedule:delete",
        "favorite:read", "favorite:write", "favorite:delete",
        "todo:read", "todo:write", "todo:delete",
        "feedback:create",
        "statistics:read:personal",
        "job_intention:read", "job_intention:write", "job_intention:delete"
    },
    UserType.ENTERPRISE: {
        # 职位管理
        "job:create", "job:read", "job:update", "job:delete",
        # 简历管理
        "resume:read",  # 仅申请学生的简历
        # 申请管理
        "application:read", "application:update",
        # 面试管理
        "interview:create", "interview:read", "interview:update",
        # Offer管理
        "offer:create", "offer:read", "offer:update", "offer:delete",
        # 活动管理
        "job_fair:create", "job_fair:read", "job_fair:update", "job_fair:register",
        "info_session:create", "info_session:read", "info_session:update", "info_session:delete", "info_session:invite",
        # 学校管理
        "school:read", "school:request_info_session", "school:favorite",
        # 聊天
        "chat:read", "chat:write",
        # 认证
        "verification:create:enterprise", "verification:create:personal", "verification:read",
        # 子账号管理
        "sub_account:create", "sub_account:read", "sub_account:delete",
        # 其他
        "profile:read", "profile:update",
        "schedule:read", "schedule:write",
        "favorite:read", "favorite:write",
        "upload:write",
        "statistics:read:personal",
        "talent:read", "talent:mark"
    },
    UserType.TEACHER: {
        # 学生管理
        "student:read", "student:update", "student:comment", "student:recommend",
        # 活动管理
        "job_fair:create", "job_fair:read", "job_fair:update", "job_fair:delete", "job_fair:approve",
        "info_session:create", "info_session:read", "info_session:update", "info_session:approve",
        # 院系管理
        "department:read",
        # 学校管理
        "school:read", "school:update", "school:verify",
        # 聊天
        "chat:read", "chat:write",
        # 审批
        "approval:job_fair", "approval:info_session",
        # 子账号管理
        "sub_account:create", "sub_account:read", "sub_account:delete",
        # 权限管理
        "permission:transfer", "class:transfer",
        # 其他
        "profile:read", "profile:update",
        "schedule:read", "schedule:write",
        "statistics:read:student_activity", "statistics:read:job_fair", "statistics:read:info_session",
        "teacher_management:read", "teacher_management:create", "teacher_management:delete"
    },
    UserType.ADMIN: {
        "*"  # 管理员拥有所有权限
    }
}

# 企业子账号权限限制
ENTERPRISE_SUB_ACCOUNT_RESTRICTIONS: Set[str] = {
    "job:create",  # 不能创建职位
    "job:delete",  # 不能删除职位
    "sub_account:create",  # 不能创建子账号
    "sub_account:delete",  # 不能删除子账号
    "verification:create:enterprise",  # 不能申请企业认证
    "verification:create:personal",  # 不能申请个人认证
    "job_fair:create",  # 不能创建双选会
}

# 教师子账号权限限制
TEACHER_SUB_ACCOUNT_RESTRICTIONS: Set[str] = {
    "job_fair:create",  # 不能创建双选会
    "info_session:create",  # 不能创建宣讲会
    "sub_account:create",  # 不能创建子账号
    "sub_account:delete",  # 不能删除子账号
    "permission:transfer",  # 不能移交权限
    "class:transfer",  # 不能移交班级
    "school:verify",  # 不能申请学校认证
}


# ==================== 统一的权限检查函数 ====================

async def check_permission(
    user: User,
    permission: str,
    db: Optional[AsyncSession] = None
) -> bool:
    """
    检查用户是否拥有指定权限
    
    Args:
        user: 用户对象
        permission: 权限字符串（格式：resource:action）
        db: 数据库会话（可选，用于检查子账号权限）
        
    Returns:
        bool: 是否有权限
    """
    # 管理员拥有所有权限
    if user.user_type == UserType.ADMIN:
        return True
    
    # 获取角色权限
    role_permissions = ENHANCED_ROLE_PERMISSIONS.get(user.user_type, set())
    
    # 检查通配符权限
    if "*" in role_permissions:
        return True
    
    # 检查具体权限
    if permission in role_permissions:
        # 如果是子账号，检查是否有权限限制
        if db:
            if user.user_type == UserType.ENTERPRISE:
                enterprise_result = await db.execute(
                    select(EnterpriseProfile).where(EnterpriseProfile.user_id == user.id)
                )
                enterprise = enterprise_result.scalar_one_or_none()
                if enterprise and not enterprise.is_main_account:
                    # 企业子账号权限限制
                    if permission in ENTERPRISE_SUB_ACCOUNT_RESTRICTIONS:
                        return False
            elif user.user_type == UserType.TEACHER:
                teacher_result = await db.execute(
                    select(TeacherProfile).where(TeacherProfile.user_id == user.id)
                )
                teacher = teacher_result.scalar_one_or_none()
                if teacher and not teacher.is_main_account:
                    # 教师子账号权限限制
                    if permission in TEACHER_SUB_ACCOUNT_RESTRICTIONS:
                        return False
        
        return True
    
    return False


async def check_data_permission_enhanced(
    resource_type: str,
    resource_id: str,
    current_user: User,
    db: AsyncSession,
    action: str = "read"
) -> bool:
    """
    增强的数据权限检查函数
    
    Args:
        resource_type: 资源类型（job, application, resume等）
        resource_id: 资源ID
        current_user: 当前用户
        db: 数据库会话
        action: 操作类型（read, update, delete）
        
    Returns:
        bool: 是否有权限
    """
    # 管理员拥有所有权限
    if current_user.user_type == UserType.ADMIN:
        return True
    
    # 根据资源类型检查权限
    if resource_type == "resume":
        # 简历权限检查
        from app.models.job import Resume
        resume_result = await db.execute(
            select(Resume).where(Resume.id == resource_id)
        )
        resume = resume_result.scalar_one_or_none()
        if not resume:
            return False
        
        # 获取学生信息
        student_result = await db.execute(
            select(StudentProfile).where(StudentProfile.id == resume.student_id)
        )
        student = student_result.scalar_one_or_none()
        if not student:
            return False
        
        # 学生：只能操作自己的简历
        if current_user.user_type == UserType.STUDENT:
            return student.user_id == current_user.id
        
        # 企业：只能查看申请学生的简历
        elif current_user.user_type == UserType.ENTERPRISE:
            # 检查是否有该学生的申请
            from app.models.job import JobApplication
            application_result = await db.execute(
                select(JobApplication).where(
                    JobApplication.student_id == student.user_id,
                    JobApplication.resume_id == resource_id
                )
            )
            application = application_result.scalar_one_or_none()
            if application:
                # 检查申请是否属于当前企业
                from app.models.job import Job
                job_result = await db.execute(
                    select(Job).where(Job.id == application.job_id)
                )
                job = job_result.scalar_one_or_none()
                if job:
                    enterprise_result = await db.execute(
                        select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
                    )
                    enterprise = enterprise_result.scalar_one_or_none()
                    if enterprise:
                        from app.services.enterprise_service import get_enterprise_ids_for_query
                        enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                        return job.enterprise_id in enterprise_ids
        
        # 教师：只能查看管辖学生的简历
        elif current_user.user_type == UserType.TEACHER:
            teacher_result = await db.execute(
                select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
            )
            teacher = teacher_result.scalar_one_or_none()
            if teacher:
                # 检查学生是否在管辖范围内
                if teacher.department_id and student.department_id:
                    return teacher.department_id == student.department_id
                elif teacher.school_id and student.school_id:
                    return teacher.school_id == student.school_id
        
        return False
    
    elif resource_type == "application":
        # 申请权限检查
        from app.models.job import JobApplication
        application_result = await db.execute(
            select(JobApplication).where(JobApplication.id == resource_id)
        )
        application = application_result.scalar_one_or_none()
        if not application:
            return False
        
        # 学生：只能操作自己的申请
        if current_user.user_type == UserType.STUDENT:
            return application.student_id == current_user.id
        
        # 企业：只能操作自己职位的申请
        elif current_user.user_type == UserType.ENTERPRISE:
            from app.models.job import Job
            job_result = await db.execute(
                select(Job).where(Job.id == application.job_id)
            )
            job = job_result.scalar_one_or_none()
            if job:
                enterprise_result = await db.execute(
                    select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
                )
                enterprise = enterprise_result.scalar_one_or_none()
                if enterprise:
                    from app.services.enterprise_service import get_enterprise_ids_for_query
                    enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                    return job.enterprise_id in enterprise_ids
        
        return False
    
    elif resource_type == "job":
        # 职位权限检查
        from app.models.job import Job
        job_result = await db.execute(
            select(Job).where(Job.id == resource_id)
        )
        job = job_result.scalar_one_or_none()
        if not job:
            return False
        
        # 企业：只能操作自己的职位
        if current_user.user_type == UserType.ENTERPRISE:
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                from app.services.enterprise_service import get_enterprise_ids_for_query
                enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                return job.enterprise_id in enterprise_ids
        
        # 学生：只能查看已发布的职位
        elif current_user.user_type == UserType.STUDENT:
            return job.status == "PUBLISHED"
        
        # 教师和管理员：可以查看所有职位
        elif current_user.user_type in [UserType.TEACHER, UserType.ADMIN]:
            return True
        
        return False
    
    # 其他资源类型的权限检查...
    
    return False


def require_permission_enhanced(
    *permissions: str,
    check_data_owner: bool = False,
    resource_type: Optional[str] = None,
    resource_id_param: str = "id"
):
    """
    增强的权限检查装饰器
    
    Args:
        *permissions: 需要的权限列表
        check_data_owner: 是否检查数据所有者
        resource_type: 资源类型（如果check_data_owner为True）
        resource_id_param: 资源ID参数名
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户
            current_user = None
            db = None
            
            for key, value in kwargs.items():
                if isinstance(value, User):
                    current_user = value
                elif isinstance(value, AsyncSession):
                    db = value
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录"
                )
            
            # 检查权限
            for permission in permissions:
                has_permission = await check_permission(current_user, permission, db)
                if not has_permission:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"缺少权限：{permission}"
                    )
            
            # 检查数据权限
            if check_data_owner and resource_type and db:
                resource_id = kwargs.get(resource_id_param)
                if resource_id:
                    has_data_permission = await check_data_permission_enhanced(
                        resource_type,
                        resource_id,
                        current_user,
                        db
                    )
                    if not has_data_permission:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="无权访问此资源"
                        )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

