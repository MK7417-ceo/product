"""Service tests: onboarding orchestration with fake outbound ports (F6c v3)."""
import pytest

from app.adapters.inbound.onboarding_service import OnboardingServiceImpl
from app.adapters.outbound.dsa_bank import BANK as DSA_BANK
from app.adapters.outbound.question_bank import StaticQuestionBank
from app.domain.user import DomainError


class FakeProfiles:
    def __init__(self):
        self.by_user = {}

    def save(self, p):
        self.by_user[p.user_id] = p

    def get_by_user(self, uid):
        return self.by_user.get(uid)


class FakePlacements:
    def __init__(self):
        self.by_id = {}

    def save(self, p):
        self.by_id[p.id] = p

    def get(self, pid):
        return self.by_id.get(pid)


class FakeRunner:
    """Pretends every run succeeds; stdout echoes a canned value."""

    def __init__(self, stdout=""):
        self.stdout = stdout
        self.calls = []

    def run(self, language, code, stdin, limits, request_id):
        self.calls.append((language, code, stdin))
        return {"verdict": "ok", "exit_code": 0,
                "stdout": self.stdout, "stderr": ""}


@pytest.fixture()
def svc():
    return OnboardingServiceImpl(
        FakeProfiles(), FakePlacements(), StaticQuestionBank(),
        dsa_bank=DSA_BANK, code_runner=FakeRunner())


def _profile_fields(**over):
    base = dict(education="B.Tech", experience_years=2, current_skills=["python"],
                target_role="AI Engineer", target_domain="AI/ML",
                target_level="intermediate", tech_focus=["python"])
    base.update(over)
    return base


def test_save_and_get_profile(svc):
    p = svc.save_profile("u1", **_profile_fields())
    assert p.target_level == "intermediate"
    assert svc.get_profile("u1").id == p.id


def test_save_profile_twice_replaces(svc):
    p1 = svc.save_profile("u1", **_profile_fields())
    p2 = svc.save_profile("u1", **_profile_fields(target_level="advanced"))
    assert p1.id == p2.id
    assert svc.get_profile("u1").target_level == "advanced"


def test_get_missing_profile(svc):
    with pytest.raises(DomainError, match="profile not found"):
        svc.get_profile("ghost")


def test_start_placement_beginner_skips_questions(svc):
    # beginners start from scratch: session completes immediately, no questions
    session, questions, coding, written = svc.start_placement("u1", "python", "beginner")
    assert questions == []
    assert coding == []
    assert session.status == "completed"
    assert session.verified_level == "beginner"


def test_start_placement_v3_counts(svc):
    session, questions, coding, written = svc.start_placement(
        "u1", "python", "intermediate")
    assert len(questions) == 15  # 5 per level x B/I/A
    assert len(coding) == 5  # 2 easy + 2 medium + 1 hard
    assert all("answer_index" not in q for q in questions)
    assert all("hidden_tests" not in c for c in coding)
    assert session.status == "open"


def test_start_placement_spread_beginner_to_advanced(svc):
    _, questions, _, _ = svc.start_placement("u1", "python", "advanced")
    levels = [q["level"] for q in questions]
    assert levels == (["beginner"] * 5 + ["intermediate"] * 5
                      + ["advanced"] * 5)


def test_start_placement_coding_mix(svc):
    _, _, coding, _ = svc.start_placement("u1", "python", "intermediate")
    from collections import Counter
    assert dict(Counter(c["difficulty"] for c in coding)) == {
        "easy": 2, "medium": 2, "hard": 1}


def test_start_placement_expert_claim_gets_v3_spread(svc):
    # expert claim also draws the B/I/A v3 spread (no expert MCQs in v3)
    _, questions, coding, _ = svc.start_placement("u1", "python", "expert")
    assert len(questions) == 15
    assert len(coding) == 5
    assert "expert" not in {q["level"] for q in questions}


def test_start_placement_unknown_topic(svc):
    with pytest.raises(DomainError, match="unknown topic"):
        svc.start_placement("u1", "cobol", "beginner")


