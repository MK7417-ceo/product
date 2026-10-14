"""SQLAlchemy models — adapter-side (the domain never imports these)."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, PrimaryKeyConstraint, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

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


class TopicModel(Base):
    """CMS: a learnable tech topic/domain (python, ml-basics, javascript, ...).

    Founder adds new topics here; content (theory + questions) hangs off the slug.
    """
    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    icon: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    color: Mapped[str] = mapped_column(String(16), nullable=False, default="#8b5cf6")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class TheoryModel(Base):
    """CMS: a markdown theory block for a topic + level, ordered for display."""
    __tablename__ = "theory_blocks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    topic_slug: Mapped[str] = mapped_column(
        String(80), ForeignKey("topics.slug", ondelete="CASCADE"), nullable=False, index=True)
    level: Mapped[str] = mapped_column(String(16), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)  # markdown
    order_index: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class BankQuestionModel(Base):
    """CMS: DB-driven question bank. Lives ALONGSIDE the static question_bank.py
    (static bank stays as fallback when a topic has no DB questions)."""
    __tablename__ = "bank_questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    topic_slug: Mapped[str] = mapped_column(
        String(80), ForeignKey("topics.slug", ondelete="CASCADE"), nullable=False, index=True)
    qtype: Mapped[str] = mapped_column(String(16), nullable=False)  # mcq | coding | written
    level: Mapped[str] = mapped_column(String(16), nullable=False)
    skill_tag: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    choices: Mapped[str] = mapped_column(Text, nullable=True)  # JSON list; mcq only
    answer_index: Mapped[int] = mapped_column(nullable=True)  # mcq only
    rubric: Mapped[str] = mapped_column(Text, nullable=True)  # JSON; written only
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


# ---------------------------------------------------------------- curriculum

class CurriculumDomainModel(Base):
    """Curriculum: a learnable domain (B.Tech CS subject, language, tech domain).

    UI rule: never show "coding/non-coding" labels — user picks a domain and we
    ask whether they start from scratch or already know something.
    """
    __tablename__ = "curriculum_domains"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    icon: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    category: Mapped[str] = mapped_column(String(16), nullable=False)  # cs-core|language|tech-domain
    order_index: Mapped[int] = mapped_column(nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)


class CurriculumModuleModel(Base):
    """Curriculum: a module inside a domain (e.g. DSA → arrays-strings)."""
    __tablename__ = "curriculum_modules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    domain_slug: Mapped[str] = mapped_column(
        String(80), ForeignKey("curriculum_domains.slug", ondelete="CASCADE"),
        nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order_index: Mapped[int] = mapped_column(nullable=False, default=0)
    estimated_days: Mapped[int] = mapped_column(nullable=False, default=7)
    is_important: Mapped[bool] = mapped_column(nullable=False, default=False)  # ⭐ highlight for users


class CurriculumLessonModel(Base):
    """Curriculum: a lesson inside a module — markdown theory + optional visual."""
    __tablename__ = "curriculum_lessons"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    module_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("curriculum_modules.id", ondelete="CASCADE"),
        nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")  # markdown
    order_index: Mapped[int] = mapped_column(nullable=False, default=0)
    estimated_minutes: Mapped[int] = mapped_column(nullable=False, default=30)
    has_visual: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_important: Mapped[bool] = mapped_column(nullable=False, default=False)  # ⭐ highlight for users


class CurriculumQuestionModel(Base):
    """Curriculum: questions with 1-10 difficulty, explanation, company tags."""
    __tablename__ = "curriculum_questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    domain_slug: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    module_slug: Mapped[str] = mapped_column(String(80), nullable=False, default="", index=True)
    lesson_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("curriculum_lessons.id", ondelete="SET NULL"),
        nullable=True, index=True)
    difficulty: Mapped[int] = mapped_column(nullable=False, default=1)  # 1-10
    qtype: Mapped[str] = mapped_column(String(16), nullable=False, default="mcq")
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    choices: Mapped[str] = mapped_column(Text, nullable=True)  # JSON; mcq only
    answer_index: Mapped[int] = mapped_column(nullable=True)  # mcq only
    explanation: Mapped[str] = mapped_column(Text, nullable=False, default="")  # why
    company_tags: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class StudyPlanModel(Base):
    """A user's day-wise study plan for one domain."""
    __tablename__ = "study_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True)
    domain_slug: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    start_level: Mapped[str] = mapped_column(String(16), nullable=False)  # scratch|beginner|intermediate
    total_days: Mapped[int] = mapped_column(nullable=False)
    current_day: Mapped[int] = mapped_column(nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class DailyTaskModel(Base):
    """One task on one day of a study plan."""
    __tablename__ = "daily_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    plan_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("study_plans.id", ondelete="CASCADE"),
        nullable=False, index=True)
    day_number: Mapped[int] = mapped_column(nullable=False)
    lesson_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("curriculum_lessons.id", ondelete="SET NULL"),
        nullable=True)
    task_type: Mapped[str] = mapped_column(String(16), nullable=False)  # learn|practice|code|revise|mock
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    question_ids: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    due_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)


class UserStreakModel(Base):
    """Per-user learning streak counters. One row per user."""
    __tablename__ = "user_streaks"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True)
    current_streak: Mapped[int] = mapped_column(nullable=False, default=0)
    longest_streak: Mapped[int] = mapped_column(nullable=False, default=0)
    last_activity_date: Mapped[Date] = mapped_column(Date, nullable=True)
    total_days_active: Mapped[int] = mapped_column(nullable=False, default=0)


class StreakActivityModel(Base):
    """One row per user per active day — powers the 30-day calendar."""
    __tablename__ = "streak_activity"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True)
    activity_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("user_id", "activity_date"),
        PrimaryKeyConstraint("user_id", "activity_date"),
    )


class UserCoinModel(Base):
    """Per-user coin wallet. One row per user."""
    __tablename__ = "user_coins"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    lifetime_earned: Mapped[int] = mapped_column(nullable=False, default=0)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow)


class CoinTransactionModel(Base):
    """Ledger of every coin earn/spend. Append-only."""
    __tablename__ = "coin_transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True)
    amount: Mapped[int] = mapped_column(nullable=False)  # +earn / -spend
    reason: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow)


class TechNewsModel(Base):
    """Cached tech news. Retention: 1 year — older rows auto-deleted by cleanup."""
    __tablename__ = "tech_news"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    source: Mapped[str] = mapped_column(String(60), nullable=False, default="")
    score: Mapped[int] = mapped_column(nullable=False, default=0)
    published_at: Mapped[str] = mapped_column(String(40), nullable=False, default="")
    fetched_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, index=True)
