"""添加全文搜索索引

Revision ID: 002_add_fulltext_indexes
Revises: 001_initial
Create Date: 2025-12-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_fulltext_indexes'
down_revision = None  # 这是第一个迁移文件
branch_labels = None
depends_on = None


def upgrade():
    # 为jobs表创建全文索引（MySQL不支持IF NOT EXISTS，需要先检查）
    conn = op.get_bind()
    # 检查索引是否已存在
    result = conn.execute(sa.text("SHOW INDEX FROM jobs WHERE Key_name = 'idx_jobs_fulltext'"))
    if not result.fetchone():
        op.execute("""
            CREATE FULLTEXT INDEX idx_jobs_fulltext 
            ON jobs(title, description, requirements)
        """)
    
    # 为resumes表创建全文索引
    result = conn.execute(sa.text("SHOW INDEX FROM resumes WHERE Key_name = 'idx_resumes_fulltext'"))
    if not result.fetchone():
        op.execute("""
            CREATE FULLTEXT INDEX idx_resumes_fulltext 
            ON resumes(content)
        """)


def downgrade():
    # 删除全文索引
    op.execute("DROP INDEX IF EXISTS idx_jobs_fulltext ON jobs")
    op.execute("DROP INDEX IF EXISTS idx_resumes_fulltext ON resumes")


