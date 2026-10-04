"""F2: profiles + placement_sessions tables."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "c3f2onboard01"
down_revision = "b2f1auth0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("education", sa.Text(), nullable=False),
        sa.Column("experience_years", sa.Float(), nullable=False, server_default="0"),
        sa.Column("current_skills", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("target_role", sa.String(120), nullable=False),
        sa.Column("target_domain", sa.String(120), nullable=False),
        sa.Column("target_level", sa.String(16), nullable=False),
        sa.Column("tech_focus", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_profiles_user_id", "profiles", ["user_id"], unique=True)

    op.create_table(
        "placement_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic", sa.String(80), nullable=False),
        sa.Column("claimed_level", sa.String(16), nullable=False),
        sa.Column("question_ids", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("answers", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("status", sa.String(16), nullable=False, server_default="open"),
        sa.Column("correct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("verified_level", sa.String(16), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_placement_sessions_user_id", "placement_sessions", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_placement_sessions_user_id", table_name="placement_sessions")
    op.drop_table("placement_sessions")
    op.drop_index("ix_profiles_user_id", table_name="profiles")
    op.drop_table("profiles")
