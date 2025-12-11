"""
为人才库添加测试数据
人才库不是单独的表，而是通过企业触达过的学生来构建的
需要创建：职位申请、面试、Offer、收藏、聊天等数据
"""
import asyncio
from sqlalchemy import select
from uuid import uuid4
from datetime import datetime, timedelta
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.profile import EnterpriseProfile, StudentProfile
from app.models.job import Job, JobApplication, Resume
from app.models.interview import Interview, Offer
from app.models.common import Favorite
from app.models.chat import ChatSession, Message
from app.models.enums import (
    ApplicationStatus, InterviewStatus, OfferStatus, 
    MessageType, FavoriteType
)


async def add_talent_pool_data():
    """为人才库添加测试数据"""
    async with AsyncSessionLocal() as db:
        try:
            # 获取一个企业
            enterprise_result = await db.execute(
                select(EnterpriseProfile).limit(1)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            
            if not enterprise:
                print("✗ 没有找到企业，请先运行数据填充脚本")
                return
            
            # 获取企业用户
            enterprise_user_result = await db.execute(
                select(User).where(User.id == enterprise.user_id)
            )
            enterprise_user = enterprise_user_result.scalar_one_or_none()
            
            if not enterprise_user:
                print("✗ 没有找到企业用户")
                return
            
            # 获取一些学生
            students_result = await db.execute(
                select(StudentProfile).limit(10)
            )
            students = students_result.scalars().all()
            
            if not students:
                print("✗ 没有找到学生，请先运行数据填充脚本")
                return
            
            print(f"✓ 找到企业: {enterprise.company_name}")
            print(f"✓ 找到 {len(students)} 个学生")
            
            # 获取企业的职位
            jobs_result = await db.execute(
                select(Job).where(Job.enterprise_id == enterprise.id).limit(5)
            )
            jobs = jobs_result.scalars().all()
            
            if not jobs:
                print("✗ 企业没有职位，创建一些职位...")
                # 创建一些职位
                for i in range(3):
                    job = Job(
                        id=str(uuid4()),
                        enterprise_id=enterprise.id,
                        title=f"测试职位{i+1}",
                        description="这是一个测试职位",
                        requirements="要求：本科及以上学历",
                        location="北京",
                        salary_min=8000,
                        salary_max=15000,
                        status="PUBLISHED"
                    )
                    db.add(job)
                await db.commit()
                
                # 重新获取职位
                jobs_result = await db.execute(
                    select(Job).where(Job.enterprise_id == enterprise.id).limit(5)
                )
                jobs = jobs_result.scalars().all()
            
            print(f"✓ 找到 {len(jobs)} 个职位")
            
            added_count = 0
            
            # 1. 创建职位申请（让一些学生申请职位）
            for i, student in enumerate(students[:5]):
                if i >= len(jobs):
                    break
                
                # 检查是否已有申请
                existing_result = await db.execute(
                    select(JobApplication).where(
                        JobApplication.job_id == jobs[i].id,
                        JobApplication.student_id == student.user_id
                    )
                )
                existing = existing_result.scalar_one_or_none()
                
                if not existing:
                    # 获取或创建简历
                    resume_result = await db.execute(
                        select(Resume).where(Resume.student_id == student.id).limit(1)
                    )
                    resume = resume_result.scalar_one_or_none()
                    
                    if not resume:
                        # 创建简历
                        resume = Resume(
                            id=str(uuid4()),
                            student_id=student.id,
                            title=f"{student.real_name}的简历",
                            content="这是一份测试简历",
                            created_at=datetime.now() - timedelta(days=i+1)
                        )
                        db.add(resume)
                        await db.flush()
                    
                    application = JobApplication(
                        id=str(uuid4()),
                        job_id=jobs[i].id,
                        resume_id=resume.id,
                        student_id=student.user_id,
                        status=ApplicationStatus.PENDING if i % 2 == 0 else ApplicationStatus.ACCEPTED,
                        created_at=datetime.now() - timedelta(days=i)
                    )
                    db.add(application)
                    added_count += 1
                    print(f"  ✓ 创建职位申请: {student.real_name} -> {jobs[i].title}")
            
            # 2. 创建面试（为一些学生创建面试，需要先有申请）
            for i, student in enumerate(students[2:7]):
                if i >= len(jobs):
                    break
                
                # 先获取或创建申请
                application_result = await db.execute(
                    select(JobApplication).where(
                        JobApplication.job_id == jobs[i % len(jobs)].id,
                        JobApplication.student_id == student.user_id
                    )
                )
                application = application_result.scalar_one_or_none()
                
                if not application:
                    # 获取或创建简历
                    resume_result = await db.execute(
                        select(Resume).where(Resume.student_id == student.id).limit(1)
                    )
                    resume = resume_result.scalar_one_or_none()
                    
                    if not resume:
                        # 创建简历
                        resume = Resume(
                            id=str(uuid4()),
                            student_id=student.id,
                            title=f"{student.real_name}的简历",
                            content="这是一份测试简历",
                            created_at=datetime.now() - timedelta(days=i+2)
                        )
                        db.add(resume)
                        await db.flush()
                    
                    # 创建申请
                    application = JobApplication(
                        id=str(uuid4()),
                        job_id=jobs[i % len(jobs)].id,
                        resume_id=resume.id,
                        student_id=student.user_id,
                        status=ApplicationStatus.ACCEPTED,
                        created_at=datetime.now() - timedelta(days=i+1)
                    )
                    db.add(application)
                    await db.flush()  # 刷新以获取ID
                
                # 检查是否已有面试
                existing_result = await db.execute(
                    select(Interview).where(
                        Interview.application_id == application.id
                    )
                )
                existing = existing_result.scalar_one_or_none()
                
                if not existing:
                    interview = Interview(
                        id=str(uuid4()),
                        application_id=application.id,
                        enterprise_id=enterprise.id,
                        student_id=student.id,
                        interview_type="ONLINE",
                        scheduled_time=datetime.now() + timedelta(days=i+1),
                        location="线上",
                        status=InterviewStatus.SCHEDULED,
                        created_at=datetime.now() - timedelta(days=i)
                    )
                    db.add(interview)
                    added_count += 1
                    print(f"  ✓ 创建面试: {student.real_name}")
            
            # 3. 创建Offer（为一些学生创建Offer，需要先有申请）
            for i, student in enumerate(students[4:6]):
                if i >= len(jobs):
                    break
                
                # 先获取或创建申请
                application_result = await db.execute(
                    select(JobApplication).where(
                        JobApplication.job_id == jobs[i % len(jobs)].id,
                        JobApplication.student_id == student.user_id
                    )
                )
                application = application_result.scalar_one_or_none()
                
                if not application:
                    # 获取或创建简历
                    resume_result = await db.execute(
                        select(Resume).where(Resume.student_id == student.id).limit(1)
                    )
                    resume = resume_result.scalar_one_or_none()
                    
                    if not resume:
                        # 创建简历
                        resume = Resume(
                            id=str(uuid4()),
                            student_id=student.id,
                            title=f"{student.real_name}的简历",
                            content="这是一份测试简历",
                            created_at=datetime.now() - timedelta(days=i+2)
                        )
                        db.add(resume)
                        await db.flush()
                    
                    # 创建申请
                    application = JobApplication(
                        id=str(uuid4()),
                        job_id=jobs[i % len(jobs)].id,
                        resume_id=resume.id,
                        student_id=student.user_id,
                        status=ApplicationStatus.ACCEPTED,
                        created_at=datetime.now() - timedelta(days=i+1)
                    )
                    db.add(application)
                    await db.flush()  # 刷新以获取ID
                
                # 获取职位信息
                job_result = await db.execute(
                    select(Job).where(Job.id == jobs[i % len(jobs)].id)
                )
                job = job_result.scalar_one_or_none()
                
                # 检查是否已有Offer
                existing_result = await db.execute(
                    select(Offer).where(
                        Offer.application_id == application.id
                    )
                )
                existing = existing_result.scalar_one_or_none()
                
                if not existing:
                    offer = Offer(
                        id=str(uuid4()),
                        application_id=application.id,
                        enterprise_id=enterprise.id,
                        student_id=student.id,
                        job_title=job.title if job else f"职位{i+1}",
                        salary=10000 + i * 1000,
                        content=f"恭喜您通过面试，我们为您提供{10000 + i * 1000}元的薪资",
                        status=OfferStatus.PENDING,
                        created_at=datetime.now() - timedelta(days=i)
                    )
                    db.add(offer)
                    added_count += 1
                    print(f"  ✓ 创建Offer: {student.real_name}")
            
            # 4. 创建收藏（收藏一些学生的简历）
            for i, student in enumerate(students[6:9]):
                # 获取学生的简历
                resume_result = await db.execute(
                    select(Resume).where(Resume.student_id == student.id).limit(1)
                )
                resume = resume_result.scalar_one_or_none()
                
                if resume:
                    # 检查是否已收藏
                    existing_result = await db.execute(
                        select(Favorite).where(
                            Favorite.user_id == enterprise_user.id,
                            Favorite.target_type == FavoriteType.RESUME,
                            Favorite.target_id == resume.id
                        )
                    )
                    existing = existing_result.scalar_one_or_none()
                    
                    if not existing:
                        favorite = Favorite(
                            id=str(uuid4()),
                            user_id=enterprise_user.id,
                            target_type=FavoriteType.RESUME,
                            target_id=resume.id,
                            created_at=datetime.now() - timedelta(days=i)
                        )
                        db.add(favorite)
                        added_count += 1
                        print(f"  ✓ 创建收藏: {student.real_name}的简历")
            
            # 5. 创建聊天会话（与一些学生聊天）
            for i, student in enumerate(students[8:10]):
                # 获取学生用户
                student_user_result = await db.execute(
                    select(User).where(User.id == student.user_id)
                )
                student_user = student_user_result.scalar_one_or_none()
                
                if student_user:
                    # 检查是否已有聊天会话
                    existing_result = await db.execute(
                        select(ChatSession).where(
                            ((ChatSession.user1_id == enterprise_user.id) & 
                             (ChatSession.user2_id == student_user.id)) |
                            ((ChatSession.user1_id == student_user.id) & 
                             (ChatSession.user2_id == enterprise_user.id))
                        )
                    )
                    existing = existing_result.scalar_one_or_none()
                    
                    if not existing:
                        chat_session = ChatSession(
                            id=str(uuid4()),
                            user1_id=enterprise_user.id,
                            user2_id=student_user.id,
                            created_at=datetime.now() - timedelta(days=i)
                        )
                        db.add(chat_session)
                        
                        # 创建一条消息
                        message = Message(
                            id=str(uuid4()),
                            session_id=chat_session.id,
                            sender_id=enterprise_user.id,
                            receiver_id=student_user.id,
                            content="你好，我们对你的简历很感兴趣",
                            message_type=MessageType.TEXT,
                            created_at=datetime.now() - timedelta(days=i)
                        )
                        db.add(message)
                        added_count += 1
                        print(f"  ✓ 创建聊天会话: {student.real_name}")
            
            await db.commit()
            print(f"\n✓ 成功添加 {added_count} 条人才库相关数据")
            print(f"✓ 企业 {enterprise.company_name} 的人才库现在应该包含触达过的学生")
            
        except Exception as e:
            await db.rollback()
            print(f"✗ 添加人才库数据失败: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(add_talent_pool_data())

