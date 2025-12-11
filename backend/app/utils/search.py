"""
搜索工具模块
提供全文搜索功能
"""
from sqlalchemy import text, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.logging import get_logger

logger = get_logger(__name__)


async def fulltext_search_jobs(
    db: AsyncSession,
    keyword: str,
    location: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> tuple[List, int]:
    """
    使用MySQL全文搜索搜索职位
    
    Args:
        db: 数据库会话
        keyword: 搜索关键词
        location: 工作地点（可选）
        limit: 返回数量限制
        offset: 偏移量
        
    Returns:
        tuple: (职位列表, 总数)
    """
    try:
        # 构建全文搜索查询
        # 注意：需要确保jobs表有FULLTEXT索引
        # CREATE FULLTEXT INDEX idx_fulltext ON jobs(title, description, requirements);
        
        base_query = """
            SELECT *, 
                   MATCH(title, description, requirements) AGAINST(:keyword IN NATURAL LANGUAGE MODE) as relevance
            FROM jobs
            WHERE MATCH(title, description, requirements) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
            AND status = 'PUBLISHED'
        """
        
        params = {"keyword": keyword}
        
        if location:
            base_query += " AND work_location LIKE :location"
            params["location"] = f"%{location}%"
        
        # 获取总数
        count_query = f"SELECT COUNT(*) as total FROM ({base_query}) as subquery"
        count_result = await db.execute(text(count_query), params)
        total = count_result.scalar() or 0
        
        # 获取分页结果
        search_query = f"{base_query} ORDER BY relevance DESC LIMIT :limit OFFSET :offset"
        params.update({"limit": limit, "offset": offset})
        
        result = await db.execute(text(search_query), params)
        rows = result.fetchall()
        
        # 将原始行数据转换为Job对象
        from sqlalchemy import select
        from app.models.job import Job
        
        jobs = []
        job_ids = []
        for row in rows:
            # 从行数据获取job_id
            job_id = row._mapping.get('id')
            if job_id:
                job_ids.append(job_id)
        
        # 批量查询Job对象（更高效）
        if job_ids:
            jobs_result = await db.execute(
                select(Job).where(Job.id.in_(job_ids))
            )
            jobs = list(jobs_result.scalars().all())
            # 按照relevance排序（如果需要，可以在这里排序）
        
        logger.info(f"全文搜索职位: 关键词='{keyword}', 找到 {total} 条结果")
        
        return jobs, total
        
    except Exception as e:
        logger.error(f"全文搜索失败，回退到普通搜索: {str(e)}")
        # 如果全文搜索失败（可能没有FULLTEXT索引），回退到普通搜索
        return await fallback_search_jobs(db, keyword, location, limit, offset)


async def fallback_search_jobs(
    db: AsyncSession,
    keyword: str,
    location: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> tuple[List, int]:
    """
    回退搜索方法（使用LIKE查询）
    """
    from sqlalchemy import select, func, or_
    from app.models.job import Job
    
    query = select(Job).where(Job.status == "PUBLISHED")
    
    if keyword:
        query = query.where(
            or_(
                Job.title.contains(keyword),
                Job.description.contains(keyword),
                Job.requirements.contains(keyword)
            )
        )
    
    if location:
        query = query.where(Job.work_location.contains(location))
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # 分页查询
    query = query.order_by(Job.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    jobs = result.scalars().all()
    
    return jobs, total


async def create_fulltext_indexes(db: AsyncSession):
    """
    创建全文搜索索引（需要在数据库迁移中执行）
    """
    try:
        # 为jobs表创建全文索引
        await db.execute(text("""
            CREATE FULLTEXT INDEX IF NOT EXISTS idx_jobs_fulltext 
            ON jobs(title, description, requirements)
        """))
        
        # 为resumes表创建全文索引
        await db.execute(text("""
            CREATE FULLTEXT INDEX IF NOT EXISTS idx_resumes_fulltext 
            ON resumes(content)
        """))
        
        await db.commit()
        logger.info("全文搜索索引创建成功")
        
    except Exception as e:
        logger.warning(f"创建全文搜索索引失败（可能已存在）: {str(e)}")
        await db.rollback()

