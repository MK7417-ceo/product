"""Domain tests: profile rules + placement scoring/verification."""
import pytest

from app.domain.profile import (
    Question,
    analyze_placement,
    analyze_placement_coding,
    analysis_to_dict,
    levels_upto,
    public_question,
    sample_placement_coding,
    sample_placement_questions,
    score_placement,
    validate_level,
    validate_profile,
)
from app.domain.user import DomainError


def _fields(**over):
    base = dict(
        education="B.Tech CSE", experience_years=1.5,
        current_skills=["python"], target_role="AI Engineer",
        target_domain="AI/ML", target_level="intermediate",
        tech_focus=["python", "ml"],
    )
    base.update(over)
    return base


def test_validate_profile_ok():
    validate_profile(**_fields())  # must not raise


def test_validate_profile_rejects():
    with pytest.raises(DomainError):
        validate_profile(**_fields(education="  "))
    with pytest.raises(DomainError):
        validate_profile(**_fields(target_level="god"))
    with pytest.raises(DomainError):
        validate_profile(**_fields(current_skills=[]))
    with pytest.raises(DomainError):
        validate_profile(**_fields(experience_years=-1))


def test_validate_level():
    assert validate_level("expert") == "expert"
    with pytest.raises(DomainError):
        validate_level("nope")


def _qs():
    return [
        Question(id="q1", topic="python", level="beginner", prompt="p1",
                 choices=("a", "b"), answer_index=0),
        Question(id="q2", topic="python", level="beginner", prompt="p2",
                 choices=("a", "b"), answer_index=1),
    ]


def test_score_placement():
    correct, total = score_placement(_qs(), {"q1": 0, "q2": 0})
    assert (correct, total) == (1, 2)


def test_public_question_hides_answer():
    pub = public_question(_qs()[0])
    assert "answer_index" not in pub
    assert pub["choices"] == ["a", "b"]


def test_levels_upto():
    assert levels_upto("beginner") == ("beginner",)
    assert levels_upto("advanced") == ("beginner", "intermediate", "advanced")
    assert levels_upto("expert") == ("beginner", "intermediate", "advanced", "expert")
    with pytest.raises(DomainError):
        levels_upto("god")


def _spread_qs():
    qs = []
    for lvl in ("beginner", "intermediate", "advanced"):
        for i in range(5):
            qs.append(Question(id=f"{lvl}-{i}", topic="python", level=lvl,
                               prompt="p", choices=("a", "b"), answer_index=0))
    return qs


def _answers_for(qs, correct_levels):
    return {q.id: (0 if q.level in correct_levels else 1) for q in qs}


def test_analyze_all_correct_verifies_claim():
    qs = _spread_qs()
    a = analyze_placement("advanced", qs, _answers_for(qs, {"beginner", "intermediate", "advanced"}))
    assert a.verified_level == "advanced"
    assert (a.correct, a.total) == (15, 15)
    assert a.levels[2].ratio == 1.0


def test_analyze_finds_true_level_not_flat_ratio():
    # aces beginner+intermediate, bombs advanced -> intermediate, not a ratio average
    qs = _spread_qs()
    a = analyze_placement("advanced", qs, _answers_for(qs, {"beginner", "intermediate"}))
    assert a.verified_level == "intermediate"
    assert a.levels[0].correct == 5 and a.levels[2].correct == 0


def test_analyze_requires_lower_levels_to_pass():
    # aces advanced but fails beginner -> stays beginner (no lucky guesses upward)
    qs = _spread_qs()
    a = analyze_placement("advanced", qs, _answers_for(qs, {"advanced"}))
    assert a.verified_level == "beginner"


def test_analyze_v3_finds_true_level_above_claim():
    # v3: the claim no longer caps verification — performance decides.
    qs = _spread_qs()
    a = analyze_placement("intermediate", qs, _answers_for(qs, {"beginner", "intermediate", "advanced"}))
    assert a.verified_level == "advanced"


def test_analyze_all_wrong_floors_at_beginner():
    qs = _spread_qs()
    a = analyze_placement("advanced", qs, _answers_for(qs, set()))
    assert a.verified_level == "beginner"
    assert "verified level: beginner" in a.summary


