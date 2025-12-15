"""
待办事项相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse

router = APIRouter()


@router.get("", response_model=TodoListResponse)
async def get_todos(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    is_completed: Optional[bool] = Query(None, description="是否完成过滤"),
    priority: Optional[str] = Query(None, description="优先级过滤"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取待办事项列表
    
    Args:
        page: 页码
        page_size: 每页数量
        is_completed: 是否完成过滤
        priority: 优先级过滤
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        待办事项列表
    """
    query = select(Todo).where(Todo.user_id == current_user.id)
    
    # 是否完成过滤
    if is_completed is not None:
        query = query.where(Todo.is_completed == is_completed)
    
    # 优先级过滤
    if priority:
        query = query.where(Todo.priority == priority)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Todo.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    todos = result.scalars().all()
    
    return {
        "items": todos,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建待办事项
    
    Args:
        title: 标题
        content: 内容
        priority: 优先级
        due_date: 截止日期
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        创建的待办事项
    """
    # 使用新的权限检查机制
    from app.core.permissions import check_permission
    has_permission = await check_permission(current_user, "todo:write", db)
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权创建待办事项"
        )
    todo = Todo(
        id=str(uuid4()),
        user_id=current_user.id,
        title=todo_data.title,
        content=todo_data.content,
        priority=todo_data.priority,
        due_date=todo_data.due_date
    )
    
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新待办事项
    
    Args:
        todo_id: 待办ID
        title: 标题
        content: 内容
        priority: 优先级
        due_date: 截止日期
        is_completed: 是否完成
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        更新后的待办事项
    """
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="待办事项不存在"
        )
    
    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == 'is_completed' and value and not todo.completed_at:
            todo.completed_at = datetime.now()
        elif field == 'is_completed' and not value:
            todo.completed_at = None
        setattr(todo, field, value)
    
    await db.commit()
    await db.refresh(todo)
    
    return todo


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除待办事项
    
    Args:
        todo_id: 待办ID
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        成功消息
    """
    # 使用资源权限检查
    from app.core.permissions import check_resource_access
    
    has_access = await check_resource_access("todo", todo_id, current_user, db, "delete")
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此待办事项"
        )
    
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="待办事项不存在"
        )
    
    await db.delete(todo)
    await db.commit()
    
    return {"message": "删除成功"}
