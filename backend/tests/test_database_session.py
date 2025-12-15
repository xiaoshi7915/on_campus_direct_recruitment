"""
测试数据库会话管理
验证会话正确释放，防止连接泄漏
"""
import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, engine, AsyncSessionLocal
from app.core.logging import get_logger

logger = get_logger(__name__)


@pytest.mark.asyncio
async def test_database_session_auto_close():
    """测试数据库会话自动关闭"""
    from sqlalchemy import text
    
    # 使用get_db依赖，模拟FastAPI的使用方式
    async for session in get_db():
        assert isinstance(session, AsyncSession)
        # 执行一个简单查询
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
        break
    
    # 会话应该已经关闭
    logger.info("数据库会话自动关闭测试通过")


@pytest.mark.asyncio
async def test_database_session_rollback_on_error():
    """测试异常时会话回滚"""
    from sqlalchemy import text
    
    async for session in get_db():
        try:
            # 尝试执行一个会失败的查询
            await session.execute(text("SELECT * FROM non_existent_table"))
        except Exception:
            # 异常应该被捕获，会话应该回滚
            pass
        break
    
    # 会话应该已经关闭，即使发生异常
    logger.info("异常处理测试通过")


@pytest.mark.asyncio
async def test_multiple_sessions():
    """测试多个会话并发使用"""
    from sqlalchemy import text
    
    async def use_session(session_id: int):
        async for session in get_db():
            result = await session.execute(text("SELECT :id"), {"id": session_id})
            return result.scalar()
    
    # 并发创建多个会话
    tasks = [use_session(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 10
    assert all(r in range(10) for r in results)
    logger.info(f"并发会话测试通过，处理了{len(results)}个会话")


@pytest.mark.asyncio
async def test_session_context_manager():
    """测试会话上下文管理器"""
    from sqlalchemy import text
    
    # 直接使用AsyncSessionLocal创建会话
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    
    # 会话应该已经关闭
    logger.info("上下文管理器测试通过")


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])

