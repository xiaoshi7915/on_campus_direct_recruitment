"""添加学校扩展字段

Revision ID: 005_add_school_extended_fields
Revises: 004_add_school_id_to_chat_sessions
Create Date: 2025-12-12

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_add_school_extended_fields'
down_revision = '004_add_school_id_to_chat_sessions'
branch_labels = None
depends_on = None


def upgrade():
    # 添加新字段：主管部门、院系介绍、主要专业介绍
    op.add_column('schools', 
        sa.Column('charge_dep', sa.String(255), nullable=True, comment='主管部门')
    )
    op.add_column('schools', 
        sa.Column('department', sa.Text(), nullable=True, comment='院系介绍')
    )
    op.add_column('schools', 
        sa.Column('major', sa.Text(), nullable=True, comment='主要专业介绍')
    )
    
    # 添加扩展字段：双一流、211/985、学校类型、办学性质、办学层次等
    op.add_column('schools', 
        sa.Column('dual_class', sa.String(255), nullable=True, comment='双一流建设学科代码')
    )
    op.add_column('schools', 
        sa.Column('dual_class_name', sa.String(255), nullable=True, comment='双一流建设学科名称')
    )
    op.add_column('schools', 
        sa.Column('f211', sa.String(255), nullable=True, comment='是否211（是/否）')
    )
    op.add_column('schools', 
        sa.Column('f985', sa.String(255), nullable=True, comment='是否985（是/否）')
    )
    op.add_column('schools', 
        sa.Column('school_type', sa.String(255), nullable=True, comment='类型代码')
    )
    op.add_column('schools', 
        sa.Column('school_type_name', sa.String(255), nullable=True, comment='类型名称')
    )
    op.add_column('schools', 
        sa.Column('nature', sa.String(255), nullable=True, comment='办学性质代码')
    )
    op.add_column('schools', 
        sa.Column('nature_name', sa.String(255), nullable=True, comment='办学性质（公办、民办、中外合作等）')
    )
    op.add_column('schools', 
        sa.Column('is_top', sa.String(255), nullable=True, comment='是否顶尖高校（是/否）')
    )
    op.add_column('schools', 
        sa.Column('level', sa.String(255), nullable=True, comment='办学层次代码')
    )
    op.add_column('schools', 
        sa.Column('level_name', sa.String(255), nullable=True, comment='办学层次名称（本科、专科）')
    )


def downgrade():
    # 删除所有新增字段
    op.drop_column('schools', 'level_name')
    op.drop_column('schools', 'level')
    op.drop_column('schools', 'is_top')
    op.drop_column('schools', 'nature_name')
    op.drop_column('schools', 'nature')
    op.drop_column('schools', 'school_type_name')
    op.drop_column('schools', 'school_type')
    op.drop_column('schools', 'f985')
    op.drop_column('schools', 'f211')
    op.drop_column('schools', 'dual_class_name')
    op.drop_column('schools', 'dual_class')
    op.drop_column('schools', 'major')
    op.drop_column('schools', 'department')
    op.drop_column('schools', 'charge_dep')

