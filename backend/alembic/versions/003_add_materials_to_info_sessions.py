"""添加materials字段到info_sessions表

Revision ID: 003_add_materials_to_info_sessions
Revises: 002_add_fulltext_indexes
Create Date: 2025-12-12

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_materials_to_info_sessions'
down_revision = '002_add_fulltext_indexes'
branch_labels = None
depends_on = None


def upgrade():
    # 添加materials字段到info_sessions表
    op.add_column('info_sessions', 
        sa.Column('materials', sa.Text(), nullable=True, comment='宣讲会资料URLs（JSON数组，存储多个文件URL）')
    )


def downgrade():
    # 删除materials字段
    op.drop_column('info_sessions', 'materials')

