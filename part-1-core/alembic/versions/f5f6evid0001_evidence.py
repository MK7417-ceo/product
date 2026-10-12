"""F5: evidence table (append-only proof of work)."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "f5f6evid0001"
down_revision = "e5f4roadmap01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "evidence",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("roadmap_id", sa.String(36), sa.ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_key", sa.String(16), nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_evidence_user_id", "evidence", ["user_id"])
    op.create_index("ix_evidence_roadmap_id", "evidence", ["roadmap_id"])
    op.create_index("ix_evidence_task_key", "evidence", ["task_key"])


def downgrade() -> None:
    op.drop_index("ix_evidence_task_key", table_name="evidence")
    op.drop_index("ix_evidence_roadmap_id", table_name="evidence")
    op.drop_index("ix_evidence_user_id", table_name="evidence")
    op.drop_table("evidence")
