"""
收藏相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.common import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteResponse, FavoriteListResponse

router = APIRouter()


@router.get("", response_model=FavoriteListResponse)
async def get_favorites(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    target_type: Optional[str] = Query(None, description="收藏类型过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取收藏列表（只能查看自己的收藏）
    
    Args:
        page: 页码
        page_size: 每页数量
        target_type: 收藏类型过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FavoriteListResponse: 收藏列表
    """
    # 构建查询（只能查看自己的收藏）
    query = select(Favorite).where(Favorite.user_id == current_user.id)
    
    # 类型过滤
    if target_type:
        query = query.where(Favorite.target_type == target_type)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Favorite.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    favorites = result.scalars().all()
    
    return {
        "items": favorites,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def create_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建收藏
    
    Args:
        favorite_data: 收藏数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        FavoriteResponse: 创建的收藏
        
    Raises:
        HTTPException: 如果已收藏
    """
    # 检查是否已收藏
    existing_result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.target_type == favorite_data.target_type,
            Favorite.target_id == favorite_data.target_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="已收藏"
        )
    
    # 创建收藏
    favorite = Favorite(
        id=str(uuid4()),
        user_id=current_user.id,
        target_type=favorite_data.target_type,
        target_id=favorite_data.target_id
    )
    
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    
    return favorite


@router.get("/check/{target_type}/{target_id}", status_code=status.HTTP_200_OK)
async def check_favorite(
    target_type: str,
    target_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    检查是否已收藏（便捷接口）
    
    Args:
        target_type: 收藏类型
        target_id: 目标ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 是否已收藏
    """
    # 检查是否已收藏
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.target_type == target_type,
            Favorite.target_id == target_id
        )
    )
    favorite = result.scalar_one_or_none()
    
    return {
        "is_favorited": favorite is not None,
        "favorite_id": favorite.id if favorite else None
    }


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    favorite_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消收藏（只能删除自己的收藏）
    
    Args:
        favorite_id: 收藏ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果收藏不存在或无权删除
    """
    # 获取收藏
    result = await db.execute(
        select(Favorite).where(
            Favorite.id == favorite_id,
            Favorite.user_id == current_user.id
        )
    )
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏不存在"
        )
    
    await db.delete(favorite)
    await db.commit()


@router.delete("/by-target/{target_type}/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite_by_target(
    target_type: str,
    target_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    根据目标取消收藏（便捷接口）
    
    Args:
        target_type: 收藏类型
        target_id: 目标ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果收藏不存在
    """
    # 获取收藏
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.target_type == target_type,
            Favorite.target_id == target_id
        )
    )
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏不存在"
        )
    
    await db.delete(favorite)
    await db.commit()


