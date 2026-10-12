"""F3: assessment_sessions table."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "d4f3assess001"
down_revision = "c3f2onboard01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assessment_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic", sa.String(80), nullable=False),
        sa.Column("level", sa.String(16), nullable=False),
        sa.Column("question_ids", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("answers", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("status", sa.String(16), nullable=False, server_default="open"),
        sa.Column("correct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("gaps", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_assessment_sessions_user_id", "assessment_sessions", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_assessment_sessions_user_id", table_name="assessment_sessions")
    op.drop_table("assessment_sessions")
