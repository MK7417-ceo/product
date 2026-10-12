"""Domain tests: assessment scoring + gap detection."""
from app.domain.assessment import score_assessment
from app.domain.profile import Question


def _q(qid, skill, ans):
    return Question(id=qid, topic="python", level="beginner", skill=skill,
                    prompt="p", choices=("a", "b"), answer_index=ans)


def test_score_and_gaps():
    qs = [_q("q1", "s1", 0), _q("q2", "s1", 1), _q("q3", "s2", 0), _q("q4", "s2", 0)]
    r = score_assessment(qs, {"q1": 0, "q2": 0, "q3": 1, "q4": 1})
    assert (r.correct, r.total) == (1, 4)
    assert r.ratio == 0.25
    # s1: 1/2 = 0.5 < 0.7 -> gap; s2: 0/2 -> gap
    assert set(r.gaps) == {"s1", "s2"}
    assert ("s1", 1, 2) in r.per_skill


def test_no_gaps_when_mastered():
    qs = [_q("q1", "s1", 0), _q("q2", "s1", 0)]
    r = score_assessment(qs, {"q1": 0, "q2": 0})
    assert r.gaps == ()
    assert r.ratio == 1.0


def test_empty_answers_all_gaps():
    qs = [_q("q1", "s1", 0)]
    r = score_assessment(qs, {})
    assert r.correct == 0
    assert r.gaps == ("s1",)
