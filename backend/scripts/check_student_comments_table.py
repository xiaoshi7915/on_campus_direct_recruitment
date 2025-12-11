"""
检查student_comments表是否存在
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


async def check_table():
    """检查student_comments表是否存在"""
    async with engine.connect() as conn:
        result = await conn.execute(text("SHOW TABLES LIKE 'student_comments'"))
        row = result.fetchone()
        if row:
            print("✅ student_comments表已存在")
        else:
            print("❌ student_comments表不存在，需要创建迁移")


if __name__ == "__main__":
    asyncio.run(check_table())




