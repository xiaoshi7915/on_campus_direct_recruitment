"""create school_verifications table

Revision ID: 007
Revises: 006
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    # 创建学校认证表
    op.create_table(
        'school_verifications',
        sa.Column('id', sa.String(36), primary_key=True, comment='认证ID'),
        sa.Column('teacher_id', sa.String(36), sa.ForeignKey('teacher_profiles.id', ondelete='CASCADE'), nullable=False, index=True, comment='教师ID'),
        sa.Column('school_id', sa.String(36), sa.ForeignKey('schools.id', ondelete='CASCADE'), nullable=False, index=True, comment='学校ID'),
        sa.Column('status', sa.String(20), nullable=False, index=True, server_default='PENDING', comment='认证状态：PENDING（待审核）、APPROVED（已通过）、REJECTED（已拒绝）'),
        
        # 认证材料
        sa.Column('school_certificate_url', sa.String(255), nullable=True, comment='学校证明文件URL'),
        sa.Column('teacher_certificate_url', sa.String(255), nullable=True, comment='教师工作证明URL'),
        sa.Column('id_card_front_url', sa.String(255), nullable=True, comment='身份证正面URL'),
        sa.Column('id_card_back_url', sa.String(255), nullable=True, comment='身份证反面URL'),
        sa.Column('authorization_letter_url', sa.String(255), nullable=True, comment='授权委托书URL'),
        sa.Column('other_documents', sa.Text(), nullable=True, comment='其他材料URLs（JSON数组）'),
        
        # 联系信息
        sa.Column('contact_person', sa.String(50), nullable=True, comment='联系人'),
        sa.Column('contact_phone', sa.String(20), nullable=True, comment='联系电话'),
        sa.Column('contact_email', sa.String(100), nullable=True, comment='联系邮箱'),

        # 审核信息
        sa.Column('reviewer_id', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, comment='审核人ID'),
        sa.Column('review_comment', sa.Text(), nullable=True, comment='审核意见'),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True, comment='审核时间'),
        
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False, comment='更新时间'),
        
        comment='学校认证申请表'
    )


def downgrade():
    op.drop_table('school_verifications')

