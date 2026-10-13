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

# F6c placement v3: 20 questions = 15 MCQ + 5 coding.
MCQ_PER_LEVEL_V3 = 5
V3_MCQ_LEVELS = ("beginner", "intermediate", "advanced")
CODING_MIX = (("easy", 2), ("medium", 2), ("hard", 1))
SUPPORTED_CODE_LANGUAGES = ("python", "c", "cpp", "java")

# F6d placement v4: +3 written (subjective) questions, 1 per level.
# Total verification = 23 questions.
WRITTEN_PER_LEVEL = 1
V3_WRITTEN_LEVELS = ("beginner", "intermediate", "advanced")
WRITTEN_MIN_CHARS = 20  # below this the answer is "too short", not graded


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
    """Random, reproducible placement set (F6c v3): MCQ_PER_LEVEL_V3 questions
    per level across beginner/intermediate/advanced — 15 total — for any
    non-beginner claim.

    The claimed level no longer narrows the spread: verification finds the
    true level purely from performance. The draw is seeded (per placement
    session id) so it is different every attempt yet fully reproducible
    and auditable. Raises DomainError when the bank cannot supply enough
    questions for a level.
    """
    validate_level(claimed_level)
    rng = random.Random(int(seed, 16) % (2**63))
    picked: list[Question] = []
    for lvl in V3_MCQ_LEVELS:
        pool = bank.pool(topic, lvl)
        if len(pool) < MCQ_PER_LEVEL_V3:
            raise DomainError(f"not enough questions for {topic}/{lvl}")
        picked.extend(rng.sample(pool, MCQ_PER_LEVEL_V3))
    return picked


def sample_placement_coding(dsa_bank, seed: str) -> list:
    """Random, reproducible coding set (F6c v3): CODING_MIX problems from the
    DSA bank (2 easy + 2 medium + 1 hard), seeded by the session id so the
    set can be re-derived on submit without a DB migration.
    """
    import hashlib
    rng = random.Random(
        int(hashlib.sha256(f"{seed}:code".encode()).hexdigest(), 16) % (2**63)
    )
    picked: list = []
    for difficulty, count in CODING_MIX:
        pool = [q for q in dsa_bank if q.difficulty == difficulty]
        if len(pool) < count:
            raise DomainError(f"not enough coding problems: {difficulty}")
        picked.extend(rng.sample(pool, count))
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
class CodingResult:
    problem_id: str
    title: str
    difficulty: str
    verdict: str  # accepted | wrong_answer | runtime_error | engine_error | not_attempted
    passed: int
    total: int


@dataclass(frozen=True)
class WrittenQuestion:
    """A subjective (free-text) placement question.

    key_concepts and sample_answer NEVER leave the server — the client
    only sees id/topic/level/prompt via public_written_question().
    """
    id: str
    topic: str
    level: str
    prompt: str
    key_concepts: tuple[str, ...]
    sample_answer: str
    max_points: int = 100


@dataclass(frozen=True)
class WrittenResult:
    question_id: str
    prompt: str
    level: str
    status: str  # scored | too_short | not_attempted
    coverage: float  # 0.0-1.0 fraction of key concepts mentioned
    matched: tuple[str, ...] = ()
    missed: tuple[str, ...] = ()


def public_written_question(q: WrittenQuestion) -> dict:
    """Client-safe shape: rubric stays on the server."""
    return {"id": q.id, "topic": q.topic, "level": q.level, "prompt": q.prompt}


def sample_placement_written(bank, topic: str, seed: str) -> list[WrittenQuestion]:
    """Seeded written set (F6d v4): WRITTEN_PER_LEVEL per level across
    beginner/intermediate/advanced. Reproducible per session id."""
    import hashlib
    rng = random.Random(
        int(hashlib.sha256(f"{seed}:written".encode()).hexdigest(), 16) % (2**63)
    )
    picked: list[WrittenQuestion] = []
    for lvl in V3_WRITTEN_LEVELS:
        pool = bank.written_pool(topic, lvl)
        if len(pool) < WRITTEN_PER_LEVEL:
            raise DomainError(f"not enough written questions for {topic}/{lvl}")
        picked.extend(rng.sample(pool, WRITTEN_PER_LEVEL))
    return picked


