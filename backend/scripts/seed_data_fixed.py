"""
数据库数据填充脚本（修复版）
为每个表添加至少50条测试数据
避免异步加载问题
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4
import random

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.user_type import UserType
from app.models.school import School, Department, Class
from app.models.profile import StudentProfile, TeacherProfile, EnterpriseProfile
from app.models.job import Job, Resume, JobApplication
from app.models.activity import JobFair, InfoSession
from app.models.interview import Interview
from app.models.chat import ChatSession, Message
from app.models.common import Schedule, Favorite
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, delete, text
from sqlalchemy.orm import sessionmaker

# 中文姓名库
CHINESE_NAMES = [
    "张伟", "王芳", "李娜", "刘强", "陈静", "杨洋", "赵敏", "黄磊", "周杰", "吴秀波",
    "徐静", "孙丽", "马超", "朱军", "胡歌", "林志玲", "郭德纲", "何炅", "罗志祥", "高圆圆",
    "范冰冰", "章子怡", "成龙", "李连杰", "周星驰", "刘德华", "张学友", "黎明", "郭富城", "梁朝伟",
    "张曼玉", "王菲", "林青霞", "巩俐", "赵薇", "周迅", "范冰冰", "李冰冰", "章子怡", "汤唯",
    "陈道明", "葛优", "姜文", "张国立", "陈宝国", "唐国强", "李雪健", "王志文", "陈建斌", "张嘉译"
] * 2

# 公司名称库
COMPANY_NAMES = [
    "阿里巴巴", "腾讯科技", "百度", "京东", "美团", "字节跳动", "滴滴出行", "小米科技", "华为技术", "中兴通讯",
    "网易", "新浪", "搜狐", "360", "携程", "拼多多", "快手", "抖音", "小红书", "B站",
    "爱奇艺", "优酷", "腾讯视频", "芒果TV", "哔哩哔哩", "知乎", "豆瓣", "虎扑", "脉脉", "拉勾网",
    "BOSS直聘", "智联招聘", "前程无忧", "猎聘", "58同城", "赶集网", "百姓网", "安居客", "链家", "贝壳找房",
    "顺丰速运", "中通快递", "圆通速递", "申通快递", "韵达快递", "德邦物流", "京东物流", "菜鸟网络", "苏宁易购", "国美电器"
] * 2

# 学校名称库
SCHOOL_NAMES = [
    "北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学", "南京大学", "中国科学技术大学", "华中科技大学", "中山大学", "四川大学",
    "北京师范大学", "华东师范大学", "东北师范大学", "华中师范大学", "陕西师范大学", "西南大学", "华南师范大学", "南京师范大学", "湖南师范大学", "首都师范大学",
    "北京理工大学", "大连理工大学", "华南理工大学", "华东理工大学", "南京理工大学", "武汉理工大学", "太原理工大学", "昆明理工大学", "西安理工大学", "长沙理工大学",
    "北京航空航天大学", "南京航空航天大学", "西北工业大学", "哈尔滨工业大学", "北京科技大学", "上海大学", "苏州大学", "郑州大学", "云南大学", "新疆大学",
    "中央财经大学", "上海财经大学", "对外经济贸易大学", "西南财经大学", "中南财经政法大学", "东北财经大学", "江西财经大学", "首都经济贸易大学", "天津财经大学", "南京财经大学"
] * 2

# 院系名称库
DEPARTMENT_NAMES = [
    "计算机科学与技术", "软件工程", "信息管理与信息系统", "数据科学与大数据技术", "人工智能", "网络工程", "信息安全", "物联网工程", "数字媒体技术", "电子信息工程",
    "通信工程", "自动化", "电气工程及其自动化", "机械工程", "材料科学与工程", "化学工程与工艺", "生物工程", "环境工程", "土木工程", "建筑学",
    "工商管理", "市场营销", "会计学", "财务管理", "人力资源管理", "旅游管理", "物流管理", "电子商务", "国际经济与贸易", "金融学",
    "经济学", "统计学", "数学与应用数学", "物理学", "化学", "生物科学", "英语", "日语", "德语", "法语",
    "汉语言文学", "新闻学", "广告学", "广播电视学", "法学", "社会学", "心理学", "教育学", "体育教育", "艺术设计"
] * 2

# 职位标题库
JOB_TITLES = [
    "Java开发工程师", "Python开发工程师", "前端开发工程师", "后端开发工程师", "全栈开发工程师", "iOS开发工程师", "Android开发工程师", "算法工程师", "数据工程师", "测试工程师",
    "产品经理", "UI设计师", "UX设计师", "运营专员", "市场专员", "销售专员", "客户经理", "商务拓展", "人力资源专员", "财务专员",
    "数据分析师", "商业分析师", "项目经理", "技术经理", "架构师", "系统架构师", "运维工程师", "安全工程师", "网络工程师", "数据库管理员",
    "内容运营", "用户运营", "活动运营", "新媒体运营", "社群运营", "电商运营", "直播运营", "短视频运营", "品牌运营", "渠道运营",
    "会计", "出纳", "审计", "税务", "投资经理", "风控专员", "合规专员", "法务专员", "行政专员", "文秘"
] * 2

# 职位描述模板
JOB_DESCRIPTION_TEMPLATE = """
岗位职责：
1. 负责{title}相关工作的开展
2. 参与项目需求分析和技术方案设计
3. 完成代码开发和测试工作
4. 配合团队完成项目交付

