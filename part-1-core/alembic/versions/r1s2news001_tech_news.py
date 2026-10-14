"""Tech news cache table with 1-year retention."""
from alembic import op
import sqlalchemy as sa

revision = "r1s2news001"
down_revision = "q9r0coin001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tech_news",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("url", sa.String(1000), nullable=False, unique=True),
        sa.Column("source", sa.String(60), nullable=False, server_default=""),
        sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("published_at", sa.String(40), nullable=False, server_default=""),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )
    op.create_index("ix_tech_news_fetched_at", "tech_news", ["fetched_at"])


def downgrade() -> None:
    op.drop_index("ix_tech_news_fetched_at", table_name="tech_news")
    op.drop_table("tech_news")
