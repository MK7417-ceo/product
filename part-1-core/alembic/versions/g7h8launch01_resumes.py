"""P3a: resumes table (one JSON resume per user, upsert)."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "g7h8launch01"
down_revision = "f5f6evid0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "resumes",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False, unique=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("data", sa.Text(), nullable=False),  # JSON: summary/skills/exp/projects/edu/links
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_resumes_user_id", "resumes", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_resumes_user_id", table_name="resumes")
    op.drop_table("resumes")
