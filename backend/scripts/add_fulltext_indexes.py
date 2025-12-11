"""
直接添加全文搜索索引脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from sqlalchemy import text
from app.core.logging import get_logger

logger = get_logger(__name__)


async def add_fulltext_indexes():
    """添加全文搜索索引"""
    print("=" * 60)
    print("开始添加全文搜索索引...")
    print("=" * 60)
    
    async with engine.begin() as conn:
        try:
            # 检查jobs表全文索引是否存在
            result = await conn.execute(text("""
                SHOW INDEX FROM jobs WHERE Key_name = 'idx_jobs_fulltext'
            """))
            jobs_index = result.fetchone()
            
            if not jobs_index:
                # 为jobs表创建全文索引
                print("正在为jobs表创建全文索引...")
                await conn.execute(text("""
                    CREATE FULLTEXT INDEX idx_jobs_fulltext 
                    ON jobs(title, description, requirements)
                """))
                print("[OK] jobs表全文索引创建成功")
            else:
                print("[SKIP] jobs表全文索引已存在，跳过")
            
            # 检查resumes表全文索引是否存在
            result = await conn.execute(text("""
                SHOW INDEX FROM resumes WHERE Key_name = 'idx_resumes_fulltext'
            """))
            resumes_index = result.fetchone()
            
            if not resumes_index:
                # 为resumes表创建全文索引
                print("正在为resumes表创建全文索引...")
                await conn.execute(text("""
                    CREATE FULLTEXT INDEX idx_resumes_fulltext 
                    ON resumes(content)
                """))
                print("[OK] resumes表全文索引创建成功")
            else:
                print("[SKIP] resumes表全文索引已存在，跳过")
            
            await conn.commit()
            print("=" * 60)
            print("全文搜索索引添加完成！")
            print("=" * 60)
            
        except Exception as e:
            await conn.rollback()
            print(f"[ERROR] 创建全文索引时出错: {str(e)}")
            logger.error(f"创建全文索引失败: {str(e)}", exc_info=True)
            raise


async def check_fulltext_indexes():
    """检查全文索引是否存在"""
    print("=" * 60)
    print("检查全文搜索索引...")
    print("=" * 60)
    
    async with engine.begin() as conn:
        try:
            # 检查jobs表的全文索引
            result = await conn.execute(text("""
                SHOW INDEX FROM jobs WHERE Key_name = 'idx_jobs_fulltext'
            """))
            jobs_index = result.fetchone()
            if jobs_index:
                print("[OK] jobs表全文索引已存在")
            else:
                print("[MISSING] jobs表全文索引不存在")
            
            # 检查resumes表的全文索引
            result = await conn.execute(text("""
                SHOW INDEX FROM resumes WHERE Key_name = 'idx_resumes_fulltext'
            """))
            resumes_index = result.fetchone()
            if resumes_index:
                print("[OK] resumes表全文索引已存在")
            else:
                print("[MISSING] resumes表全文索引不存在")
            
            print("=" * 60)
            
        except Exception as e:
            print(f"[ERROR] 检查索引时出错: {str(e)}")
            logger.error(f"检查索引失败: {str(e)}", exc_info=True)


async def main():
    """主函数"""
    # 先检查索引
    await check_fulltext_indexes()
    
    # 添加索引
    await add_fulltext_indexes()
    
    # 再次检查确认
    await check_fulltext_indexes()


if __name__ == "__main__":
    asyncio.run(main())

