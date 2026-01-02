"""add job intention fields

Revision ID: 006
Revises: 005_add_school_extended_fields
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005_add_school_extended_fields'
branch_labels = None
depends_on = None


def upgrade():
    # 添加新字段到job_intentions表（如果不存在）
    conn = op.get_bind()
    
    columns_to_add = [
        ('job_type_list', sa.Text(), '职位类型列表（JSON数组）'),
        ('industry_list', sa.Text(), '行业列表（JSON数组，包含一级和二级行业）'),
        ('work_location_list', sa.Text(), '工作地点列表（JSON数组）'),
        ('job_nature', sa.String(20), '求职类型：FULL_TIME（全职）、PART_TIME（兼职）'),
        ('salary_min', sa.Integer(), '期望薪资最小值（单位：千元/月）'),
        ('salary_max', sa.Integer(), '期望薪资最大值（单位：千元/月）'),
        ('part_time_days', sa.String(50), '兼职每周工作天数'),
        ('work_time_slot', sa.String(50), '兼职工作时间段'),
    ]
    
    for col_name, col_type, comment in columns_to_add:
        result = conn.execute(sa.text(f"SHOW COLUMNS FROM job_intentions LIKE '{col_name}'"))
        if not result.fetchone():
            op.add_column('job_intentions', sa.Column(col_name, col_type, nullable=True, comment=comment))


def downgrade():
    op.drop_column('job_intentions', 'work_time_slot')
    op.drop_column('job_intentions', 'part_time_days')
    op.drop_column('job_intentions', 'salary_max')
    op.drop_column('job_intentions', 'salary_min')
    op.drop_column('job_intentions', 'job_nature')
    op.drop_column('job_intentions', 'work_location_list')
    op.drop_column('job_intentions', 'industry_list')
    op.drop_column('job_intentions', 'job_type_list')

