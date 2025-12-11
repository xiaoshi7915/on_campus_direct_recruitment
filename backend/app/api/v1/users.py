"""
用户相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_admin
from app.models.user import User

router = APIRouter()


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户信息
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 用户信息
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "phone": current_user.phone,
        "email": current_user.email,
        "user_type": current_user.user_type,
        "status": current_user.status,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }


@router.get("")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索（用户名、手机号、邮箱）"),
    user_type: Optional[str] = Query(None, description="用户类型过滤"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态过滤"),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户列表（仅管理员）
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词搜索
        user_type: 用户类型过滤
        status_filter: 状态过滤
        current_user: 当前登录用户（必须是管理员）
        db: 数据库会话
        
    Returns:
        dict: 用户列表
    """
    # 构建查询
    query = select(User)
    
    # 关键词搜索
    if keyword:
        conditions = [User.username.contains(keyword)]
        # 处理可能为NULL的字段
        conditions.append(User.phone.contains(keyword))
        conditions.append(User.email.contains(keyword))
        query = query.where(or_(*conditions))
    
    # 用户类型过滤
    if user_type:
        query = query.where(User.user_type == user_type)
    
    # 状态过滤
    if status_filter:
        query = query.where(User.status == status_filter)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(User.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    # 转换为字典（不包含密码哈希）
    users_list = []
    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "user_type": user.user_type,
            "status": user.status,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        })
    
    return {
        "items": users_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


