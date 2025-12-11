"""
为指定企业添加人才库数据（20条记录）
"""
import asyncio
from sqlalchemy import select
from datetime import datetime, timedelta
from uuid import uuid4
from app.core.database import AsyncSessionLocal
from app.models.profile import EnterpriseProfile, StudentProfile
from app.models.job import Job, JobApplication, Resume
from app.models.interview import Interview
from app.models.interview import Offer
from app.models.common import Favorite
from app.models.chat import ChatSession
from app.models.talent_pool import TalentPool
from app.models.user import User
from app.models.enums import ApplicationStatus


async def add_talent_pool_data_for_enterprise():
    """为当前登录企业添加20条人才库数据"""
    async with AsyncSessionLocal() as db:
        try:
            # 获取第一个企业（或指定企业）
            enterprise_result = await db.execute(
                select(EnterpriseProfile).order_by(EnterpriseProfile.created_at).limit(1)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            
            if not enterprise:
                print("❌ 没有找到企业，请先创建企业")
                return
            
            print(f"✓ 找到企业: {enterprise.company_name} (ID: {enterprise.id})")
            
            # 获取所有学生（获取更多，因为有些可能已存在）
            students_result = await db.execute(select(StudentProfile).limit(50))
            students = students_result.scalars().all()
            
            print(f"✓ 找到 {len(students)} 个学生")
            
            # 获取企业的职位
            jobs_result = await db.execute(
                select(Job).where(Job.enterprise_id == enterprise.id).limit(5)
            )
            jobs = jobs_result.scalars().all()
            
            if not jobs:
                print("⚠️  企业没有职位，将创建虚拟职位申请记录")
            
            added_count = 0
            processed_count = 0
            
            for i, student in enumerate(students):
                if added_count >= 20:
                    break
                
                processed_count += 1
                try:
                    # 检查是否已存在
                    existing = await db.execute(
                        select(TalentPool).where(
                            TalentPool.enterprise_id == enterprise.id,
                            TalentPool.student_id == student.id
                        )
                    )
                    if existing.scalar_one_or_none():
                        print(f"  跳过学生 {student.real_name}（已存在）")
                        continue
                    
                    # 获取学生的简历
                    resume_result = await db.execute(
                        select(Resume).where(Resume.student_id == student.id).limit(1)
                    )
                    resume = resume_result.scalar_one_or_none()
                    
                    # 创建不同类型的触达记录
                    contact_time = datetime.now() - timedelta(days=i % 10)
                    status = ["ALL", "FAVORITED", "COMMUNICATING", "INTERVIEWED", "HIRED"][i % 5]
                    
                    # 根据状态创建不同的关联记录
                    application_id = None
                    interview_id = None
                    offer_id = None
                    
                    if i % 5 == 0:  # ALL - 创建职位申请
                        if jobs:
                            job = jobs[i % len(jobs)]
                            if resume:
                                application = JobApplication(
                                    id=str(uuid4()),
                                    job_id=job.id,
                                    student_id=student.user_id,
                                    resume_id=resume.id,
                                    status=ApplicationStatus.PENDING,
                                    created_at=contact_time
                                )
                                db.add(application)
                                await db.flush()
                                application_id = application.id
                    elif i % 5 == 1:  # FAVORITED - 创建收藏
                        if resume:
                            favorite = Favorite(
                                id=str(uuid4()),
                                user_id=enterprise.user_id,
                                target_type="RESUME",
                                target_id=resume.id,
                                created_at=contact_time
                            )
                            db.add(favorite)
                    elif i % 5 == 2:  # COMMUNICATING - 创建聊天会话
                        chat_session = ChatSession(
                            id=str(uuid4()),
                            user1_id=enterprise.user_id,
                            user2_id=student.user_id,
                            created_at=contact_time
                        )
                        db.add(chat_session)
                    elif i % 5 == 3:  # INTERVIEWED - 创建面试记录
                        if jobs and resume:
                            job = jobs[i % len(jobs)]
                            application_result = await db.execute(
                                select(JobApplication).where(
                                    JobApplication.job_id == job.id,
                                    JobApplication.student_id == student.user_id
                                ).limit(1)
                            )
                            application = application_result.scalar_one_or_none()
                            
                            if not application:
                                application = JobApplication(
                                    id=str(uuid4()),
                                    job_id=job.id,
                                    student_id=student.user_id,
                                    resume_id=resume.id,
                                    status=ApplicationStatus.ACCEPTED,
                                    created_at=contact_time
                                )
                                db.add(application)
                                await db.flush()
                            
                            interview = Interview(
                                id=str(uuid4()),
                                enterprise_id=enterprise.id,
                                student_id=student.id,
                                application_id=application.id,
                                scheduled_time=contact_time + timedelta(days=1),
                                status="SCHEDULED",
                                created_at=contact_time
                            )
                            db.add(interview)
                            await db.flush()
                            interview_id = interview.id
                    elif i % 5 == 4:  # HIRED - 创建Offer
                        if jobs and resume:
                            job = jobs[i % len(jobs)]
                            application_result = await db.execute(
                                select(JobApplication).where(
                                    JobApplication.job_id == job.id,
                                    JobApplication.student_id == student.user_id
                                ).limit(1)
                            )
                            application = application_result.scalar_one_or_none()
                            
                            if not application:
                                application = JobApplication(
                                    id=str(uuid4()),
                                    job_id=job.id,
                                    student_id=student.user_id,
                                    resume_id=resume.id,
                                    status=ApplicationStatus.ACCEPTED,
                                    created_at=contact_time
                                )
                                db.add(application)
                                await db.flush()
                            
                            offer = Offer(
                                id=str(uuid4()),
                                enterprise_id=enterprise.id,
                                student_id=student.id,
                                application_id=application.id,
                                job_title=job.title,
                                content=f"恭喜您通过面试，我们诚挚邀请您加入我们！",
                                status="PENDING",
                                created_at=contact_time
                            )
                            db.add(offer)
                            await db.flush()
                            offer_id = offer.id
                    
                    # 创建人才库记录
                    talent = TalentPool(
                        id=str(uuid4()),
                        enterprise_id=enterprise.id,
                        student_id=student.id,
                        resume_id=resume.id if resume else None,
                        status=status,
                        application_id=application_id,
                        interview_id=interview_id,
                        offer_id=offer_id,
                        first_contact_time=contact_time,
                        last_contact_time=contact_time,
                        created_at=contact_time
                    )
                    db.add(talent)
                    await db.flush()
                    
                    added_count += 1
                    print(f"  ✓ 添加学生 {student.real_name} ({status})")
                    
                except Exception as e:
                    print(f"  ❌ 添加学生 {student.real_name} 失败: {str(e)}")
                    continue
            
            await db.commit()
            print(f"\n✅ 成功为企业 {enterprise.company_name} 添加了 {added_count} 条人才库记录")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(add_talent_pool_data_for_enterprise())

