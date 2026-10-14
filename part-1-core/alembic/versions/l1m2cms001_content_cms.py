"""Content CMS tables: topics, theory_blocks, bank_questions.

Revision ID: l1m2cms001
Revises: i9j0bill01
"""
from alembic import op
import sqlalchemy as sa

revision = "l1m2cms001"
down_revision = "i9j0bill01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "topics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True, index=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("icon", sa.String(80), nullable=False, server_default=""),
        sa.Column("color", sa.String(16), nullable=False, server_default="#8b5cf6"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "theory_blocks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("topic_slug", sa.String(80), nullable=False, index=True),
        sa.Column("level", sa.String(16), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["topic_slug"], ["topics.slug"], ondelete="CASCADE"),
    )
    op.create_table(
        "bank_questions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("topic_slug", sa.String(80), nullable=False, index=True),
        sa.Column("qtype", sa.String(16), nullable=False),
        sa.Column("level", sa.String(16), nullable=False),
        sa.Column("skill_tag", sa.String(80), nullable=False, server_default=""),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("choices", sa.Text(), nullable=True),
        sa.Column("answer_index", sa.Integer(), nullable=True),
        sa.Column("rubric", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["topic_slug"], ["topics.slug"], ondelete="CASCADE"),
    )
    # Seed the two existing topics so CMS and static bank agree.
    op.execute(
        "INSERT INTO topics (id, slug, name, description, is_active, created_at) "
        "VALUES "
        "('seed-python-000000000000000000000001', 'python', 'Python', "
        "'Python programming from basics to advanced', 1, CURRENT_TIMESTAMP), "
        "('seed-mlbasic-00000000000000000000001', 'ml-basics', 'ML Basics', "
        "'Machine learning fundamentals', 1, CURRENT_TIMESTAMP)"
    )


def downgrade() -> None:
    op.drop_table("bank_questions")
    op.drop_table("theory_blocks")
    op.drop_table("topics")
