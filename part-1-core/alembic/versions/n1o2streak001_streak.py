"""User streak tables: user_streaks + streak_activity.

Revision ID: n1o2streak001
Revises: m1n2curr001
"""
from alembic import op
import sqlalchemy as sa

revision = "n1o2streak001"
down_revision = "m1n2curr001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_streaks",
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("longest_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_activity_date", sa.Date(), nullable=True),
        sa.Column("total_days_active", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_table(
        "streak_activity",
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("activity_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "activity_date"),
    )
    op.create_index("ix_streak_activity_user", "streak_activity", ["user_id"])
    op.create_index("ix_streak_activity_date", "streak_activity", ["activity_date"])


def downgrade() -> None:
    op.drop_index("ix_streak_activity_date", table_name="streak_activity")
    op.drop_index("ix_streak_activity_user", table_name="streak_activity")
    op.drop_table("streak_activity")
    op.drop_table("user_streaks")
