"""Weekly test domain — pure logic for scheduled weekly assessments.

Every study plan gets a weekly test: 20 questions drawn from the domain's
question pool with a fixed difficulty mix, never repeating questions from
previous weeks of the same plan.

Test shape:
- 5 easy   (difficulty 1-3)
- 10 medium (difficulty 4-7)
- 5 hard   (difficulty 8-10)

Grades (score %):
- S: 90+  — Outstanding! 🏆
- A: 75+  — Excellent
- B: 60+  — Good
- C: 45+  — Fair — keep practicing
- D: 30+  — Needs work
- F: <30  — Revisit the basics
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, timedelta


EASY_RANGE = (1, 3)
MEDIUM_RANGE = (4, 7)
HARD_RANGE = (8, 10)

EASY_COUNT = 5
MEDIUM_COUNT = 10
HARD_COUNT = 5
TOTAL_QUESTIONS = EASY_COUNT + MEDIUM_COUNT + HARD_COUNT  # 20

TEST_DURATION_MINUTES = 30
SCHEDULE_INTERVAL_DAYS = 7


@dataclass(frozen=True)
class WeeklyTestQuestion:
    """One question selected for a weekly test (ids only — content lives in DB)."""

    question_id: str
    difficulty: int


@dataclass
class WeeklyTest:
    """A scheduled weekly test for a user's study plan."""

    id: str
    user_id: str
    domain_slug: str
    plan_id: str | None
    week_number: int
    scheduled_date: date
    status: str = "scheduled"  # scheduled|active|completed|missed
    score: int | None = None
    total_questions: int = TOTAL_QUESTIONS
    question_ids: list[str] = field(default_factory=list)


def _in_range(difficulty: int, low: int, high: int) -> bool:
    return low <= difficulty <= high


def generate_weekly_test(
    domain_slug: str,
    week_number: int,
    questions_pool: list[dict],
    used_ids: set[str] | None = None,
    seed: int | None = None,
) -> list[WeeklyTestQuestion]:
    """Pick 20 questions: 5 easy + 10 medium + 5 hard, no repeats.

    `questions_pool`: list of {"id": str, "difficulty": int}.
    `used_ids`: question ids already used in previous weeks — excluded.
    Deterministic when `seed` is given (seeded shuffle).
    Falls back gracefully when the pool is thin: fills from whatever is
    available, preferring unused questions.
    """
    if week_number < 1:
        raise ValueError("week_number must be >= 1")
    used = set(used_ids or ())
    rng = random.Random(seed if seed is not None else hash((domain_slug, week_number)))

    def bucket(low: int, high: int) -> list[dict]:
        items = [q for q in questions_pool if _in_range(q["difficulty"], low, high)]
        fresh = [q for q in items if q["id"] not in used]
        # Prefer unused; if not enough fresh, reuse least-recently-used.
        rng.shuffle(fresh)
        rng.shuffle(items)
        ordered = fresh + [q for q in items if q["id"] not in {x["id"] for x in fresh}]
        # Deduplicate by id while preserving order.
        seen: set[str] = set()
        out: list[dict] = []
        for q in ordered:
            if q["id"] not in seen:
                seen.add(q["id"])
                out.append(q)
        return out

    picks: list[WeeklyTestQuestion] = []
    picked_ids: set[str] = set()

    # Take per band, then top-up if a band was thin.
    easy = bucket(*EASY_RANGE)[:EASY_COUNT]
    medium = bucket(*MEDIUM_RANGE)[:MEDIUM_COUNT]
    hard = bucket(*HARD_RANGE)[:HARD_COUNT]
    for q in easy + medium + hard:
        if q["id"] not in picked_ids:
            picks.append(WeeklyTestQuestion(question_id=q["id"], difficulty=q["difficulty"]))
            picked_ids.add(q["id"])

    # Top-up from the whole pool if any band was thin.
    if len(picks) < TOTAL_QUESTIONS:
        rest = bucket(1, 10)
        for q in rest:
            if len(picks) >= TOTAL_QUESTIONS:
                break
            if q["id"] not in picked_ids:
                picks.append(WeeklyTestQuestion(question_id=q["id"], difficulty=q["difficulty"]))
                picked_ids.add(q["id"])

    rng.shuffle(picks)
    return picks[:TOTAL_QUESTIONS]


def calculate_grade(score_pct: float) -> dict:
    """Grade a score percentage. Pure."""
    if score_pct >= 90:
        return {"grade": "S", "message": "Outstanding! 🏆"}
    if score_pct >= 75:
        return {"grade": "A", "message": "Excellent! Keep it up."}
    if score_pct >= 60:
        return {"grade": "B", "message": "Good — you're on track."}
    if score_pct >= 45:
        return {"grade": "C", "message": "Fair — keep practicing."}
    if score_pct >= 30:
        return {"grade": "D", "message": "Needs work — revisit weak areas."}
    return {"grade": "F", "message": "Revisit the basics and try again."}


def should_schedule(last_test_date: date | None, today: date) -> bool:
    """True when 7+ days passed since the last scheduled test (or never)."""
    if last_test_date is None:
        return True
    return (today - last_test_date).days >= SCHEDULE_INTERVAL_DAYS


def next_test_date(from_date: date) -> date:
    """The date one week after `from_date`."""
    return from_date + timedelta(days=SCHEDULE_INTERVAL_DAYS)
