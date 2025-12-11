"""
检查所有数据库表是否存在
"""
import asyncio
from sqlalchemy import text, inspect
from app.core.database import engine, Base
# 导入所有模型
from app.models.user import User
from app.models.school import School, Department, Class
from app.models.profile import StudentProfile, TeacherProfile, EnterpriseProfile
from app.models.job import Resume, Job, JobIntention, JobApplication
from app.models.activity import JobFair, JobFairRegistration, InfoSession, InfoSessionRegistration
from app.models.interview import Interview, Offer
from app.models.chat import ChatSession, Message
from app.models.common import Favorite, Schedule, Feedback
from app.models.todo import Todo
from app.models.mark import Mark
from app.models.rights import Rights, RightsPackage, RightsPackageItem, UserRights, RightsPurchase


async def check_all_tables():
    """检查所有模型对应的数据库表是否存在"""
    async with engine.connect() as conn:
        # 获取所有已定义的表名
        inspector = inspect(engine.sync_engine)
        db_tables = set(inspector.get_table_names())
        
        # 获取所有模型定义的表名
        model_tables = set(Base.metadata.tables.keys())
        
        print("=" * 80)
        print("数据库表存在性检查")
        print("=" * 80)
        
        print(f"\n数据库中的表数量: {len(db_tables)}")
        print(f"模型定义的表数量: {len(model_tables)}")
        
        # 检查模型中有但数据库中没有的表
        missing_tables = model_tables - db_tables
        if missing_tables:
            print(f"\n⚠️  模型中有但数据库中没有的表 ({len(missing_tables)}个):")
            for table in sorted(missing_tables):
                print(f"  - {table}")
        else:
            print("\n✓ 所有模型都有对应的数据库表")
        
        # 检查数据库中有但模型中没有的表
        extra_tables = db_tables - model_tables
        if extra_tables:
            print(f"\n⚠️  数据库中有但模型中没有的表 ({len(extra_tables)}个):")
            for table in sorted(extra_tables):
                print(f"  - {table}")
        
        # 列出所有关键表
        print("\n" + "=" * 80)
        print("关键表检查:")
        print("=" * 80)
        key_tables = [
            'users', 'enterprise_profiles', 'student_profiles', 'teacher_profiles',
            'jobs', 'resumes', 'job_applications',
            'info_sessions', 'job_fairs',
            'interviews', 'offers',
            'chat_sessions', 'messages',
            'favorites', 'schedules', 'feedback'
        ]
        
        for table_name in key_tables:
            if table_name in db_tables:
                print(f"✓ {table_name}")
            else:
                print(f"✗ {table_name} - 缺失")
        
        await conn.commit()
        
        print("\n" + "=" * 80)
        print("检查完成")
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(check_all_tables())

