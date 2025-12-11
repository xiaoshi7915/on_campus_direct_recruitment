"""
创建marks表的脚本
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def create_marks_table():
    """创建marks表"""
    async with engine.connect() as conn:
        # 检查表是否存在
        check_table = text("""
            SELECT COUNT(*) as count
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
            AND table_name = 'marks'
        """)
        result = await conn.execute(check_table)
        table_exists = result.scalar() > 0
        
        if table_exists:
            print("marks表已存在，跳过创建")
            return
        
        # 创建marks表（先创建表，再添加外键约束）
        create_table = text("""
            CREATE TABLE marks (
                id VARCHAR(36) PRIMARY KEY COMMENT '标记ID',
                user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
                target_type VARCHAR(20) NOT NULL COMMENT '标记类型：RESUME, SCHOOL等',
                target_id VARCHAR(36) NOT NULL COMMENT '目标ID',
                note TEXT COMMENT '备注',
                color VARCHAR(20) DEFAULT 'blue' COMMENT '标记颜色',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                INDEX idx_user_id (user_id),
                INDEX idx_target (target_type, target_id),
                UNIQUE KEY uq_mark (user_id, target_type, target_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标记表'
        """)
        
        await conn.execute(create_table)
        await conn.commit()
        
        # 添加外键约束（如果users表存在）
        try:
            add_fk = text("""
                ALTER TABLE marks
                ADD CONSTRAINT fk_marks_user
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            """)
            await conn.execute(add_fk)
            await conn.commit()
            print("✅ marks表创建成功，外键约束已添加")
        except Exception as e:
            print(f"⚠️ marks表创建成功，但外键约束添加失败（可能users表不存在）: {e}")
            print("✅ marks表已创建，可以手动添加外键约束")


if __name__ == "__main__":
    asyncio.run(create_marks_table())
