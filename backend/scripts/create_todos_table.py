"""
创建todos表的脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.todo import Todo  # 导入Todo模型


async def create_todos_table():
    """
    创建todos表（使用SQLAlchemy）
    """
    async with engine.begin() as conn:
        # 使用SQLAlchemy创建表
        await conn.run_sync(Base.metadata.create_all, tables=[Todo.__table__])
    
    print("todos表创建成功！")


if __name__ == "__main__":
    asyncio.run(create_todos_table())
