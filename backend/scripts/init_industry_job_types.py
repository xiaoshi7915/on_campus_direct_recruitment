"""
初始化行业职位类型维表数据
涵盖绝大多数行业包括细分行业的绝大多数岗位数据
"""
import asyncio
import sys
import os
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.models.industry_job_type import IndustryCategory, SubIndustry, JobType


# 行业分类数据（一级行业）
INDUSTRY_CATEGORIES = [
    {"name": "互联网/IT", "code": "IT", "sort_order": 1},
    {"name": "金融", "code": "FINANCE", "sort_order": 2},
    {"name": "教育", "code": "EDUCATION", "sort_order": 3},
    {"name": "医疗健康", "code": "HEALTHCARE", "sort_order": 4},
    {"name": "制造业", "code": "MANUFACTURING", "sort_order": 5},
    {"name": "零售/电商", "code": "RETAIL", "sort_order": 6},
    {"name": "房地产", "code": "REAL_ESTATE", "sort_order": 7},
    {"name": "咨询", "code": "CONSULTING", "sort_order": 8},
    {"name": "媒体/广告", "code": "MEDIA", "sort_order": 9},
    {"name": "能源/环保", "code": "ENERGY", "sort_order": 10},
    {"name": "交通/物流", "code": "LOGISTICS", "sort_order": 11},
    {"name": "餐饮/酒店", "code": "HOSPITALITY", "sort_order": 12},
    {"name": "建筑/工程", "code": "CONSTRUCTION", "sort_order": 13},
    {"name": "政府/非营利", "code": "GOVERNMENT", "sort_order": 14},
    {"name": "其他", "code": "OTHER", "sort_order": 99},
]