def test_coding_redrived_on_submit():
    # the coding set on submit must equal the set handed out at start
    s = OnboardingServiceImpl(
        FakeProfiles(), FakePlacements(), StaticQuestionBank(),
        dsa_bank=DSA_BANK, code_runner=FakeRunner())
    session, _, coding_at_start, _ = s.start_placement("u1", "python", "advanced")
    _, analysis = s.submit_placement("u1", session.id, {}, code={})
    at_submit = [c["problem_id"] for c in analysis["coding"]]
    assert at_submit == [c["id"] for c in coding_at_start]


def test_submit_all_correct_verifies_claim(svc):
    bank = StaticQuestionBank()
    session, _, _, _ = svc.start_placement("u1", "python", "intermediate")
    answers = {q.id: q.answer_index for q in
               [bank.get(qid) for qid in session.question_ids]}
    done, analysis = svc.submit_placement("u1", session.id, answers)
    assert done.status == "completed"
    assert done.verified_level == "advanced"
    assert done.correct == 15
    assert analysis["verified_level"] == "advanced"
    assert set(analysis["levels"]) == {"beginner", "intermediate", "advanced"}
    assert "; coding 0/5 accepted" in analysis["summary"]


def test_submit_coding_accepted_with_fake_runner(svc):
    # OrderedRunner pops expected outputs in grading order: the service
    # grades each problem's hidden tests sequentially, so this is deterministic.
    from app.domain.profile import sample_placement_coding

    class OrderedRunner:
        def __init__(self, problems):
            self.queue = [(t.stdin, t.expected)
                          for q in problems for t in q.hidden_tests]

        def run(self, language, code, stdin, limits, request_id):
            exp_stdin, expected = self.queue.pop(0)
            assert stdin == exp_stdin, "grading order changed"
            return {"verdict": "ok", "exit_code": 0,
                    "stdout": expected, "stderr": ""}

    s = OnboardingServiceImpl(
        FakeProfiles(), FakePlacements(), StaticQuestionBank(),
        dsa_bank=DSA_BANK, code_runner=None)  # replaced below
    session, _, coding, _ = s.start_placement("u1", "python", "advanced")
    problems = sample_placement_coding(DSA_BANK, session.id)
    s._runner = OrderedRunner(problems)
    code = {c["id"]: {"language": "python", "code": "print('x')"}
            for c in coding}
    _, analysis = s.submit_placement("u1", session.id, {}, code=code)
    assert analysis["coding_accepted"] == 5
    assert analysis["coding_total"] == 5
    assert all(c["verdict"] == "accepted" for c in analysis["coding"])


def test_submit_coding_not_attempted_without_code(svc):
    session, _, _, _ = svc.start_placement("u1", "python", "advanced")
    _, analysis = svc.submit_placement("u1", session.id, {})
    assert analysis["coding_accepted"] == 0
    assert all(c["verdict"] == "not_attempted"
               for c in analysis["coding"])


def test_submit_coding_engine_error_without_runner():
    s = OnboardingServiceImpl(
        FakeProfiles(), FakePlacements(), StaticQuestionBank(),
        dsa_bank=DSA_BANK, code_runner=None)
    session, _, coding, _ = s.start_placement("u1", "python", "advanced")
    code = {c["id"]: {"language": "python", "code": "print(1)"}
            for c in coding}
    done, analysis = s.submit_placement("u1", session.id, {}, code=code)
    # MCQ grading still completes; coding degrades honestly
    assert done.status == "completed"
    assert all(c["verdict"] == "engine_error" for c in analysis["coding"])


def test_submit_all_wrong_steps_down(svc):
    session, _, _, _ = svc.start_placement("u1", "python", "advanced")
    answers = {qid: 99 for qid in session.question_ids}  # nothing matches
    done, analysis = svc.submit_placement("u1", session.id, answers)
    assert done.verified_level == "beginner"
    assert "verified level: beginner" in analysis["summary"]


def test_submit_partial_finds_true_level(svc):
    bank = StaticQuestionBank()
    session, _, _, _ = svc.start_placement("u1", "python", "advanced")
    answers = {}
    for qid in session.question_ids:
        q = bank.get(qid)
        # ace beginner+intermediate, bomb advanced
        answers[qid] = q.answer_index if q.level != "advanced" else 99
    done, analysis = svc.submit_placement("u1", session.id, answers)
    assert done.verified_level == "intermediate"
    assert analysis["levels"]["advanced"]["correct"] == 0


