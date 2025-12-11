"""
创建student_comments表的迁移脚本（修复版本）
先检查表是否存在，如果不存在则创建（不使用外键约束，避免类型不匹配问题）
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


async def create_table():
    """创建student_comments表（不使用外键约束，避免类型不匹配）"""
    async with engine.begin() as conn:
        # 先检查表是否存在
        check_result = await conn.execute(text("SHOW TABLES LIKE 'student_comments'"))
        if check_result.fetchone():
            print("✅ student_comments表已存在")
            return
        
        # 创建student_comments表（不使用外键约束，避免类型不匹配问题）
        await conn.execute(text("""
            CREATE TABLE `student_comments` (
                `id` VARCHAR(36) NOT NULL PRIMARY KEY COMMENT '点评ID',
                `teacher_id` VARCHAR(36) NOT NULL COMMENT '教师ID',
                `student_id` VARCHAR(36) NOT NULL COMMENT '学生ID',
                `content` TEXT NOT NULL COMMENT '点评内容',
                `score` INT NULL COMMENT '评分（1-5分）',
                `tags` VARCHAR(255) NULL COMMENT '标签（逗号分隔，如：学习能力强,团队合作好）',
                `is_public` VARCHAR(20) NOT NULL DEFAULT 'PRIVATE' COMMENT '是否公开（PRIVATE-仅教师可见，PUBLIC-公开）',
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                INDEX `idx_teacher_id` (`teacher_id`),
                INDEX `idx_student_id` (`student_id`),
                INDEX `idx_created_at` (`created_at`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生点评表';
        """))
        print("✅ student_comments表创建成功")


if __name__ == "__main__":
    asyncio.run(create_table())



