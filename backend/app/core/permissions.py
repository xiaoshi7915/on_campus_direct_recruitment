"""
权限管理模块
实现基于角色的权限控制（RBAC）和数据权限隔离
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
    "transfer": "移交",
    "cancel": "取消"
}

# ==================== 模块化权限定义 ====================

# 功能模块定义
MODULES = {
    "settings": {
        "name": "个人设置",
        "icon": "settings",
        "permissions": [
            "settings:profile",  # 个人中心管理
            "settings:feedback",  # 意见反馈
            "settings:sub_account",  # 子账号管理（仅主账号）
            "settings:system_message",  # 系统消息
            "settings:schedule",  # 日程管理
        ]
    },
    "job": {
        "name": "职位管理",
        "icon": "briefcase",
        "permissions": [
            "job:create", "job:read", "job:update", "job:delete",
            "job:apply", "job:publish"
        ]
    },
    "talent": {
        "name": "人才管理",
        "icon": "users",
        "permissions": [
            "talent:search", "talent:library", "talent:application",
            "talent:resume", "talent:recommend", "talent:mark"
        ]
    },
    "school": {
        "name": "学校管理",
        "icon": "school",
        "permissions": [
            "school:search", "school:job_fair", "school:info_session",
            "school:department", "school:read", "school:update", "school:verify"
        ]
    },
    "student": {
        "name": "学生管理",
        "icon": "graduation-cap",
        "permissions": [
            "student:read", "student:update", "student:comment", "student:recommend"
        ]
    },
    "statistics": {
        "name": "数据统计",
        "icon": "chart-bar",
        "permissions": [
            "statistics:read:personal", "statistics:read:enterprise",
            "statistics:read:teacher", "statistics:read:admin"
        ]
    }
}

# 角色可访问的模块映射
ROLE_MODULES: Dict[UserType, Set[str]] = {
    UserType.STUDENT: {"settings", "job", "school", "statistics"},
    UserType.ENTERPRISE: {"settings", "job", "talent", "school", "statistics"},
    UserType.TEACHER: {"settings", "student", "school", "statistics"},
    UserType.ADMIN: {"settings", "job", "talent", "school", "student", "statistics"}
}

# 完善的角色权限映射（使用Set提高查找效率）
ROLE_PERMISSIONS = {
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
        "job_fair:read", "job_fair:register",  # 企业不能创建双选会，只能查看和报名
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
ENTERPRISE_SUB_ACCOUNT_RESTRICTIONS = {
    "job:create",  # 不能创建职位
    "job:delete",  # 不能删除职位
    "sub_account:create",  # 不能创建子账号
    "sub_account:delete",  # 不能删除子账号
    "verification:create:enterprise",  # 不能申请企业认证
    "verification:create:personal",  # 不能申请个人认证
    "job_fair:create",  # 不能创建双选会
}

# 教师子账号权限限制
TEACHER_SUB_ACCOUNT_RESTRICTIONS = {
    "job_fair:create",  # 不能创建双选会
    "info_session:create",  # 不能创建宣讲会
    "sub_account:create",  # 不能创建子账号
    "sub_account:delete",  # 不能删除子账号
    "permission:transfer",  # 不能移交权限
    "class:transfer",  # 不能移交班级
    "school:verify",  # 不能申请学校认证
}


async def check_permission(
    user: User,
    permission: str,
    db: Optional[AsyncSession] = None
) -> bool:
    """
    检查用户是否拥有指定权限（统一权限检查函数）
    
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
    role_permissions = ROLE_PERMISSIONS.get(user.user_type, set())
    
    # 检查通配符权限
    if "*" in role_permissions:
        return True
    
    # 检查具体权限
    if permission in role_permissions:
        # 如果是子账号，检查是否有权限限制
        if db:
            if user.user_type == UserType.ENTERPRISE:
                from app.models.profile import EnterpriseProfile
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


