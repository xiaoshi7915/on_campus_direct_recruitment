"""
设置数据库字符集为utf8mb4的脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


async def set_charset():
    """
    设置数据库和表的字符集为utf8mb4
    """
    async with engine.begin() as conn:
        # 设置数据库字符集
        await conn.execute(text("ALTER DATABASE college_zhaopin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        print("✅ 数据库字符集已设置为utf8mb4")
        
        # 获取所有表名
        result = await conn.execute(text("""
            SELECT TABLE_NAME 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'college_zhaopin'
        """))
        tables = [row[0] for row in result]
        
        # 为每个表设置字符集
        for table in tables:
            try:
                await conn.execute(text(f"""
                    ALTER TABLE `{table}` 
                    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """))
                print(f"✅ 表 {table} 字符集已设置为utf8mb4")
            except Exception as e:
                print(f"⚠️  表 {table} 设置字符集失败: {e}")


if __name__ == "__main__":
    asyncio.run(set_charset())



