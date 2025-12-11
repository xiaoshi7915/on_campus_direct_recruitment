"""
为teacher_profiles表添加新字段的迁移脚本
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


async def add_teacher_fields():
    """为teacher_profiles表添加新字段"""
    async with AsyncSessionLocal() as db:
        try:
            print("正在检查并添加teacher_profiles表的新字段...")
            
            # 检查字段是否存在，如果不存在则添加
            check_and_add_field = """
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'teacher_profiles'
            AND COLUMN_NAME = ?
            """
            
            # 检查position字段
            result = await db.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'teacher_profiles'
                AND COLUMN_NAME = 'position'
            """))
            count = result.scalar()
            
            if count == 0:
                print("添加position字段...")
                await db.execute(text("""
                    ALTER TABLE teacher_profiles
                    ADD COLUMN position VARCHAR(50) NULL COMMENT '职务名称'
                """))
                print("✅ position字段添加成功")
            else:
                print("✅ position字段已存在")
            
            # 检查teaching_major字段
            result = await db.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'teacher_profiles'
                AND COLUMN_NAME = 'teaching_major'
            """))
            count = result.scalar()
            
            if count == 0:
                print("添加teaching_major字段...")
                await db.execute(text("""
                    ALTER TABLE teacher_profiles
                    ADD COLUMN teaching_major VARCHAR(100) NULL COMMENT '授课专业'
                """))
                print("✅ teaching_major字段添加成功")
            else:
                print("✅ teaching_major字段已存在")
            
            # 检查teaching_grade字段
            result = await db.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'teacher_profiles'
                AND COLUMN_NAME = 'teaching_grade'
            """))
            count = result.scalar()
            
            if count == 0:
                print("添加teaching_grade字段...")
                await db.execute(text("""
                    ALTER TABLE teacher_profiles
                    ADD COLUMN teaching_grade VARCHAR(50) NULL COMMENT '授课年级'
                """))
                print("✅ teaching_grade字段添加成功")
            else:
                print("✅ teaching_grade字段已存在")
            
            await db.commit()
            print("\n✅ 所有字段检查完成！")
            
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
    print("为teacher_profiles表添加新字段")
    print("=" * 60)
    
    await add_teacher_fields()
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

