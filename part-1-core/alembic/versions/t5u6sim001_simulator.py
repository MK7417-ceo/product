"""Placement Simulator tables — attempts and per-round results."""
from alembic import op
import sqlalchemy as sa

revision = "t5u6sim001"
down_revision = "s3t4week001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "simulator_attempts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("company", sa.String(80), nullable=False, server_default="general"),
        sa.Column("status", sa.String(16), nullable=False, server_default="in_progress"),
        sa.Column("current_round", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("final_score", sa.Integer(), nullable=True),
        sa.Column("coins_earned", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_table(
        "simulator_rounds",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("attempt_id", sa.String(36),
                  sa.ForeignKey("simulator_attempts.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("round_name", sa.String(80), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("passed", sa.Boolean(), nullable=True),
        sa.Column("question_ids", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("answers", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("simulator_rounds")
    op.drop_table("simulator_attempts")
