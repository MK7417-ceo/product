"""SQLAlchemy models — adapter-side (the domain never imports these)."""
from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="user")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expires_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(nullable=False, default=False)


class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    education: Mapped[str] = mapped_column(Text, nullable=False)
    experience_years: Mapped[float] = mapped_column(nullable=False, default=0)
    current_skills: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON list
    target_role: Mapped[str] = mapped_column(String(120), nullable=False)
    target_domain: Mapped[str] = mapped_column(String(120), nullable=False)
    target_level: Mapped[str] = mapped_column(String(16), nullable=False)
    tech_focus: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON list
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class PlacementModel(Base):
    __tablename__ = "placement_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(80), nullable=False)
    claimed_level: Mapped[str] = mapped_column(String(16), nullable=False)
    question_ids: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON list
    answers: Mapped[str] = mapped_column(Text, nullable=False, default="{}")  # JSON dict
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")
    correct: Mapped[int] = mapped_column(nullable=False, default=0)
    total: Mapped[int] = mapped_column(nullable=False, default=0)
    verified_level: Mapped[str] = mapped_column(String(16), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class AssessmentModel(Base):
    __tablename__ = "assessment_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(80), nullable=False)
    level: Mapped[str] = mapped_column(String(16), nullable=False)
    question_ids: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON list
    answers: Mapped[str] = mapped_column(Text, nullable=False, default="{}")  # JSON dict
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")
    correct: Mapped[int] = mapped_column(nullable=False, default=0)
    total: Mapped[int] = mapped_column(nullable=False, default=0)
    gaps: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON list of skill tags
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
