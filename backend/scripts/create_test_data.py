"""
创建测试数据脚本
用于测试审批流程和教师管理功能
"""
import sys
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.profile import TeacherProfile, EnterpriseProfile
from app.models.school import School, Department
from app.models.activity import JobFair, InfoSession
from app.models.user_type import UserType

# 配置数据库连接
DATABASE_URL = settings.DATABASE_URL.replace("mysql+pymysql", "mysql+aiomysql")
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_test_data():
    """创建测试数据"""
    async with AsyncSessionLocal() as db:
        try:
            print("=" * 60)
            print("开始创建测试数据")
            print("=" * 60)
            
            # 1. 创建测试学校
            print("\n1. 创建测试学校...")
            school_result = await db.execute(
                select(School).where(School.name == "测试大学")
            )
            school = school_result.scalar_one_or_none()
            
            if not school:
                school = School(
                    id=str(uuid4()),
                    name="测试大学",
                    code="TEST001",
                    province="山西省",
                    city="太原市",
                    address="测试地址123号",
                    is_verified=True
                )
                db.add(school)
                await db.flush()
                print(f"✅ 创建学校: {school.name} (ID: {school.id})")
            else:
                print(f"✅ 学校已存在: {school.name} (ID: {school.id})")
            
            # 2. 创建测试院系
            print("\n2. 创建测试院系...")
            dept_result = await db.execute(
                select(Department).where(
                    Department.name == "计算机科学与技术",
                    Department.school_id == school.id
                )
            )
            department = dept_result.scalar_one_or_none()
            
            if not department:
                department = Department(
                    id=str(uuid4()),
                    school_id=school.id,
                    name="计算机科学与技术",
                    code="CS001",
                    description="计算机科学与技术专业",
                    honors="国家级重点学科"
                )
                db.add(department)
                await db.flush()
                print(f"✅ 创建院系: {department.name} (ID: {department.id})")
            else:
                print(f"✅ 院系已存在: {department.name} (ID: {department.id})")
            
            # 3. 创建主账号教师
            print("\n3. 创建主账号教师...")
            main_teacher_user_result = await db.execute(
                select(User).where(User.username == "main_teacher")
            )
            main_teacher_user = main_teacher_user_result.scalar_one_or_none()
            
            if not main_teacher_user:
                main_teacher_user = User(
                    id=str(uuid4()),
                    username="main_teacher",
                    password_hash=get_password_hash("teacher123"),
                    phone="13800000001",
                    email="main_teacher@test.edu",
                    user_type=UserType.TEACHER,
                    status="ACTIVE"
                )
                db.add(main_teacher_user)
                await db.flush()
                
                main_teacher_profile = TeacherProfile(
                    id=str(uuid4()),
                    user_id=main_teacher_user.id,
                    real_name="主账号教师",
                    school_id=school.id,
                    department_id=department.id,
                    title="教授",
                    position="系主任",
                    is_main_account=True
                )
                db.add(main_teacher_profile)
                await db.flush()
                print(f"✅ 创建主账号教师: {main_teacher_user.username} (ID: {main_teacher_profile.id})")
            else:
                print(f"✅ 主账号教师已存在: {main_teacher_user.username}")
            
            # 4. 创建待审批教师
            print("\n4. 创建待审批教师...")
            pending_teacher_user_result = await db.execute(
                select(User).where(User.username == "pending_teacher")
            )
            pending_teacher_user = pending_teacher_user_result.scalar_one_or_none()
            
            if not pending_teacher_user:
                pending_teacher_user = User(
                    id=str(uuid4()),
                    username="pending_teacher",
                    password_hash=get_password_hash("teacher123"),
                    phone="13800000002",
                    email="pending_teacher@test.edu",
                    user_type=UserType.TEACHER,
                    status="PENDING"  # 待审批状态
                )
                db.add(pending_teacher_user)
                await db.flush()
                
                pending_teacher_profile = TeacherProfile(
                    id=str(uuid4()),
                    user_id=pending_teacher_user.id,
                    real_name="待审批教师",
                    school_id=school.id,
                    department_id=department.id,
                    title="讲师",
                    is_main_account=False
                )
                db.add(pending_teacher_profile)
                await db.flush()
                print(f"✅ 创建待审批教师: {pending_teacher_user.username} (ID: {pending_teacher_profile.id})")
            else:
                print(f"✅ 待审批教师已存在: {pending_teacher_user.username}")
            
            # 5. 创建测试企业
            print("\n5. 创建测试企业...")
            enterprise_user_result = await db.execute(
                select(User).where(User.username == "test_enterprise")
            )
            enterprise_user = enterprise_user_result.scalar_one_or_none()
            
            if not enterprise_user:
                enterprise_user = User(
                    id=str(uuid4()),
                    username="test_enterprise",
                    password_hash=get_password_hash("enterprise123"),
                    phone="13800000003",
                    email="test@enterprise.com",
                    user_type=UserType.ENTERPRISE,
                    status="ACTIVE"
                )
                db.add(enterprise_user)
                await db.flush()
                
                enterprise_profile = EnterpriseProfile(
                    id=str(uuid4()),
                    user_id=enterprise_user.id,
                    company_name="测试企业有限公司",
                    industry="互联网",
                    address="企业地址123号"
                )
                db.add(enterprise_profile)
                await db.flush()
                print(f"✅ 创建企业: {enterprise_user.username} (ID: {enterprise_profile.id})")
            else:
                print(f"✅ 企业已存在: {enterprise_user.username}")
            
            # 6. 创建待审批的双选会
            print("\n6. 创建待审批的双选会...")
            start_time = datetime.now() + timedelta(days=7)
            end_time = start_time + timedelta(hours=8)
            
            pending_job_fair = JobFair(
                id=str(uuid4()),
                school_id=school.id,
                title="2025年春季校园双选会（待审批）",
                description="测试待审批的双选会",
                start_time=start_time,
                end_time=end_time,
                location="学校体育馆",
                max_enterprises=50,
                status="PENDING"  # 待审批状态
            )
            db.add(pending_job_fair)
            await db.flush()
            print(f"✅ 创建待审批双选会: {pending_job_fair.title} (ID: {pending_job_fair.id})")
            
            # 7. 创建待审批的宣讲会
            print("\n7. 创建待审批的宣讲会...")
            session_start = datetime.now() + timedelta(days=5)
            session_end = session_start + timedelta(hours=2)
            
            enterprise_result = await db.execute(
                select(EnterpriseProfile).where(EnterpriseProfile.user_id == enterprise_user.id)
            )
            enterprise = enterprise_result.scalar_one_or_none()
            
            if enterprise:
                pending_info_session = InfoSession(
                    id=str(uuid4()),
                    enterprise_id=enterprise.id,
                    school_id=school.id,
                    title="测试企业2025年校园宣讲会（待审批）",
                    description="测试待审批的宣讲会",
                    start_time=session_start,
                    end_time=session_end,
                    location="学校报告厅",
                    session_type="OFFLINE",
                    max_students=200,
                    status="PENDING"  # 待审批状态
                )
                db.add(pending_info_session)
                await db.flush()
                print(f"✅ 创建待审批宣讲会: {pending_info_session.title} (ID: {pending_info_session.id})")
            
            await db.commit()
            
            print("\n" + "=" * 60)
            print("测试数据创建完成！")
            print("=" * 60)
            print("\n测试账号信息：")
            print("- 主账号教师: main_teacher / teacher123")
            print("- 待审批教师: pending_teacher / teacher123")
            print("- 测试企业: test_enterprise / enterprise123")
            print("\n可以测试的功能：")
            print("1. 教师审批功能（管理员登录后审批 pending_teacher）")
            print("2. 双选会/宣讲会审批功能（教师或管理员审批）")
            print("3. 子账号管理功能（主账号教师登录后创建子账号）")
            
        except Exception as e:
            await db.rollback()
            print(f"\n❌ 创建测试数据失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_test_data())