def test_analysis_to_dict_shape():
    qs = _spread_qs()
    a = analyze_placement("intermediate", qs, _answers_for(qs, {"beginner", "intermediate"}))
    d = analysis_to_dict(a)
    assert d["verified_level"] == "intermediate"
    assert set(d["levels"]) == {"beginner", "intermediate", "advanced"}
    assert d["levels"]["beginner"] == {"correct": 5, "total": 5, "ratio": 1.0}
    assert d["coding_total"] == 0
    assert d["coding"] == []


class _FakeBank:
    def __init__(self, questions):
        self._qs = questions

    def pool(self, topic, level):
        return [q for q in self._qs if q.topic == topic and q.level == level]


def test_sample_spread_and_deterministic():
    bank = _FakeBank(_spread_qs())
    first = sample_placement_questions(bank, "python", "advanced", "ab" * 16)
    second = sample_placement_questions(bank, "python", "advanced", "ab" * 16)
    assert [q.id for q in first] == [q.id for q in second]  # same seed -> same set
    assert len(first) == 15
    assert [q.level for q in first] == ["beginner"] * 5 + ["intermediate"] * 5 + ["advanced"] * 5
    assert len({q.id for q in first}) == 15  # no repeats


def test_sample_differs_across_seeds():
    bank = _FakeBank(_spread_qs())
    a = sample_placement_questions(bank, "python", "advanced", "ab" * 16)
    b = sample_placement_questions(bank, "python", "advanced", "cd" * 16)
    assert [q.id for q in a] != [q.id for q in b]


def test_sample_v3_same_spread_for_all_claims():
    # v3: every non-beginner claim draws the same B/I/A spread
    bank = _FakeBank(_spread_qs())
    for claim in ("intermediate", "advanced", "expert"):
        qs = sample_placement_questions(bank, "python", claim, "ab" * 16)
        assert len(qs) == 15
        assert [q.level for q in qs] == (
            ["beginner"] * 5 + ["intermediate"] * 5 + ["advanced"] * 5)


def test_sample_raises_when_bank_thin():
    bank = _FakeBank(_spread_qs()[:6])  # only 6 beginner questions... actually 4 beginner + 2 intermediate
    with pytest.raises(DomainError, match="not enough questions"):
        sample_placement_questions(bank, "python", "advanced", "ab" * 16)


# ---- F6c v3 coding sampling + grading ----

def _dsa_bank():
    from app.adapters.outbound.dsa_bank import BANK
    return BANK


def test_sample_coding_mix_and_deterministic():
    bank = _dsa_bank()
    first = sample_placement_coding(bank, "ab" * 16)
    second = sample_placement_coding(bank, "ab" * 16)
    assert [q.id for q in first] == [q.id for q in second]
    assert len(first) == 5
    from collections import Counter
    assert dict(Counter(q.difficulty for q in first)) == {
        "easy": 2, "medium": 2, "hard": 1}
    assert len({q.id for q in first}) == 5


def test_sample_coding_differs_across_seeds():
    bank = _dsa_bank()
    a = sample_placement_coding(bank, "ab" * 16)
    b = sample_placement_coding(bank, "cd" * 16)
    assert [q.id for q in a] != [q.id for q in b]


def test_sample_coding_raises_when_bank_thin():
    bank = [q for q in _dsa_bank() if q.difficulty == "easy"][:1]
    with pytest.raises(DomainError, match="not enough coding problems"):
        sample_placement_coding(bank, "ab" * 16)


def test_analyze_coding_not_attempted_without_code():
    problems = sample_placement_coding(_dsa_bank(), "ab" * 16)
    results = analyze_placement_coding(problems, {}, lambda p, l, c: ("accepted", 1, 1))
    assert all(r.verdict == "not_attempted" for r in results)
    assert len(results) == 5


def test_analyze_coding_uses_grade_fn():
    problems = sample_placement_coding(_dsa_bank(), "ab" * 16)[:2]
    subs = {p.id: {"language": "python", "code": "print(1)"} for p in problems}
    results = analyze_placement_coding(
        problems, subs, lambda p, l, c: ("accepted", 3, 3))
    assert [r.verdict for r in results] == ["accepted", "accepted"]
    assert all((r.passed, r.total) == (3, 3) for r in results)


def test_analyze_coding_rejects_bad_language():
    problems = sample_placement_coding(_dsa_bank(), "ab" * 16)[:1]
    p = problems[0]
    results = analyze_placement_coding(
        problems, {p.id: {"language": "rust", "code": "fn main(){ }"}},
        lambda p, l, c: ("accepted", 1, 1))
    assert results[0].verdict == "runtime_error"
