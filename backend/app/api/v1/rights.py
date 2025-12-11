"""
权益管理相关API路由（管理员端）
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import uuid4

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.permissions import require_admin
from app.models.user import User
from app.models.rights import Rights, RightsPackage, RightsPackageItem, UserRights, RightsPurchase
from pydantic import BaseModel, Field

router = APIRouter()


# ==================== 权益管理 ====================

class RightsResponse(BaseModel):
    """权益响应模式"""
    id: str
    name: str
    code: str
    description: Optional[str]
    type: str  # 注意：这是权益类型，不是Python的type函数
    value: Optional[int]
    is_active: bool
    created_at: str
    updated_at: str
    
    @classmethod
    def from_orm(cls, obj):
        """从ORM对象创建响应对象"""
        return cls(
            id=obj.id,
            name=obj.name,
            code=obj.code,
            description=obj.description,
            type=obj.type,
            value=obj.value,
            is_active=obj.is_active,
            created_at=obj.created_at.isoformat() if obj.created_at else None,
            updated_at=obj.updated_at.isoformat() if obj.updated_at else None
        )
    
    class Config:
        from_attributes = True
        populate_by_name = True


class RightsCreate(BaseModel):
    """创建权益请求模式"""
    name: str = Field(..., min_length=1, max_length=100, description="权益名称")
    code: str = Field(..., min_length=1, max_length=50, description="权益代码")
    description: Optional[str] = Field(None, description="描述")
    type: str = Field(..., description="权益类型")
    value: Optional[int] = Field(None, description="权益值")
    is_active: bool = Field(True, description="是否激活")


class RightsUpdate(BaseModel):
    """更新权益请求模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="权益名称")
    description: Optional[str] = Field(None, description="描述")
    type: Optional[str] = Field(None, description="权益类型")
    value: Optional[int] = Field(None, description="权益值")
    is_active: Optional[bool] = Field(None, description="是否激活")


class RightsListResponse(BaseModel):
    """权益列表响应模式"""
    items: List[RightsResponse]
    total: int
    page: int
    page_size: int


