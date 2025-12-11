"""
创建feedback表（如果不存在）
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def create_feedback_table():
    """创建feedback表"""
    async with engine.connect() as conn:
        try:
            # 检查表是否存在（表名是feedbacks）
            result = await conn.execute(text("SHOW TABLES LIKE 'feedbacks'"))
            row = result.fetchone()
            
            if row:
                print("✓ feedbacks表已存在")
            else:
                print("⚠️  feedbacks表不存在，正在创建...")
                # 创建feedbacks表（根据模型定义）
                await conn.execute(text("""
                    CREATE TABLE feedbacks (
                        id VARCHAR(36) PRIMARY KEY COMMENT '反馈ID',
                        user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
                        user_type VARCHAR(20) NOT NULL COMMENT '用户类型',
                        title VARCHAR(100) NOT NULL COMMENT '标题',
                        content TEXT NOT NULL COMMENT '内容',
                        images VARCHAR(500) NULL COMMENT '图片URLs（逗号分隔）',
                        status VARCHAR(20) DEFAULT 'PENDING' NOT NULL COMMENT '状态',
                        reply TEXT NULL COMMENT '回复',
                        replied_at DATETIME NULL COMMENT '回复时间',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL COMMENT '更新时间',
                        INDEX idx_user_id (user_id),
                        INDEX idx_status (status),
                        INDEX idx_created_at (created_at),
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='反馈表'
                """))
                await conn.commit()
                print("✓ feedback表创建成功")
        except Exception as e:
            print(f"✗ 创建feedback表失败: {e}")
            await conn.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(create_feedback_table())

