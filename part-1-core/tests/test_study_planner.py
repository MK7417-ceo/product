"""Tests for the study plan generator (pure domain, no DB)."""
import pytest

from app.domain.study_planner import (
    START_LEVELS,
    TARGET_LEVEL,
    day_kind,
    difficulty_window,
    generate_plan,
    plan_summary,
    to_study_plan_record,
)
from app.domain.user import DomainError


def _lessons(n):
    return [{"id": f"l{i}", "title": f"Lesson {i}"} for i in range(1, n + 1)]


# ---- plan length per start level ----

def test_scratch_plan_is_120_days():
    days = generate_plan("dsa", "scratch", _lessons(50))
    assert len(days) == 120


def test_beginner_plan_is_90_days():
    days = generate_plan("python", "beginner", _lessons(40))
    assert len(days) == 90


def test_intermediate_plan_is_60_days():
    days = generate_plan("networking", "intermediate", _lessons(30), coding=False)
    assert len(days) == 60


def test_start_levels_cover_all_three():
    assert set(START_LEVELS) == {"scratch", "beginner", "intermediate"}


def test_invalid_level_raises():
    with pytest.raises(DomainError):
        generate_plan("dsa", "expert", [])


def test_empty_domain_slug_raises():
    with pytest.raises(DomainError):
        generate_plan("", "scratch", [])


# ---- revision / mock cadence ----

def test_every_7th_day_is_revision():
    for d in (7, 14, 21, 28, 35):
        assert day_kind(d) == "revision", d


def test_every_30th_day_is_mock():
    for d in (30, 60, 90, 120):
        assert day_kind(d) == "mock", d


def test_mock_wins_over_revision_on_shared_days():
    # 210 would be both; rule must prefer mock (not reachable in 120d plans,
    # but the rule is pinned here)
    assert day_kind(210) == "mock"


def test_revision_day_has_revise_task_and_mock_is_timed():
    days = generate_plan("dsa", "scratch", _lessons(20))
    rev = next(d for d in days if d["day"] == 7)
    assert rev["kind"] == "revision"
    assert any(t["type"] == "revise" for t in rev["tasks"])
    mock = next(d for d in days if d["day"] == 30)
    assert mock["kind"] == "mock"
    mt = next(t for t in mock["tasks"] if t["type"] == "mock")
    assert mt["timed"] is True
    assert mt["count"] > 0


# ---- difficulty ramp: basic -> expert, never a hard jump ----

def test_scratch_difficulty_ramps_by_quarter():
    assert difficulty_window(1, "scratch") == (1, 4)
    assert difficulty_window(30, "scratch") == (1, 4)
    assert difficulty_window(31, "scratch") == (3, 6)
    assert difficulty_window(61, "scratch") == (5, 8)
    assert difficulty_window(91, "scratch") == (7, 10)
    assert difficulty_window(120, "scratch") == (7, 10)


def test_beginner_starts_at_difficulty_3():
    lo, _ = difficulty_window(1, "beginner")
    assert lo == 3


def test_intermediate_starts_at_difficulty_5():
    lo, hi = difficulty_window(1, "intermediate")
    assert lo == 5
    assert hi <= 10


def test_difficulty_never_exceeds_10():
    for day in (1, 30, 60, 90, 120):
        for level in START_LEVELS:
            lo, hi = difficulty_window(day, level)
            assert 1 <= lo <= hi <= 10


def test_difficulty_is_monotonic_within_a_plan():
    days = generate_plan("dsa", "scratch", _lessons(20))
    los = []
    for d in days:
        for t in d["tasks"]:
            if t["type"] in ("practice", "mock"):
                los.append(t["difficulty_range"][0])
    assert los == sorted(los)


# ---- month/week structure ----

def test_month_week_structure():
    days = generate_plan("dsa", "scratch", [])
    by_day = {d["day"]: d for d in days}
    assert (by_day[1]["month"], by_day[1]["week"]) == (1, 1)
    assert (by_day[30]["month"], by_day[30]["week"]) == (1, 5)
    assert (by_day[31]["month"], by_day[31]["week"]) == (2, 5)
    assert (by_day[60]["month"], by_day[60]["week"]) == (2, 9)
    assert (by_day[120]["month"], by_day[120]["week"]) == (4, 18)


# ---- lesson distribution ----

def test_all_lessons_assigned_to_learning_days_only():
    lessons = _lessons(40)
    days = generate_plan("python", "beginner", lessons)
    seen = []
    for d in days:
        for t in d["tasks"]:
            if t["type"] == "learn":
                seen.append(t["lesson_id"])
                assert d["kind"] == "learn"
    assert sorted(seen) == sorted(l["id"] for l in lessons)


def test_string_lessons_are_accepted():
    days = generate_plan("dsa", "scratch", ["Arrays", "Strings"])
    titles = [
        t["title"]
        for d in days
        for t in d["tasks"]
        if t["type"] == "learn"
    ]
    assert "Arrays" in titles and "Strings" in titles


# ---- coding vs non-coding task mix ----

def test_coding_domain_gets_code_tasks():
    days = generate_plan("python", "beginner", _lessons(10), coding=True)
    learn_days = [d for d in days if d["kind"] == "learn"]
    assert all(any(t["type"] == "code" for t in d["tasks"]) for d in learn_days)


def test_non_coding_domain_has_no_code_tasks():
    days = generate_plan("networking", "beginner", _lessons(10), coding=False)
    for d in days:
        assert not any(t["type"] == "code" for t in d["tasks"])


def test_scratch_has_more_learn_tasks_than_intermediate():
    # Scratch pace: 2 learn tasks/day; intermediate: 1/day (same lessons).
    s_day1 = generate_plan("dsa", "scratch", _lessons(20))[0]
    i_day1 = generate_plan("dsa", "intermediate", _lessons(20))[0]
    s_learn = sum(1 for t in s_day1["tasks"] if t["type"] == "learn")
    i_learn = sum(1 for t in i_day1["tasks"] if t["type"] == "learn")
    assert s_learn == 2
    assert i_learn == 1
    assert s_learn > i_learn


# ---- summary & determinism ----

def test_plan_summary_counts():
    s = plan_summary("dsa", "scratch", _lessons(68))
    assert s["total_days"] == 120
    assert s["total_months"] == 4
    assert s["total_lessons"] == 68
    assert s["target_level"] == TARGET_LEVEL == "Expert"
    assert s["est_questions"] > 400


def test_plan_is_deterministic():
    lessons = _lessons(25)
    a = generate_plan("dsa", "scratch", lessons)
    b = generate_plan("dsa", "scratch", lessons)
    assert a == b


def test_to_study_plan_record_shape():
    days = generate_plan("dsa", "beginner", _lessons(10))
    rec = to_study_plan_record("dsa", "beginner", days, user_id="u1")
    assert rec["domain_slug"] == "dsa"
    assert rec["start_level"] == "beginner"
    assert rec["total_days"] == 90
    assert rec["status"] == "active"
    assert rec["user_id"] == "u1"
    assert len(rec["days"]) == 90
