"""Domain: Daily DSA — curated coding question of the day. PURE.

Honest stand-in for a LeetCode feed (LeetCode offers no official public
API): a curated bank with a deterministic date-seeded pick, so every user
gets the same question on the same day. Hidden tests never leave the
server; grading runs user code against them through the code engine.
The DailyDSAProvider port lets the user's future AI replace the curated
bank later without any API or frontend change.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.domain.user import DomainError

DIFFICULTIES = ("easy", "medium", "hard")


@dataclass(frozen=True)
class Example:
    stdin: str
    stdout: str
    explanation: str = ""


@dataclass(frozen=True)
class HiddenTest:
    stdin: str
    expected: str


@dataclass(frozen=True)
class DSAQuestion:
    id: str
    title: str
    difficulty: str
    description: str
    examples: tuple[Example, ...]
    starter_code: str  # python template
    hidden_tests: tuple[HiddenTest, ...]  # NEVER sent to clients
    topic_tags: tuple[str, ...] = ()
    hints: tuple[str, ...] = ()

    def validate(self) -> None:
        if self.difficulty not in DIFFICULTIES:
            raise DomainError(f"bad difficulty: {self.difficulty}")
        if not self.hidden_tests:
            raise DomainError(f"{self.id}: needs hidden tests")
        if not self.examples:
            raise DomainError(f"{self.id}: needs examples")


def pick_for_date(bank: list[DSAQuestion], day: date) -> DSAQuestion:
    """Deterministic question-of-the-day: rotates through the bank."""
    if not bank:
        raise DomainError("dsa bank is empty")
    return bank[day.toordinal() % len(bank)]


def public_dsa(q: DSAQuestion) -> dict:
    """Client-safe view: hidden tests never leave the server."""
    return {
        "id": q.id,
        "title": q.title,
        "difficulty": q.difficulty,
        "description": q.description,
        "examples": [
            {"stdin": e.stdin, "stdout": e.stdout, "explanation": e.explanation}
            for e in q.examples
        ],
        "starter_code": q.starter_code,
        "hidden_test_count": len(q.hidden_tests),
        "topic_tags": list(q.topic_tags),
        "hints": list(q.hints),
    }


def parse_day(raw: str) -> date:
    if not raw:
        return date.today()
    try:
        y, m, d = (int(p) for p in raw.split("-"))
        return date(y, m, d)
    except (ValueError, TypeError):
        raise DomainError("date must be YYYY-MM-DD")


@dataclass(frozen=True)
class DSAVerdict:
    passed: int
    total: int
    verdict: str  # accepted | wrong_answer | runtime_error | engine_error
    failed_case: dict | None = None

    @property
    def accepted(self) -> bool:
        return self.verdict == "accepted"


def grade_dsa(run_one, question: DSAQuestion, language: str,
              code: str) -> DSAVerdict:
    """Grade code against hidden tests.

    run_one(language, code, stdin) -> (ok, stdout, error): injected so the
    domain stays pure and tests don't need the engine.
    """
    passed = 0
    for i, t in enumerate(question.hidden_tests):
        ok, stdout, error = run_one(language, code, t.stdin)
        if not ok:
            return DSAVerdict(passed, len(question.hidden_tests),
                              "runtime_error" if error else "engine_error",
                              {"test_index": i, "error": error or "no output"})
        if stdout.strip() != t.expected.strip():
            return DSAVerdict(
                passed, len(question.hidden_tests), "wrong_answer",
                {"test_index": i, "stdin": t.stdin,
                 "expected": t.expected.strip(),
                 "got": stdout.strip()},
            )
        passed += 1
    return DSAVerdict(passed, len(question.hidden_tests), "accepted")
