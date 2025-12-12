"""
直接执行SQL添加school_id字段到chat_sessions表
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from sqlalchemy import text


async def add_school_id_column():
    """添加school_id字段到chat_sessions表"""
    async with AsyncSessionLocal() as session:
        try:
            # 检查字段是否已存在
            check_sql = """
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'chat_sessions'
            AND COLUMN_NAME = 'school_id'
            """
            result = await session.execute(text(check_sql))
            count = result.scalar()
            
            if count > 0:
                print("字段 school_id 已存在，跳过添加")
                return
            
            # 添加school_id字段
            print("正在添加 school_id 字段...")
            await session.execute(text("""
                ALTER TABLE chat_sessions
                ADD COLUMN school_id VARCHAR(36) NULL COMMENT '学校ID（如果与学校聊天）'
            """))
            
            # 添加外键约束
            print("正在添加外键约束...")
            await session.execute(text("""
                ALTER TABLE chat_sessions
                ADD CONSTRAINT fk_chat_sessions_school_id
                FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE
            """))
            
            # 添加索引
            print("正在添加索引...")
            await session.execute(text("""
                CREATE INDEX ix_chat_sessions_school_id ON chat_sessions(school_id)
            """))
            
            await session.commit()
            print("✅ 成功添加 school_id 字段到 chat_sessions 表")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ 执行失败: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(add_school_id_column())
