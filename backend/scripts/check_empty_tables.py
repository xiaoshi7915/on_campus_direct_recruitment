"""
检查数据库中哪些表是空的
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from app.models import (
    User, School, Department, Class,
    StudentProfile, TeacherProfile, EnterpriseProfile,
    Job, Resume, JobIntention, JobApplication,
    JobFair, JobFairRegistration, InfoSession, InfoSessionRegistration,
    Interview, Offer,
    ChatSession, Message,
    Schedule, Favorite, Feedback,
    Rights, RightsPackage, RightsPackageItem, UserRights, RightsPurchase
)

# 所有表的映射
TABLES = {
    "users": User,
    "schools": School,
    "departments": Department,
    "classes": Class,
    "student_profiles": StudentProfile,
    "teacher_profiles": TeacherProfile,
    "enterprise_profiles": EnterpriseProfile,
    "jobs": Job,
    "resumes": Resume,
    "job_intentions": JobIntention,
    "job_applications": JobApplication,
    "job_fairs": JobFair,
    "job_fair_registrations": JobFairRegistration,
    "info_sessions": InfoSession,
    "info_session_registrations": InfoSessionRegistration,
    "interviews": Interview,
    "offers": Offer,
    "chat_sessions": ChatSession,
    "messages": Message,
    "schedules": Schedule,
    "favorites": Favorite,
    "feedbacks": Feedback,
    "rights": Rights,
    "rights_packages": RightsPackage,
    "rights_package_items": RightsPackageItem,
    "user_rights": UserRights,
    "rights_purchases": RightsPurchase,
}


async def check_table_count(db: AsyncSession, model, table_name: str):
    """检查表的记录数"""
    try:
        result = await db.execute(select(func.count()).select_from(model))
        count = result.scalar() or 0
        return count
    except Exception as e:
        print(f"检查表 {table_name} 时出错: {e}")
        return -1


async def main():
    """主函数"""
    print("=" * 60)
    print("检查数据库表数据情况...")
    print("=" * 60)
    
    empty_tables = []
    non_empty_tables = []
    
    async with AsyncSession(engine) as db:
        for table_name, model in TABLES.items():
            count = await check_table_count(db, model, table_name)
            if count == 0:
                empty_tables.append(table_name)
                print(f"[空] {table_name}: {count} 条记录")
            elif count > 0:
                non_empty_tables.append((table_name, count))
                print(f"[有数据] {table_name}: {count} 条记录")
            else:
                print(f"[错误] {table_name}: 无法检查")
    
    print("\n" + "=" * 60)
    print("汇总结果")
    print("=" * 60)
    print(f"有数据的表: {len(non_empty_tables)} 个")
    print(f"空表: {len(empty_tables)} 个")
    
    if empty_tables:
        print("\n需要填充数据的表:")
        for table in empty_tables:
            print(f"  - {table}")
    else:
        print("\n所有表都有数据！")
    
    print("=" * 60)
    
    return empty_tables


if __name__ == "__main__":
    empty_tables = asyncio.run(main())


