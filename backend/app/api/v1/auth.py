"""
认证相关API路由
包括注册、登录、刷新令牌等功能
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.core.config import settings
from app.schemas.auth import RegisterRequest, LoginResponse, TokenResponse
from app.models.user import User
from app.models.user_type import UserType

router = APIRouter()

# OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    从JWT令牌中解析用户信息并返回用户对象
    
    Args:
        token: JWT访问令牌（可为None）
        db: 数据库会话
        
    Returns:
        User: 当前用户对象
        
    Raises:
        HTTPException: 如果令牌无效或用户不存在
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # 从数据库查询用户
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    获取当前登录用户（可选）
    如果用户未登录，返回None
    
    Args:
        token: JWT访问令牌（可选）
        db: 数据库会话
        
    Returns:
        Optional[User]: 当前用户对象，如果未登录则返回None
    """
    if not token:
        return None
    
    try:
        payload = verify_token(token)
        if payload is None:
            return None
        
        username: str = payload.get("sub")
        if username is None:
            return None
        
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        return user
    except Exception:
        return None


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口
    
    Args:
        request: 注册请求数据
        db: 数据库会话
        
    Returns:
        dict: 注册结果
        
    Raises:
        HTTPException: 如果用户名已存在
    """
    # 检查用户名是否已存在
    result = await db.execute(
        select(User).where(User.username == request.username)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )
    
    # 禁止管理员通过注册接口注册
    if request.user_type == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="管理员账号不能通过注册接口创建，请联系系统管理员"
        )
    
    # 创建新用户（处理空字符串）
    # 教师注册后状态设为ACTIVE（需要完成学校认证后才能成为主账号）
    # 学生和企业用户注册后状态设为ACTIVE
    initial_status = "ACTIVE"
    
    user = User(
        id=str(uuid4()),
        username=request.username,
        password_hash=get_password_hash(request.password),
        phone=request.phone if request.phone and request.phone.strip() else None,
        email=request.email if request.email and request.email.strip() else None,
        user_type=UserType(request.user_type),
        status=initial_status
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return {
        "message": "注册成功",
        "user_id": user.id
    }


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录接口
    支持用户名/手机号/邮箱登录
    
    Args:
        form_data: OAuth2密码请求表单
        db: 数据库会话
        
    Returns:
        LoginResponse: 登录响应，包含访问令牌和刷新令牌
        
    Raises:
        HTTPException: 如果用户名或密码错误
    """
    # 查询用户（支持用户名、手机号、邮箱登录）
    result = await db.execute(
        select(User).where(
            (User.username == form_data.username) |
            (User.phone == form_data.username) |
            (User.email == form_data.username)
        )
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户状态
    if user.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )
    
    # 创建访问令牌和刷新令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "user_type": user.user_type},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": str(user.id)}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str = Field(..., description="刷新令牌")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    刷新访问令牌接口
    
    Args:
        request: 刷新令牌请求（包含refresh_token）
        db: 数据库会话
        
    Returns:
        TokenResponse: 新的访问令牌
        
    Raises:
        HTTPException: 如果刷新令牌无效
    """
    payload = verify_token(request.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌无效"
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌无效"
        )
    
    # 查询用户
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    # 创建新的访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "user_type": user.user_type},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==================== 密码管理 ====================

class ForgotPasswordRequest(BaseModel):
    """忘记密码请求"""
    phone: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    phone: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    verification_code: str = Field(..., description="验证码")
    new_password: str = Field(..., min_length=6, description="新密码")


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    忘记密码 - 发送验证码
    
    Args:
        request: 忘记密码请求（手机号、邮箱或用户名）
        db: 数据库会话
        
    Returns:
        dict: 发送结果
    """
    # 查询用户
    query = select(User)
    conditions = []
    
    if request.phone:
        conditions.append(User.phone == request.phone)
    if request.email:
        conditions.append(User.email == request.email)
    if request.username:
        conditions.append(User.username == request.username)
    
    if not conditions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供手机号、邮箱或用户名"
        )
    
    from sqlalchemy import or_
    query = query.where(or_(*conditions))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 发送验证码（优先使用手机号）
    if user.phone:
        from app.services.sms import send_sms_code
        code = await send_sms_code(user.phone)
        return {
            "success": True,
            "message": "验证码已发送到手机",
            "phone": user.phone[:3] + "****" + user.phone[-4:] if user.phone else None,
            "code": code if settings.DEBUG else None  # 开发环境返回验证码
        }
    elif user.email:
        # TODO: 实现邮箱验证码发送
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="邮箱验证码功能暂未实现，请使用手机号"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未绑定手机号或邮箱，无法发送验证码"
        )


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    重置密码
    
    Args:
        request: 重置密码请求
        db: 数据库会话
        
    Returns:
        dict: 重置结果
    """
    # 查询用户
    query = select(User)
    conditions = []
    
    if request.phone:
        conditions.append(User.phone == request.phone)
    if request.email:
        conditions.append(User.email == request.email)
    if request.username:
        conditions.append(User.username == request.username)
    
    if not conditions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供手机号、邮箱或用户名"
        )
    
    from sqlalchemy import or_
    query = query.where(or_(*conditions))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证验证码（优先使用手机号）
    if user.phone:
        from app.services.sms import verify_sms_code
        if not await verify_sms_code(user.phone, request.verification_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误或已过期"
            )
    elif user.email:
        # TODO: 实现邮箱验证码验证
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="邮箱验证码功能暂未实现"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未绑定手机号或邮箱"
        )
    
    # 更新密码
    user.password_hash = get_password_hash(request.new_password)
    await db.commit()
    
    return {
        "success": True,
        "message": "密码重置成功"
    }


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    修改密码（需要登录）
    
    Args:
        request: 修改密码请求
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 修改结果
    """
    # 验证旧密码
    if not verify_password(request.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    # 检查新密码是否与旧密码相同
    if verify_password(request.new_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码不能与旧密码相同"
        )
    
    # 更新密码
    current_user.password_hash = get_password_hash(request.new_password)
    await db.commit()
    
    return {
        "success": True,
        "message": "密码修改成功"
    }

