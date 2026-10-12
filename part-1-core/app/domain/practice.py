"""Domain: daily practice rhythm. PURE.

Every user gets 3 fresh questions per day, deterministic for (user, date) —
no storage needed, the same day always serves the same set. Answer keys
never leave the server; submit is scored server-side.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from app.domain.profile import Question, public_question
from app.domain.user import DomainError

DAILY_COUNT = 3


@dataclass(frozen=True)
class DailySet:
    date: str  # YYYY-MM-DD
    question_ids: tuple[str, ...]


def daily_question_ids(user_id: str, date: str, bank, count: int = DAILY_COUNT) -> DailySet:
    """Deterministic daily pick, seeded by user+date. Same input, same set."""
    if not user_id:
        raise DomainError("user_id required")
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        raise DomainError("date must be YYYY-MM-DD")
    pool = list(bank.all_questions() if hasattr(bank, "all_questions") else [])
    if not pool:
        # fall back: collect across topics/levels via the port interface
        seen: dict[str, object] = {}
        for topic in bank.topics():
            for level in ("beginner", "intermediate", "advanced", "expert"):
                for q in bank.questions(topic, level, 100):
                    seen[q.id] = q
        pool = list(seen.values())
    if len(pool) < count:
        raise DomainError("question bank too small for daily set")
    rng = random.Random(f"{user_id}:{date}:v1")
    ids = [q.id for q in pool]
    rng.shuffle(ids)
    return DailySet(date=date, question_ids=tuple(ids[:count]))


def daily_questions(user_id: str, date: str, bank, count: int = DAILY_COUNT) -> list[dict]:
    """Client-safe daily questions (no answer keys)."""
    picked = daily_question_ids(user_id, date, bank, count)
    out = []
    for qid in picked.question_ids:
        q = bank.get(qid)
        if q:
            out.append(public_question(q))
    return out


def score_daily(user_id: str, date: str, answers: dict[str, int], bank) -> tuple[int, int]:
    """Score a daily submission against the deterministic set for that day."""
    picked = daily_question_ids(user_id, date, bank)
    if set(answers) - set(picked.question_ids):
        raise DomainError("answers contain unknown question ids")
    correct = 0
    for qid in picked.question_ids:
        q = bank.get(qid)
        if q and answers.get(qid) == q.answer_index:
            correct += 1
    return correct, len(picked.question_ids)


def todays_tasks(roadmap, limit: int = 2) -> list:
    """Top actionable tasks for today: highest priority first."""
    if not roadmap:
        return []
    weight = {"high": 0, "medium": 1, "low": 2}
    actionable = [t for t in roadmap.tasks if t.status in ("pending", "in_progress")]
    actionable.sort(key=lambda t: (weight.get(t.priority, 3), t.id))
    return actionable[:limit]