任职要求：
1. 本科及以上学历，{major}相关专业优先
2. 具备良好的沟通能力和团队协作精神
3. 有相关工作经验者优先
4. 工作认真负责，学习能力强
"""


async def clear_tables(db: AsyncSession):
    """清空所有表的数据（按依赖顺序）"""
    print("清空现有数据...")
    try:
        # 按依赖顺序删除
        await db.execute(delete(Message))
        await db.execute(delete(ChatSession))
        await db.execute(delete(Favorite))
        await db.execute(delete(Schedule))
        await db.execute(delete(Interview))
        await db.execute(delete(JobApplication))
        await db.execute(delete(Resume))
        await db.execute(delete(Job))
        await db.execute(delete(InfoSession))
        await db.execute(delete(JobFair))
        await db.execute(delete(StudentProfile))
        await db.execute(delete(TeacherProfile))
        await db.execute(delete(EnterpriseProfile))
        await db.execute(delete(Class))
        await db.execute(delete(Department))
        await db.execute(delete(School))
        await db.execute(delete(User))
        await db.commit()
        print("[OK] 数据清空完成")
    except Exception as e:
        print(f"[WARN] 清空数据时出错（可能表不存在）: {e}")
        await db.rollback()


async def create_schools(db: AsyncSession, count: int = 50):
    """创建学校数据"""
    print(f"创建 {count} 所学校...")
    schools = []
    for i in range(count):
        school = School(
            id=str(uuid4()),
            name=random.choice(SCHOOL_NAMES) + (f"（{i+1}校区）" if i > 0 else ""),
            code=f"SCH{random.randint(10000, 99999)}",
            province=random.choice(["北京", "上海", "广东", "江苏", "浙江", "四川", "湖北", "湖南", "山东", "河南"]),
            city=random.choice(["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "长沙", "济南", "郑州"]),
            address=f"{random.choice(['大学城', '科技园', '教育园区'])}第{i+1}号",
            website=f"https://www.{random.choice(['edu', 'university'])}.edu.cn",
            description=f"{random.choice(SCHOOL_NAMES)}是一所综合性大学，致力于培养优秀人才。"
        )
        schools.append(school)
        db.add(school)
    
    await db.commit()
    # 刷新所有对象
    for school in schools:
        await db.refresh(school)
    print(f"[OK] 成功创建 {len(schools)} 所学校")
    return schools


async def create_departments(db: AsyncSession, schools: list, count_per_school: int = 3):
    """创建院系数据"""
    print(f"创建院系数据（每所学校 {count_per_school} 个院系）...")
    departments = []
    for school in schools:
        school_id = school.id  # 直接使用ID，避免延迟加载
        for i in range(count_per_school):
            dept = Department(
                id=str(uuid4()),
                school_id=school_id,
                name=random.choice(DEPARTMENT_NAMES),
                code=f"DEPT{random.randint(10000, 99999)}",
                description=f"{random.choice(DEPARTMENT_NAMES)}院系"
            )
            departments.append(dept)
            db.add(dept)
    
    await db.commit()
    for dept in departments:
        await db.refresh(dept)
    print(f"[OK] 成功创建 {len(departments)} 个院系")
    return departments


async def create_classes(db: AsyncSession, departments: list, count_per_dept: int = 2):
    """创建班级数据"""
    print(f"创建班级数据（每个院系 {count_per_dept} 个班级）...")
    classes = []
    for dept in departments:
        dept_id = dept.id  # 直接使用ID
        for i in range(count_per_dept):
            cls = Class(
                id=str(uuid4()),
                department_id=dept_id,
                name=f"{random.choice(DEPARTMENT_NAMES)}{2020 + random.randint(0, 4)}级{i+1}班",
                grade=f"{2020 + random.randint(0, 4)}"
            )
            classes.append(cls)
            db.add(cls)
    
    await db.commit()
    for cls in classes:
        await db.refresh(cls)
    print(f"[OK] 成功创建 {len(classes)} 个班级")
    return classes


async def create_users(db: AsyncSession, count: int = 200):
    """创建用户数据"""
    print(f"创建 {count} 个用户...")
    users = []
    user_types = [UserType.STUDENT] * 100 + [UserType.TEACHER] * 50 + [UserType.ENTERPRISE] * 45 + [UserType.ADMIN] * 5
    
    used_usernames = set()
    for i in range(count):
        user_type = user_types[i] if i < len(user_types) else random.choice([UserType.STUDENT, UserType.TEACHER, UserType.ENTERPRISE])
        
        # 生成唯一用户名
        while True:
            username = f"user{uuid4().hex[:8]}"
            if username not in used_usernames:
                used_usernames.add(username)
                break
        
        user = User(
            id=str(uuid4()),
            username=username,
            password_hash=get_password_hash("123456"),
            phone=f"1{random.randint(3, 9)}{random.randint(100000000, 999999999)}",
            email=f"{username}@example.com",
            user_type=user_type,
            status="ACTIVE"
        )
        users.append(user)
        db.add(user)
    
    await db.commit()
    for user in users:
        await db.refresh(user)
    print(f"[OK] 成功创建 {len(users)} 个用户")
    return users


async def create_student_profiles(db: AsyncSession, users: list, classes: list):
    """创建学生档案"""
    print("创建学生档案...")
    student_users = [u for u in users if u.user_type == UserType.STUDENT]
    profiles = []
    
    # 获取所有class_id和department_id
    class_ids = [cls.id for cls in classes]
    dept_ids = list(set([cls.department_id for cls in classes]))
    
    for i, user in enumerate(student_users[:100]):
        cls_id = random.choice(class_ids) if class_ids else None
        dept_id = random.choice(dept_ids) if dept_ids else None
        
        # 获取school_id
        if cls_id:
            cls_result = await db.execute(select(Class).where(Class.id == cls_id))
            cls_obj = cls_result.scalar_one_or_none()
            if cls_obj:
                dept_result = await db.execute(select(Department).where(Department.id == cls_obj.department_id))
                dept_obj = dept_result.scalar_one_or_none()
                school_id = dept_obj.school_id if dept_obj else None
            else:
                school_id = None
        else:
            school_id = None
        
        profile = StudentProfile(
            id=str(uuid4()),
            user_id=user.id,
            real_name=random.choice(CHINESE_NAMES),
            student_id=f"STU{random.randint(2020000000, 2029999999)}",
            school_id=school_id,
            department_id=dept_id,
            class_id=cls_id,
            grade=f"{random.randint(2020, 2024)}",
            major=random.choice(DEPARTMENT_NAMES)
        )
        profiles.append(profile)
        db.add(profile)
    
    await db.commit()
    for profile in profiles:
        await db.refresh(profile)
    print(f"[OK] 成功创建 {len(profiles)} 个学生档案")
    return profiles


async def create_teacher_profiles(db: AsyncSession, users: list, departments: list):
    """创建教师档案"""
    print("创建教师档案...")
    teacher_users = [u for u in users if u.user_type == UserType.TEACHER]
    profiles = []
    
    dept_ids = [dept.id for dept in departments]
    school_ids = list(set([dept.school_id for dept in departments]))
    
    for i, user in enumerate(teacher_users[:50]):
        dept_id = random.choice(dept_ids) if dept_ids else None
        school_id = random.choice(school_ids) if school_ids else None
        
        profile = TeacherProfile(
            id=str(uuid4()),
            user_id=user.id,
            real_name=random.choice(CHINESE_NAMES),
            school_id=school_id,
            department_id=dept_id,
            title=random.choice(["教授", "副教授", "讲师", "助教"])
        )
        profiles.append(profile)
        db.add(profile)
    
    await db.commit()
    for profile in profiles:
        await db.refresh(profile)
    print(f"[OK] 成功创建 {len(profiles)} 个教师档案")
    return profiles


async def create_enterprise_profiles(db: AsyncSession, users: list):
    """创建企业档案"""
    print("创建企业档案...")
    enterprise_users = [u for u in users if u.user_type == UserType.ENTERPRISE]
    profiles = []
    
    for i, user in enumerate(enterprise_users[:45]):
        company_name = random.choice(COMPANY_NAMES) + (f"（{i+1}分公司）" if i > 0 else "")
        profile = EnterpriseProfile(
            id=str(uuid4()),
            user_id=user.id,
            company_name=company_name,
            unified_code=f"91{random.randint(100000000000000, 999999999999999)}",
            industry=random.choice(["互联网", "金融", "制造业", "教育", "医疗", "零售", "物流", "房地产", "能源", "传媒"]),
            scale=random.choice(["1-50人", "51-200人", "201-500人", "501-1000人", "1000人以上"]),
            address=f"{random.choice(['科技园', '产业园', '商务区'])}第{i+1}号",
            website=f"https://www.{company_name.lower().replace('（', '').replace('）', '').replace(' ', '')}.com",
            description=f"{company_name}是一家专注于{random.choice(['技术创新', '产品研发', '市场拓展', '客户服务'])}的企业。"
        )
        profiles.append(profile)
        db.add(profile)
    
    await db.commit()
    for profile in profiles:
        await db.refresh(profile)
    print(f"[OK] 成功创建 {len(profiles)} 个企业档案")
    return profiles


async def create_jobs(db: AsyncSession, enterprise_profiles: list, count: int = 50):
    """创建职位数据"""
    print(f"创建 {count} 个职位...")
    jobs = []
    enterprise_ids = [ep.id for ep in enterprise_profiles]
    
    for i in range(count):
        enterprise_id = random.choice(enterprise_ids) if enterprise_ids else None
        if not enterprise_id:
            continue
            
        title = random.choice(JOB_TITLES)
        major = random.choice(DEPARTMENT_NAMES)
        
        job = Job(
            id=str(uuid4()),
            enterprise_id=enterprise_id,
            title=title,
            department=random.choice(["技术部", "产品部", "运营部", "市场部", "销售部", "人事部", "财务部"]),
            job_type=random.choice(["FULL_TIME", "PART_TIME", "INTERN"]),
            salary_min=random.choice([5000, 8000, 10000, 15000, 20000]),
            salary_max=random.choice([10000, 15000, 20000, 30000, 50000]),
            work_location=random.choice(["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉"]),
            experience=random.choice(["不限", "1-3年", "3-5年", "5年以上"]),
            education=random.choice(["不限", "本科", "硕士", "博士"]),
            description=JOB_DESCRIPTION_TEMPLATE.format(title=title, major=major),
            requirements=f"1. {major}相关专业\n2. 具备良好的学习能力\n3. 有相关项目经验优先",
            status=random.choice(["PUBLISHED", "DRAFT", "CLOSED"]),
            view_count=random.randint(0, 1000),
            apply_count=random.randint(0, 100),
            tags=",".join(random.sample(["高薪", "五险一金", "带薪年假", "弹性工作", "团队氛围好", "发展空间大"], 3))
        )
        jobs.append(job)
        db.add(job)
    
    await db.commit()
    for job in jobs:
        await db.refresh(job)
    print(f"[OK] 成功创建 {len(jobs)} 个职位")
    return jobs


async def create_resumes(db: AsyncSession, student_profiles: list, count: int = 50):
    """创建简历数据"""
    print(f"创建 {count} 份简历...")
    resumes = []
    student_ids = [sp.id for sp in student_profiles]
    
    for i in range(count):
        student_id = random.choice(student_ids) if student_ids else None
        if not student_id:
            continue
        
        # 获取学生信息
        student_result = await db.execute(select(StudentProfile).where(StudentProfile.id == student_id))
        student = student_result.scalar_one_or_none()
        if not student:
            continue
        
        resume_content = f"""
