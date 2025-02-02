"""Add role fix

Revision ID: 038ef971c3ac
Revises: fbf8594977a1
Create Date: 2025-01-31 23:54:58.881334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '038ef971c3ac'
down_revision: Union[str, None] = 'fbf8594977a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('student', 'teacher', 'admin', name='userrole'),
               nullable=True,
               existing_server_default=sa.text("'student'::userrole"))
    op.drop_column('users', 'full_name')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('student', 'teacher', 'admin', name='userrole'),
               nullable=False,
               existing_server_default=sa.text("'student'::userrole"))
    # ### end Alembic commands ###
