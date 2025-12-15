"""
添加缺失的数据库索引
根据常用查询字段添加索引以提升查询性能
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine
from app.core.logging import get_logger

logger = get_logger(__name__)

# 需要添加的索引列表
INDEXES_TO_ADD = [
    # Job表索引
    ("jobs", ["status", "created_at"], "idx_job_status_created"),
    ("jobs", ["enterprise_id", "status"], "idx_job_enterprise_status"),
    ("jobs", ["work_location"], "idx_job_location"),
    ("jobs", ["job_type"], "idx_job_type"),
    ("jobs", ["education"], "idx_job_education"),
    
    # JobApplication表索引
    ("job_applications", ["student_id", "status"], "idx_application_student_status"),
    ("job_applications", ["job_id", "status"], "idx_application_job_status"),
    ("job_applications", ["created_at"], "idx_application_created"),
    
    # Resume表索引
    ("resumes", ["student_id", "is_default"], "idx_resume_student_default"),
    ("resumes", ["created_at"], "idx_resume_created"),
    
    # Message表索引
    ("messages", ["session_id", "created_at"], "idx_message_session_created"),
    ("messages", ["sender_id", "created_at"], "idx_message_sender_created"),
    ("messages", ["receiver_id", "is_read"], "idx_message_receiver_read"),
    
    # ChatSession表索引
    ("chat_sessions", ["user1_id", "last_message_at"], "idx_session_user1_lastmsg"),
    ("chat_sessions", ["user2_id", "last_message_at"], "idx_session_user2_lastmsg"),
    
    # StudentProfile表索引
    ("student_profiles", ["department_id", "grade"], "idx_student_dept_grade"),
    ("student_profiles", ["school_id", "department_id"], "idx_student_school_dept"),
    ("student_profiles", ["real_name"], "idx_student_name"),
    ("student_profiles", ["student_id"], "idx_student_student_id"),
    
    # Todo表索引
    ("todos", ["user_id", "is_completed"], "idx_todo_user_completed"),
    ("todos", ["user_id", "priority"], "idx_todo_user_priority"),
    ("todos", ["user_id", "created_at"], "idx_todo_user_created"),
    
    # Interview表索引
    ("interviews", ["enterprise_id", "status"], "idx_interview_enterprise_status"),
    ("interviews", ["student_id", "status"], "idx_interview_student_status"),
    ("interviews", ["scheduled_at"], "idx_interview_scheduled"),
    
    # JobFair表索引
    ("job_fairs", ["school_id", "status"], "idx_jobfair_school_status"),
    ("job_fairs", ["start_date"], "idx_jobfair_start"),
    
    # InfoSession表索引
    ("info_sessions", ["enterprise_id", "status"], "idx_infosession_enterprise_status"),
    ("info_sessions", ["school_id", "status"], "idx_infosession_school_status"),
    ("info_sessions", ["scheduled_at"], "idx_infosession_scheduled"),
]


async def check_index_exists(table_name: str, index_name: str) -> bool:
    """检查索引是否存在"""
    async with engine.connect() as conn:
        result = await conn.execute(
            text("""
                SELECT COUNT(*) as count
                FROM information_schema.statistics
                WHERE table_schema = DATABASE()
                AND table_name = :table_name
                AND index_name = :index_name
            """),
            {"table_name": table_name, "index_name": index_name}
        )
        row = result.fetchone()
        return row[0] > 0 if row else False


async def add_index(table_name: str, columns: list, index_name: str):
    """添加索引"""
    try:
        # 检查索引是否已存在
        exists = await check_index_exists(table_name, index_name)
        if exists:
            logger.info(f"✅ 索引 {index_name} 已存在，跳过")
            return True
        
        # 构建索引SQL
        columns_str = ", ".join(columns)
        sql = f"CREATE INDEX {index_name} ON {table_name} ({columns_str})"
        
        async with engine.begin() as conn:
            await conn.execute(text(sql))
            logger.info(f"✅ 成功添加索引: {index_name} on {table_name}({columns_str})")
        
        return True
    except Exception as e:
        logger.error(f"❌ 添加索引失败 {index_name}: {str(e)}")
        return False


async def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("开始添加缺失的数据库索引")
    logger.info("=" * 60)
    
    results = []
    for table_name, columns, index_name in INDEXES_TO_ADD:
        result = await add_index(table_name, columns, index_name)
        results.append((index_name, result))
    
    # 输出结果
    logger.info("\n" + "=" * 60)
    logger.info("索引添加结果")
    logger.info("=" * 60)
    
    success = sum(1 for _, result in results if result)
    failed = len(results) - success
    
    for index_name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        logger.info(f"{index_name}: {status}")
    
    logger.info(f"\n总计: {success} 成功, {failed} 失败")
    
    if failed == 0:
        logger.info("\n🎉 所有索引添加完成！")
    else:
        logger.warning(f"\n⚠️  有 {failed} 个索引添加失败")


if __name__ == "__main__":
    asyncio.run(main())