def test_double_submit_rejected(svc):
    session, _, _, _ = svc.start_placement("u1", "python", "intermediate")
    svc.submit_placement("u1", session.id, {})
    with pytest.raises(DomainError, match="already completed"):
        svc.submit_placement("u1", session.id, {})


def test_other_users_session_rejected(svc):
    session, _, _, _ = svc.start_placement("u1", "python", "intermediate")
    with pytest.raises(DomainError, match="not found"):
        svc.submit_placement("u2", session.id, {})


# ---- F6d v4: written (subjective) questions ----

def test_start_placement_v4_written_counts(svc):
    _, _, _, written = svc.start_placement("u1", "python", "intermediate")
    assert len(written) == 3  # 1 per level x B/I/A
    assert [w["level"] for w in written] == ["beginner", "intermediate", "advanced"]
    # rubric never leaks
    assert all("key_concepts" not in w for w in written)
    assert all("sample_answer" not in w for w in written)


def test_written_rubric_grader_scores_concepts():
    from app.domain.profile import WrittenQuestion, grade_written
    q = WrittenQuestion(
        id="w1", topic="python", level="beginner", prompt="p",
        key_concepts=("mutable", "immutable", "ordered"),
        sample_answer="s",
    )
    r = grade_written(q, "A list is mutable and ordered, while a tuple is immutable.")
    assert r.status == "scored"
    assert r.coverage == 1.0
    assert set(r.matched) == {"mutable", "immutable", "ordered"}


def test_written_rubric_partial_coverage():
    from app.domain.profile import WrittenQuestion, grade_written
    q = WrittenQuestion(
        id="w1", topic="python", level="beginner", prompt="p",
        key_concepts=("mutable", "immutable", "ordered", "hash table"),
        sample_answer="s",
    )
    r = grade_written(q, "Lists are mutable and ordered collections in Python.")
    assert r.status == "scored"
    assert r.coverage == 0.5
    assert "hash table" in r.missed


def test_written_blank_and_short():
    from app.domain.profile import WrittenQuestion, grade_written
    q = WrittenQuestion(
        id="w1", topic="python", level="beginner", prompt="p",
        key_concepts=("mutable",), sample_answer="s",
    )
    assert grade_written(q, "").status == "not_attempted"
    assert grade_written(q, "   ").status == "not_attempted"
    assert grade_written(q, "idk").status == "too_short"


def test_submit_placement_grades_written(svc):
    session, _, _, written = svc.start_placement("u1", "python", "intermediate")
    qid = written[0]["id"]
    done, analysis = svc.submit_placement(
        "u1", session.id, {},
        written={qid: "A list is mutable and ordered, a tuple is immutable."},
    )
    assert done.status == "completed"
    assert analysis["written_total"] == 3
    by_id = {w["question_id"]: w for w in analysis["written"]}
    assert by_id[qid]["status"] == "scored"
    assert by_id[qid]["coverage"] > 0
    # unanswered written -> not_attempted, not a failure
    others = [w for w in analysis["written"] if w["question_id"] != qid]
    assert all(w["status"] == "not_attempted" for w in others)
    # verified level still comes from MCQ
    assert done.verified_level == "beginner"


def test_written_does_not_move_verified_level(svc):
    # perfect written answers cannot lift the verified level above MCQ evidence
    from app.adapters.outbound.question_bank import StaticQuestionBank
    bank = StaticQuestionBank()
    session, _, _, written = svc.start_placement("u1", "python", "advanced")
    answers = {}
    for qid in session.question_ids:
        q = bank.get(qid)
        answers[qid] = q.answer_index if q.level == "beginner" else 99
    written_answers = {w["id"]: "mutable immutable ordered hash table key collision "
                                "global interpreter lock thread CPU-bound multiprocessing"
                       for w in written}
    done, _ = svc.submit_placement("u1", session.id, answers, written=written_answers)
    assert done.verified_level == "beginner"


def test_start_placement_written_works_for_all_topics(svc):
    # regression: ml-basics placement crashed with no written bank
    for topic in ["python", "ml-basics"]:
        _, _, _, written = svc.start_placement("u1", topic, "intermediate")
        assert len(written) == 3
        assert [w["level"] for w in written] == [
            "beginner", "intermediate", "advanced"]
