"""
为指定教师添加管辖学生数据
"""
import sys
import asyncio
from uuid import uuid4

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.core.config import settings
from app.models.user import User
from app.models.profile import TeacherProfile, StudentProfile
from app.models.school import School, Department, Class
from app.models.user_type import UserType

# 创建数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

# 创建异步会话
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def add_students_for_teacher(teacher_name: str = "陈中和", student_count: int = 20):
    """
    为指定教师添加管辖学生数据
    
    Args:
        teacher_name: 教师姓名
        student_count: 要添加的学生数量
    """
    async with AsyncSessionLocal() as db:
        try:
            # 1. 查找教师
            print(f"正在查找教师：{teacher_name}...")
            teacher_profile_result = await db.execute(
                select(TeacherProfile).join(User).where(TeacherProfile.real_name == teacher_name)
            )
            teacher_profile = teacher_profile_result.scalar_one_or_none()
            
            if not teacher_profile:
                print(f"❌ 未找到姓名为 '{teacher_name}' 的教师")
                return
            
            print(f"✅ 找到教师：{teacher_profile.real_name} (ID: {teacher_profile.id})")
            print(f"   学校ID: {teacher_profile.school_id}")
            print(f"   院系ID: {teacher_profile.department_id}")
            
            # 2. 获取教师的学校和院系信息
            school_id = teacher_profile.school_id
            department_id = teacher_profile.department_id
            
            if not school_id and not department_id:
                print("❌ 该教师没有关联学校或院系，无法添加管辖学生")
                return
            
            # 3. 查找该教师管辖范围内的现有学生
            student_query = select(StudentProfile)
            if department_id:
                student_query = student_query.where(StudentProfile.department_id == department_id)
            elif school_id:
                student_query = student_query.where(StudentProfile.school_id == school_id)
            
            existing_students_result = await db.execute(student_query)
            existing_students = existing_students_result.scalars().all()
            existing_count = len(existing_students)
            
            print(f"   当前管辖学生数：{existing_count}")
            
            # 4. 如果需要添加更多学生，查找可用的班级
            if existing_count < student_count:
                need_count = student_count - existing_count
                print(f"   需要添加 {need_count} 个学生...")
                
                # 查找该教师管辖范围内的班级
                class_query = select(Class)
                if department_id:
                    # 查找该院系的班级
                    dept_result = await db.execute(select(Department).where(Department.id == department_id))
                    dept = dept_result.scalar_one_or_none()
                    if dept:
                        class_query = class_query.where(Class.department_id == department_id)
                elif school_id:
                    # 查找该学校的班级
                    dept_ids_result = await db.execute(
                        select(Department.id).where(Department.school_id == school_id)
                    )
                    dept_ids = [row[0] for row in dept_ids_result.all()]
                    if dept_ids:
                        class_query = class_query.where(Class.department_id.in_(dept_ids))
                
                classes_result = await db.execute(class_query)
                classes = classes_result.scalars().all()
                
                if not classes:
                    print("❌ 未找到可用的班级，无法添加学生")
                    return
                
                # 获取学校ID（如果班级有部门，从部门获取）
                if not school_id and classes:
                    first_class = classes[0]
                    dept_result = await db.execute(
                        select(Department).where(Department.id == first_class.department_id)
                    )
                    dept = dept_result.scalar_one_or_none()
                    if dept:
                        school_id = dept.school_id
                        department_id = dept.id
                
                # 5. 创建新学生用户和档案
                chinese_names = [
                    "张伟", "王芳", "李娜", "刘强", "陈静", "杨洋", "黄磊", "周杰", "吴敏", "徐涛",
                    "朱琳", "马超", "胡军", "林峰", "罗敏", "高强", "梁静", "何伟", "韩梅", "唐勇",
                    "冯丽", "于洋", "董明", "余静", "叶军", "程丽", "苏强", "魏敏", "薛涛", "姜静"
                ]
                
                created_count = 0
                for i in range(need_count):
                    # 创建用户
                    username = f"student_{uuid4().hex[:8]}"
                    user = User(
                        id=str(uuid4()),
                        username=username,
                        password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5Y",  # 默认密码：password
                        user_type=UserType.STUDENT,
                        status="ACTIVE"
                    )
                    db.add(user)
                    await db.flush()
                    
                    # 选择班级
                    selected_class = classes[i % len(classes)]
                    
                    # 创建学生档案
                    student_profile = StudentProfile(
                        id=str(uuid4()),
                        user_id=user.id,
                        real_name=chinese_names[i % len(chinese_names)] + f"_{i+1}",
                        student_id=f"STU{2024000000 + existing_count + i + 1}",
                        school_id=school_id,
                        department_id=selected_class.department_id,
                        class_id=selected_class.id,
                        grade="2024",
                        major="计算机科学与技术"
                    )
                    db.add(student_profile)
                    created_count += 1
                
                await db.commit()
                print(f"✅ 成功添加 {created_count} 个学生")
            else:
                print(f"✅ 该教师已有 {existing_count} 个管辖学生，已达到或超过目标数量 {student_count}")
            
            # 6. 统计最终结果
            final_students_result = await db.execute(student_query)
            final_students = final_students_result.scalars().all()
            final_count = len(final_students)
            
            print(f"\n📊 最终统计：")
            print(f"   教师：{teacher_profile.real_name}")
            if teacher_profile.school_id:
                school_result = await db.execute(select(School).where(School.id == teacher_profile.school_id))
                school = school_result.scalar_one_or_none()
                if school:
                    print(f"   学校：{school.name}")
            if teacher_profile.department_id:
                dept_result = await db.execute(select(Department).where(Department.id == teacher_profile.department_id))
                dept = dept_result.scalar_one_or_none()
                if dept:
                    print(f"   院系：{dept.name}")
            print(f"   管辖学生总数：{final_count}")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 错误：{str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()


async def main():
    """主函数"""
    print("=" * 60)
    print("为教师添加管辖学生数据")
    print("=" * 60)
    
    # 为陈中和老师添加20个学生
    await add_students_for_teacher("陈中和", 20)
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

