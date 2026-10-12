"""P3f: tier on users + account_links table."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "i9j0bill01"
down_revision = "h8i9cert01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("tier", sa.String(16), nullable=False,
                                     server_default="free"))
    op.create_table(
        "account_links",
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("github", sa.String(80), nullable=False, server_default=""),
        sa.Column("linkedin", sa.String(80), nullable=False, server_default=""),
        sa.Column("leetcode", sa.String(80), nullable=False, server_default=""),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("account_links")
    op.drop_column("users", "tier")
