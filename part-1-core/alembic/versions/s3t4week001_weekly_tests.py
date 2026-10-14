"""Weekly tests table — scheduled 20-question assessments per study plan."""
from alembic import op
import sqlalchemy as sa

revision = "s3t4week001"
down_revision = "r1s2news001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "weekly_tests",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("domain_slug", sa.String(80), nullable=False, index=True),
        sa.Column("plan_id", sa.String(36),
                  sa.ForeignKey("study_plans.id", ondelete="SET NULL"),
                  nullable=True, index=True),
        sa.Column("week_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("scheduled_date", sa.Date(), nullable=False, index=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="scheduled"),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total_questions", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("question_ids", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("answers", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("weekly_tests")
