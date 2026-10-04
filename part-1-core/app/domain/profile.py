"""Domain: onboarding profile + placement (level verification). PURE.

Skill levels never come from self-report alone: a claimed level must be
verified by answering questions. All scoring is deterministic.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.user import DomainError

LEVELS = ("beginner", "intermediate", "advanced", "expert")


@dataclass(frozen=True)
class Profile:
    id: str
    user_id: str
    education: str
    experience_years: float
    current_skills: tuple[str, ...]
    target_role: str
    target_domain: str
    target_level: str
    tech_focus: tuple[str, ...]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class Question:
    id: str
    topic: str
    level: str
    prompt: str
    choices: tuple[str, ...]
    answer_index: int  # NEVER sent to clients


@dataclass
class Placement:
    id: str
    user_id: str
    topic: str
    claimed_level: str
    question_ids: tuple[str, ...]
    answers: dict[str, int] = field(default_factory=dict)
    status: str = "open"  # open | completed
    correct: int = 0
    total: int = 0
    verified_level: str | None = None


def validate_level(level: str) -> str:
    if level not in LEVELS:
        raise DomainError(f"unknown level: {level}")
    return level


def validate_profile(
    education: str,
    experience_years: float,
    current_skills: list[str],
    target_role: str,
    target_domain: str,
    target_level: str,
    tech_focus: list[str],
) -> None:
    if not education.strip():
        raise DomainError("education is required")
    if experience_years < 0 or experience_years > 60:
        raise DomainError("experience_years out of range")
    if not target_role.strip():
        raise DomainError("target_role is required")
    if not target_domain.strip():
        raise DomainError("target_domain is required")
    validate_level(target_level)
    if not current_skills:
        raise DomainError("list at least one current skill")
    if not tech_focus:
        raise DomainError("tech_focus is required")


def public_question(q: Question) -> dict:
    """Client-safe view: the answer key never leaves the core."""
    return {"id": q.id, "topic": q.topic, "level": q.level,
            "prompt": q.prompt, "choices": list(q.choices)}


def score_placement(questions: list[Question], answers: dict[str, int]) -> tuple[int, int]:
    correct = sum(1 for q in questions if answers.get(q.id) == q.answer_index)
    return correct, len(questions)


def verify_level(claimed: str, ratio: float) -> str:
    """Map a score ratio to a verified level, stepping down from the claim."""
    idx = LEVELS.index(claimed)
    if ratio >= 0.7:
        return claimed
    if ratio >= 0.4:
        return LEVELS[max(0, idx - 1)]
    return LEVELS[max(0, idx - 2)]