async def get_user_modules(user: User, db: Optional[AsyncSession] = None) -> List[str]:
    """
    获取用户可访问的模块列表
    
    Args:
        user: 用户对象
        db: 数据库会话（可选，用于检查子账号权限）
        
    Returns:
        List[str]: 可访问的模块ID列表
    """
    # 管理员可以访问所有模块
    if user.user_type == UserType.ADMIN:
        return list(MODULES.keys())
    
    # 获取角色可访问的模块
    modules = ROLE_MODULES.get(user.user_type, set())
    
    # 如果是子账号，检查是否有模块访问限制
    if db:
        if user.user_type == UserType.ENTERPRISE:
            from app.models.profile import EnterpriseProfile
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise and not enterprise.is_main_account:
                # 企业子账号不能访问子账号管理模块
                modules = modules - {"settings"} if "sub_account:create" not in ROLE_PERMISSIONS.get(user.user_type, set()) else modules
        elif user.user_type == UserType.TEACHER:
            teacher_result = await db.execute(
                select(TeacherProfile).where(TeacherProfile.user_id == user.id)
            )
            teacher = teacher_result.scalar_one_or_none()
            if teacher and not teacher.is_main_account:
                # 教师子账号不能访问子账号管理模块
                modules = modules - {"settings"} if "sub_account:create" not in ROLE_PERMISSIONS.get(user.user_type, set()) else modules
    
    return list(modules)


async def has_module_access(user: User, module_id: str, db: Optional[AsyncSession] = None) -> bool:
    """
    检查用户是否有模块访问权限
    
    Args:
        user: 用户对象
        module_id: 模块ID
        db: 数据库会话（可选）
        
    Returns:
        bool: 是否有权限访问该模块
    """
    modules = await get_user_modules(user, db)
    return module_id in modules


def require_module(module_id: str):
    """
    模块访问权限装饰器
    
    Args:
        module_id: 模块ID
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = None
            db_session = None
            
            for key, value in kwargs.items():
                if isinstance(value, User):
                    current_user = value
                elif isinstance(value, AsyncSession):
                    db_session = value
            
            if not current_user:
                for arg in args:
                    if isinstance(arg, User):
                        current_user = arg
                    elif isinstance(arg, AsyncSession):
                        db_session = arg
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录"
                )
            
            has_access = await has_module_access(current_user, module_id, db_session)
            if not has_access:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"无权访问模块：{MODULES.get(module_id, {}).get('name', module_id)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_permission(*permissions: str):
    """
    权限装饰器，检查用户是否拥有指定权限（增强版，支持子账号权限限制）
    
    Args:
        *permissions: 需要的权限列表
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户和数据库会话
            current_user = None
            db_session = None
            
            for key, value in kwargs.items():
                if isinstance(value, User):
                    current_user = value
                elif isinstance(value, AsyncSession):
                    db_session = value
            
            if not current_user:
                # 尝试从依赖注入获取
                for arg in args:
                    if isinstance(arg, User):
                        current_user = arg
                    elif isinstance(arg, AsyncSession):
                        db_session = arg
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录"
                )
            
            # 检查权限
            for permission in permissions:
                has_permission = await check_permission(current_user, permission, db_session)
                
                # 记录权限检查日志（异步执行，不阻塞）
                try:
                    await log_permission_check(
                        user_id=current_user.id,
                        user_type=current_user.user_type.value,
                        permission=permission,
                        result=has_permission,
                        reason=None if has_permission else "权限不足"
                    )
                except Exception:
                    # 日志记录失败不影响权限检查
                    pass
                
                if not has_permission:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"缺少权限：{permission}"
                    )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_user_type(*user_types: UserType):
    """
    要求用户类型装饰器
    
    Args:
        *user_types: 允许的用户类型列表
        
    Returns:
        依赖函数
    """
    # 延迟导入以避免循环依赖
    from app.api.v1.auth import get_current_user
    
    async def check_user_type(
        current_user: User = Depends(get_current_user)
    ) -> User:
        """
        检查用户类型
        
        Args:
            current_user: 当前登录用户
            
        Returns:
            User: 当前用户
            
        Raises:
            HTTPException: 如果用户类型不符合要求
        """
        if current_user.user_type not in user_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"此操作仅限 {', '.join([ut.value for ut in user_types])} 用户"
            )
        return current_user
    
    return check_user_type


# 便捷的用户类型检查函数（延迟创建以避免循环导入）
def _create_user_type_deps():
    """创建用户类型依赖函数"""
    return {
        "require_student": require_user_type(UserType.STUDENT),
        "require_enterprise": require_user_type(UserType.ENTERPRISE),
        "require_teacher": require_user_type(UserType.TEACHER),
        "require_admin": require_user_type(UserType.ADMIN)
    }

# 延迟创建依赖函数
_user_type_deps = None

def get_require_student():
    """获取学生用户类型依赖"""
    global _user_type_deps
    if _user_type_deps is None:
        _user_type_deps = _create_user_type_deps()
    return _user_type_deps["require_student"]

