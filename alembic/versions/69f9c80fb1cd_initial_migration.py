"""Initial migration

Revision ID: 69f9c80fb1cd
Revises: 
Create Date: 2024-06-19 10:33:32.677065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69f9c80fb1cd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='auth'
    )
    op.create_index(op.f('ix_auth_users_email'), 'users', ['email'], unique=True, schema='auth')
    op.create_index(op.f('ix_auth_users_id'), 'users', ['id'], unique=False, schema='auth')
    op.create_index(op.f('ix_auth_users_username'), 'users', ['username'], unique=True, schema='auth')
    op.drop_table('alembic_version')
    op.drop_index('ix_articles_content', table_name='articles')
    op.drop_index('ix_articles_id', table_name='articles')
    op.drop_index('ix_articles_title', table_name='articles')
    op.drop_table('articles')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='articles_pkey')
    )
    op.create_index('ix_articles_title', 'articles', ['title'], unique=False)
    op.create_index('ix_articles_id', 'articles', ['id'], unique=False)
    op.create_index('ix_articles_content', 'articles', ['content'], unique=False)
    op.create_table('alembic_version',
    sa.Column('version_num', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('version_num', name='alembic_version_pkc')
    )
    op.drop_index(op.f('ix_auth_users_username'), table_name='users', schema='auth')
    op.drop_index(op.f('ix_auth_users_id'), table_name='users', schema='auth')
    op.drop_index(op.f('ix_auth_users_email'), table_name='users', schema='auth')
    op.drop_table('users', schema='auth')
    # ### end Alembic commands ###