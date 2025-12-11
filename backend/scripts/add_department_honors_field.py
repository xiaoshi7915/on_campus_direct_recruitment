"""
为departments表添加honors字段
"""
import sys
import asyncio

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.core.config import settings

# 创建数据库引擎（使用aiomysql驱动）
database_url = settings.DATABASE_URL.replace("mysql+pymysql://", "mysql+aiomysql://")
engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True
)

# 创建异步会话
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def add_department_honors_field():
    """为departments表添加honors字段"""
    async with AsyncSessionLocal() as db:
        try:
            print("正在检查departments表的honors字段...")
            
            # 检查字段是否存在
            result = await db.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'departments'
                AND COLUMN_NAME = 'honors'
            """))
            count = result.scalar()
            
            if count == 0:
                print("添加honors字段...")
                await db.execute(text("""
                    ALTER TABLE departments
                    ADD COLUMN honors TEXT NULL COMMENT '资质荣誉'
                """))
                await db.commit()
                print("✅ honors字段添加成功")
            else:
                print("✅ honors字段已存在")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 错误：{str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()


async def main():
    """主函数"""
    print("=" * 60)
    print("为departments表添加honors字段")
    print("=" * 60)
    
    await add_department_honors_field()
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())




