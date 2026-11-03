"""AI/RAG answers — DB-first doubt solver storage.

PENDING LLM answers live here but are NEVER served as DB hits until an
admin approves them (see domain/ai_answer.py). Only APPROVED rows are
returned by the DB-first lookup.
"""
from alembic import op
import sqlalchemy as sa

revision = "v7w8ai001"
down_revision = "u6v7pwd001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_answers",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("question", sa.Text, nullable=False),
        sa.Column("normalized_question", sa.String(500), nullable=False,
                  index=True),
        sa.Column("answer", sa.Text, nullable=False),
        sa.Column("source", sa.String(16), nullable=False,
                  server_default="llm"),
        sa.Column("status", sa.String(16), nullable=False,
                  server_default="pending", index=True),
        sa.Column("topic_slug", sa.String(80), nullable=False,
                  server_default=""),
        sa.Column("created_by", sa.String(36), nullable=False,
                  server_default=""),
        sa.Column("approved_by", sa.String(36), nullable=False,
                  server_default=""),
        sa.Column("embedding_json", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("ai_answers")
