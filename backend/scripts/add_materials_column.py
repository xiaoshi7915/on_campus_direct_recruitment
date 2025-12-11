"""
直接添加materials字段到info_sessions表
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def add_materials_column():
    """添加materials字段到info_sessions表"""
    async with engine.connect() as conn:
        try:
            # 检查字段是否已存在
            result = await conn.execute(text("DESCRIBE info_sessions"))
            rows = result.fetchall()
            columns = [row[0] for row in rows]
            
            if 'materials' in columns:
                print("✓ materials字段已存在")
            else:
                # 添加materials字段
                await conn.execute(text("""
                    ALTER TABLE info_sessions 
                    ADD COLUMN materials TEXT NULL 
                    COMMENT '宣讲会资料URLs（JSON数组，存储多个文件URL）'
                """))
                await conn.commit()
                print("✓ materials字段添加成功")
        except Exception as e:
            print(f"✗ 添加materials字段失败: {e}")
            await conn.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(add_materials_column())

