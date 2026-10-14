"""Domain: study plan generator. PURE — no DB, no I/O, no network.

Product guarantees (user-mandated, Oct 2026):
- The user picks a DOMAIN (never shown coding/non-coding labels) and their
  prior level: 'scratch' | 'beginner' | 'intermediate'.
- Plans train the user from their level up to EXPERT gradually:
  basic -> ... -> expert, company-level preparation. Difficulty never jumps
  straight to hard.
- Output is month/week/day structured for display.
- Every 7th day = REVISION day. Every 30th day = MOCK TEST day
  (timed, mixed difficulty). Mock wins if a day qualifies for both.
- Deterministic: same (domain_slug, start_level, lessons) -> same plan.

Storage/API contract (study_plans + daily_tasks tables are owned by a
sibling task; this module defines the shapes they must store):

    POST /api/v1/study-plans/preview
      body: {"domain_slug": str, "start_level": str,
             "lessons": [...], "coding": bool}
      -> 200 {"domain_slug", "start_level", "summary", "days"}
      Pure generation, no persistence. Implemented in
      app/api/v1/study_plans.py.

    POST /api/v1/study-plans
      body: same as preview
      -> 201 {"id", "domain_slug", "start_level", "total_days",
              "status": "active", "created_at"}
      -> 501 while the study_plans table is not ready.

    study_plans row: {id, user_id, domain_slug, start_level ("scratch" |
      "beginner" | "intermediate"), total_days, status ("active" |
      "completed" | "abandoned"), created_at}

    daily_tasks row: {id, plan_id, user_id, day, month, week,
      kind ("learn" | "revision" | "mock"), tasks: [task...],
      status ("pending" | "in_progress" | "completed")}
    Task shapes produced by this module:
      learn:    {"type": "learn", "lesson_id", "title", "minutes"}
      practice: {"type": "practice", "count", "difficulty_range": [lo, hi],
                 "minutes"}
      code:     {"type": "code", "count", "minutes"}
      revise:   {"type": "revise", "title", "count", "minutes"}
      mock:     {"type": "mock", "title", "count", "minutes", "timed": True,
                 "difficulty_range": [lo, hi]}
"""
from __future__ import annotations

from math import ceil

from app.domain.user import DomainError

START_LEVELS = ("scratch", "beginner", "intermediate")

TARGET_LEVEL = "Expert"

REVISION_EVERY = 7
MOCK_EVERY = 30

# Pacing per prior level. total_days: scratch ~120, beginner ~90,
# intermediate ~60 (DSA-scale curriculum; shorter domains scale via lessons).
_LEVEL_CONFIG = {
    "scratch": {
        "total_days": 120,
        "start_difficulty": 1,
        "learn_per_day": 2,      # more learning, slower pace
        "learn_minutes": 30,
        "practice_count": 8,
        "practice_minutes": 20,
        "code_count": 1,
        "code_minutes": 30,
    },
    "beginner": {
        "total_days": 90,
        "start_difficulty": 3,
        "learn_per_day": 1,      # balanced
        "learn_minutes": 30,
        "practice_count": 10,
        "practice_minutes": 20,
        "code_count": 2,
        "code_minutes": 40,
    },
    "intermediate": {
        "total_days": 60,
        "start_difficulty": 5,
        "learn_per_day": 1,      # more practice/code
        "learn_minutes": 25,
        "practice_count": 12,
        "practice_minutes": 25,
        "code_count": 3,
        "code_minutes": 45,
    },
}

REVISION_QUESTIONS = 15
REVISION_MINUTES = 30
MOCK_QUESTIONS = 25
MOCK_MINUTES = 60


def _require_level(start_level: str) -> dict:
    try:
        return _LEVEL_CONFIG[start_level]
    except KeyError:
        raise DomainError(
            f"start_level must be one of {START_LEVELS}, got {start_level!r}"
        )


