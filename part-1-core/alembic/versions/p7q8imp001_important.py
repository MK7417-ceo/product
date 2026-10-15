"""Add is_important to curriculum modules and lessons (⭐ highlight)."""
from alembic import op
import sqlalchemy as sa

revision = "p7q8imp001"
down_revision = "n5o6merge001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("curriculum_modules",
                  sa.Column("is_important", sa.Boolean(), nullable=False, server_default="0"))
    op.add_column("curriculum_lessons",
                  sa.Column("is_important", sa.Boolean(), nullable=False, server_default="0"))
    # Mark key placement modules as important
    important_modules = [
        "arrays-strings", "linked-lists", "stacks-queues", "trees-graphs",
        "dynamic-programming", "sorting-searching",
        "sql", "normalization", "transactions",
        "processes", "scheduling", "synchronization", "memory",
        "osi-tcpip", "routing",
    ]
    for slug in important_modules:
        op.execute(
            f"UPDATE curriculum_modules SET is_important = 1 WHERE slug LIKE '%{slug}%'"
        )


def downgrade() -> None:
    op.drop_column("curriculum_lessons", "is_important")
    op.drop_column("curriculum_modules", "is_important")
