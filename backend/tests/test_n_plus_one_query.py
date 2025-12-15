"""
测试N+1查询优化
验证使用selectinload后查询次数减少
"""
import pytest
import asyncio
from sqlalchemy import select, event
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.chat import ChatSession
from app.models.user import User
from app.models.school import School
from app.core.logging import get_logger

logger = get_logger(__name__)

# 记录查询次数
query_count = 0


@event.listens_for(AsyncSession, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """监听SQL执行，统计查询次数"""
    global query_count
    if statement.strip().upper().startswith("SELECT"):
        query_count += 1


@pytest.mark.asyncio
async def test_chat_sessions_without_optimization():
    """测试未优化的查询（N+1问题）"""
    global query_count
    query_count = 0
    
    async for db in get_db():
        # 模拟未优化的查询（不使用selectinload）
        result = await db.execute(
            select(ChatSession).limit(10)
        )
        sessions = result.scalars().all()
        
        # 手动查询关联数据（模拟N+1问题）
        for session in sessions:
            if session.user1_id:
                await db.execute(select(User).where(User.id == session.user1_id))
            if session.user2_id:
                await db.execute(select(User).where(User.id == session.user2_id))
            if session.school_id:
                await db.execute(select(School).where(School.id == session.school_id))
        
        queries_without_optimization = query_count
        logger.info(f"未优化查询次数: {queries_without_optimization}")
        break
    
    return queries_without_optimization


@pytest.mark.asyncio
async def test_chat_sessions_with_optimization():
    """测试优化后的查询（使用selectinload）"""
    from sqlalchemy.orm import selectinload
    
    global query_count
    query_count = 0
    
    async for db in get_db():
        # 使用selectinload优化查询
        result = await db.execute(
            select(ChatSession)
            .options(
                selectinload(ChatSession.user1),
                selectinload(ChatSession.user2),
                selectinload(ChatSession.school)
            )
            .limit(10)
        )
        sessions = result.scalars().all()
        
        # 访问关联数据（不会触发额外查询）
        for session in sessions:
            _ = session.user1
            _ = session.user2
            _ = session.school
        
        queries_with_optimization = query_count
        logger.info(f"优化后查询次数: {queries_with_optimization}")
        break
    
    return queries_with_optimization


@pytest.mark.asyncio
async def test_query_optimization_comparison():
    """对比优化前后的查询次数"""
    queries_without = await test_chat_sessions_without_optimization()
    queries_with = await test_chat_sessions_with_optimization()
    
    if queries_without > 0 and queries_with > 0:
        improvement = ((queries_without - queries_with) / queries_without) * 100
        logger.info(f"查询优化效果: 减少了{improvement:.1f}%的查询次数")
        assert queries_with < queries_without, "优化后查询次数应该减少"
    else:
        pytest.skip("无法进行对比测试（可能没有数据）")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