# 细分行业数据（二级行业）
SUB_INDUSTRIES = {
    "互联网/IT": [
        {"name": "互联网服务", "code": "IT_INTERNET", "sort_order": 1},
        {"name": "软件开发", "code": "IT_SOFTWARE", "sort_order": 2},
        {"name": "电子商务", "code": "IT_ECOMMERCE", "sort_order": 3},
        {"name": "游戏", "code": "IT_GAME", "sort_order": 4},
        {"name": "人工智能", "code": "IT_AI", "sort_order": 5},
        {"name": "大数据", "code": "IT_BIGDATA", "sort_order": 6},
        {"name": "云计算", "code": "IT_CLOUD", "sort_order": 7},
        {"name": "区块链", "code": "IT_BLOCKCHAIN", "sort_order": 8},
        {"name": "物联网", "code": "IT_IOT", "sort_order": 9},
        {"name": "网络安全", "code": "IT_SECURITY", "sort_order": 10},
    ],
    "金融": [
        {"name": "银行", "code": "FINANCE_BANK", "sort_order": 1},
        {"name": "证券", "code": "FINANCE_SECURITIES", "sort_order": 2},
        {"name": "保险", "code": "FINANCE_INSURANCE", "sort_order": 3},
        {"name": "基金", "code": "FINANCE_FUND", "sort_order": 4},
        {"name": "投资", "code": "FINANCE_INVESTMENT", "sort_order": 5},
        {"name": "互联网金融", "code": "FINANCE_FINTECH", "sort_order": 6},
        {"name": "支付", "code": "FINANCE_PAYMENT", "sort_order": 7},
    ],
    "教育": [
        {"name": "在线教育", "code": "EDU_ONLINE", "sort_order": 1},
        {"name": "K12教育", "code": "EDU_K12", "sort_order": 2},
        {"name": "高等教育", "code": "EDU_HIGHER", "sort_order": 3},
        {"name": "职业培训", "code": "EDU_VOCATIONAL", "sort_order": 4},
        {"name": "语言培训", "code": "EDU_LANGUAGE", "sort_order": 5},
        {"name": "早教", "code": "EDU_EARLY", "sort_order": 6},
    ],
    "医疗健康": [
        {"name": "医院", "code": "HEALTH_HOSPITAL", "sort_order": 1},
        {"name": "医疗器械", "code": "HEALTH_DEVICE", "sort_order": 2},
        {"name": "医药", "code": "HEALTH_PHARMA", "sort_order": 3},
        {"name": "互联网医疗", "code": "HEALTH_ONLINE", "sort_order": 4},
        {"name": "健康管理", "code": "HEALTH_MANAGEMENT", "sort_order": 5},
        {"name": "体检", "code": "HEALTH_CHECKUP", "sort_order": 6},
    ],
    "制造业": [
        {"name": "汽车制造", "code": "MFG_AUTO", "sort_order": 1},
        {"name": "电子制造", "code": "MFG_ELECTRONICS", "sort_order": 2},
        {"name": "机械制造", "code": "MFG_MACHINERY", "sort_order": 3},
        {"name": "化工", "code": "MFG_CHEMICAL", "sort_order": 4},
        {"name": "纺织", "code": "MFG_TEXTILE", "sort_order": 5},
        {"name": "食品", "code": "MFG_FOOD", "sort_order": 6},
    ],
    "零售/电商": [
        {"name": "电商平台", "code": "RETAIL_PLATFORM", "sort_order": 1},
        {"name": "新零售", "code": "RETAIL_NEW", "sort_order": 2},
        {"name": "超市/便利店", "code": "RETAIL_SUPERMARKET", "sort_order": 3},
        {"name": "品牌零售", "code": "RETAIL_BRAND", "sort_order": 4},
    ],
    "房地产": [
        {"name": "房地产开发", "code": "RE_DEVELOPMENT", "sort_order": 1},
        {"name": "房地产中介", "code": "RE_AGENCY", "sort_order": 2},
        {"name": "物业管理", "code": "RE_PROPERTY", "sort_order": 3},
        {"name": "建筑设计", "code": "RE_DESIGN", "sort_order": 4},
    ],
    "咨询": [
        {"name": "管理咨询", "code": "CONSULT_MANAGEMENT", "sort_order": 1},
        {"name": "财务咨询", "code": "CONSULT_FINANCE", "sort_order": 2},
        {"name": "IT咨询", "code": "CONSULT_IT", "sort_order": 3},
        {"name": "人力资源咨询", "code": "CONSULT_HR", "sort_order": 4},
    ],
    "媒体/广告": [
        {"name": "广告", "code": "MEDIA_AD", "sort_order": 1},
        {"name": "公关", "code": "MEDIA_PR", "sort_order": 2},
        {"name": "影视", "code": "MEDIA_FILM", "sort_order": 3},
        {"name": "出版", "code": "MEDIA_PUBLISH", "sort_order": 4},
        {"name": "新媒体", "code": "MEDIA_NEW", "sort_order": 5},
    ],
    "能源/环保": [
        {"name": "石油", "code": "ENERGY_OIL", "sort_order": 1},
        {"name": "电力", "code": "ENERGY_POWER", "sort_order": 2},
        {"name": "新能源", "code": "ENERGY_NEW", "sort_order": 3},
        {"name": "环保", "code": "ENERGY_ENV", "sort_order": 4},
    ],
    "交通/物流": [
        {"name": "物流", "code": "LOGISTICS_LOGISTICS", "sort_order": 1},
        {"name": "快递", "code": "LOGISTICS_EXPRESS", "sort_order": 2},
        {"name": "交通运输", "code": "LOGISTICS_TRANSPORT", "sort_order": 3},
        {"name": "航空", "code": "LOGISTICS_AIR", "sort_order": 4},
    ],
    "餐饮/酒店": [
        {"name": "餐饮", "code": "HOSPITALITY_RESTAURANT", "sort_order": 1},
        {"name": "酒店", "code": "HOSPITALITY_HOTEL", "sort_order": 2},
        {"name": "旅游", "code": "HOSPITALITY_TRAVEL", "sort_order": 3},
    ],
    "建筑/工程": [
        {"name": "建筑施工", "code": "CONSTRUCTION_BUILD", "sort_order": 1},
        {"name": "工程咨询", "code": "CONSTRUCTION_CONSULT", "sort_order": 2},
        {"name": "装饰装修", "code": "CONSTRUCTION_DECORATE", "sort_order": 3},
    ],
    "政府/非营利": [
        {"name": "政府机构", "code": "GOVERNMENT_GOV", "sort_order": 1},
        {"name": "事业单位", "code": "GOVERNMENT_INSTITUTION", "sort_order": 2},
        {"name": "非营利组织", "code": "GOVERNMENT_NPO", "sort_order": 3},
    ],
}

