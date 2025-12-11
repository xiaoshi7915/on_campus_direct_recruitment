"""
企业服务层 - 处理主账号、子账号逻辑
"""
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.profile import EnterpriseProfile


async def get_effective_enterprise_id(
    db: AsyncSession,
    enterprise: EnterpriseProfile
) -> str:
    """
    获取有效的企业ID（如果是子账号，返回主账号ID；如果是主账号，返回自己的ID）
    
    Args:
        db: 数据库会话
        enterprise: 企业档案
        
    Returns:
        str: 有效的企业ID（用于数据查询）
    """
    if enterprise.is_main_account:
        return enterprise.id
    elif enterprise.main_account_id:
        return enterprise.main_account_id
    else:
        # 如果既不是主账号，也没有主账号ID，返回自己的ID
        return enterprise.id


async def get_enterprise_ids_for_query(
    db: AsyncSession,
    enterprise: EnterpriseProfile
) -> list[str]:
    """
    获取用于查询的企业ID列表（包括主账号和所有子账号）
    用于主账号查看所有数据，子账号只能查看主账号的数据
    
    Args:
        db: 数据库会话
        enterprise: 企业档案
        
    Returns:
        list[str]: 企业ID列表
    """
    if enterprise.is_main_account:
        # 主账号：返回主账号ID + 所有子账号ID
        enterprise_ids = [enterprise.id]
        # 获取所有子账号
        sub_accounts_result = await db.execute(
            select(EnterpriseProfile).where(
                EnterpriseProfile.main_account_id == enterprise.id
            )
        )
        sub_accounts = sub_accounts_result.scalars().all()
        enterprise_ids.extend([sub.id for sub in sub_accounts])
        return enterprise_ids
    elif enterprise.main_account_id:
        # 子账号：只返回主账号ID（子账号只能查看主账号的数据）
        return [enterprise.main_account_id]
    else:
        # 如果既不是主账号，也没有主账号ID，返回自己的ID
        return [enterprise.id]


async def can_manage_enterprise_data(
    enterprise: EnterpriseProfile,
    target_enterprise_id: str
) -> bool:
    """
    检查是否可以管理指定企业的数据
    
    Args:
        enterprise: 当前企业档案
        target_enterprise_id: 目标企业ID
        
    Returns:
        bool: 是否可以管理
    """
    # 如果是主账号，可以管理自己的数据和所有子账号的数据
    if enterprise.is_main_account:
        if enterprise.id == target_enterprise_id:
            return True
        # 检查是否是自己的子账号
        if enterprise.main_account_id == target_enterprise_id:
            return False  # 主账号不能管理子账号的数据（子账号独立管理）
        # 这里可以扩展：检查target_enterprise_id是否是自己的子账号
        return False
    else:
        # 子账号只能管理主账号的数据（查看权限）
        if enterprise.main_account_id == target_enterprise_id:
            return True
        return False