def get_require_enterprise():
    """获取企业用户类型依赖"""
    global _user_type_deps
    if _user_type_deps is None:
        _user_type_deps = _create_user_type_deps()
    return _user_type_deps["require_enterprise"]

def get_require_teacher():
    """获取教师用户类型依赖"""
    global _user_type_deps
    if _user_type_deps is None:
        _user_type_deps = _create_user_type_deps()
    return _user_type_deps["require_teacher"]

def get_require_admin():
    """获取管理员用户类型依赖"""
    global _user_type_deps
    if _user_type_deps is None:
        _user_type_deps = _create_user_type_deps()
    return _user_type_deps["require_admin"]

# 便捷访问函数（直接调用）
def require_student():
    """获取学生用户类型依赖"""
    return get_require_student()

def require_enterprise():
    """获取企业用户类型依赖"""
    return get_require_enterprise()

def require_teacher():
    """获取教师用户类型依赖"""
    return get_require_teacher()

def require_admin():
    """获取管理员用户类型依赖"""
    return get_require_admin()


async def check_data_permission(
    resource_owner_id: str,
    current_user: User,
    db: AsyncSession,
    allow_admin: bool = True
) -> bool:
    """
    检查数据权限（用户只能操作自己的数据）- 增强版
    
    Args:
        resource_owner_id: 资源所有者ID
        current_user: 当前登录用户
        db: 数据库会话
        allow_admin: 是否允许管理员访问
        
    Returns:
        bool: 是否有权限
    """
    # 管理员可以访问所有数据
    if allow_admin and current_user.user_type == UserType.ADMIN:
        return True
    
    # 检查是否是资源所有者
    if resource_owner_id == current_user.id:
        return True
    
    # 教师可以查看管辖的学生数据
    if current_user.user_type == UserType.TEACHER:
        # 检查是否是管辖的学生
        teacher_result = await db.execute(
            select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
        )
        teacher = teacher_result.scalar_one_or_none()
        
        if teacher:
            # 查询学生是否在教师的管辖范围内
            student_result = await db.execute(
                select(StudentProfile).where(StudentProfile.user_id == resource_owner_id)
            )
            student = student_result.scalar_one_or_none()
            
            if student:
                # 检查院系权限
                if teacher.department_id and student.department_id:
                    if teacher.department_id == student.department_id:
                        return True
                # 检查学校权限
                elif teacher.school_id and student.school_id:
                    if teacher.school_id == student.school_id:
                        return True
    
    return False