# 职位类型数据（根据行业分类）
JOB_TYPES = {
    "互联网/IT": [
        {"name": "前端开发", "code": "JOB_FRONTEND", "sort_order": 1},
        {"name": "后端开发", "code": "JOB_BACKEND", "sort_order": 2},
        {"name": "全栈开发", "code": "JOB_FULLSTACK", "sort_order": 3},
        {"name": "移动开发", "code": "JOB_MOBILE", "sort_order": 4},
        {"name": "算法工程师", "code": "JOB_ALGORITHM", "sort_order": 5},
        {"name": "数据开发", "code": "JOB_DATA", "sort_order": 6},
        {"name": "数据分析师", "code": "JOB_DATA_ANALYST", "sort_order": 7},
        {"name": "测试工程师", "code": "JOB_TEST", "sort_order": 8},
        {"name": "运维工程师", "code": "JOB_DEVOPS", "sort_order": 9},
        {"name": "产品经理", "code": "JOB_PM", "sort_order": 10},
        {"name": "UI/UX设计师", "code": "JOB_UIUX", "sort_order": 11},
        {"name": "项目经理", "code": "JOB_PROJECT_MANAGER", "sort_order": 12},
        {"name": "技术总监", "code": "JOB_CTO", "sort_order": 13},
        {"name": "架构师", "code": "JOB_ARCHITECT", "sort_order": 14},
    ],
    "金融": [
        {"name": "金融分析师", "code": "FINANCE_ANALYST", "sort_order": 1},
        {"name": "投资顾问", "code": "FINANCE_ADVISOR", "sort_order": 2},
        {"name": "风控专员", "code": "FINANCE_RISK", "sort_order": 3},
        {"name": "银行柜员", "code": "FINANCE_TELLER", "sort_order": 4},
        {"name": "客户经理", "code": "FINANCE_ACCOUNT_MANAGER", "sort_order": 5},
        {"name": "精算师", "code": "FINANCE_ACTUARY", "sort_order": 6},
        {"name": "金融产品经理", "code": "FINANCE_PM", "sort_order": 7},
    ],
    "教育": [
        {"name": "教师", "code": "EDU_TEACHER", "sort_order": 1},
        {"name": "课程研发", "code": "EDU_CURRICULUM", "sort_order": 2},
        {"name": "教育产品经理", "code": "EDU_PM", "sort_order": 3},
        {"name": "教学运营", "code": "EDU_OPERATION", "sort_order": 4},
        {"name": "教研", "code": "EDU_RESEARCH", "sort_order": 5},
    ],
    "医疗健康": [
        {"name": "医生", "code": "HEALTH_DOCTOR", "sort_order": 1},
        {"name": "护士", "code": "HEALTH_NURSE", "sort_order": 2},
        {"name": "医疗产品经理", "code": "HEALTH_PM", "sort_order": 3},
        {"name": "医疗器械销售", "code": "HEALTH_SALES", "sort_order": 4},
        {"name": "医药研发", "code": "HEALTH_RD", "sort_order": 5},
    ],
    "制造业": [
        {"name": "机械工程师", "code": "MFG_ENGINEER", "sort_order": 1},
        {"name": "工艺工程师", "code": "MFG_PROCESS", "sort_order": 2},
        {"name": "质量工程师", "code": "MFG_QUALITY", "sort_order": 3},
        {"name": "生产管理", "code": "MFG_PRODUCTION", "sort_order": 4},
        {"name": "研发工程师", "code": "MFG_RD", "sort_order": 5},
    ],
    "零售/电商": [
        {"name": "电商运营", "code": "RETAIL_OPERATION", "sort_order": 1},
        {"name": "商品管理", "code": "RETAIL_MERCHANDISE", "sort_order": 2},
        {"name": "供应链管理", "code": "RETAIL_SUPPLY", "sort_order": 3},
        {"name": "市场推广", "code": "RETAIL_MARKETING", "sort_order": 4},
    ],
    "房地产": [
        {"name": "房地产销售", "code": "RE_SALES", "sort_order": 1},
        {"name": "房地产策划", "code": "RE_PLANNING", "sort_order": 2},
        {"name": "建筑设计", "code": "RE_ARCHITECT", "sort_order": 3},
        {"name": "工程管理", "code": "RE_PROJECT", "sort_order": 4},
    ],
    "咨询": [
        {"name": "咨询顾问", "code": "CONSULT_CONSULTANT", "sort_order": 1},
        {"name": "分析师", "code": "CONSULT_ANALYST", "sort_order": 2},
        {"name": "项目经理", "code": "CONSULT_PM", "sort_order": 3},
    ],
    "媒体/广告": [
        {"name": "广告策划", "code": "MEDIA_PLANNING", "sort_order": 1},
        {"name": "文案", "code": "MEDIA_COPY", "sort_order": 2},
        {"name": "设计师", "code": "MEDIA_DESIGNER", "sort_order": 3},
        {"name": "媒介", "code": "MEDIA_MEDIA", "sort_order": 4},
    ],
    "能源/环保": [
        {"name": "能源工程师", "code": "ENERGY_ENGINEER", "sort_order": 1},
        {"name": "环保工程师", "code": "ENERGY_ENV_ENGINEER", "sort_order": 2},
        {"name": "项目管理", "code": "ENERGY_PM", "sort_order": 3},
    ],
    "交通/物流": [
        {"name": "物流管理", "code": "LOGISTICS_MANAGEMENT", "sort_order": 1},
        {"name": "供应链管理", "code": "LOGISTICS_SUPPLY", "sort_order": 2},
        {"name": "运营管理", "code": "LOGISTICS_OPERATION", "sort_order": 3},
    ],
    "餐饮/酒店": [
        {"name": "餐饮管理", "code": "HOSPITALITY_MANAGEMENT", "sort_order": 1},
        {"name": "酒店管理", "code": "HOSPITALITY_HOTEL_MGMT", "sort_order": 2},
        {"name": "厨师", "code": "HOSPITALITY_CHEF", "sort_order": 3},
    ],
    "建筑/工程": [
        {"name": "建筑工程师", "code": "CONSTRUCTION_ENGINEER", "sort_order": 1},
        {"name": "结构工程师", "code": "CONSTRUCTION_STRUCTURE", "sort_order": 2},
        {"name": "工程管理", "code": "CONSTRUCTION_PM", "sort_order": 3},
    ],
    "政府/非营利": [
        {"name": "行政", "code": "GOVERNMENT_ADMIN", "sort_order": 1},
        {"name": "文员", "code": "GOVERNMENT_CLERK", "sort_order": 2},
        {"name": "项目管理", "code": "GOVERNMENT_PM", "sort_order": 3},
    ],
    "其他": [
        {"name": "其他", "code": "OTHER", "sort_order": 1},
    ],
}

