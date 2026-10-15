"""Tests for the weekly test system — domain logic + service."""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.domain import weekly_test as wt


def _pool(n_easy=20, n_med=30, n_hard=20):
    pool = []
    for i in range(n_easy):
        pool.append({"id": f"e{i}", "difficulty": 2})
    for i in range(n_med):
        pool.append({"id": f"m{i}", "difficulty": 5})
    for i in range(n_hard):
        pool.append({"id": f"h{i}", "difficulty": 9})
    return pool


# ---- generate_weekly_test ----

def test_generates_20_questions():
    picks = wt.generate_weekly_test("dsa", 1, _pool(), seed=42)
    assert len(picks) == 20


def test_difficulty_mix():
    picks = wt.generate_weekly_test("dsa", 1, _pool(), seed=42)
    easy = sum(1 for p in picks if 1 <= p.difficulty <= 3)
    med = sum(1 for p in picks if 4 <= p.difficulty <= 7)
    hard = sum(1 for p in picks if 8 <= p.difficulty <= 10)
    assert easy == 5
    assert med == 10
    assert hard == 5


def test_no_repeats_across_weeks():
    pool = _pool()
    week1 = wt.generate_weekly_test("dsa", 1, pool, seed=1)
    used = {p.question_id for p in week1}
    week2 = wt.generate_weekly_test("dsa", 2, pool, used_ids=used, seed=2)
    week2_ids = {p.question_id for p in week2}
    assert not (used & week2_ids), "week 2 reused week 1 questions"


def test_deterministic_with_seed():
    pool = _pool()
    a = wt.generate_weekly_test("dsa", 1, pool, seed=99)
    b = wt.generate_weekly_test("dsa", 1, pool, seed=99)
    assert [p.question_id for p in a] == [p.question_id for p in b]


def test_thin_pool_graceful():
    # Only 8 questions available — should return 8, not crash.
    pool = [{"id": f"q{i}", "difficulty": 5} for i in range(8)]
    picks = wt.generate_weekly_test("dsa", 1, pool, seed=1)
    assert len(picks) == 8
    assert len({p.question_id for p in picks}) == 8


def test_invalid_week_number():
    with pytest.raises(ValueError):
        wt.generate_weekly_test("dsa", 0, _pool())


# ---- calculate_grade ----

@pytest.mark.parametrize("pct,grade", [
    (95, "S"), (90, "S"), (89.9, "A"), (75, "A"),
    (74.9, "B"), (60, "B"), (59.9, "C"), (45, "C"),
    (44.9, "D"), (30, "D"), (29.9, "F"), (0, "F"),
])
def test_grades(pct, grade):
    assert wt.calculate_grade(pct)["grade"] == grade


def test_grade_has_message():
    for pct in (95, 80, 65, 50, 35, 10):
        g = wt.calculate_grade(pct)
        assert g["message"], f"no message for {pct}"


# ---- should_schedule / next_test_date ----

def test_should_schedule_first_time():
    assert wt.should_schedule(None, date(2026, 10, 15)) is True


def test_should_schedule_after_7_days():
    last = date(2026, 10, 1)
    assert wt.should_schedule(last, date(2026, 10, 8)) is True
    assert wt.should_schedule(last, date(2026, 10, 7)) is False


def test_next_test_date():
    assert wt.next_test_date(date(2026, 10, 15)) == date(2026, 10, 22)


def test_weekly_test_dataclass_defaults():
    t = wt.WeeklyTest(
        id="x", user_id="u", domain_slug="dsa", plan_id=None,
        week_number=1, scheduled_date=date.today())
    assert t.status == "scheduled"
    assert t.total_questions == 20
    assert t.score is None
