"""Domain: curriculum — expert-level training structure. PURE — no framework, no DB.

Curriculum = domains → modules → lessons → questions (difficulty 1-10).
Study plans generate day-wise daily tasks from this structure.

Key design decisions:
- Difficulty is 1-10 (gradual ramp: 1-3 basic, 4-6 intermediate, 7-8 advanced, 9-10 expert)
- Questions explain WHY (explanation field) — this is for LEARNING, not just testing
- company_tags track which companies ask this (placement prep)
- The UI must NOT show "coding/non-coding" labels — the user just picks a domain
  and we ask: "scratch se seekhoge ya kuch aata hai?" (start_level)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

from app.domain.user import DomainError

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

VALID_CATEGORIES = ("cs-core", "language", "tech-domain")
VALID_START_LEVELS = ("scratch", "beginner", "intermediate")
VALID_TASK_TYPES = ("learn", "practice", "code", "revise", "mock")
VALID_TASK_STATUS = ("pending", "done", "skipped")
VALID_PLAN_STATUS = ("active", "completed", "paused")
VALID_QTYPES = ("mcq", "coding", "written")

# Difficulty bands (for display / ramp logic)
DIFFICULTY_BANDS = {
    (1, 3): "basic",
    (4, 6): "intermediate",
    (7, 8): "advanced",
    (9, 10): "expert",
}


def difficulty_band(difficulty: int) -> str:
    """Map 1-10 difficulty to a band name."""
    for (lo, hi), band in DIFFICULTY_BANDS.items():
        if lo <= difficulty <= hi:
            return band
    raise DomainError(f"difficulty must be 1-10, got {difficulty}")


def validate_slug(slug: str, what: str = "slug") -> str:
    cleaned = (slug or "").strip().lower()
    if not cleaned or not _SLUG_RE.match(cleaned):
        raise DomainError(f"invalid {what}: use lowercase letters, digits, dashes")
    if len(cleaned) > 80:
        raise DomainError(f"{what} too long (max 80)")
    return cleaned


def validate_category(category: str) -> str:
    cleaned = (category or "").strip().lower()
    if cleaned not in VALID_CATEGORIES:
        raise DomainError(f"invalid category: must be one of {VALID_CATEGORIES}")
    return cleaned


def validate_difficulty(difficulty: int) -> int:
    try:
        d = int(difficulty)
    except (TypeError, ValueError):
        raise DomainError("difficulty must be an integer 1-10")
    if not 1 <= d <= 10:
        raise DomainError("difficulty must be 1-10")
    return d


def validate_qtype(qtype: str) -> str:
    cleaned = (qtype or "").strip().lower()
    if cleaned not in VALID_QTYPES:
        raise DomainError(f"invalid qtype: must be one of {VALID_QTYPES}")
    return cleaned


def validate_start_level(level: str) -> str:
    cleaned = (level or "").strip().lower()
    if cleaned not in VALID_START_LEVELS:
        raise DomainError(f"invalid start_level: must be one of {VALID_START_LEVELS}")
    return cleaned


def validate_task_type(task_type: str) -> str:
    cleaned = (task_type or "").strip().lower()
    if cleaned not in VALID_TASK_TYPES:
        raise DomainError(f"invalid task_type: must be one of {VALID_TASK_TYPES}")
    return cleaned


def validate_task_status(status: str) -> str:
    cleaned = (status or "").strip().lower()
    if cleaned not in VALID_TASK_STATUS:
        raise DomainError(f"invalid task status: must be one of {VALID_TASK_STATUS}")
    return cleaned


# ---------------------------------------------------------------- entities

@dataclass(frozen=True)
class CurriculumDomain:
    id: str
    slug: str
    name: str
    icon: str = ""
    description: str = ""
    category: str = "tech-domain"  # cs-core | language | tech-domain
    order_index: int = 0
    is_active: bool = True


@dataclass(frozen=True)
class CurriculumModule:
    id: str
    domain_slug: str
    slug: str
    name: str
    description: str = ""
    order_index: int = 0
    estimated_days: int = 7


@dataclass(frozen=True)
class CurriculumLesson:
    id: str
    module_id: str
    slug: str
    title: str
    content: str = ""  # markdown theory
    order_index: int = 0
    estimated_minutes: int = 30
    has_visual: bool = False  # whether an animated diagram exists


@dataclass(frozen=True)
class CurriculumQuestion:
    id: str
    domain_slug: str
    module_slug: str = ""
    lesson_id: str | None = None
    difficulty: int = 1  # 1-10
    qtype: str = "mcq"  # mcq | coding | written
    prompt: str = ""
    choices: tuple[str, ...] = ()
    answer_index: int | None = None  # mcq only
    explanation: str = ""  # WHY this answer — for learning
    company_tags: tuple[str, ...] = ()  # ["tcs", "amazon", ...]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class StudyPlan:
    id: str
    user_id: str
    domain_slug: str
    start_level: str  # scratch | beginner | intermediate
    total_days: int
    current_day: int = 1
    status: str = "active"  # active | completed | paused
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class DailyTask:
    id: str
    plan_id: str
    day_number: int
    lesson_id: str | None = None
    task_type: str = "learn"  # learn | practice | code | revise | mock
    title: str = ""
    description: str = ""
    question_ids: tuple[str, ...] = ()
    status: str = "pending"  # pending | done | skipped
    due_date: date | None = None


# ---------------------------------------------------------------- validators

def validate_domain(name: str, category: str) -> None:
    if not (name or "").strip():
        raise DomainError("domain name is required")
    if len(name.strip()) > 120:
        raise DomainError("domain name too long (max 120)")
    validate_category(category)


def validate_module(name: str, estimated_days: int) -> None:
    if not (name or "").strip():
        raise DomainError("module name is required")
    if len(name.strip()) > 120:
        raise DomainError("module name too long (max 120)")
    try:
        days = int(estimated_days)
    except (TypeError, ValueError):
        raise DomainError("estimated_days must be an integer")
    if not 1 <= days <= 90:
        raise DomainError("estimated_days must be 1-90")


def validate_lesson(title: str, estimated_minutes: int) -> None:
    if not (title or "").strip():
        raise DomainError("lesson title is required")
    if len(title.strip()) > 200:
        raise DomainError("lesson title too long (max 200)")
    try:
        mins = int(estimated_minutes)
    except (TypeError, ValueError):
        raise DomainError("estimated_minutes must be an integer")
    if not 5 <= mins <= 240:
        raise DomainError("estimated_minutes must be 5-240")


def validate_curriculum_question(qtype: str, prompt: str, difficulty: int,
                                 choices: tuple[str, ...],
                                 answer_index: int | None) -> None:
    if not (prompt or "").strip():
        raise DomainError("question prompt is required")
    validate_difficulty(difficulty)
    if qtype == "mcq":
        if len(choices) < 2:
            raise DomainError("mcq needs at least 2 choices")
        if answer_index is None or not (0 <= answer_index < len(choices)):
            raise DomainError("mcq needs a valid answer_index")
    elif qtype in ("coding", "written"):
        if answer_index is not None:
            raise DomainError(f"{qtype} questions must not have answer_index")


def validate_study_plan(start_level: str, total_days: int) -> None:
    validate_start_level(start_level)
    try:
        days = int(total_days)
    except (TypeError, ValueError):
        raise DomainError("total_days must be an integer")
    if not 7 <= days <= 365:
        raise DomainError("total_days must be 7-365")


# ---------------------------------------------------------------- plan generation

def plan_task_types_for_day(day_number: int, total_days: int) -> list[str]:
    """Decide which task types a given day gets.

    Rhythm: learn → practice → (code for hands-on) → revise every 7th day →
    mock every 14th day. This gives the "daily task" feel with variety.
    """
    types = ["learn", "practice"]
    if day_number % 3 == 0:
        types.append("code")
    if day_number % 7 == 0:
        types.append("revise")
    if day_number % 14 == 0:
        types.append("mock")
    # Last day is always a mock (final assessment)
    if day_number == total_days and "mock" not in types:
        types.append("mock")
    return types


def difficulty_for_day(day_number: int, total_days: int, start_level: str) -> int:
    """Gradual ramp: difficulty rises from start_level's floor to 10.

    scratch → starts at 1, beginner → starts at 3, intermediate → starts at 5.
    Never jumps straight to hard — "dheere dheere level badhega".
    """
    floors = {"scratch": 1, "beginner": 3, "intermediate": 5}
    floor = floors[start_level]
    if total_days <= 1:
        return floor
    progress = (day_number - 1) / (total_days - 1)  # 0.0 → 1.0
    return min(10, floor + int(progress * (10 - floor)))
