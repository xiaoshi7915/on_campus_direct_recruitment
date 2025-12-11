"""
修复企业主账号标记
确保至少有一个企业是主账号
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.profile import EnterpriseProfile


async def fix_enterprise_main_account():
    """修复企业主账号标记"""
    async with AsyncSessionLocal() as db:
        try:
            # 获取所有企业
            result = await db.execute(select(EnterpriseProfile))
            enterprises = result.scalars().all()
            
            if not enterprises:
                print("✗ 没有找到企业")
                return
            
            print(f"✓ 找到 {len(enterprises)} 个企业")
            
            # 检查是否有主账号
            main_accounts = [e for e in enterprises if e.is_main_account]
            
            if not main_accounts:
                print("⚠️  没有主账号，将第一个企业设置为主账号")
                if enterprises:
                    enterprises[0].is_main_account = True
                    enterprises[0].main_account_id = None
                    await db.commit()
                    print(f"✓ 已将企业 '{enterprises[0].company_name}' 设置为主账号")
            else:
                print(f"✓ 已有 {len(main_accounts)} 个主账号")
                for main in main_accounts:
                    print(f"  - {main.company_name} (ID: {main.id})")
            
            # 检查子账号的主账号ID是否正确
            sub_accounts = [e for e in enterprises if not e.is_main_account and e.main_account_id]
            print(f"\n✓ 找到 {len(sub_accounts)} 个子账号")
            
            # 验证子账号的主账号ID是否有效
            main_account_ids = {e.id for e in main_accounts}
            invalid_sub_accounts = []
            for sub in sub_accounts:
                if sub.main_account_id not in main_account_ids:
                    invalid_sub_accounts.append(sub)
            
            if invalid_sub_accounts:
                print(f"⚠️  找到 {len(invalid_sub_accounts)} 个子账号的主账号ID无效，将修复")
                for sub in invalid_sub_accounts:
                    # 设置为第一个主账号的子账号
                    if main_accounts:
                        sub.main_account_id = main_accounts[0].id
                        print(f"  - 修复子账号 '{sub.company_name}' 的主账号ID")
                await db.commit()
            
            await db.commit()
            print("\n✓ 企业主账号检查完成")
            
        except Exception as e:
            await db.rollback()
            print(f"✗ 修复失败: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(fix_enterprise_main_account())

