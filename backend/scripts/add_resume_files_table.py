"""
创建 resume_files 表以支持一个简历多个附件文件
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


async def create_resume_files_table():
    """创建resume_files表（支持一个简历多个附件）"""
    async with engine.begin() as conn:
        # 先检查表是否存在
        check_result = await conn.execute(text("SHOW TABLES LIKE 'resume_files'"))
        if check_result.fetchone():
            print("✅ resume_files表已存在")
            return
        
        # 创建resume_files表
        await conn.execute(text("""
            CREATE TABLE `resume_files` (
                `id` VARCHAR(36) NOT NULL PRIMARY KEY COMMENT '文件ID',
                `resume_id` VARCHAR(36) NOT NULL COMMENT '简历ID',
                `file_url` VARCHAR(500) NOT NULL COMMENT '文件URL',
                `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
                `file_size` INT NULL COMMENT '文件大小（字节）',
                `file_type` VARCHAR(50) NULL COMMENT '文件类型（PDF、Word等）',
                `upload_order` INT DEFAULT 0 COMMENT '上传顺序',
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                INDEX `idx_resume_id` (`resume_id`),
                INDEX `idx_upload_order` (`resume_id`, `upload_order`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='简历附件文件表'
        """))
        print("✅ 成功创建 resume_files 表")


if __name__ == "__main__":
    asyncio.run(create_resume_files_table())



