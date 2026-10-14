"""Remove redundant profiles.id; user_id becomes the PK.

Revision ID: k1l2prof001
Revises: j0k1oauth001

1:1 table — the separate UUID id is redundant when user_id is already UNIQUE.
"""
from alembic import op
import sqlalchemy as sa

revision = "k1l2prof001"
down_revision = "j0k1oauth001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Recreate profiles with user_id as PK (SQLite needs table rebuild for PK change)
    op.create_table(
        "profiles_new",
        sa.Column("user_id", sa.String(36), primary_key=True),
        sa.Column("education", sa.Text(), nullable=False),
        sa.Column("experience_years", sa.Float(), nullable=False, server_default="0"),
        sa.Column("current_skills", sa.Text(), nullable=False, server_default="'[]'"),
        sa.Column("target_role", sa.String(120), nullable=False),
        sa.Column("target_domain", sa.String(120), nullable=False),
        sa.Column("target_level", sa.String(16), nullable=False),
        sa.Column("tech_focus", sa.Text(), nullable=False, server_default="'[]'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.execute(
        "INSERT INTO profiles_new "
        "(user_id, education, experience_years, current_skills, target_role, "
        " target_domain, target_level, tech_focus, created_at) "
        "SELECT user_id, education, experience_years, current_skills, target_role, "
        " target_domain, target_level, tech_focus, created_at FROM profiles"
    )
    op.drop_table("profiles")
    op.rename_table("profiles_new", "profiles")


def downgrade() -> None:
    # Restore id column (new UUIDs; original values unrecoverable)
    op.create_table(
        "profiles_old",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False, unique=True),
        sa.Column("education", sa.Text(), nullable=False),
        sa.Column("experience_years", sa.Float(), nullable=False, server_default="0"),
        sa.Column("current_skills", sa.Text(), nullable=False, server_default="'[]'"),
        sa.Column("target_role", sa.String(120), nullable=False),
        sa.Column("target_domain", sa.String(120), nullable=False),
        sa.Column("target_level", sa.String(16), nullable=False),
        sa.Column("tech_focus", sa.Text(), nullable=False, server_default="'[]'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.execute(
        "INSERT INTO profiles_old "
        "(id, user_id, education, experience_years, current_skills, target_role, "
        " target_domain, target_level, tech_focus, created_at) "
        "SELECT hex(randomblob(16)), user_id, education, experience_years, "
        " current_skills, target_role, target_domain, target_level, tech_focus, "
        " created_at FROM profiles"
    )
    op.drop_table("profiles")
    op.rename_table("profiles_old", "profiles")
