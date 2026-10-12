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
    tier: Mapped[str] = mapped_column(String(16), nullable=False, default="free")
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


class RoadmapModel(Base):
    __tablename__ = "roadmaps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(nullable=False, default=1)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    source: Mapped[str] = mapped_column(String(80), nullable=False, default="manual")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoadmapTaskModel(Base):
    __tablename__ = "roadmap_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # row uuid
    task_key: Mapped[str] = mapped_column(String(16), nullable=False, index=True)  # logical id (t0001…)
    roadmap_id: Mapped[str] = mapped_column(String(36), ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    why_it_matters: Mapped[str] = mapped_column(Text, nullable=False, default="")
    target_skills: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON list
    prerequisites: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON list
    effort_minutes: Mapped[int] = mapped_column(nullable=False, default=30)
    priority: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    expected_evidence: Mapped[str] = mapped_column(Text, nullable=False, default="")
    acceptance_criteria: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class EvidenceModel(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    roadmap_id: Mapped[str] = mapped_column(String(36), ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False, index=True)
    task_key: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class ResumeModel(Base):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    data: Mapped[str] = mapped_column(Text, nullable=False)  # JSON resume body
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class CertificateModel(Base):
    __tablename__ = "certificates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    ref_id: Mapped[str] = mapped_column(String(64), nullable=False)
    verification_code: Mapped[str] = mapped_column(String(16), nullable=False, unique=True, index=True)
    issued_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False, default="")


class AccountLinkModel(Base):
    __tablename__ = "account_links"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    github: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    linkedin: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    leetcode: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
