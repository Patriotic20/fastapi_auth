"""Change nullable False

Revision ID: 2208f758cd4d
Revises: a947e689ae57
Create Date: 2025-02-03 16:14:01.852936

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision: str = "2208f758cd4d"
down_revision: Union[str, None] = "a947e689ae57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Ensure that all user_id values exist in users
    op.execute("""
        DELETE FROM students 
        WHERE user_id IS NOT NULL AND user_id NOT IN (SELECT id FROM users)
    """)

    # Ensure there are no NULL values before altering column
    op.execute("""
        UPDATE students 
        SET user_id = (SELECT id FROM users LIMIT 1) 
        WHERE user_id IS NULL
    """)

    # Alter column to be NOT NULL
    op.alter_column("students", "user_id",
                    existing_type=sa.INTEGER(),
                    nullable=False)

    # Add foreign key constraint with ON DELETE CASCADE
    op.create_foreign_key(
        "students_user_id_fkey",  # Explicitly name the constraint
        "students", "users",
        ["user_id"], ["id"],
        ondelete="CASCADE"
    )

def downgrade() -> None:
    # Drop the foreign key constraint
    op.drop_constraint("students_user_id_fkey", "students", type_="foreignkey")

    # Revert column to be nullable
    op.alter_column("students", "user_id",
                    existing_type=sa.INTEGER(),
                    nullable=True)
