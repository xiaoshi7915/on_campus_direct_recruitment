"""
只填充空表的数据，不清空现有数据
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4
import random

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.user_type import UserType
from app.models.school import School, Department, Class
from app.models.profile import StudentProfile, TeacherProfile, EnterpriseProfile
from app.models.job import Job, Resume, JobIntention, JobApplication
from app.models.activity import JobFair, JobFairRegistration, InfoSession, InfoSessionRegistration
from app.models.interview import Interview, Offer
from app.models.chat import ChatSession, Message
from app.models.common import Schedule, Favorite, Feedback
from app.models.rights import Rights, RightsPackage, RightsPackageItem, UserRights, RightsPurchase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def check_table_empty(db: AsyncSession, model):
    """检查表是否为空"""
    result = await db.execute(select(func.count()).select_from(model))
    count = result.scalar() or 0
    return count == 0


async def create_job_intentions(db: AsyncSession, count: int = 50):
    """创建求职意向数据"""
    # 检查是否为空
    if not await check_table_empty(db, JobIntention):
        print("[SKIP] job_intentions 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个求职意向...")
    
    # 获取学生档案
    result = await db.execute(select(StudentProfile))
    student_profiles = list(result.scalars().all())
    
    if not student_profiles:
        print("[SKIP] 没有学生档案，跳过创建求职意向")
        return []
    
    intentions = []
    for i in range(count):
        student = random.choice(student_profiles)
        
        # 检查是否已有求职意向
        existing = await db.execute(
            select(JobIntention).where(JobIntention.student_id == student.id)
        )
        if existing.scalar_one_or_none():
            continue
        
        intention = JobIntention(
            id=str(uuid4()),
            student_id=student.id,
            job_type=random.choice(["FULL_TIME", "PART_TIME", "INTERN"]),
            industry=random.choice(["互联网", "金融", "制造业", "教育", "医疗", "零售", "物流", "房地产", "能源", "传媒"]),
            salary_expect=random.choice([5000, 8000, 10000, 15000, 20000]),
            work_location=random.choice(["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉"])
        )
        intentions.append(intention)
        db.add(intention)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(intentions)} 个求职意向")
    return intentions


async def create_job_fair_registrations(db: AsyncSession, count: int = 50):
    """创建双选会报名数据"""
    # 检查是否为空
    if not await check_table_empty(db, JobFairRegistration):
        print("[SKIP] job_fair_registrations 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个双选会报名...")
    
    # 获取双选会和企业档案
    job_fairs_result = await db.execute(select(JobFair))
    job_fairs = list(job_fairs_result.scalars().all())
    
    enterprises_result = await db.execute(select(EnterpriseProfile))
    enterprises = list(enterprises_result.scalars().all())
    
    if not job_fairs or not enterprises:
        print("[SKIP] 没有双选会或企业档案，跳过创建报名")
        return []
    
    registrations = []
    for i in range(count):
        job_fair = random.choice(job_fairs)
        enterprise = random.choice(enterprises)
        
        # 检查是否已报名
        existing = await db.execute(
            select(JobFairRegistration).where(
                JobFairRegistration.job_fair_id == job_fair.id,
                JobFairRegistration.enterprise_id == enterprise.id
            )
        )
        if existing.scalar_one_or_none():
            continue
        
        registration = JobFairRegistration(
            id=str(uuid4()),
            job_fair_id=job_fair.id,
            enterprise_id=enterprise.id,
            status=random.choice(["PENDING", "APPROVED", "REJECTED", "CHECKED_IN"]),
            check_in_time=datetime.now() - timedelta(days=random.randint(0, 30)) if i % 3 == 0 else None
        )
        registrations.append(registration)
        db.add(registration)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(registrations)} 个双选会报名")
    return registrations


async def create_info_session_registrations(db: AsyncSession, count: int = 50):
    """创建宣讲会报名数据"""
    # 检查是否为空
    if not await check_table_empty(db, InfoSessionRegistration):
        print("[SKIP] info_session_registrations 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个宣讲会报名...")
    
    # 获取宣讲会和学生档案
    info_sessions_result = await db.execute(select(InfoSession))
    info_sessions = list(info_sessions_result.scalars().all())
    
    students_result = await db.execute(select(StudentProfile))
    students = list(students_result.scalars().all())
    
    if not info_sessions or not students:
        print("[SKIP] 没有宣讲会或学生档案，跳过创建报名")
        return []
    
    registrations = []
    for i in range(count):
        info_session = random.choice(info_sessions)
        student = random.choice(students)
        
        # 检查是否已报名
        existing = await db.execute(
            select(InfoSessionRegistration).where(
                InfoSessionRegistration.session_id == info_session.id,
                InfoSessionRegistration.student_id == student.id
            )
        )
        if existing.scalar_one_or_none():
            continue
        
        registration = InfoSessionRegistration(
            id=str(uuid4()),
            session_id=info_session.id,
            student_id=student.id,
            status=random.choice(["PENDING", "APPROVED", "REJECTED", "CHECKED_IN"]),
            check_in_time=datetime.now() - timedelta(days=random.randint(0, 30)) if i % 3 == 0 else None
        )
        registrations.append(registration)
        db.add(registration)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(registrations)} 个宣讲会报名")
    return registrations


async def create_offers(db: AsyncSession, count: int = 50):
    """创建Offer数据"""
    # 检查是否为空
    if not await check_table_empty(db, Offer):
        print("[SKIP] offers 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个Offer...")
    
    # 获取已接受的申请
    applications_result = await db.execute(
        select(JobApplication).where(JobApplication.status == "ACCEPTED")
    )
    applications = list(applications_result.scalars().all())
    
    if not applications:
        print("[SKIP] 没有已接受的申请，跳过创建Offer")
        return []
    
    offers = []
    for i in range(min(count, len(applications))):
        application = applications[i] if i < len(applications) else random.choice(applications)
        
        # 检查是否已有Offer
        existing = await db.execute(
            select(Offer).where(Offer.application_id == application.id)
        )
        if existing.scalar_one_or_none():
            continue
        
        # 获取学生档案
        student_profile_result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == application.student_id)
        )
        student_profile = student_profile_result.scalar_one_or_none()
        
        if not student_profile:
            continue
        
        # 获取职位信息
        job_result = await db.execute(select(Job).where(Job.id == application.job_id))
        job = job_result.scalar_one_or_none()
        if not job:
            continue
        
        # 获取企业ID
        enterprise_id = job.enterprise_id
        
        offer = Offer(
            id=str(uuid4()),
            application_id=application.id,
            enterprise_id=enterprise_id,
            student_id=student_profile.id,
            job_title=job.title,
            salary=random.choice([8000, 10000, 15000, 20000, 25000]),
            start_date=datetime.now() + timedelta(days=random.randint(30, 90)),
            content=f"恭喜您获得{job.title}职位的Offer，期待您的加入！",
            status=random.choice(["PENDING", "ACCEPTED", "REJECTED", "EXPIRED"]),
            expires_at=datetime.now() + timedelta(days=random.randint(7, 30)) if i % 2 == 0 else None
        )
        offers.append(offer)
        db.add(offer)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(offers)} 个Offer")
    return offers


async def create_feedbacks(db: AsyncSession, count: int = 50):
    """创建反馈数据"""
    # 检查是否为空
    if not await check_table_empty(db, Feedback):
        print("[SKIP] feedbacks 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个反馈...")
    
    # 获取用户
    users_result = await db.execute(select(User))
    users = list(users_result.scalars().all())
    
    if not users:
        print("[SKIP] 没有用户，跳过创建反馈")
        return []
    
    feedbacks = []
    for i in range(count):
        user = random.choice(users)
        
        feedback = Feedback(
            id=str(uuid4()),
            user_id=user.id,
            user_type=user.user_type.value,
            title=random.choice([
                "系统使用问题",
                "功能建议",
                "BUG反馈",
                "界面优化建议",
                "其他问题"
            ]),
            content=random.choice([
                "希望增加更多筛选条件",
                "页面加载速度较慢",
                "建议优化用户体验",
                "发现了一个小问题",
                "整体使用体验很好"
            ]),
            status=random.choice(["PENDING", "PROCESSING", "RESOLVED", "CLOSED"]),
            reply=random.choice([None, "感谢您的反馈，我们会尽快处理", "问题已解决"]) if i % 2 == 0 else None,
            replied_at=datetime.now() - timedelta(days=random.randint(0, 10)) if i % 2 == 0 else None
        )
        feedbacks.append(feedback)
        db.add(feedback)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(feedbacks)} 个反馈")
    return feedbacks


async def create_rights(db: AsyncSession, count: int = 50):
    """创建权益数据"""
    # 检查是否为空
    if not await check_table_empty(db, Rights):
        print("[SKIP] rights 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个权益...")
    
    rights_types = ["JOB_POST", "RESUME_VIEW", "TALENT_SEARCH", "PREMIUM_BADGE", "PRIORITY_DISPLAY"]
    rights_list = []
    rights_names = [
        "发布职位权益", "查看简历权益", "人才搜索权益", "VIP标识权益", "优先展示权益",
        "高级搜索权益", "批量操作权益", "数据导出权益", "定制化服务权益", "专属客服权益"
    ]
    
    for i in range(count):
        # 确保名称唯一
        name = f"{rights_names[i % len(rights_names)]}{i+1}"
        code = f"RIGHT{random.randint(10000, 99999)}"
        
        # 检查code是否已存在
        existing_code = await db.execute(select(Rights).where(Rights.code == code))
        if existing_code.scalar_one_or_none():
            code = f"RIGHT{random.randint(100000, 999999)}"
        
        right = Rights(
            id=str(uuid4()),
            name=name,
            code=code,
            description=f"权益描述{i+1}",
            type=random.choice(rights_types),
            value=random.randint(1, 100),
            is_active=random.choice([True, False])
        )
        rights_list.append(right)
        db.add(right)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(rights_list)} 个权益")
    return rights_list


async def create_rights_packages(db: AsyncSession, rights: list, count: int = 50):
    """创建权益套餐数据"""
    # 检查是否为空
    if not await check_table_empty(db, RightsPackage):
        print("[SKIP] rights_packages 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个权益套餐...")
    
    packages = []
    package_names = ["基础套餐", "标准套餐", "高级套餐", "企业套餐", "VIP套餐"]
    
    for i in range(count):
        # 确保名称唯一
        name = f"{package_names[i % len(package_names)]}{i+1}"
        
        # 检查名称是否已存在（使用循环确保唯一）
        max_attempts = 10
        for attempt in range(max_attempts):
            existing_name = await db.execute(select(RightsPackage).where(RightsPackage.name == name))
            if not existing_name.scalar_one_or_none():
                break
            name = f"{package_names[i % len(package_names)]}{i+1}-{random.randint(100, 999)}"
        
        package = RightsPackage(
            id=str(uuid4()),
            name=name,
            description=f"套餐描述{i+1}",
            price=random.choice([99.00, 199.00, 299.00, 499.00, 999.00]),
            duration_days=random.choice([30, 60, 90, 180, 365]),
            is_active=random.choice([True, False])
        )
        packages.append(package)
        db.add(package)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(packages)} 个权益套餐")
    return packages


async def create_rights_package_items(db: AsyncSession, packages: list, rights: list, count: int = 100):
    """创建权益套餐项数据"""
    # 检查是否为空
    if not await check_table_empty(db, RightsPackageItem):
        print("[SKIP] rights_package_items 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个权益套餐项...")
    
    if not packages or not rights:
        print("[SKIP] 没有权益套餐或权益，跳过创建套餐项")
        return []
    
    items = []
    for i in range(count):
        package = random.choice(packages)
        right = random.choice(rights)
        
        # 检查是否已存在
        existing = await db.execute(
            select(RightsPackageItem).where(
                RightsPackageItem.package_id == package.id,
                RightsPackageItem.rights_id == right.id
            )
        )
        if existing.scalar_one_or_none():
            continue
        
        item = RightsPackageItem(
            id=str(uuid4()),
            package_id=package.id,
            rights_id=right.id,
            quantity=random.randint(1, 10)
        )
        items.append(item)
        db.add(item)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(items)} 个权益套餐项")
    return items


async def create_user_rights(db: AsyncSession, users: list, rights: list, count: int = 50):
    """创建用户权益数据"""
    # 检查是否为空
    if not await check_table_empty(db, UserRights):
        print("[SKIP] user_rights 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个用户权益...")
    
    # 如果传入的列表为空，从数据库获取
    if not users:
        users_result = await db.execute(select(User))
        users = list(users_result.scalars().all())
    
    if not rights:
        rights_result = await db.execute(select(Rights))
        rights = list(rights_result.scalars().all())
    
    if not users or not rights:
        print("[SKIP] 没有用户或权益，跳过创建用户权益")
        return []
    
    user_rights_list = []
    for i in range(count):
        user = random.choice(users)
        right = random.choice(rights)
        
        # 检查是否已存在
        existing = await db.execute(
            select(UserRights).where(
                UserRights.user_id == user.id,
                UserRights.rights_id == right.id
            )
        )
        if existing.scalar_one_or_none():
            continue
        
        user_right = UserRights(
            id=str(uuid4()),
            user_id=user.id,
            rights_id=right.id,
            quantity=random.randint(1, 100),
            expires_at=datetime.now() + timedelta(days=random.randint(30, 365)) if i % 2 == 0 else None
        )
        user_rights_list.append(user_right)
        db.add(user_right)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(user_rights_list)} 个用户权益")
    return user_rights_list


async def create_rights_purchases(db: AsyncSession, users: list, packages: list, count: int = 50):
    """创建权益购买数据"""
    # 检查是否为空
    if not await check_table_empty(db, RightsPurchase):
        print("[SKIP] rights_purchases 表已有数据，跳过")
        return []
    
    print(f"创建 {count} 个权益购买...")
    
    # 如果传入的列表为空，从数据库获取
    if not users:
        users_result = await db.execute(select(User))
        users = list(users_result.scalars().all())
    
    if not packages:
        packages_result = await db.execute(select(RightsPackage))
        packages = list(packages_result.scalars().all())
    
    if not users or not packages:
        print("[SKIP] 没有用户或权益套餐，跳过创建购买记录")
        return []
    
    # 预先获取所有套餐的价格
    package_prices = {}
    for package in packages:
        package_prices[package.id] = float(package.price) if hasattr(package.price, '__float__') else float(str(package.price))
    
    purchases = []
    for i in range(count):
        user = random.choice(users)
        package = random.choice(packages)
        
        purchase = RightsPurchase(
            id=str(uuid4()),
            user_id=user.id,
            package_id=package.id,
            amount=package_prices.get(package.id, 99.00),
            status=random.choice(["PENDING", "PAID", "CANCELLED", "REFUNDED"])
        )
        purchases.append(purchase)
        db.add(purchase)
    
    await db.commit()
    print(f"[OK] 成功创建 {len(purchases)} 个权益购买")
    return purchases


async def main():
    """主函数"""
    print("=" * 60)
    print("开始填充空表数据...")
    print("=" * 60)
    
    async with AsyncSession(engine) as db:
        try:
            # 1. 创建求职意向
            job_intentions = await create_job_intentions(db, count=50)
            
            # 2. 创建双选会报名
            job_fair_registrations = await create_job_fair_registrations(db, count=50)
            
            # 3. 创建宣讲会报名
            info_session_registrations = await create_info_session_registrations(db, count=50)
            
            # 4. 创建Offer
            offers = await create_offers(db, count=50)
            
            # 5. 创建反馈
            feedbacks = await create_feedbacks(db, count=50)
            
            # 6. 创建权益相关数据（需要按顺序创建）
            rights = await create_rights(db, count=50)
            
            # 获取用户列表（用于后续创建）
            users_result = await db.execute(select(User))
            users = list(users_result.scalars().all())
            
            # 获取权益列表（如果刚创建的为空，则从数据库获取）
            if not rights:
                rights_result = await db.execute(select(Rights))
                rights = list(rights_result.scalars().all())
            
            rights_packages = await create_rights_packages(db, rights, count=50)
            
            # 获取权益套餐列表（如果刚创建的为空，则从数据库获取）
            if not rights_packages:
                packages_result = await db.execute(select(RightsPackage))
                rights_packages = list(packages_result.scalars().all())
            
            rights_package_items = await create_rights_package_items(db, rights_packages, rights, count=100)
            user_rights = await create_user_rights(db, users, rights, count=50)
            rights_purchases = await create_rights_purchases(db, users, rights_packages, count=50)
            
            print("=" * 60)
            print("数据填充完成！")
            print("=" * 60)
            print(f"总计创建：")
            print(f"  - 求职意向: {len(job_intentions)}")
            print(f"  - 双选会报名: {len(job_fair_registrations)}")
            print(f"  - 宣讲会报名: {len(info_session_registrations)}")
            print(f"  - Offer: {len(offers)}")
            print(f"  - 反馈: {len(feedbacks)}")
            print(f"  - 权益: {len(rights)}")
            print(f"  - 权益套餐: {len(rights_packages)}")
            print(f"  - 权益套餐项: {len(rights_package_items)}")
            print(f"  - 用户权益: {len(user_rights)}")
            print(f"  - 权益购买: {len(rights_purchases)}")
            print("=" * 60)
            
        except Exception as e:
            print(f"错误：{e}")
            import traceback
            traceback.print_exc()
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())

