"""
日程相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.common import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse, ScheduleListResponse

router = APIRouter()


@router.get("", response_model=ScheduleListResponse)
async def get_schedules(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    schedule_type: Optional[str] = Query(None, description="日程类型过滤"),
    start_date: Optional[str] = Query(None, description="开始日期（YYYY-MM-DD）"),
    end_date: Optional[str] = Query(None, description="结束日期（YYYY-MM-DD）"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取日程列表（只能查看自己的日程）
    
    Args:
        page: 页码
        page_size: 每页数量
        schedule_type: 日程类型过滤
        start_date: 开始日期
        end_date: 结束日期
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ScheduleListResponse: 日程列表
    """
    # 构建查询（只能查看自己的日程）
    query = select(Schedule).where(Schedule.user_id == current_user.id)
    
    # 日程类型过滤
    if schedule_type:
        query = query.where(Schedule.schedule_type == schedule_type)
    
    # 日期范围过滤
    if start_date:
        from datetime import datetime
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.where(Schedule.start_time >= start_datetime)
    
    if end_date:
        from datetime import datetime
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.where(Schedule.start_time <= end_datetime)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Schedule.start_time.asc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    schedules = result.scalars().all()
    
    return {
        "items": schedules,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取日程详情
    
    Args:
        schedule_id: 日程ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ScheduleResponse: 日程详情
        
    Raises:
        HTTPException: 如果日程不存在或无权查看
    """
    result = await db.execute(
        select(Schedule).where(
            Schedule.id == schedule_id,
            Schedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="日程不存在"
        )
    
    return schedule


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建日程
    
    Args:
        schedule_data: 日程数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ScheduleResponse: 创建的日程
    """
    # 创建日程
    schedule = Schedule(
        id=str(uuid4()),
        user_id=current_user.id,
        title=schedule_data.title,
        content=schedule_data.content,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time,
        schedule_type=schedule_data.schedule_type,
        related_id=schedule_data.related_id,
        reminder_time=schedule_data.reminder_time,
        is_completed=False
    )
    
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: str,
    schedule_data: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新日程（只能更新自己的日程）
    
    Args:
        schedule_id: 日程ID
        schedule_data: 更新的日程数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ScheduleResponse: 更新后的日程
        
    Raises:
        HTTPException: 如果日程不存在或无权修改
    """
    # 获取日程
    result = await db.execute(
        select(Schedule).where(
            Schedule.id == schedule_id,
            Schedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="日程不存在"
        )
    
    # 更新日程信息
    update_data = schedule_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(schedule, field, value)
    
    await db.commit()
    await db.refresh(schedule)
    
    return schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除日程（只能删除自己的日程）
    
    Args:
        schedule_id: 日程ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Raises:
        HTTPException: 如果日程不存在或无权删除
    """
    # 获取日程
    result = await db.execute(
        select(Schedule).where(
            Schedule.id == schedule_id,
            Schedule.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="日程不存在"
        )
    
    await db.delete(schedule)
    await db.commit()


@router.post("/{schedule_id}/complete", response_model=ScheduleResponse)
async def complete_schedule(
    schedule_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    标记日程为已完成
    
    Args:
        schedule_id: 日程ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ScheduleResponse: 更新后的日程
    """
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    schedule = result.scalar_one_or_none()
    
    if not schedule or schedule.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="日程不存在或无权操作"
        )
    
    schedule.is_completed = True
    await db.commit()
    await db.refresh(schedule)
    
    return schedule


@router.post("/{schedule_id}/uncomplete", response_model=ScheduleResponse)
async def uncomplete_schedule(
    schedule_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消日程完成标记
    
    Args:
        schedule_id: 日程ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        ScheduleResponse: 更新后的日程
    """
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    schedule = result.scalar_one_or_none()
    
    if not schedule or schedule.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="日程不存在或无权操作"
        )
    
    schedule.is_completed = False
    await db.commit()
    await db.refresh(schedule)
    
    return schedule

