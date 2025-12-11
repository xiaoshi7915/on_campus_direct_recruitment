"""
同步现有数据到人才库表
将企业触达过的学生数据同步到talent_pools表
"""
import asyncio
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4
from app.core.database import AsyncSessionLocal
from app.models.profile import EnterpriseProfile, StudentProfile
from app.models.job import Job, JobApplication, Resume
from app.models.interview import Interview, Offer
from app.models.common import Favorite
from app.models.chat import ChatSession, Message
from app.models.talent_pool import TalentPool
from app.models.user import User


async def sync_talent_pool_data():
    """同步现有数据到人才库表"""
    async with AsyncSessionLocal() as db:
        try:
            # 获取所有企业
            enterprises_result = await db.execute(select(EnterpriseProfile))
            enterprises = enterprises_result.scalars().all()
            
            print(f"✓ 找到 {len(enterprises)} 个企业")
            
            total_synced = 0
            
            for enterprise in enterprises:
                # 获取企业用户
                user_result = await db.execute(select(User).where(User.id == enterprise.user_id))
                enterprise_user = user_result.scalar_one_or_none()
                
                if not enterprise_user:
                    continue
                
                print(f"\n处理企业: {enterprise.company_name}")
                
                # 1. 通过职位申请触达的学生
                applications_result = await db.execute(
                    select(StudentProfile.id, JobApplication.id.label('app_id'), JobApplication.resume_id, JobApplication.created_at).join(
                        JobApplication, StudentProfile.user_id == JobApplication.student_id
                    ).where(
                        JobApplication.job_id.in_(
                            select(Job.id).where(Job.enterprise_id == enterprise.id)
                        )
                    ).distinct()
                )
                applications = applications_result.all()
                
                for app_row in applications:
                    student_id = app_row.id
                    app_id = app_row.app_id
                    resume_id = app_row.resume_id
                    contact_time = app_row.created_at
                    
                    # 检查是否已存在（在同一批次中可能已创建）
                    existing = await db.execute(
                        select(TalentPool).where(
                            TalentPool.enterprise_id == enterprise.id,
                            TalentPool.student_id == student_id
                        )
                    )
                    talent = existing.scalar_one_or_none()
                    
                    if not talent:
                        talent = TalentPool(
                            id=str(uuid4()),
                            enterprise_id=enterprise.id,
                            student_id=student_id,
                            resume_id=resume_id,
                            application_id=app_id,
                            status="ALL",
                            first_contact_time=contact_time,
                            last_contact_time=contact_time
                        )
                        db.add(talent)
                        total_synced += 1
                        await db.flush()  # 立即刷新，避免重复键错误
                    else:
                        if not talent.first_contact_time or contact_time < talent.first_contact_time:
                            talent.first_contact_time = contact_time
                        if not talent.last_contact_time or contact_time > talent.last_contact_time:
                            talent.last_contact_time = contact_time
                        if not talent.application_id:
                            talent.application_id = app_id
                        if not talent.resume_id and resume_id:
                            talent.resume_id = resume_id
                
                # 2. 通过面试触达的学生
                interviews_result = await db.execute(
                    select(Interview.student_id, Interview.id.label('interview_id'), Interview.created_at).where(
                        Interview.enterprise_id == enterprise.id
                    ).distinct()
                )
                interviews = interviews_result.all()
                
                for int_row in interviews:
                    student_id = int_row.student_id
                    interview_id = int_row.interview_id
                    contact_time = int_row.created_at
                    
                    existing = await db.execute(
                        select(TalentPool).where(
                            TalentPool.enterprise_id == enterprise.id,
                            TalentPool.student_id == student_id
                        )
                    )
                    talent = existing.scalar_one_or_none()
                    
                    if not talent:
                        talent = TalentPool(
                            id=str(uuid4()),
                            enterprise_id=enterprise.id,
                            student_id=student_id,
                            interview_id=interview_id,
                            status="INTERVIEWED",
                            first_contact_time=contact_time,
                            last_contact_time=contact_time
                        )
                        db.add(talent)
                        total_synced += 1
                        await db.flush()  # 立即刷新，避免重复键错误
                    else:
                        if not talent.first_contact_time or contact_time < talent.first_contact_time:
                            talent.first_contact_time = contact_time
                        if not talent.last_contact_time or contact_time > talent.last_contact_time:
                            talent.last_contact_time = contact_time
                        if not talent.interview_id:
                            talent.interview_id = interview_id
                        talent.status = "INTERVIEWED"
                
                # 3. 通过Offer触达的学生
                offers_result = await db.execute(
                    select(Offer.student_id, Offer.id.label('offer_id'), Offer.created_at).where(
                        Offer.enterprise_id == enterprise.id
                    ).distinct()
                )
                offers = offers_result.all()
                
                for offer_row in offers:
                    student_id = offer_row.student_id
                    offer_id = offer_row.offer_id
                    contact_time = offer_row.created_at
                    
                    existing = await db.execute(
                        select(TalentPool).where(
                            TalentPool.enterprise_id == enterprise.id,
                            TalentPool.student_id == student_id
                        )
                    )
                    talent = existing.scalar_one_or_none()
                    
                    if not talent:
                        talent = TalentPool(
                            id=str(uuid4()),
                            enterprise_id=enterprise.id,
                            student_id=student_id,
                            offer_id=offer_id,
                            status="HIRED",
                            first_contact_time=contact_time,
                            last_contact_time=contact_time
                        )
                        db.add(talent)
                        total_synced += 1
                        await db.flush()  # 立即刷新，避免重复键错误
                    else:
                        if not talent.first_contact_time or contact_time < talent.first_contact_time:
                            talent.first_contact_time = contact_time
                        if not talent.last_contact_time or contact_time > talent.last_contact_time:
                            talent.last_contact_time = contact_time
                        if not talent.offer_id:
                            talent.offer_id = offer_id
                        talent.status = "HIRED"
                
                # 4. 通过收藏触达的学生
                favorites_result = await db.execute(
                    select(Favorite.target_id, Favorite.created_at).where(
                        Favorite.user_id == enterprise_user.id,
                        Favorite.target_type == "RESUME"
                    ).distinct()
                )
                favorite_resume_ids = {row.target_id: row.created_at for row in favorites_result.all()}
                
                if favorite_resume_ids:
                    resumes_result = await db.execute(
                        select(Resume.student_id, Resume.id).where(Resume.id.in_(favorite_resume_ids.keys()))
                    )
                    resume_student_map = {row.id: row.student_id for row in resumes_result.all()}
                    
                    for resume_id, contact_time in favorite_resume_ids.items():
                        if resume_id in resume_student_map:
                            student_id = resume_student_map[resume_id]
                            
                            existing = await db.execute(
                                select(TalentPool).where(
                                    TalentPool.enterprise_id == enterprise.id,
                                    TalentPool.student_id == student_id
                                )
                            )
                            talent = existing.scalar_one_or_none()
                            
                            if not talent:
                                talent = TalentPool(
                                    id=str(uuid4()),
                                    enterprise_id=enterprise.id,
                                    student_id=student_id,
                                    resume_id=resume_id,
                                    status="FAVORITED",
                                    first_contact_time=contact_time,
                                    last_contact_time=contact_time
                                )
                                db.add(talent)
                                total_synced += 1
                                await db.flush()  # 立即刷新，避免重复键错误
                            else:
                                if not talent.first_contact_time or contact_time < talent.first_contact_time:
                                    talent.first_contact_time = contact_time
                                if not talent.last_contact_time or contact_time > talent.last_contact_time:
                                    talent.last_contact_time = contact_time
                                if not talent.resume_id:
                                    talent.resume_id = resume_id
                                if talent.status == "ALL":
                                    talent.status = "FAVORITED"
                
                # 5. 通过聊天触达的学生
                chat_sessions_result = await db.execute(
                    select(ChatSession.user2_id, ChatSession.last_message_at).where(
                        ChatSession.user1_id == enterprise_user.id
                    ).distinct()
                )
                chat_user_ids1 = {row.user2_id: row.last_message_at for row in chat_sessions_result.all()}
                
                chat_sessions_result2 = await db.execute(
                    select(ChatSession.user1_id, ChatSession.last_message_at).where(
                        ChatSession.user2_id == enterprise_user.id
                    ).distinct()
                )
                chat_user_ids2 = {row.user1_id: row.last_message_at for row in chat_sessions_result2.all()}
                
                chat_user_ids = {**chat_user_ids1, **chat_user_ids2}
                
                if chat_user_ids:
                    students_result = await db.execute(
                        select(StudentProfile.id, StudentProfile.user_id).where(
                            StudentProfile.user_id.in_(chat_user_ids.keys())
                        )
                    )
                    user_student_map = {row.user_id: row.id for row in students_result.all()}
                    
                    for user_id, contact_time in chat_user_ids.items():
                        if user_id in user_student_map:
                            student_id = user_student_map[user_id]
                            
                            existing = await db.execute(
                                select(TalentPool).where(
                                    TalentPool.enterprise_id == enterprise.id,
                                    TalentPool.student_id == student_id
                                )
                            )
                            talent = existing.scalar_one_or_none()
                            
                            if not talent:
                                talent = TalentPool(
                                    id=str(uuid4()),
                                    enterprise_id=enterprise.id,
                                    student_id=student_id,
                                    status="COMMUNICATING",
                                    first_contact_time=contact_time or datetime.now(),
                                    last_contact_time=contact_time or datetime.now()
                                )
                                db.add(talent)
                                total_synced += 1
                                await db.flush()  # 立即刷新，避免重复键错误
                            else:
                                if contact_time:
                                    if not talent.first_contact_time or contact_time < talent.first_contact_time:
                                        talent.first_contact_time = contact_time
                                    if not talent.last_contact_time or contact_time > talent.last_contact_time:
                                        talent.last_contact_time = contact_time
                                if talent.status in ["ALL", "FAVORITED"]:
                                    talent.status = "COMMUNICATING"
                
            await db.commit()
            print(f"\n✓ 成功同步 {total_synced} 条人才库数据")
            
        except Exception as e:
            await db.rollback()
            print(f"✗ 同步失败: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(sync_talent_pool_data())

