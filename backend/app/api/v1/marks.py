"""
标记相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.mark import Mark
from app.schemas.mark import MarkCreate, MarkUpdate, MarkResponse, MarkListResponse

router = APIRouter()


@router.get("", response_model=MarkListResponse)
async def get_marks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    target_type: Optional[str] = Query(None, description="标记类型过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取标记列表（只能查看自己的标记）
    
    Args:
        page: 页码
        page_size: 每页数量
        target_type: 标记类型过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MarkListResponse: 标记列表
    """
    # 构建查询（只能查看自己的标记）
    query = select(Mark).where(Mark.user_id == current_user.id)
    
    # 标记类型过滤
    if target_type:
        query = query.where(Mark.target_type == target_type)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Mark.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    marks = result.scalars().all()
    
    return {
        "items": [MarkResponse.model_validate(mark) for mark in marks],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{target_type}/{target_id}", response_model=MarkResponse)
async def get_mark(
    target_type: str,
    target_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取特定目标的标记
    
    Args:
        target_type: 标记类型
        target_id: 目标ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MarkResponse: 标记信息
    """
    result = await db.execute(
        select(Mark).where(
            Mark.user_id == current_user.id,
            Mark.target_type == target_type,
            Mark.target_id == target_id
        )
    )
    mark = result.scalar_one_or_none()
    
    if not mark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标记不存在"
        )
    
    return MarkResponse.model_validate(mark)


@router.post("", response_model=MarkResponse, status_code=status.HTTP_201_CREATED)
async def create_mark(
    mark_data: MarkCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建标记
    
    Args:
        mark_data: 标记数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MarkResponse: 创建的标记
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "talent:mark", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有企业用户才能创建标记"
        )
    # 检查是否已存在
    existing_result = await db.execute(
        select(Mark).where(
            Mark.user_id == current_user.id,
            Mark.target_type == mark_data.target_type,
            Mark.target_id == mark_data.target_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        # 如果已存在，更新它
        if mark_data.note is not None:
            existing.note = mark_data.note
        if mark_data.color is not None:
            existing.color = mark_data.color
        await db.commit()
        await db.refresh(existing)
        return MarkResponse.model_validate(existing)
    
    # 创建新标记
    mark = Mark(
        id=str(uuid4()),
        user_id=current_user.id,
        target_type=mark_data.target_type,
        target_id=mark_data.target_id,
        note=mark_data.note,
        color=mark_data.color or "blue"
    )
    db.add(mark)
    await db.commit()
    await db.refresh(mark)
    
    return MarkResponse.model_validate(mark)


@router.put("/{mark_id}", response_model=MarkResponse)
async def update_mark(
    mark_id: str,
    mark_data: MarkUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新标记
    
    Args:
        mark_id: 标记ID
        mark_data: 更新数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MarkResponse: 更新后的标记
    """
    # 使用资源权限检查
    from app.core.permissions import check_resource_access
    
    has_access = await check_resource_access("mark", mark_id, current_user, db, "update")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此标记"
        )
    
    result = await db.execute(select(Mark).where(Mark.id == mark_id))
    mark = result.scalar_one_or_none()
    
    if not mark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标记不存在"
        )
    
    # 更新字段
    if mark_data.note is not None:
        mark.note = mark_data.note
    if mark_data.color is not None:
        mark.color = mark_data.color
    
    await db.commit()
    await db.refresh(mark)
    
    return MarkResponse.model_validate(mark)


@router.delete("/{mark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mark(
    mark_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除标记
    
    Args:
        mark_id: 标记ID
        current_user: 当前登录用户
        db: 数据库会话
    """
    # 使用资源权限检查
    from app.core.permissions import check_resource_access
    
    has_access = await check_resource_access("mark", mark_id, current_user, db, "delete")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此标记"
        )
    
    result = await db.execute(select(Mark).where(Mark.id == mark_id))
    mark = result.scalar_one_or_none()
    
    if not mark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标记不存在"
        )
    
    await db.delete(mark)
    await db.commit()



