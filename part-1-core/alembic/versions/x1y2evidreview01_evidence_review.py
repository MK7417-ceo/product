"""Add evidence review lifecycle and reviewer audit fields.

Revision ID: x1y2evidreview01
Revises: w9x0merge001
"""
from alembic import op
import sqlalchemy as sa

revision = "x1y2evidreview01"
down_revision = "w9x0merge001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Batch mode is required for SQLite table rebuilds when adding the
    # reviewer foreign key. It also remains valid on PostgreSQL.
    with op.batch_alter_table("evidence") as batch_op:
        batch_op.add_column(
            sa.Column("status", sa.String(length=24), nullable=False,
                      server_default="legacy_unverified"),
        )
        batch_op.add_column(
            sa.Column("reviewed_by", sa.String(length=36), nullable=True),
        )
        batch_op.add_column(
            sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        )
        batch_op.add_column(
            sa.Column("review_note", sa.Text(), nullable=False, server_default=""),
        )
        batch_op.create_foreign_key(
            "fk_evidence_reviewed_by_users", "users",
            ["reviewed_by"], ["id"], ondelete="SET NULL",
        )
    op.create_index("ix_evidence_status", "evidence", ["status"])

    # Historical v1 submissions auto-completed roadmap tasks. They were never
    # independently reviewed, so preserve the record without calling it verified.
    op.execute("""
        UPDATE roadmap_tasks
        SET status = 'in_progress'
        WHERE status = 'completed'
          AND EXISTS (
              SELECT 1 FROM evidence
              WHERE evidence.roadmap_id = roadmap_tasks.roadmap_id
                AND evidence.task_key = roadmap_tasks.task_key
          )
    """)


def downgrade() -> None:
    op.drop_index("ix_evidence_status", table_name="evidence")
    with op.batch_alter_table("evidence") as batch_op:
        batch_op.drop_constraint("fk_evidence_reviewed_by_users", type_="foreignkey")
        batch_op.drop_column("review_note")
        batch_op.drop_column("reviewed_at")
        batch_op.drop_column("reviewed_by")
        batch_op.drop_column("status")