@router.get("", response_model=RightsListResponse)
async def get_rights(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    type_filter: Optional[str] = Query(None, alias="type", description="类型过滤"),
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取权益列表（仅管理员）
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词搜索
        type_filter: 类型过滤
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        RightsListResponse: 权益列表
    """
    query = select(Rights)
    
    # 关键词搜索
    if keyword:
        query = query.where(
            Rights.name.contains(keyword) | Rights.description.contains(keyword)
        )
    
    # 类型过滤
    if type_filter:
        query = query.where(Rights.type == type_filter)
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Rights.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    rights_orm = result.scalars().all()
    
    # 转换为响应对象
    rights_list = [
        RightsResponse(
            id=right.id,
            name=right.name,
            code=right.code,
            description=right.description,
            type=right.type,
            value=right.value,
            is_active=right.is_active,
            created_at=right.created_at.isoformat() if right.created_at else None,
            updated_at=right.updated_at.isoformat() if right.updated_at else None
        )
        for right in rights_orm
    ]
    
    return {
        "items": rights_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("", response_model=RightsResponse, status_code=status.HTTP_201_CREATED)
async def create_right(
    rights_data: RightsCreate,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    创建权益（仅管理员）
    
    Args:
        rights_data: 权益数据
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        RightsResponse: 创建的权益
    """
    # 检查代码是否已存在
    existing = await db.execute(
        select(Rights).where(Rights.code == rights_data.code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="权益代码已存在"
        )
    
    # 创建权益
    right = Rights(
        id=str(uuid4()),
        name=rights_data.name,
        code=rights_data.code,
        description=rights_data.description,
        type=rights_data.type,
        value=rights_data.value,
        is_active=rights_data.is_active
    )
    
    db.add(right)
    await db.commit()
    await db.refresh(right)
    
    return RightsResponse(
        id=right.id,
        name=right.name,
        code=right.code,
        description=right.description,
        type=right.type,
        value=right.value,
        is_active=right.is_active,
        created_at=right.created_at.isoformat() if right.created_at else None,
        updated_at=right.updated_at.isoformat() if right.updated_at else None
    )


@router.put("/{right_id}", response_model=RightsResponse)
async def update_right(
    right_id: str,
    rights_data: RightsUpdate,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    更新权益（仅管理员）
    
    Args:
        right_id: 权益ID
        rights_data: 更新的权益数据
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        RightsResponse: 更新后的权益
    """
    result = await db.execute(select(Rights).where(Rights.id == right_id))
    right = result.scalar_one_or_none()
    
    if not right:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权益不存在"
        )
    
    # 更新权益信息
    update_data = rights_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(right, field, value)
    
    await db.commit()
    await db.refresh(right)
    
    return RightsResponse(
        id=right.id,
        name=right.name,
        code=right.code,
        description=right.description,
        type=right.type,
        value=right.value,
        is_active=right.is_active,
        created_at=right.created_at.isoformat() if right.created_at else None,
        updated_at=right.updated_at.isoformat() if right.updated_at else None
    )


@router.delete("/{right_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_right(
    right_id: str,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    删除权益（仅管理员）
    
    Args:
        right_id: 权益ID
        current_user: 当前登录用户（管理员）
        db: 数据库会话
    """
    result = await db.execute(select(Rights).where(Rights.id == right_id))
    right = result.scalar_one_or_none()
    
    if not right:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权益不存在"
        )
    
    await db.delete(right)
    await db.commit()


# ==================== 权益套餐管理 ====================

class RightsPackageItemResponse(BaseModel):
    """权益套餐项响应模式"""
    id: str
    package_id: str
    rights_id: str
    quantity: int
    created_at: str
    
    class Config:
        from_attributes = True


class RightsPackageResponse(BaseModel):
    """权益套餐响应模式"""
    id: str
    name: str
    description: Optional[str]
    price: float
    duration_days: Optional[int]
    is_active: bool
    created_at: str
    updated_at: str
    items: List[RightsPackageItemResponse] = []
    
    class Config:
        from_attributes = True


class RightsPackageItemCreate(BaseModel):
    """创建权益套餐项请求模式"""
    rights_id: str = Field(..., description="权益ID")
    quantity: int = Field(1, ge=1, description="数量")


class RightsPackageCreate(BaseModel):
    """创建权益套餐请求模式"""
    name: str = Field(..., min_length=1, max_length=100, description="套餐名称")
    description: Optional[str] = Field(None, description="描述")
    price: float = Field(..., ge=0, description="价格")
    duration_days: Optional[int] = Field(None, ge=1, description="时长（天）")
    is_active: bool = Field(True, description="是否激活")
    items: List[RightsPackageItemCreate] = Field(default_factory=list, description="套餐项列表")


class RightsPackageUpdate(BaseModel):
    """更新权益套餐请求模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="套餐名称")
    description: Optional[str] = Field(None, description="描述")
    price: Optional[float] = Field(None, ge=0, description="价格")
    duration_days: Optional[int] = Field(None, ge=1, description="时长（天）")
    is_active: Optional[bool] = Field(None, description="是否激活")


class RightsPackageListResponse(BaseModel):
    """权益套餐列表响应模式"""
    items: List[RightsPackageResponse]
    total: int
    page: int
    page_size: int


@router.get("/packages", response_model=RightsPackageListResponse)
async def get_rights_packages(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    获取权益套餐列表（仅管理员）
    
    Args:
        page: 页码
        page_size: 每页数量
        keyword: 关键词搜索
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        RightsPackageListResponse: 权益套餐列表
    """
    query = select(RightsPackage)
    
    # 关键词搜索
    if keyword:
        query = query.where(
            RightsPackage.name.contains(keyword) | RightsPackage.description.contains(keyword)
        )
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(RightsPackage.created_at.desc()).offset(offset).limit(page_size)
    
    result = await db.execute(query)
    packages = result.scalars().all()
    
    # 获取每个套餐的项
    package_list = []
    for package in packages:
        items_result = await db.execute(
            select(RightsPackageItem).where(RightsPackageItem.package_id == package.id)
        )
        items = items_result.scalars().all()
        
        package_dict = {
            "id": package.id,
            "name": package.name,
            "description": package.description,
            "price": float(package.price) if package.price else 0.0,
            "duration_days": package.duration_days,
            "is_active": package.is_active,
            "created_at": package.created_at.isoformat() if package.created_at else None,
            "updated_at": package.updated_at.isoformat() if package.updated_at else None,
            "items": [
                {
                    "id": item.id,
                    "package_id": item.package_id,
                    "rights_id": item.rights_id,
                    "quantity": item.quantity,
                    "created_at": item.created_at.isoformat() if item.created_at else None
                }
                for item in items
            ]
        }
        package_list.append(package_dict)
    
    return {
        "items": package_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/packages", response_model=RightsPackageResponse, status_code=status.HTTP_201_CREATED)
async def create_rights_package(
    package_data: RightsPackageCreate,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    创建权益套餐（仅管理员）
    
    Args:
        package_data: 套餐数据
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        RightsPackageResponse: 创建的套餐
    """
    # 检查名称是否已存在
    existing = await db.execute(
        select(RightsPackage).where(RightsPackage.name == package_data.name)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="套餐名称已存在"
        )
    
    # 创建套餐
    package = RightsPackage(
        id=str(uuid4()),
        name=package_data.name,
        description=package_data.description,
        price=package_data.price,
        duration_days=package_data.duration_days,
        is_active=package_data.is_active
    )
    
    db.add(package)
    await db.flush()  # 获取package.id
    
    # 创建套餐项
    for item_data in package_data.items:
        # 检查权益是否存在
        right_result = await db.execute(
            select(Rights).where(Rights.id == item_data.rights_id)
        )
        if not right_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"权益不存在: {item_data.rights_id}"
            )
        
        item = RightsPackageItem(
            id=str(uuid4()),
            package_id=package.id,
            rights_id=item_data.rights_id,
            quantity=item_data.quantity
        )
        db.add(item)
    
    await db.commit()
    await db.refresh(package)
    
    # 获取套餐项
    items_result = await db.execute(
        select(RightsPackageItem).where(RightsPackageItem.package_id == package.id)
    )
    items = items_result.scalars().all()
    
    return {
        "id": package.id,
        "name": package.name,
        "description": package.description,
        "price": float(package.price) if package.price else 0.0,
        "duration_days": package.duration_days,
        "is_active": package.is_active,
        "created_at": package.created_at.isoformat() if package.created_at else None,
        "updated_at": package.updated_at.isoformat() if package.updated_at else None,
        "items": [
            {
                "id": item.id,
                "package_id": item.package_id,
                "rights_id": item.rights_id,
                "quantity": item.quantity,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            for item in items
        ]
    }


@router.put("/packages/{package_id}", response_model=RightsPackageResponse)
async def update_rights_package(
    package_id: str,
    package_data: RightsPackageUpdate,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    更新权益套餐（仅管理员）
    
    Args:
        package_id: 套餐ID
        package_data: 更新的套餐数据
        current_user: 当前登录用户（管理员）
        db: 数据库会话
        
    Returns:
        RightsPackageResponse: 更新后的套餐
    """
    result = await db.execute(select(RightsPackage).where(RightsPackage.id == package_id))
    package = result.scalar_one_or_none()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="套餐不存在"
        )
    
    # 更新套餐信息
    update_data = package_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(package, field, value)
    
    await db.commit()
    await db.refresh(package)
    
    # 获取套餐项
    items_result = await db.execute(
        select(RightsPackageItem).where(RightsPackageItem.package_id == package.id)
    )
    items = items_result.scalars().all()
    
    return {
        "id": package.id,
        "name": package.name,
        "description": package.description,
        "price": float(package.price) if package.price else 0.0,
        "duration_days": package.duration_days,
        "is_active": package.is_active,
        "created_at": package.created_at.isoformat() if package.created_at else None,
        "updated_at": package.updated_at.isoformat() if package.updated_at else None,
        "items": [
            {
                "id": item.id,
                "package_id": item.package_id,
                "rights_id": item.rights_id,
                "quantity": item.quantity,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            for item in items
        ]
    }


@router.delete("/packages/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rights_package(
    package_id: str,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db)
):
    """
    删除权益套餐（仅管理员）
    
    Args:
        package_id: 套餐ID
        current_user: 当前登录用户（管理员）
        db: 数据库会话
    """
    result = await db.execute(select(RightsPackage).where(RightsPackage.id == package_id))
    package = result.scalar_one_or_none()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="套餐不存在"
        )
    
    await db.delete(package)
    await db.commit()

