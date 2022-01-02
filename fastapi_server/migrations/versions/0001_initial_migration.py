"""Initial Migration3

Revision ID: 849d12c13c8a
Revises:
Create Date: 2021-12-19 17:06:36.345137

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = '849d12c13c8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user', sa.Column('id', sa.Integer(), nullable=True),
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('password_hashed', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False), sa.Column('is_disabled', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False), sa.PrimaryKeyConstraint('id', 'username', 'email')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_is_admin'), 'user', ['is_admin'], unique=False)
    op.create_index(op.f('ix_user_is_disabled'), 'user', ['is_disabled'], unique=False)
    op.create_index(op.f('ix_user_is_verified'), 'user', ['is_verified'], unique=False)
    op.create_index(op.f('ix_user_password_hashed'), 'user', ['password_hashed'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_password_hashed'), table_name='user')
    op.drop_index(op.f('ix_user_is_verified'), table_name='user')
    op.drop_index(op.f('ix_user_is_disabled'), table_name='user')
    op.drop_index(op.f('ix_user_is_admin'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###