def _normalize_text(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _concept_mentioned(concept: str, normalized: str) -> bool:
    """v1 heuristic: a concept counts as mentioned when its phrase appears,
    or when all of its significant words appear (plural-tolerant)."""
    concept = concept.lower().strip()
    if not concept:
        return False
    if concept in normalized:
        return True
    words = [w for w in concept.split() if len(w) > 2]
    if not words:
        return False
    tokens = set(normalized.split())

    def singular(w: str) -> str:
        return w[:-1] if w.endswith("s") and len(w) > 3 else w

    return all(w in tokens or singular(w) in tokens for w in words)


def grade_written(question: WrittenQuestion, answer: str) -> WrittenResult:
    """Deterministic rubric grader v1 (heuristic).

    Checks which key concepts the answer mentions — a coverage signal, not
    a deep understanding judgement. The analysis labels it accordingly.
    This is the `grade_written` seam: an LLM grader v2 can replace this
    function without changing any API shape.
    """
    text = (answer or "").strip()
    if not text:
        return WrittenResult(
            question_id=question.id, prompt=question.prompt,
            level=question.level, status="not_attempted", coverage=0.0,
        )
    if len(text) < WRITTEN_MIN_CHARS:
        return WrittenResult(
            question_id=question.id, prompt=question.prompt,
            level=question.level, status="too_short", coverage=0.0,
        )
    normalized = _normalize_text(text)
    matched = tuple(c for c in question.key_concepts
                    if _concept_mentioned(c, normalized))
    missed = tuple(c for c in question.key_concepts if c not in matched)
    coverage = len(matched) / len(question.key_concepts) if question.key_concepts else 0.0
    return WrittenResult(
        question_id=question.id, prompt=question.prompt,
        level=question.level, status="scored", coverage=round(coverage, 3),
        matched=matched, missed=missed,
    )


def analyze_placement_written(
    questions: list[WrittenQuestion], written_answers: dict[str, str],
) -> tuple[WrittenResult, ...]:
    """Grade each written answer. Missing/blank -> not_attempted (not a failure)."""
    return tuple(
        grade_written(q, (written_answers or {}).get(q.id, ""))
        for q in questions
    )


@dataclass(frozen=True)
class PlacementAnalysis:
    claimed_level: str
    verified_level: str
    levels: tuple[LevelResult, ...]
    correct: int
    total: int
    summary: str
    coding: tuple[CodingResult, ...] = ()
    coding_accepted: int = 0
    coding_total: int = 0
    written: tuple[WrittenResult, ...] = ()


def analyze_placement(
    claimed_level: str, questions: list[Question], answers: dict[str, int],
    coding: tuple[CodingResult, ...] = (),
    written: tuple[WrittenResult, ...] = (),
) -> PlacementAnalysis:
    """Per-level analysis of a placement attempt.

    Verified level = the highest level where the user scored >= PASS_RATIO
    *and* every lower level also passed. This finds the true level instead
    of grading one flat ratio. Coding and written results are reported
    separately and feed roadmap gaps; they do not move the verified level.
    """
    levels = [lvl for lvl in V3_MCQ_LEVELS
              if any(q.level == lvl for q in questions)]
    if not levels:
        levels = list(levels_upto(claimed_level))
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
    coding_accepted = sum(1 for c in coding if c.verdict == "accepted")
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
        if coding:
            summary += f"; coding {coding_accepted}/{len(coding)} accepted"
        if written:
            scored = [w for w in written if w.status == "scored"]
            if scored:
                avg = sum(w.coverage for w in scored) / len(scored)
                summary += f"; written {avg:.0%} concept coverage"
    return PlacementAnalysis(
        claimed_level=claimed_level,
        verified_level=verified,
        levels=tuple(results),
        correct=correct,
        total=total,
        summary=summary,
        coding=coding,
        coding_accepted=coding_accepted,
        coding_total=len(coding),
        written=written,
    )


def analyze_placement_coding(problems, code_submissions: dict, grade_fn) -> tuple[CodingResult, ...]:
    """Grade coding submissions for a placement session.

    problems: list of DSAQuestion (re-derived from the session seed).
    code_submissions: {problem_id: {"language": str, "code": str}}.
    grade_fn(problem, language, code) -> (verdict, passed, total_tests):
        injected so the domain stays pure; the service wires the engine.
    Missing/blank code -> not_attempted. Engine failures surface as
    engine_error via grade_fn — they never block MCQ grading.
    """
    results: list[CodingResult] = []
    for p in problems:
        sub = (code_submissions or {}).get(p.id) or {}
        code = (sub.get("code") or "").strip()
        language = sub.get("language") or "python"
        if not code:
            results.append(CodingResult(
                problem_id=p.id, title=p.title, difficulty=p.difficulty,
                verdict="not_attempted", passed=0,
                total=len(p.hidden_tests)))
            continue
        if language not in SUPPORTED_CODE_LANGUAGES:
            results.append(CodingResult(
                problem_id=p.id, title=p.title, difficulty=p.difficulty,
                verdict="runtime_error", passed=0,
                total=len(p.hidden_tests)))
            continue
        verdict, passed, total = grade_fn(p, language, code)
        results.append(CodingResult(
            problem_id=p.id, title=p.title, difficulty=p.difficulty,
            verdict=verdict, passed=passed, total=total))
    return tuple(results)


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
        "coding_accepted": a.coding_accepted,
        "coding_total": a.coding_total,
        "coding": [
            {"problem_id": c.problem_id, "title": c.title,
             "difficulty": c.difficulty, "verdict": c.verdict,
             "passed": c.passed, "total": c.total}
            for c in a.coding
        ],
        "written_total": len(a.written),
        "written": [
            {"question_id": w.question_id, "prompt": w.prompt,
             "level": w.level, "status": w.status,
             "coverage": w.coverage, "matched": list(w.matched),
             "concepts_total": len(w.matched) + len(w.missed)}
            for w in a.written
        ],
    }
