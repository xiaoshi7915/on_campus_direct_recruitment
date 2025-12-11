"""
测试数据库连接脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


async def test_connection():
    """
    测试数据库连接
    """
    try:
        async with engine.connect() as conn:
            # 执行简单查询
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row:
                print("✅ 数据库连接成功！")
                print(f"查询结果: {row[0]}")
                
            # 查询数据库版本
            result = await conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()
            if version:
                print(f"MySQL版本: {version[0]}")
                
            # 查询当前数据库
            result = await conn.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()
            if db_name:
                print(f"当前数据库: {db_name[0]}")
                
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_connection())

