"""
人才库服务
用于自动同步和更新企业人才库数据
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4
from app.models.talent_pool import TalentPool
from app.models.profile import StudentProfile
from app.models.job import Resume
from app.models.common import Favorite
from app.models.chat import ChatSession
from app.models.interview import Interview
from app.models.interview import Offer
from app.models.job import JobApplication


async def sync_talent_to_pool(
    db: AsyncSession,
    enterprise_id: str,
    student_id: str,
    contact_type: str = "APPLICATION",  # APPLICATION, INTERVIEW, OFFER, FAVORITE, CHAT
    resume_id: str = None,
    application_id: str = None,
    interview_id: str = None,
    offer_id: str = None
):
    """
    同步学生到企业人才库
    
    Args:
        db: 数据库会话
        enterprise_id: 企业ID
        student_id: 学生ID
        contact_type: 接触类型
        resume_id: 简历ID
        application_id: 申请ID
        interview_id: 面试ID
        offer_id: Offer ID
    """
    # 检查是否已存在
    result = await db.execute(
        select(TalentPool).where(
            TalentPool.enterprise_id == enterprise_id,
            TalentPool.student_id == student_id
        )
    )
    talent = result.scalar_one_or_none()
    
    now = datetime.now()
    
    if talent:
        # 更新现有记录
        if not talent.first_contact_time:
            talent.first_contact_time = now
        talent.last_contact_time = now
        
        # 更新关联信息
        if resume_id:
            talent.resume_id = resume_id
        if application_id:
            talent.application_id = application_id
        if interview_id:
            talent.interview_id = interview_id
        if offer_id:
            talent.offer_id = offer_id
        
        # 更新状态（优先级：HIRED > INTERVIEWED > COMMUNICATING > FAVORITED > ALL）
        if offer_id:
            talent.status = "HIRED"
        elif interview_id:
            talent.status = "INTERVIEWED"
        elif contact_type == "CHAT":
            talent.status = "COMMUNICATING"
        elif contact_type == "FAVORITE":
            talent.status = "FAVORITED"
    else:
        # 创建新记录
        talent = TalentPool(
            id=str(uuid4()),
            enterprise_id=enterprise_id,
            student_id=student_id,
            resume_id=resume_id,
            application_id=application_id,
            interview_id=interview_id,
            offer_id=offer_id,
            status="ALL",
            first_contact_time=now,
            last_contact_time=now
        )
        
        # 设置初始状态
        if offer_id:
            talent.status = "HIRED"
        elif interview_id:
            talent.status = "INTERVIEWED"
        elif contact_type == "CHAT":
            talent.status = "COMMUNICATING"
        elif contact_type == "FAVORITE":
            talent.status = "FAVORITED"
        
        db.add(talent)
    
    await db.flush()
    return talent


async def update_talent_status(
    db: AsyncSession,
    enterprise_id: str,
    student_id: str,
    status: str,
    last_contact_time: datetime = None
):
    """
    更新人才库状态
    
    Args:
        db: 数据库会话
        enterprise_id: 企业ID
        student_id: 学生ID
        status: 状态
        last_contact_time: 最后联系时间
    """
    result = await db.execute(
        select(TalentPool).where(
            TalentPool.enterprise_id == enterprise_id,
            TalentPool.student_id == student_id
        )
    )
    talent = result.scalar_one_or_none()
    
    if talent:
        talent.status = status
        if last_contact_time:
            talent.last_contact_time = last_contact_time
        await db.flush()
        return talent
    
    return None


