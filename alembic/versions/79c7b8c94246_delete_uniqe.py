"""Delete uniqe

Revision ID: 79c7b8c94246
Revises: 5a9a7df16e7a
Create Date: 2025-02-02 18:16:44.033047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79c7b8c94246'
down_revision: Union[str, None] = '5a9a7df16e7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('students_user_id_key', 'students', type_='unique')
    op.drop_constraint('teachers_user_id_key', 'teachers', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('teachers_user_id_key', 'teachers', ['user_id'])
    op.create_unique_constraint('students_user_id_key', 'students', ['user_id'])
    # ### end Alembic commands ###
