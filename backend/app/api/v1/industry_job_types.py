"""
行业职位类型维表相关API路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.core.database import get_db
from app.models.industry_job_type import IndustryCategory, SubIndustry, JobType
from pydantic import BaseModel

router = APIRouter()


class IndustryCategoryResponse(BaseModel):
    """行业分类响应"""
    id: str
    name: str
    code: Optional[str]
    sort_order: int
    
    class Config:
        from_attributes = True


class SubIndustryResponse(BaseModel):
    """细分行业响应"""
    id: str
    category_id: str
    name: str
    code: Optional[str]
    sort_order: int
    
    class Config:
        from_attributes = True


class JobTypeResponse(BaseModel):
    """职位类型响应"""
    id: str
    category_id: Optional[str]
    sub_industry_id: Optional[str]
    name: str
    code: Optional[str]
    description: Optional[str]
    sort_order: int
    
    class Config:
        from_attributes = True


@router.get("/industry-categories", response_model=List[IndustryCategoryResponse])
async def get_industry_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有行业分类（一级行业）
    """
    result = await db.execute(
        select(IndustryCategory)
        .order_by(IndustryCategory.sort_order, IndustryCategory.name)
    )
    categories = result.scalars().all()
    return categories


@router.get("/sub-industries", response_model=List[SubIndustryResponse])
async def get_sub_industries(
    category_id: Optional[str] = Query(None, description="行业分类ID，不传则返回所有"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取细分行业（二级行业）
    
    Args:
        category_id: 行业分类ID，如果提供则只返回该分类下的细分行业
    """
    query = select(SubIndustry)
    if category_id:
        query = query.where(SubIndustry.category_id == category_id)
    query = query.order_by(SubIndustry.sort_order, SubIndustry.name)
    
    result = await db.execute(query)
    sub_industries = result.scalars().all()
    return sub_industries


@router.get("/job-types", response_model=List[JobTypeResponse])
async def get_job_types(
    category_id: Optional[str] = Query(None, description="行业分类ID"),
    sub_industry_id: Optional[str] = Query(None, description="细分行业ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取职位类型
    
    Args:
        category_id: 行业分类ID，如果提供则只返回该分类下的职位类型
        sub_industry_id: 细分行业ID，如果提供则只返回该细分行业下的职位类型
    """
    query = select(JobType)
    
    if sub_industry_id:
        query = query.where(JobType.sub_industry_id == sub_industry_id)
    elif category_id:
        query = query.where(JobType.category_id == category_id)
    
    query = query.order_by(JobType.sort_order, JobType.name)
    
    result = await db.execute(query)
    job_types = result.scalars().all()
    return job_types

