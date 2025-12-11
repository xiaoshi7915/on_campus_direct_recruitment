"""
检查所有模型和数据库表的一致性
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
    """检查所有模型和数据库表的一致性"""
    async with engine.connect() as conn:
        # 获取所有已定义的表名
        inspector = inspect(engine.sync_engine)
        db_tables = set(inspector.get_table_names())
        
        # 获取所有模型定义的表名
        model_tables = set(Base.metadata.tables.keys())
        
        print("=" * 80)
        print("数据库表一致性检查")
        print("=" * 80)
        
        print(f"\n数据库中的表数量: {len(db_tables)}")
        print(f"模型定义的表数量: {len(model_tables)}")
        
        # 检查数据库中有但模型中没有的表
        only_in_db = db_tables - model_tables
        if only_in_db:
            print(f"\n⚠️  仅在数据库中的表: {only_in_db}")
        else:
            print("\n✓ 所有数据库表都有对应的模型")
        
        # 检查模型中有但数据库中没有的表
        only_in_model = model_tables - db_tables
        if only_in_model:
            print(f"\n⚠️  仅在模型中的表: {only_in_model}")
        else:
            print("\n✓ 所有模型都有对应的数据库表")
        
        # 检查每个表的字段
        print("\n" + "=" * 80)
        print("检查关键表的字段:")
        print("=" * 80)
        
        key_tables = ['info_sessions', 'job_fairs', 'users', 'enterprise_profiles', 
                     'student_profiles', 'jobs', 'resumes', 'job_applications']
        
        for table_name in key_tables:
            if table_name in db_tables:
                result = await conn.execute(text(f"DESCRIBE {table_name}"))
                rows = result.fetchall()
                columns = [row[0] for row in rows]
                
                # 检查模型定义的字段
                if table_name in model_tables:
                    table = Base.metadata.tables[table_name]
                    model_columns = set(table.columns.keys())
                    db_columns = set(columns)
                    
                    missing_in_db = model_columns - db_columns
                    extra_in_db = db_columns - model_columns
                    
                    if missing_in_db:
                        print(f"\n⚠️  {table_name}: 模型中有但数据库中没有的字段: {missing_in_db}")
                    elif extra_in_db:
                        print(f"\n⚠️  {table_name}: 数据库中有但模型中没有的字段: {extra_in_db}")
                    else:
                        print(f"\n✓ {table_name}: 字段一致")
        
        await conn.commit()
        
        print("\n" + "=" * 80)
        print("检查完成")
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(check_all_tables())