# 通用职位类型（不关联特定行业）
COMMON_JOB_TYPES = [
    {"name": "销售", "code": "COMMON_SALES", "sort_order": 1},
    {"name": "市场", "code": "COMMON_MARKETING", "sort_order": 2},
    {"name": "人力资源", "code": "COMMON_HR", "sort_order": 3},
    {"name": "财务", "code": "COMMON_FINANCE", "sort_order": 4},
    {"name": "行政", "code": "COMMON_ADMIN", "sort_order": 5},
    {"name": "法务", "code": "COMMON_LEGAL", "sort_order": 6},
    {"name": "客服", "code": "COMMON_SERVICE", "sort_order": 7},
    {"name": "运营", "code": "COMMON_OPERATION", "sort_order": 8},
]


async def init_industry_job_types():
    """初始化行业职位类型维表数据"""
    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已有数据
            from sqlalchemy import select, func
            result = await db.execute(select(func.count()).select_from(IndustryCategory))
            count = result.scalar()
            if count > 0:
                print(f"[SKIP] 行业职位类型维表已有数据（{count}条），跳过初始化")
                return
            
            print("开始初始化行业职位类型维表数据...")
            
            # 创建一级行业
            category_map = {}
            for cat_data in INDUSTRY_CATEGORIES:
                category = IndustryCategory(
                    id=str(uuid4()),
                    name=cat_data["name"],
                    code=cat_data.get("code"),
                    sort_order=cat_data.get("sort_order", 0)
                )
                db.add(category)
                category_map[cat_data["name"]] = category
            
            await db.commit()
            print(f"✓ 创建了 {len(INDUSTRY_CATEGORIES)} 个一级行业")
            
            # 创建细分行业
            sub_industry_map = {}
            for category_name, sub_list in SUB_INDUSTRIES.items():
                if category_name not in category_map:
                    continue
                category = category_map[category_name]
                
                for sub_data in sub_list:
                    sub_industry = SubIndustry(
                        id=str(uuid4()),
                        category_id=category.id,
                        name=sub_data["name"],
                        code=sub_data.get("code"),
                        sort_order=sub_data.get("sort_order", 0)
                    )
                    db.add(sub_industry)
                    sub_industry_map[f"{category_name}_{sub_data['name']}"] = sub_industry
            
            await db.commit()
            print(f"✓ 创建了 {len(sub_industry_map)} 个细分行业")
            
            # 创建职位类型（关联到一级行业）
            job_type_count = 0
            for category_name, job_list in JOB_TYPES.items():
                if category_name not in category_map:
                    continue
                category = category_map[category_name]
                
                for job_data in job_list:
                    job_type = JobType(
                        id=str(uuid4()),
                        category_id=category.id,
                        name=job_data["name"],
                        code=job_data.get("code"),
                        sort_order=job_data.get("sort_order", 0)
                    )
                    db.add(job_type)
                    job_type_count += 1
            
            # 创建通用职位类型（不关联行业）
            for job_data in COMMON_JOB_TYPES:
                job_type = JobType(
                    id=str(uuid4()),
                    category_id=None,
                    name=job_data["name"],
                    code=job_data.get("code"),
                    sort_order=job_data.get("sort_order", 0)
                )
                db.add(job_type)
                job_type_count += 1
            
            await db.commit()
            print(f"✓ 创建了 {job_type_count} 个职位类型")
            
            print("✓ 行业职位类型维表数据初始化完成！")
            
        except Exception as e:
            await db.rollback()
            print(f"✗ 初始化失败: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(init_industry_job_types())

