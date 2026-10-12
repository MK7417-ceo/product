"""F4: roadmaps + roadmap_tasks tables."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "e5f4roadmap01"
down_revision = "d4f3assess001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roadmaps",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("source", sa.String(80), nullable=False, server_default="manual"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_roadmaps_user_id", "roadmaps", ["user_id"])

    op.create_table(
        "roadmap_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("task_key", sa.String(16), nullable=False),
        sa.Column("roadmap_id", sa.String(36), sa.ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("why_it_matters", sa.Text(), nullable=False, server_default=""),
        sa.Column("target_skills", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("prerequisites", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("effort_minutes", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("priority", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("expected_evidence", sa.Text(), nullable=False, server_default=""),
        sa.Column("acceptance_criteria", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_roadmap_tasks_roadmap_id", "roadmap_tasks", ["roadmap_id"])


def downgrade() -> None:
    op.drop_index("ix_roadmap_tasks_roadmap_id", table_name="roadmap_tasks")
    op.drop_table("roadmap_tasks")
    op.drop_index("ix_roadmaps_user_id", table_name="roadmaps")
    op.drop_table("roadmaps")
