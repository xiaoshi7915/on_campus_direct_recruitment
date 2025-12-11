"""
添加 resumes 表的 file_url 列
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


async def add_file_url_column():
    """添加 file_url 列到 resumes 表"""
    async with engine.begin() as conn:
        try:
            # 检查列是否已存在
            check_sql = text("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'resumes'
                AND COLUMN_NAME = 'file_url'
            """)
            result = await conn.execute(check_sql)
            count = result.scalar()
            
            if count > 0:
                print("✅ file_url 列已存在，无需添加")
                return
            
            # 添加 file_url 列
            alter_sql = text("""
                ALTER TABLE resumes
                ADD COLUMN file_url VARCHAR(500) NULL COMMENT '电子版简历文件URL（PDF、Word等）'
                AFTER content
            """)
            
            await conn.execute(alter_sql)
            print("✅ 成功添加 file_url 列到 resumes 表")
            
        except Exception as e:
            print(f"❌ 添加 file_url 列失败: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(add_file_url_column())

