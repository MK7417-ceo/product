"""Allow NULL password_hash for OAuth users.

Revision ID: j0k1oauth001
Revises: i9j0bill01
"""
from alembic import op
import sqlalchemy as sa

revision = "j0k1oauth001"
down_revision = "i9j0bill01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # OAuth users have no password; empty-string workaround replaced by real NULL.
    # Convert existing "" to NULL for cleanliness, then allow NULL.
    op.execute("UPDATE users SET password_hash = NULL WHERE password_hash = ''")
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("password_hash", existing_type=sa.Text(), nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("password_hash", existing_type=sa.Text(), nullable=False)