姓名：{student.real_name}
学号：{student.student_id}
专业：{student.major}
年级：{student.grade}
毕业年份：{student.graduation_year if hasattr(student, 'graduation_year') else '2024'}

工作经历：
曾在{random.choice(COMPANY_NAMES)}实习{random.randint(3, 12)}个月

项目经历：
参与过{random.choice(['校园管理系统', '电商平台', '移动应用', '数据分析'])}项目

技能：
{','.join(random.sample(["Java", "Python", "JavaScript", "Vue", "React", "MySQL", "Redis"], 3))}

自我介绍：
我是{student.real_name}，{student.major}专业，热爱编程，有良好的团队协作能力。
"""
        resume = Resume(
            id=str(uuid4()),
            student_id=student_id,
            title=f"{student.real_name}的简历",
            content=resume_content,
            is_default=(i == 0)
        )
        resumes.append(resume)
        db.add(resume)
    
    await db.commit()
    for resume in resumes:
        await db.refresh(resume)
    print(f"[OK] 成功创建 {len(resumes)} 份简历")
    return resumes


async def create_job_applications(db: AsyncSession, student_profiles: list, jobs: list, resumes: list, count: int = 50):
    """创建职位申请数据"""
    print(f"创建 {count} 个职位申请...")
    applications = []
    student_user_ids = [sp.user_id for sp in student_profiles]
    job_ids = [job.id for job in jobs]
    resume_ids = [resume.id for resume in resumes]
    
    for i in range(count):
        student_user_id = random.choice(student_user_ids) if student_user_ids else None
        job_id = random.choice(job_ids) if job_ids else None
        resume_id = random.choice(resume_ids) if resume_ids else None
        
        if not student_user_id or not job_id:
            continue
        
        # 获取job的enterprise_id
        job_result = await db.execute(select(Job).where(Job.id == job_id))
        job = job_result.scalar_one_or_none()
        if not job:
            continue
        
        application = JobApplication(
            id=str(uuid4()),
            job_id=job_id,
            student_id=student_user_id,
            resume_id=resume_id if resume_id else None,
            status=random.choice(["PENDING", "REVIEWING", "ACCEPTED", "REJECTED"]),
            message=f"尊敬的HR，我对{job.title}职位非常感兴趣，希望能有机会加入贵公司。"
        )
        applications.append(application)
        db.add(application)
    
    await db.commit()
    for app in applications:
        await db.refresh(app)
    print(f"[OK] 成功创建 {len(applications)} 个职位申请")
    return applications


async def create_job_fairs(db: AsyncSession, schools: list, enterprise_profiles: list, count: int = 50):
    """创建双选会数据"""
    print(f"创建 {count} 个双选会...")
    job_fairs = []
    school_ids = [s.id for s in schools]
    enterprise_ids = [ep.id for ep in enterprise_profiles]
    
    for i in range(count):
        school_id = random.choice(school_ids) if school_ids else None
        start_time = datetime.now() + timedelta(days=random.randint(-30, 90))
        
        job_fair = JobFair(
            id=str(uuid4()),
            school_id=school_id,
            title=f"{random.choice(SCHOOL_NAMES)}2024年{'春季' if i < 25 else '秋季'}双选会",
            description=f"本次双选会邀请了{random.randint(50, 200)}家企业，提供{random.randint(500, 2000)}个职位。",
            start_time=start_time,
            end_time=start_time + timedelta(hours=random.randint(4, 8)),
            location=f"{random.choice(['体育馆', '会议中心', '活动中心'])}",
            status=random.choice(["DRAFT", "PUBLISHED", "ONGOING", "ENDED"]),
            max_enterprises=random.randint(50, 200),
            created_by=random.choice(enterprise_ids) if enterprise_ids and i % 3 == 0 else None
        )
        job_fairs.append(job_fair)
        db.add(job_fair)
    
    await db.commit()
    for jf in job_fairs:
        await db.refresh(jf)
    print(f"[OK] 成功创建 {len(job_fairs)} 个双选会")
    return job_fairs


async def create_info_sessions(db: AsyncSession, enterprise_profiles: list, schools: list, count: int = 50):
    """创建宣讲会数据"""
    print(f"创建 {count} 个宣讲会...")
    info_sessions = []
    enterprise_ids = [ep.id for ep in enterprise_profiles]
    school_ids = [s.id for s in schools]
    
    for i in range(count):
        enterprise_id = random.choice(enterprise_ids) if enterprise_ids else None
        school_id = random.choice(school_ids) if school_ids else None
        
        if not enterprise_id:
            continue
        
        # 获取企业名称
        ent_result = await db.execute(select(EnterpriseProfile).where(EnterpriseProfile.id == enterprise_id))
        enterprise = ent_result.scalar_one_or_none()
        company_name = enterprise.company_name if enterprise else "某公司"
        
        start_time = datetime.now() + timedelta(days=random.randint(-30, 90))
        
        info_session = InfoSession(
            id=str(uuid4()),
            enterprise_id=enterprise_id,
            school_id=school_id,
            title=f"{company_name}2024校园宣讲会",
            description=f"{company_name}将在{random.choice(SCHOOL_NAMES)}举办校园宣讲会，欢迎同学们参加。",
            start_time=start_time,
            end_time=start_time + timedelta(hours=random.randint(2, 4)),
            location=f"{random.choice(['报告厅', '礼堂', '会议室'])}",
            session_type=random.choice(["OFFLINE", "ONLINE", "HYBRID"]),
            live_url=f"https://live.example.com/session{i+1}" if i % 3 == 0 else None,
            status=random.choice(["DRAFT", "PUBLISHED", "ONGOING", "ENDED"]),
            max_students=random.randint(100, 500),
            check_in_count=random.randint(0, 200)
        )
        info_sessions.append(info_session)
        db.add(info_session)
    
    await db.commit()
    for is_obj in info_sessions:
        await db.refresh(is_obj)
    print(f"[OK] 成功创建 {len(info_sessions)} 个宣讲会")
    return info_sessions


async def create_interviews(db: AsyncSession, applications: list, count: int = 50):
    """创建面试数据"""
    print(f"创建 {count} 个面试...")
    interviews = []
    
    for i in range(min(count, len(applications))):
        app = applications[i] if i < len(applications) else random.choice(applications)
        
        # 获取job的enterprise_id
        job_result = await db.execute(select(Job).where(Job.id == app.job_id))
        job = job_result.scalar_one_or_none()
        if not job:
            continue
        
        # 获取学生档案ID
        student_result = await db.execute(select(StudentProfile).where(StudentProfile.user_id == app.student_id))
        student_profile = student_result.scalar_one_or_none()
        if not student_profile:
            continue
        
        scheduled_time = datetime.now() + timedelta(days=random.randint(1, 30))
        
        interview = Interview(
            id=str(uuid4()),
            application_id=app.id,
            enterprise_id=job.enterprise_id,
            student_id=student_profile.id,
            interview_type=random.choice(["VIDEO", "PHONE", "ONSITE"]),
            scheduled_time=scheduled_time,
            duration=random.choice([30, 60, 90]),
            location=random.choice(["公司会议室", "线上", "学校会议室"]) if i % 2 == 0 else None,
            meeting_url=f"https://meeting.example.com/{uuid4()}" if i % 3 == 0 else None,
            status=random.choice(["SCHEDULED", "CONFIRMED", "COMPLETED", "CANCELLED"]),
            feedback=random.choice([None, "面试表现良好", "需要进一步评估", "待定"]) if i % 2 == 0 else None
        )
        interviews.append(interview)
        db.add(interview)
    
    await db.commit()
    for interview in interviews:
        await db.refresh(interview)
    print(f"[OK] 成功创建 {len(interviews)} 个面试")
    return interviews


async def create_schedules(db: AsyncSession, users: list, job_fairs: list, info_sessions: list, interviews: list, count: int = 50):
    """创建日程数据"""
    print(f"创建 {count} 个日程...")
    schedules = []
    user_ids = [u.id for u in users]
    job_fair_ids = [jf.id for jf in job_fairs]
    info_session_ids = [is_obj.id for is_obj in info_sessions]
    interview_ids = [iv.id for iv in interviews]
    
    for i in range(count):
        user_id = random.choice(user_ids) if user_ids else None
        if not user_id:
            continue
        
        schedule_type = random.choice(["JOB_FAIR", "INFO_SESSION", "INTERVIEW", "CUSTOM"])
        related_id = None
        title = f"自定义日程{i+1}"
        
        if schedule_type == "JOB_FAIR" and job_fair_ids:
            related_id = random.choice(job_fair_ids)
            title = f"参加双选会"
        elif schedule_type == "INFO_SESSION" and info_session_ids:
            related_id = random.choice(info_session_ids)
            title = f"参加宣讲会"
        elif schedule_type == "INTERVIEW" and interview_ids:
            related_id = random.choice(interview_ids)
            title = f"面试"
        
        start_time = datetime.now() + timedelta(days=random.randint(-30, 90))
        
        schedule = Schedule(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            content=f"日程内容：{title}",
            start_time=start_time,
            end_time=start_time + timedelta(hours=random.randint(1, 4)),
            schedule_type=schedule_type,
            related_id=related_id,
            reminder_time=start_time - timedelta(hours=1) if i % 2 == 0 else None,
            is_completed=random.choice([True, False]) if start_time < datetime.now() else False
        )
        schedules.append(schedule)
        db.add(schedule)
    
    await db.commit()
    for schedule in schedules:
        await db.refresh(schedule)
    print(f"[OK] 成功创建 {len(schedules)} 个日程")
    return schedules


async def create_favorites(db: AsyncSession, users: list, jobs: list, resumes: list, count: int = 50):
    """创建收藏数据"""
    print(f"创建 {count} 个收藏...")
    favorites = []
    user_ids = [u.id for u in users]
    job_ids = [job.id for job in jobs]
    resume_ids = [resume.id for resume in resumes]
    
    for i in range(count):
        user_id = random.choice(user_ids) if user_ids else None
        if not user_id:
            continue
        
        target_type = random.choice(["JOB", "RESUME", "ENTERPRISE"])
        target_id = None
        
        if target_type == "JOB" and job_ids:
            target_id = random.choice(job_ids)
        elif target_type == "RESUME" and resume_ids:
            target_id = random.choice(resume_ids)
        else:
            continue
        
        favorite = Favorite(
            id=str(uuid4()),
            user_id=user_id,
            target_type=target_type,
            target_id=target_id
        )
        favorites.append(favorite)
        db.add(favorite)
    
    await db.commit()
    for favorite in favorites:
        await db.refresh(favorite)
    print(f"[OK] 成功创建 {len(favorites)} 个收藏")
    return favorites


async def create_chat_sessions_and_messages(db: AsyncSession, users: list, count_sessions: int = 50, count_messages: int = 200):
    """创建聊天会话和消息"""
    print(f"创建 {count_sessions} 个聊天会话和 {count_messages} 条消息...")
    sessions = []
    messages = []
    user_ids = [u.id for u in users]
    
    # 创建会话
    created_sessions = set()
    for i in range(count_sessions):
        if len(user_ids) < 2:
            break
        
        user1_id = random.choice(user_ids)
        user2_id = random.choice([uid for uid in user_ids if uid != user1_id])
        
        # 检查是否已存在会话
        session_key = tuple(sorted([user1_id, user2_id]))
        if session_key in created_sessions:
            continue
        created_sessions.add(session_key)
        
        session = ChatSession(
            id=str(uuid4()),
            user1_id=user1_id,
            user2_id=user2_id,
            last_message_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        sessions.append(session)
        db.add(session)
    
    await db.commit()
    for session in sessions:
        await db.refresh(session)
    print(f"[OK] 成功创建 {len(sessions)} 个聊天会话")
    
    # 创建消息
    session_ids = [s.id for s in sessions]
    for i in range(count_messages):
        if not session_ids:
            break
        
        session_id = random.choice(session_ids)
        session_result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
        session_obj = session_result.scalar_one_or_none()
        if not session_obj:
            continue
        
        sender = random.choice([session_obj.user1_id, session_obj.user2_id])
        receiver = session_obj.user2_id if sender == session_obj.user1_id else session_obj.user1_id
        
        message = Message(
            id=str(uuid4()),
            session_id=session_id,
            sender_id=sender,
            receiver_id=receiver,
            content=random.choice([
                "你好，请问这个职位还在招聘吗？",
                "我对贵公司很感兴趣，希望能了解更多信息。",
                "我的简历已发送，请查收。",
                "感谢您的回复，我会认真考虑的。",
                "请问面试时间可以调整吗？",
                "好的，我会准时参加面试。"
            ]),
            message_type="TEXT",
            is_read=random.choice([True, False]),
            created_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        messages.append(message)
        db.add(message)
        
        # 更新会话的最后消息时间
        session_obj.last_message_at = message.created_at
    
    await db.commit()
    print(f"[OK] 成功创建 {len(messages)} 条消息")
    return sessions, messages


async def main():
    """主函数"""
    print("=" * 60)
    print("开始填充数据库测试数据...")
    print("=" * 60)
    
    # 创建异步会话
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        try:
            # 清空现有数据
            await clear_tables(db)
            
            # 1. 创建学校、院系、班级
            schools = await create_schools(db, count=50)
            departments = await create_departments(db, schools, count_per_school=3)
            classes = await create_classes(db, departments, count_per_dept=2)
            
            # 2. 创建用户
            users = await create_users(db, count=200)
            
            # 3. 创建用户档案
            student_profiles = await create_student_profiles(db, users, classes)
            teacher_profiles = await create_teacher_profiles(db, users, departments)
            enterprise_profiles = await create_enterprise_profiles(db, users)
            
            # 4. 创建职位和简历
            jobs = await create_jobs(db, enterprise_profiles, count=50)
            resumes = await create_resumes(db, student_profiles, count=50)
            
            # 5. 创建职位申请
            applications = await create_job_applications(db, student_profiles, jobs, resumes, count=50)
            
            # 6. 创建双选会和宣讲会
            job_fairs = await create_job_fairs(db, schools, enterprise_profiles, count=50)
            info_sessions = await create_info_sessions(db, enterprise_profiles, schools, count=50)
            
            # 7. 创建面试
            interviews = await create_interviews(db, applications, count=50)
            
            # 8. 创建日程
            schedules = await create_schedules(db, users, job_fairs, info_sessions, interviews, count=50)
            
            # 9. 创建收藏
            favorites = await create_favorites(db, users, jobs, resumes, count=50)
            
            # 10. 创建聊天会话和消息
            chat_sessions, chat_messages = await create_chat_sessions_and_messages(
                db, users, count_sessions=50, count_messages=200
            )
            
            print("=" * 60)
            print("数据填充完成！")
            print("=" * 60)
            print(f"总计创建：")
            print(f"  - 学校: {len(schools)}")
            print(f"  - 院系: {len(departments)}")
            print(f"  - 班级: {len(classes)}")
            print(f"  - 用户: {len(users)}")
            print(f"  - 学生档案: {len(student_profiles)}")
            print(f"  - 教师档案: {len(teacher_profiles)}")
            print(f"  - 企业档案: {len(enterprise_profiles)}")
            print(f"  - 职位: {len(jobs)}")
            print(f"  - 简历: {len(resumes)}")
            print(f"  - 职位申请: {len(applications)}")
            print(f"  - 双选会: {len(job_fairs)}")
            print(f"  - 宣讲会: {len(info_sessions)}")
            print(f"  - 面试: {len(interviews)}")
            print(f"  - 日程: {len(schedules)}")
            print(f"  - 收藏: {len(favorites)}")
            print(f"  - 聊天会话: {len(chat_sessions)}")
            print(f"  - 消息: {len(chat_messages)}")
            print("=" * 60)
            
        except Exception as e:
            print(f"错误：{e}")
            import traceback
            traceback.print_exc()
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())

