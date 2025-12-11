"""
查看企业主账号信息
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.profile import EnterpriseProfile
from app.models.user import User


async def check_enterprise_main_account():
    """查看企业主账号信息"""
    async with AsyncSessionLocal() as db:
        try:
            # 查找小米科技相关的企业
            result = await db.execute(
                select(EnterpriseProfile).where(
                    EnterpriseProfile.company_name.like('%小米科技%')
                )
            )
            enterprises = result.scalars().all()
            
            if not enterprises:
                print("✗ 没有找到小米科技相关的企业")
                return
            
            print(f"✓ 找到 {len(enterprises)} 个小米科技相关的企业\n")
            
            for enterprise in enterprises:
                # 获取用户信息
                user_result = await db.execute(
                    select(User).where(User.id == enterprise.user_id)
                )
                user = user_result.scalar_one_or_none()
                
                print(f"企业: {enterprise.company_name}")
                print(f"  企业ID: {enterprise.id}")
                print(f"  用户ID: {enterprise.user_id}")
                print(f"  用户名: {user.username if user else 'N/A'}")
                print(f"  是否主账号: {enterprise.is_main_account}")
                print(f"  主账号ID: {enterprise.main_account_id}")
                
                # 如果是子账号，查找主账号信息
                if not enterprise.is_main_account and enterprise.main_account_id:
                    main_result = await db.execute(
                        select(EnterpriseProfile).where(
                            EnterpriseProfile.id == enterprise.main_account_id
                        )
                    )
                    main_account = main_result.scalar_one_or_none()
                    if main_account:
                        main_user_result = await db.execute(
                            select(User).where(User.id == main_account.user_id)
                        )
                        main_user = main_user_result.scalar_one_or_none()
                        print(f"  主账号信息:")
                        print(f"    公司名: {main_account.company_name}")
                        print(f"    企业ID: {main_account.id}")
                        print(f"    用户名: {main_user.username if main_user else 'N/A'}")
                
                # 如果是主账号，查找子账号
                if enterprise.is_main_account:
                    sub_result = await db.execute(
                        select(EnterpriseProfile).where(
                            EnterpriseProfile.main_account_id == enterprise.id
                        )
                    )
                    sub_accounts = sub_result.scalars().all()
                    print(f"  子账号数量: {len(sub_accounts)}")
                    if sub_accounts:
                        print(f"  子账号列表:")
                        for sub in sub_accounts:
                            sub_user_result = await db.execute(
                                select(User).where(User.id == sub.user_id)
                            )
                            sub_user = sub_user_result.scalar_one_or_none()
                            print(f"    - {sub.company_name} (ID: {sub.id}, 用户名: {sub_user.username if sub_user else 'N/A'})")
                
                print()
            
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_enterprise_main_account())


