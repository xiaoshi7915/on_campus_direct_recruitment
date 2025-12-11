"""
权限管理模块
实现基于角色的权限控制（RBAC）和数据权限隔离
"""
from fastapi import Depends, HTTPException, status
from typing import List, Optional, Callable
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.user_type import UserType
from app.models.profile import TeacherProfile, StudentProfile
from app.core.database import get_db


# 角色权限映射
ROLE_PERMISSIONS = {
    UserType.STUDENT: [
        "resume:read", "resume:write", "resume:delete",
        "job:read", "job:apply",
        "application:read", "application:write",
        "schedule:read", "schedule:write", "schedule:delete",
        "favorite:read", "favorite:write", "favorite:delete",
        "chat:read", "chat:write",
        "info_session:read", "info_session:register",
        "job_fair:read", "job_fair:register",
        "interview:read", "interview:update",
        "profile:read", "profile:write"
    ],
    UserType.ENTERPRISE: [
        "job:read", "job:write", "job:delete",
        "resume:read",
        "application:read", "application:update",
        "interview:read", "interview:write", "interview:update",
        "info_session:read", "info_session:write", "info_session:delete",
        "job_fair:read", "job_fair:write", "job_fair:register",
        "chat:read", "chat:write",
        "schedule:read", "schedule:write",
        "favorite:read", "favorite:write",
        "profile:read", "profile:write",
        "upload:write"
    ],
    UserType.TEACHER: [
        "student:read", "student:update",
        "job_fair:read", "job_fair:write", "job_fair:delete",
        "info_session:read", "info_session:write",
        "schedule:read", "schedule:write",
        "profile:read", "profile:write",
        "statistics:read"
    ],
    UserType.ADMIN: [
        "*"  # 管理员拥有所有权限
    ]
}


def require_permission(*permissions: str):
    """
    权限装饰器，检查用户是否拥有指定权限
    
    Args:
        *permissions: 需要的权限列表
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户
            current_user = None
            for key, value in kwargs.items():
                if isinstance(value, User):
                    current_user = value
                    break
            
            if not current_user:
                # 尝试从依赖注入获取
                for arg in args:
                    if isinstance(arg, User):
                        current_user = arg
                        break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录"
                )
            
            # 检查权限
            user_permissions = ROLE_PERMISSIONS.get(current_user.user_type, [])
            
            # 管理员拥有所有权限
            if current_user.user_type == UserType.ADMIN or "*" in user_permissions:
                return await func(*args, **kwargs)
            
            # 检查是否拥有所需权限
            for permission in permissions:
                if permission not in user_permissions:
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
    检查数据权限（用户只能操作自己的数据）
    
    Args:
        resource_owner_id: 资源所有者ID
        current_user: 当前登录用户
        db: 数据库会话
        allow_admin: 是否允许管理员访问
        
    Returns:
        bool: 是否有权限
        
    Raises:
        HTTPException: 如果无权限
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
                select(StudentProfile).where(
                    StudentProfile.user_id == resource_owner_id,
                    StudentProfile.department_id == teacher.department_id
                )
            )
            student = student_result.scalar_one_or_none()
            
            if student:
                return True
    
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

