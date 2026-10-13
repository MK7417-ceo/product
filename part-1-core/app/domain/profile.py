"""Domain: onboarding profile + placement (level verification). PURE.

Skill levels never come from self-report alone: a claimed level must be
verified by answering questions. Placement draws a RANDOM, reproducible
sample of questions across every level from beginner up to the claimed
level, then analyses per-level performance to find the true level.
All scoring is deterministic.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.user import DomainError

LEVELS = ("beginner", "intermediate", "advanced", "expert")

QUESTIONS_PER_LEVEL = 4
PASS_RATIO = 0.7


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
    skill: str = ""  # skill tag used for gap reports; defaults to topic


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


def levels_upto(claimed: str) -> tuple[str, ...]:
    """Every level from beginner up to and including the claimed level."""
    validate_level(claimed)
    return LEVELS[: LEVELS.index(claimed) + 1]


def sample_placement_questions(bank, topic: str, claimed_level: str, seed: str) -> list[Question]:
    """Random, reproducible placement set: QUESTIONS_PER_LEVEL questions per
    level, from beginner up to the claimed level.

    The draw is seeded (per placement session id) so it is different every
    attempt yet fully reproducible and auditable. Raises DomainError when the
    bank cannot supply enough questions for a level.
    """
    levels = levels_upto(claimed_level)
    rng = random.Random(int(seed, 16) % (2**63))
    picked: list[Question] = []
    for lvl in levels:
        pool = bank.pool(topic, lvl)
        if len(pool) < QUESTIONS_PER_LEVEL:
            raise DomainError(f"not enough questions for {topic}/{lvl}")
        picked.extend(rng.sample(pool, QUESTIONS_PER_LEVEL))
    return picked


@dataclass(frozen=True)
class LevelResult:
    level: str
    correct: int
    total: int

    @property
    def ratio(self) -> float:
        return self.correct / self.total if self.total else 0.0


@dataclass(frozen=True)
class PlacementAnalysis:
    claimed_level: str
    verified_level: str
    levels: tuple[LevelResult, ...]
    correct: int
    total: int
    summary: str


def analyze_placement(
    claimed_level: str, questions: list[Question], answers: dict[str, int]
) -> PlacementAnalysis:
    """Per-level analysis of a placement attempt.

    Verified level = the highest level (never above the claim) where the
    user scored >= PASS_RATIO *and* every lower level also passed. This
    finds the true level instead of grading one flat ratio.
    """
    levels = levels_upto(claimed_level)
    results: list[LevelResult] = []
    for lvl in levels:
        qs = [q for q in questions if q.level == lvl]
        correct = sum(1 for q in qs if answers.get(q.id) == q.answer_index)
        results.append(LevelResult(level=lvl, correct=correct, total=len(qs)))
    verified = "beginner"
    for r in results:
        if r.total and r.ratio >= PASS_RATIO:
            verified = r.level
        else:
            break
    correct = sum(r.correct for r in results)
    total = sum(r.total for r in results)
    if total == 0:
        # No questions asked (e.g. beginner fast-path): nothing to analyse.
        summary = (
            f"claimed {claimed_level} — starting from basics, "
            "no verification needed"
        )
    else:
        breakdown = ", ".join(
            f"{r.level} {r.correct}/{r.total}" for r in results
        )
        summary = (
            f"{breakdown} -> verified level: {verified} "
            f"(claimed {claimed_level})"
        )
    return PlacementAnalysis(
        claimed_level=claimed_level,
        verified_level=verified,
        levels=tuple(results),
        correct=correct,
        total=total,
        summary=summary,
    )


def analysis_to_dict(a: PlacementAnalysis) -> dict:
    return {
        "claimed_level": a.claimed_level,
        "verified_level": a.verified_level,
        "correct": a.correct,
        "total": a.total,
        "summary": a.summary,
        "levels": {
            r.level: {"correct": r.correct, "total": r.total,
                      "ratio": round(r.ratio, 3)}
            for r in a.levels
        },
    }
