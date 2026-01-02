"""add_school_id_to_chat_sessions

Revision ID: 004_add_school_id_to_chat_sessions
Revises: 003_add_materials_to_info_sessions
Create Date: 2024-12-12 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_school_id_to_chat_sessions'
down_revision = '003_add_materials_to_info_sessions'
branch_labels = None
depends_on = None


def upgrade():
    # 添加school_id字段（如果不存在）
    conn = op.get_bind()
    result = conn.execute(sa.text("SHOW COLUMNS FROM chat_sessions LIKE 'school_id'"))
    if not result.fetchone():
        op.add_column('chat_sessions', sa.Column('school_id', sa.String(36), nullable=True, comment='学校ID（如果与学校聊天）'))
    
    # 添加外键约束（如果不存在）
    result = conn.execute(sa.text("""
        SELECT CONSTRAINT_NAME 
        FROM information_schema.TABLE_CONSTRAINTS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'chat_sessions' 
        AND CONSTRAINT_NAME = 'fk_chat_sessions_school_id'
    """))
    if not result.fetchone():
        op.create_foreign_key(
            'fk_chat_sessions_school_id',
            'chat_sessions', 'schools',
            ['school_id'], ['id'],
            ondelete='CASCADE'
        )
    
    # 添加索引（如果不存在）
    result = conn.execute(sa.text("SHOW INDEX FROM chat_sessions WHERE Key_name = 'ix_chat_sessions_school_id'"))
    if not result.fetchone():
        op.create_index('ix_chat_sessions_school_id', 'chat_sessions', ['school_id'])
    
    # 注意：由于MySQL不支持部分唯一约束，我们需要在应用层确保唯一性
    # 对于用户-用户聊天：user1_id + user2_id 唯一（user2_id不为空，school_id为空）
    # 对于用户-学校聊天：user1_id + school_id 唯一（school_id不为空，user2_id为空）


def downgrade():
    # 删除索引
    op.drop_index('ix_chat_sessions_school_id', table_name='chat_sessions')
    
    # 删除外键约束
    op.drop_constraint('fk_chat_sessions_school_id', 'chat_sessions', type_='foreignkey')
    
    # 删除字段
    op.drop_column('chat_sessions', 'school_id')

