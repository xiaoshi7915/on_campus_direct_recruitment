"""
简单检查数据库表是否存在（使用SQL）
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def check_tables():
    """检查关键表是否存在"""
    async with engine.connect() as conn:
        # 关键表列表
        key_tables = [
            'users', 'enterprise_profiles', 'student_profiles', 'teacher_profiles',
            'jobs', 'resumes', 'job_applications',
            'info_sessions', 'job_fairs', 'job_fair_registrations',
            'info_session_registrations',
            'interviews', 'offers',
            'chat_sessions', 'messages',
            'favorites', 'schedules', 'feedback',
            'todos', 'marks',
            'rights', 'rights_packages', 'rights_package_items', 
            'user_rights', 'rights_purchases'
        ]
        
        print("=" * 80)
        print("数据库表存在性检查")
        print("=" * 80)
        
        missing_tables = []
        existing_tables = []
        
        for table_name in key_tables:
            try:
                result = await conn.execute(text(f"SHOW TABLES LIKE '{table_name}'"))
                row = result.fetchone()
                if row:
                    existing_tables.append(table_name)
                    print(f"✓ {table_name}")
                else:
                    missing_tables.append(table_name)
                    print(f"✗ {table_name} - 缺失")
            except Exception as e:
                print(f"✗ {table_name} - 检查失败: {e}")
                missing_tables.append(table_name)
        
        print("\n" + "=" * 80)
        print(f"总结: {len(existing_tables)} 个表存在, {len(missing_tables)} 个表缺失")
        print("=" * 80)
        
        if missing_tables:
            print("\n缺失的表:")
            for table in missing_tables:
                print(f"  - {table}")
        
        await conn.commit()


if __name__ == "__main__":
    asyncio.run(check_tables())

