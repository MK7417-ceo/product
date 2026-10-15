"""Domain: content CMS. PURE — no framework, no DB, no network imports.

Topics are the unit of "what can be learned" (python, ml-basics, javascript,
...). Theory blocks are ordered markdown lessons per topic+level. Bank
questions are DB-driven questions that live ALONGSIDE the static bank in
adapters/outbound/question_bank.py (static stays as fallback).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.user import DomainError

VALID_LEVELS = ("beginner", "intermediate", "advanced")
VALID_QTYPES = ("mcq", "coding", "written")
_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_slug(slug: str) -> str:
    cleaned = (slug or "").strip().lower()
    if not cleaned or not _SLUG_RE.match(cleaned):
        raise DomainError("invalid topic slug: use lowercase letters, digits, dashes")
    if len(cleaned) > 80:
        raise DomainError("topic slug too long (max 80)")
    return cleaned


def validate_level(level: str) -> str:
    cleaned = (level or "").strip().lower()
    if cleaned not in VALID_LEVELS:
        raise DomainError(f"invalid level: must be one of {VALID_LEVELS}")
    return cleaned


def validate_qtype(qtype: str) -> str:
    cleaned = (qtype or "").strip().lower()
    if cleaned not in VALID_QTYPES:
        raise DomainError(f"invalid qtype: must be one of {VALID_QTYPES}")
    return cleaned


@dataclass(frozen=True)
class Topic:
    id: str
    slug: str
    name: str
    description: str = ""
    icon: str = ""
    color: str = "#8b5cf6"
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class TheoryBlock:
    id: str
    topic_slug: str
    level: str
    title: str
    content: str  # markdown
    order_index: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class BankQuestion:
    id: str
    topic_slug: str
    qtype: str  # mcq | coding | written
    level: str
    prompt: str
    skill_tag: str = ""
    choices: tuple[str, ...] = ()  # mcq only
    answer_index: int | None = None  # mcq only
    rubric: dict = field(default_factory=dict)  # written only
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def validate_topic(name: str, description: str = "", icon: str = "",
                   color: str = "#8b5cf6") -> None:
    if not (name or "").strip():
        raise DomainError("topic name is required")
    if len(name.strip()) > 120:
        raise DomainError("topic name too long (max 120)")


def validate_theory(title: str, content: str) -> None:
    if not (title or "").strip():
        raise DomainError("theory title is required")
    if not (content or "").strip():
        raise DomainError("theory content is required")


def validate_bank_question(qtype: str, prompt: str, choices: tuple[str, ...],
                           answer_index: int | None) -> None:
    if not (prompt or "").strip():
        raise DomainError("question prompt is required")
    if qtype == "mcq":
        if len(choices) < 2:
            raise DomainError("mcq needs at least 2 choices")
        if answer_index is None or not (0 <= answer_index < len(choices)):
            raise DomainError("mcq needs a valid answer_index")
    elif qtype in ("coding", "written"):
        if answer_index is not None:
            raise DomainError(f"{qtype} questions must not have answer_index")
