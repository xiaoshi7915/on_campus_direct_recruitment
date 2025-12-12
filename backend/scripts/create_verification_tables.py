"""
创建认证相关数据库表
"""
import sys
import asyncio

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.core.config import settings

# 创建数据库引擎（使用aiomysql驱动）
database_url = settings.DATABASE_URL.replace("mysql+pymysql://", "mysql+aiomysql://")
engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True
)

# 创建异步会话
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_verification_tables():
    """创建认证相关数据库表"""
    async with AsyncSessionLocal() as db:
        try:
            # 创建企业认证申请表
            print("创建enterprise_verifications表...")
            await db.execute(text("""
                CREATE TABLE IF NOT EXISTS enterprise_verifications (
                    id VARCHAR(36) PRIMARY KEY COMMENT '认证ID',
                    enterprise_id VARCHAR(36) NOT NULL COMMENT '企业ID',
                    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '认证状态',
                    business_license_url VARCHAR(255) NULL COMMENT '营业执照URL',
                    legal_person_id_front_url VARCHAR(255) NULL COMMENT '法人身份证正面URL',
                    legal_person_id_back_url VARCHAR(255) NULL COMMENT '法人身份证反面URL',
                    authorization_letter_url VARCHAR(255) NULL COMMENT '授权委托书URL',
                    other_documents TEXT NULL COMMENT '其他材料URLs（JSON数组）',
                    reviewer_id VARCHAR(36) NULL COMMENT '审核人ID',
                    review_comment TEXT NULL COMMENT '审核意见',
                    reviewed_at DATETIME NULL COMMENT '审核时间',
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX ix_enterprise_verifications_enterprise_id (enterprise_id),
                    INDEX ix_enterprise_verifications_status (status),
                    FOREIGN KEY (enterprise_id) REFERENCES enterprise_profiles(id) ON DELETE CASCADE,
                    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业认证申请表'
            """))
            
            # 创建个人身份认证申请表
            print("创建personal_verifications表...")
            await db.execute(text("""
                CREATE TABLE IF NOT EXISTS personal_verifications (
                    id VARCHAR(36) PRIMARY KEY COMMENT '认证ID',
                    user_id VARCHAR(36) NOT NULL COMMENT '用户ID',
                    user_type VARCHAR(20) NOT NULL COMMENT '用户类型',
                    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '认证状态',
                    id_card_front_url VARCHAR(255) NULL COMMENT '身份证正面URL',
                    id_card_back_url VARCHAR(255) NULL COMMENT '身份证反面URL',
                    real_name VARCHAR(50) NULL COMMENT '真实姓名',
                    id_card_number VARCHAR(18) NULL COMMENT '身份证号',
                    other_documents TEXT NULL COMMENT '其他材料URLs（JSON数组）',
                    reviewer_id VARCHAR(36) NULL COMMENT '审核人ID',
                    review_comment TEXT NULL COMMENT '审核意见',
                    reviewed_at DATETIME NULL COMMENT '审核时间',
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX ix_personal_verifications_user_id (user_id),
                    INDEX ix_personal_verifications_status (status),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='个人身份认证申请表'
            """))
            
            await db.commit()
            print("✅ 认证相关表创建成功")
            
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
    print("创建认证相关数据库表")
    print("=" * 60)
    await create_verification_tables()
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