def difficulty_window(day: int, start_level: str) -> tuple[int, int]:
    """Difficulty [lo, hi] for a plan day.

    Ramps basic -> expert over ~90 days, shifted by the user's start level:
    scratch starts at 1, beginner at 3, intermediate at 5. Difficulty 1-10.
    """
    cfg = _require_level(start_level)
    quarter = min(3, (day - 1) // 30)  # 0..3 -> days 1-30, 31-60, 61-90, 91+
    lo = min(cfg["start_difficulty"] + quarter * 2, 8)
    hi = min(10, lo + 3)
    return (lo, hi)


def day_kind(day: int) -> str:
    """'mock' every 30th day, 'revision' every 7th day, else 'learn'."""
    if day % MOCK_EVERY == 0:
        return "mock"
    if day % REVISION_EVERY == 0:
        return "revision"
    return "learn"


def _normalize_lessons(lessons: list) -> list[dict]:
    """Accept lesson dicts or plain title strings; return uniform dicts."""
    out: list[dict] = []
    for i, lesson in enumerate(lessons or []):
        if isinstance(lesson, dict):
            out.append(
                {
                    "id": lesson.get("id", f"lesson-{i + 1}"),
                    "title": lesson.get("title") or f"Lesson {i + 1}",
                }
            )
        else:
            out.append({"id": f"lesson-{i + 1}", "title": str(lesson)})
    return out


def _learn_task(lesson: dict, minutes: int) -> dict:
    return {
        "type": "learn",
        "lesson_id": lesson["id"],
        "title": lesson["title"],
        "minutes": minutes,
    }


def _practice_task(count: int, minutes: int, difficulty_range: list[int]) -> dict:
    return {
        "type": "practice",
        "count": count,
        "difficulty_range": difficulty_range,
        "minutes": minutes,
    }


def _code_task(count: int, minutes: int) -> dict:
    return {"type": "code", "count": count, "minutes": minutes}


def _revision_task(day: int, difficulty_range: list[int]) -> dict:
    week = (day - 1) // 7 + 1
    return {
        "type": "revise",
        "title": f"Revision — Week {week}",
        "count": REVISION_QUESTIONS,
        "difficulty_range": difficulty_range,
        "minutes": REVISION_MINUTES,
    }


def _mock_task(day: int, difficulty_range: list[int]) -> dict:
    return {
        "type": "mock",
        "title": f"Mock Test — Day {day}",
        "count": MOCK_QUESTIONS,
        "difficulty_range": difficulty_range,
        "minutes": MOCK_MINUTES,
        "timed": True,
    }


def generate_plan(
    domain_slug: str,
    start_level: str,
    lessons: list,
    coding: bool = True,
) -> list[dict]:
    """Generate a full day-wise study plan.

    Args:
        domain_slug: topic slug, e.g. "dsa", "python", "networking".
        start_level: 'scratch' | 'beginner' | 'intermediate'.
        lessons: list of lesson dicts {"id", "title"} or plain title strings.
                 Spread evenly across learning days (never on revision/mock).
        coding: whether the domain includes hands-on code tasks.

    Returns:
        [{"day": 1, "month": 1, "week": 1, "kind": "learn",
          "tasks": [...]}, ...]
    """
    cfg = _require_level(start_level)
    if not domain_slug:
        raise DomainError("domain_slug is required")
    norm_lessons = _normalize_lessons(lessons)

    total_days = cfg["total_days"]
    kinds = [day_kind(d) for d in range(1, total_days + 1)]
    learning_days = [d for d, k in enumerate(kinds, start=1) if k == "learn"]
    # Pace: each learning day carries the level's learn_per_day lessons;
    # if lessons overflow the slots, days take more so nothing is dropped.
    per_day = (
        max(cfg["learn_per_day"], ceil(len(norm_lessons) / len(learning_days)))
        if norm_lessons
        else 0
    )

    days: list[dict] = []
    li = 0
    for day, kind in enumerate(kinds, start=1):
        lo, hi = difficulty_window(day, start_level)
        drange = [lo, hi]
        if kind == "mock":
            tasks = [_mock_task(day, drange)]
        elif kind == "revision":
            tasks = [_revision_task(day, drange)]
        else:
            chunk = norm_lessons[li : li + per_day] if per_day else []
            li += per_day
            tasks = [
                _learn_task(lesson, cfg["learn_minutes"]) for lesson in chunk
            ]
            tasks.append(
                _practice_task(cfg["practice_count"], cfg["practice_minutes"], drange)
            )
            if coding:
                tasks.append(_code_task(cfg["code_count"], cfg["code_minutes"]))
        days.append(
            {
                "day": day,
                "month": (day - 1) // 30 + 1,
                "week": (day - 1) // 7 + 1,
                "kind": kind,
                "tasks": tasks,
            }
        )
    return days


def plan_summary(
    domain_slug: str,
    start_level: str,
    lessons: list | None = None,
    coding: bool = True,
) -> dict:
    """Headline stats for a plan preview (used by the onboarding UI)."""
    cfg = _require_level(start_level)
    total_days = cfg["total_days"]
    est_questions = 0
    est_minutes = 0
    for day in range(1, total_days + 1):
        lo, hi = difficulty_window(day, start_level)
        kind = day_kind(day)
        if kind == "mock":
            t = _mock_task(day, [lo, hi])
        elif kind == "revision":
            t = _revision_task(day, [lo, hi])
            est_minutes += t["minutes"]
            est_questions += t["count"]
            continue
        else:
            est_minutes += cfg["learn_per_day"] * cfg["learn_minutes"]
            est_minutes += cfg["practice_minutes"]
            est_questions += cfg["practice_count"]
            if coding:
                est_minutes += cfg["code_minutes"]
            continue
        est_minutes += t["minutes"]
        est_questions += t["count"]
    return {
        "domain_slug": domain_slug,
        "start_level": start_level,
        "total_days": total_days,
        "total_months": ceil(total_days / 30),
        "total_lessons": len(lessons or []),
        "est_questions": est_questions,
        "est_minutes": est_minutes,
        "target_level": TARGET_LEVEL,
    }


def to_study_plan_record(
    domain_slug: str,
    start_level: str,
    days: list[dict],
    user_id: str | None = None,
) -> dict:
    """Shape a study_plans DB row from a generated plan.

    The sibling task owns the study_plans/daily_tasks tables; this is the
    exact record shape the API should persist (days expand into daily_tasks).
    """
    _require_level(start_level)
    return {
        "user_id": user_id,
        "domain_slug": domain_slug,
        "start_level": start_level,
        "total_days": len(days),
        "status": "active",
        "days": days,
    }
