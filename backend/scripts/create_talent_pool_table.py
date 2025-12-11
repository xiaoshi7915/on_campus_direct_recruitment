"""
创建企业人才库表
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def create_talent_pool_table():
    """创建talent_pools表"""
    async with engine.connect() as conn:
        try:
            # 检查表是否存在
            result = await conn.execute(text("SHOW TABLES LIKE 'talent_pools'"))
            row = result.fetchone()
            
            if row:
                print("✓ talent_pools表已存在")
            else:
                print("⚠️  talent_pools表不存在，正在创建...")
                # 创建talent_pools表
                await conn.execute(text("""
                    CREATE TABLE talent_pools (
                        id VARCHAR(36) PRIMARY KEY COMMENT '人才库ID',
                        enterprise_id VARCHAR(36) NOT NULL COMMENT '企业ID',
                        student_id VARCHAR(36) NOT NULL COMMENT '学生ID',
                        resume_id VARCHAR(36) NULL COMMENT '简历ID',
                        status VARCHAR(20) DEFAULT 'ALL' NOT NULL COMMENT '状态：ALL, FAVORITED, COMMUNICATING, INTERVIEWED, HIRED',
                        application_id VARCHAR(36) NULL COMMENT '申请ID',
                        interview_id VARCHAR(36) NULL COMMENT '面试ID',
                        offer_id VARCHAR(36) NULL COMMENT 'Offer ID',
                        notes TEXT NULL COMMENT '备注',
                        tags VARCHAR(255) NULL COMMENT '标签（逗号分隔）',
                        first_contact_time DATETIME NULL COMMENT '首次接触时间',
                        last_contact_time DATETIME NULL COMMENT '最后联系时间',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL COMMENT '更新时间',
                        UNIQUE KEY uq_enterprise_student (enterprise_id, student_id),
                        INDEX idx_enterprise_id (enterprise_id),
                        INDEX idx_student_id (student_id),
                        INDEX idx_enterprise_status (enterprise_id, status),
                        INDEX idx_last_contact_time (last_contact_time),
                        FOREIGN KEY (enterprise_id) REFERENCES enterprise_profiles(id) ON DELETE CASCADE,
                        FOREIGN KEY (student_id) REFERENCES student_profiles(id) ON DELETE CASCADE,
                        FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE SET NULL,
                        FOREIGN KEY (application_id) REFERENCES job_applications(id) ON DELETE SET NULL,
                        FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE SET NULL,
                        FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE SET NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='企业人才库表'
                """))
                await conn.commit()
                print("✓ talent_pools表创建成功")
        except Exception as e:
            print(f"✗ 创建talent_pools表失败: {e}")
            await conn.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(create_talent_pool_table())


