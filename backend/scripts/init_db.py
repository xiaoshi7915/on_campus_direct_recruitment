"""
初始化数据库脚本
用于创建所有数据库表
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine, Base
from app.models import *  # 导入所有模型


async def init_db():
    """
    初始化数据库，创建所有表
    使用utf8mb4字符集
    """
    async with engine.begin() as conn:
        # 设置数据库字符集为utf8mb4
        await conn.execute(text("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"))
        await conn.execute(text("SET CHARACTER SET utf8mb4"))
        
        # 删除所有表（谨慎使用，仅用于开发环境）
        # await conn.run_sync(Base.metadata.drop_all)
        
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
    
    print("数据库表创建成功！使用utf8mb4字符集")


if __name__ == "__main__":
    asyncio.run(init_db())