async def check_resource_access(
    resource_type: str,
    resource_id: str,
    current_user: User,
    db: AsyncSession,
    action: str = "read"
) -> bool:
    """
    增强的资源权限检查函数（支持多种资源类型）
    
    Args:
        resource_type: 资源类型（job, application, resume, job_fair, info_session等）
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
            # 如果学生信息不存在，企业用户仍然可以查看（可能是数据问题）
            # 但为了安全，非企业用户不允许查看
            if current_user.user_type == UserType.ENTERPRISE:
                return True
            return False
        
        # 学生：只能操作自己的简历
        if current_user.user_type == UserType.STUDENT:
            return student.user_id == current_user.id
        
        # 企业：可以查看所有简历（用于人才搜索和人才库）
        # 如果简历关联了该企业的申请，则允许查看
        # 如果简历在人才库中，也允许查看
        elif current_user.user_type == UserType.ENTERPRISE:
            # 检查是否有该企业的申请记录
            from app.models.job import JobApplication
            application_result = await db.execute(
                select(JobApplication).where(
                    JobApplication.student_id == student.user_id,
                    JobApplication.resume_id == resource_id
                )
            )
            applications = application_result.scalars().all()
            
            if applications:
                from app.models.job import Job
                from app.models.profile import EnterpriseProfile
                enterprise_result = await db.execute(
                    select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
                )
                enterprise = enterprise_result.scalar_one_or_none()
                if enterprise:
                    from app.services.enterprise_service import get_enterprise_ids_for_query
                    enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                    # 检查是否有任何申请关联到该企业的职位
                    for application in applications:
                        job_result = await db.execute(
                            select(Job).where(Job.id == application.job_id)
                        )
                        job = job_result.scalar_one_or_none()
                        if job and job.enterprise_id in enterprise_ids:
                            return True
            
            # 检查是否在人才库中
            from app.models.talent_pool import TalentPool
            talent_pool_result = await db.execute(
                select(TalentPool).where(
                    TalentPool.student_id == student.id,
                    TalentPool.resume_id == resource_id
                )
            )
            talent_pools = talent_pool_result.scalars().all()
            
            if talent_pools:
                from app.models.profile import EnterpriseProfile
                enterprise_result = await db.execute(
                    select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
                )
                enterprise = enterprise_result.scalar_one_or_none()
                if enterprise:
                    from app.services.enterprise_service import get_enterprise_ids_for_query
                    enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                    # 检查是否有任何人才库记录属于该企业
                    for talent_pool in talent_pools:
                        if talent_pool.enterprise_id in enterprise_ids:
                            return True
            
            # 企业用户可以查看所有简历（用于人才搜索功能）
            # 这是业务需求：企业需要能够搜索和查看所有学生的简历
            return True
        
        # 教师：只能查看管辖学生的简历
        elif current_user.user_type == UserType.TEACHER:
            teacher_result = await db.execute(
                select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
            )
            teacher = teacher_result.scalar_one_or_none()
            if teacher:
                if teacher.department_id and student.department_id:
                    return teacher.department_id == student.department_id
                elif teacher.school_id and student.school_id:
                    return teacher.school_id == student.school_id
        
        return False
    
    elif resource_type == "application":
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
    
    elif resource_type == "interview":
        from app.models.interview import Interview
        interview_result = await db.execute(
            select(Interview).where(Interview.id == resource_id)
        )
        interview = interview_result.scalar_one_or_none()
        if not interview:
            return False
        
        # 企业：只能操作自己企业的面试
        if current_user.user_type == UserType.ENTERPRISE:
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                from app.services.enterprise_service import get_enterprise_ids_for_query
                enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                return interview.enterprise_id in enterprise_ids
        
        # 学生：只能操作自己的面试
        elif current_user.user_type == UserType.STUDENT:
            student_result = await db.execute(
                select(StudentProfile).where(StudentProfile.user_id == current_user.id)
            )
            student = student_result.scalar_one_or_none()
            if student:
                return interview.student_id == student.id
        
        return False
    
    elif resource_type == "offer":
        from app.models.interview import Offer
        offer_result = await db.execute(
            select(Offer).where(Offer.id == resource_id)
        )
        offer = offer_result.scalar_one_or_none()
        if not offer:
            return False
        
        # 企业：只能操作自己企业的Offer
        if current_user.user_type == UserType.ENTERPRISE:
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                from app.services.enterprise_service import get_enterprise_ids_for_query
                enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                return offer.enterprise_id in enterprise_ids
        
        # 学生：只能操作自己的Offer
        elif current_user.user_type == UserType.STUDENT:
            student_result = await db.execute(
                select(StudentProfile).where(StudentProfile.user_id == current_user.id)
            )
            student = student_result.scalar_one_or_none()
            if student:
                return offer.student_id == student.id
        
        return False
    
    elif resource_type == "job_fair":
        from app.models.activity import JobFair
        job_fair_result = await db.execute(
            select(JobFair).where(JobFair.id == resource_id)
        )
        job_fair = job_fair_result.scalar_one_or_none()
        if not job_fair:
            return False
        
        # 企业：只能操作自己创建的双选会
        if current_user.user_type == UserType.ENTERPRISE:
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                from app.services.enterprise_service import get_enterprise_ids_for_query
                enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                return job_fair.created_by in enterprise_ids
        
        # 教师：只能操作自己学校的双选会
        elif current_user.user_type == UserType.TEACHER:
            teacher_result = await db.execute(
                select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
            )
            teacher = teacher_result.scalar_one_or_none()
            if teacher and teacher.school_id:
                return job_fair.school_id == teacher.school_id
        
        # 学生：只能查看已发布的双选会
        elif current_user.user_type == UserType.STUDENT:
            return job_fair.status == "PUBLISHED"
        
        # 管理员：可以操作所有双选会
        elif current_user.user_type == UserType.ADMIN:
            return True
        
        return False
    
    elif resource_type == "info_session":
        from app.models.activity import InfoSession
        info_session_result = await db.execute(
            select(InfoSession).where(InfoSession.id == resource_id)
        )
        info_session = info_session_result.scalar_one_or_none()
        if not info_session:
            return False
        
        # 企业：只能操作自己创建的宣讲会
        if current_user.user_type == UserType.ENTERPRISE:
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                from app.services.enterprise_service import get_enterprise_ids_for_query
                enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                return info_session.enterprise_id in enterprise_ids
        
        # 教师：只能操作自己学校的宣讲会
        elif current_user.user_type == UserType.TEACHER:
            teacher_result = await db.execute(
                select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
            )
            teacher = teacher_result.scalar_one_or_none()
            if teacher and teacher.school_id:
                return info_session.school_id == teacher.school_id
        
        # 学生：只能查看已发布的宣讲会
        elif current_user.user_type == UserType.STUDENT:
            return info_session.status == "PUBLISHED"
        
        # 管理员：可以操作所有宣讲会
        elif current_user.user_type == UserType.ADMIN:
            return True
        
        return False
    
    elif resource_type == "talent_pool":
        from app.models.talent_pool import TalentPool
        talent_pool_result = await db.execute(
            select(TalentPool).where(TalentPool.id == resource_id)
        )
        talent_pool = talent_pool_result.scalar_one_or_none()
        if not talent_pool:
            return False
        
        # 企业：只能操作自己的人才库
        if current_user.user_type == UserType.ENTERPRISE:
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == current_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            if enterprise:
                from app.services.enterprise_service import get_enterprise_ids_for_query
                enterprise_ids = await get_enterprise_ids_for_query(db, enterprise)
                return talent_pool.enterprise_id in enterprise_ids
        
        return False
    
    elif resource_type == "schedule":
        from app.models.common import Schedule
        schedule_result = await db.execute(
            select(Schedule).where(Schedule.id == resource_id)
        )
        schedule = schedule_result.scalar_one_or_none()
        if not schedule:
            return False
        
        # 用户只能操作自己的日程
        if schedule.user_id == current_user.id:
            return True
        
        return False
    
    elif resource_type == "favorite":
        from app.models.common import Favorite
        favorite_result = await db.execute(
            select(Favorite).where(Favorite.id == resource_id)
        )
        favorite = favorite_result.scalar_one_or_none()
        if not favorite:
            return False
        
        # 用户只能操作自己的收藏
        if favorite.user_id == current_user.id:
            return True
        
        return False
    
    elif resource_type == "todo":
        from app.models.todo import Todo
        todo_result = await db.execute(
            select(Todo).where(Todo.id == resource_id)
        )
        todo = todo_result.scalar_one_or_none()
        if not todo:
            return False
        
        # 用户只能操作自己的待办事项
        if todo.user_id == current_user.id:
            return True
        
        return False
    
    elif resource_type == "mark":
        from app.models.mark import Mark
        mark_result = await db.execute(
            select(Mark).where(Mark.id == resource_id)
        )
        mark = mark_result.scalar_one_or_none()
        if not mark:
            return False
        
        # 企业用户只能操作自己的标记（通过user_id检查）
        if current_user.user_type == UserType.ENTERPRISE:
            if mark.user_id == current_user.id:
                return True
        
        return False
    
    # 其他资源类型的权限检查...
    
    return False


def require_data_permission_dep(
    resource_owner_id: str,
    allow_admin: bool = True
):
    """
    数据权限检查依赖函数工厂
    
    Args:
        resource_owner_id: 资源所有者ID
        allow_admin: 是否允许管理员访问
        
    Returns:
        依赖函数
    """
    # 延迟导入以避免循环依赖
    from app.api.v1.auth import get_current_user
    
    async def check_data_permission_inner(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        """
        数据权限检查依赖函数
        
        Args:
            current_user: 当前登录用户
            db: 数据库会话
            
        Returns:
            User: 当前用户
            
        Raises:
            HTTPException: 如果无权限
        """
        has_permission = await check_data_permission(
            resource_owner_id,
            current_user,
            db,
            allow_admin
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此资源"
            )
        
        return current_user
    
    return check_data_permission_inner


async def check_teacher_student_access(
    student_user_id: str,
    current_user: User,
    db: AsyncSession
) -> bool:
    """
    检查教师是否可以访问学生数据
    
    Args:
        student_user_id: 学生用户ID
        current_user: 当前登录用户（教师）
        db: 数据库会话
        
    Returns:
        bool: 是否有权限
    """
    if current_user.user_type != UserType.TEACHER:
        return False
    
    # 获取教师信息
    teacher_result = await db.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    )
    teacher = teacher_result.scalar_one_or_none()
    
    if not teacher:
        return False
    
    # 获取学生信息
    student_result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == student_user_id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        return False
    
    # 检查是否在同一部门
    if teacher.department_id and student.department_id:
        return teacher.department_id == student.department_id
    
    # 检查是否在同一学校
    if teacher.school_id and student.school_id:
        return teacher.school_id == student.school_id
    
    return False

