"""
企业相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.api.v1.auth import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.profile import EnterpriseProfile

router = APIRouter()


class EnterpriseListItem(BaseModel):
    """企业列表项（简化版，用于下拉框）"""
    id: str
    company_name: str
    
    class Config:
        from_attributes = True


class EnterpriseListResponse(BaseModel):
    """企业列表响应"""
    items: list[EnterpriseListItem]
    total: int


@router.get("/list", response_model=EnterpriseListResponse)
async def get_enterprise_list(
    keyword: Optional[str] = Query(None, description="关键词搜索（企业名称）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=200, description="每页数量"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    获取企业列表（用于下拉框选择）
    
    Args:
        keyword: 关键词搜索
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户（可选）
        db: 数据库会话
        
    Returns:
        EnterpriseListResponse: 企业列表
    """
    # 构建查询
    query = select(EnterpriseProfile)
    
    # 关键词搜索
    if keyword:
        query = query.where(
            EnterpriseProfile.company_name.contains(keyword)
        )
    
    # 只返回已认证的企业（可选，根据需求调整）
    # query = query.where(EnterpriseProfile.is_verified == True)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(EnterpriseProfile.company_name.asc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    enterprises = result.scalars().all()
    
    # 转换为响应模型
    items = [
        EnterpriseListItem(id=ent.id, company_name=ent.company_name)
        for ent in enterprises
    ]
    
    return {
        "items": items,
        "total": total
    }




