"""
检查数据库表结构脚本
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def check_table_structure():
    """检查info_sessions表结构"""
    async with engine.connect() as conn:
        # 检查info_sessions表结构
        result = await conn.execute(text("DESCRIBE info_sessions"))
        rows = result.fetchall()
        
        print("=" * 60)
        print("info_sessions表结构:")
        print("=" * 60)
        columns = []
        for row in rows:
            column_name = row[0]
            column_type = row[1]
            columns.append(column_name)
            print(f"{column_name:30} {column_type}")
        
        print("\n" + "=" * 60)
        print("检查materials字段:")
        print("=" * 60)
        if 'materials' in columns:
            print("✓ materials字段存在")
        else:
            print("✗ materials字段不存在，需要添加")
        
        await conn.commit()


if __name__ == "__main__":
    asyncio.run(check_table_structure())

