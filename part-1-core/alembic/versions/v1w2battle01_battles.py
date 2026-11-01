"""1v1 battles table — queue, challenge, live and finished battles."""
from alembic import op
import sqlalchemy as sa

revision = "v1w2battle01"
down_revision = "u6v7pwd001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "battles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("topic", sa.String(80), nullable=False, index=True),
        sa.Column("bracket", sa.String(16), nullable=False, index=True),
        sa.Column("level", sa.String(16), nullable=False, server_default=""),
        sa.Column("question_ids", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("player1_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("player2_id", sa.String(36),
                  sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=True, index=True),
        sa.Column("invite_email", sa.String(320), nullable=True),
        sa.Column("invite_code", sa.String(16), nullable=True, unique=True, index=True),
        sa.Column("rematch_of", sa.String(36), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="waiting"),
        sa.Column("window_seconds", sa.Integer(), nullable=False, server_default="180"),
        sa.Column("player1_answers", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("player2_answers", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("player1_times", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("player2_times", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("player1_score", sa.Integer(), nullable=True),
        sa.Column("player2_score", sa.Integer(), nullable=True),
        sa.Column("player1_correct", sa.Integer(), nullable=True),
        sa.Column("player2_correct", sa.Integer(), nullable=True),
        sa.Column("winner_id", sa.String(36), nullable=True),
        sa.Column("flagged", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("flag_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("rewards", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("battles")
