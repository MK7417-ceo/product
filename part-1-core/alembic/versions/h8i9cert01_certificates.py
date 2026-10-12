"""P3b: certificates table."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "h8i9cert01"
down_revision = "g7h8launch01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "certificates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("ref_id", sa.String(64), nullable=False),
        sa.Column("verification_code", sa.String(16), nullable=False, unique=True),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False, server_default=""),
        sa.UniqueConstraint("user_id", "kind", "ref_id",
                            name="uq_certificates_user_ref"),
    )
    op.create_index("ix_certificates_user_id", "certificates", ["user_id"])
    op.create_index("ix_certificates_code", "certificates", ["verification_code"])


def downgrade() -> None:
    # dropping the table removes its constraints; no ALTER needed
    op.drop_index("ix_certificates_code", table_name="certificates")
    op.drop_index("ix_certificates_user_id", table_name="certificates")
    op.drop_table("certificates")
