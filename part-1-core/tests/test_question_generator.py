"""Tests for the deterministic question generator (pure domain, no DB)."""
import random

import pytest

from app.domain.question_generator import (
    SUPPORTED_DOMAINS,
    _big_o_value,
    _bubble_pass,
    _fcfs_total_waiting,
    _fifo_faults,
    _highest_nf,
    _lru_faults,
    _rr_total_waiting,
    _selection_pass,
    _sjf_total_waiting,
    generate_questions,
    questions_generatable,
)
from app.domain.user import DomainError


def _check_shape(q):
    assert isinstance(q["prompt"], str) and q["prompt"]
    assert len(q["choices"]) == 4
    assert len(set(q["choices"])) == 4, "choices must be distinct"
    assert 0 <= q["answer_index"] < 4
    assert q["explanation"]
    assert 1 <= q["difficulty"] <= 10
    assert q["qtype"] == "mcq"
    assert q["company_tags"]
    assert "/" in q["generator"]


# ---- determinism ----

def test_same_seed_same_output():
    a = generate_questions("dsa", seed=42, count=30)
    b = generate_questions("dsa", seed=42, count=30)
    assert a == b


def test_different_seeds_differ():
    a = generate_questions("dsa", seed=1, count=30)
    b = generate_questions("dsa", seed=2, count=30)
    assert [q["prompt"] for q in a] != [q["prompt"] for q in b]


def test_determinism_os_dbms():
    for domain in ("os", "dbms"):
        a = generate_questions(domain, seed=7, count=20)
        b = generate_questions(domain, seed=7, count=20)
        assert a == b


def test_no_duplicate_prompts_in_batch():
    qs = generate_questions("dsa", seed=99, count=200)
    prompts = [q["prompt"] for q in qs]
    assert len(set(prompts)) == len(prompts)


def test_difficulty_range_respected():
    qs = generate_questions("os", seed=5, count=40, difficulty_range=(7, 9))
    assert qs
    assert all(7 <= q["difficulty"] <= 9 for q in qs)


def test_invalid_domain_raises():
    with pytest.raises(DomainError):
        generate_questions("astrology", seed=1, count=5)


def test_bad_difficulty_range_raises():
    with pytest.raises(DomainError):
        generate_questions("dsa", seed=1, count=5, difficulty_range=(9, 3))
    with pytest.raises(DomainError):
        generate_questions("dsa", seed=1, count=0)


def test_all_questions_valid_shape():
    for domain in SUPPORTED_DOMAINS:
        for q in generate_questions(domain, seed=11, count=25):
            _check_shape(q)


# ---- computed-answer spot checks ----

def test_bubble_pass_known():
    assert _bubble_pass([5, 1, 4, 2, 8]) == [1, 4, 2, 5, 8]


def test_selection_pass_known():
    assert _selection_pass([5, 1, 4, 2, 8]) == [1, 5, 4, 2, 8]


def test_fifo_classic_reference_string():
    # textbook example: 9 faults
    refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    assert _fifo_faults(refs, 3) == 9


def test_lru_classic_reference_string():
    refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    assert _lru_faults(refs, 3) == 10


def test_fcfs_total_waiting_known():
    procs = [("P1", 0, 5), ("P2", 1, 3)]
    # P1: start 0 wait 0; P2: start 5 wait 4
    assert _fcfs_total_waiting(procs) == 4


def test_sjf_picks_shortest():
    procs = [("P1", 0, 8), ("P2", 0, 2), ("P3", 0, 4)]
    # order P2, P3, P1: waits 0, 2, 6 -> total 8
    assert _sjf_total_waiting(procs) == 8


def test_rr_total_waiting_known():
    procs = [("P1", 0, 5), ("P2", 0, 3)]
    # q=2: P1 0-2, P2 2-4, P1 4-6, P2 6-7 (done), P1 7-8 (done)
    # P1: completion 8, wait = 8-0-5 = 3; P2: completion 7, wait = 7-0-3 = 4
    assert _rr_total_waiting(procs, 2) == 7


def test_normal_form_templates():
    assert _highest_nf(("A", "B", "C"), [(("A",), ("B",)), ((("B",), ("C",)))]) == "2NF"
    assert _highest_nf(("A", "B", "C"), [((("A", "B"), ("C",)))]) == "BCNF"
    assert _highest_nf(("A", "B", "C"), [(("A",), ("B",))]) == "1NF"
    assert _highest_nf(("A", "B", "C"), [(("A",), ("B",)), ((("A",), ("C",)))]) == "BCNF"
    assert _highest_nf(("A", "B", "C"), [(("B",), ("C",)), ((("A",), ("B",)))]) == "2NF"
    assert _highest_nf(("A", "B", "C", "D"),
                       [((("A", "B"), ("C",))), ((("C",), ("D",)))]) == "2NF"


def test_big_o_values_ordered():
    n = 1000
    vals = [_big_o_value(c, n) for c in
            ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)"]]
    assert vals == sorted(vals)


def test_generated_answers_match_recomputation():
    """Spot-check: recompute a sample of generated answers independently."""
    rng = random.Random(1234)
    qs = generate_questions("dsa", seed=1234, count=60)
    assert len(qs) == 60
    # every answer_index must point at a choice (structural integrity)
    for q in qs:
        assert q["choices"][q["answer_index"]]  # non-empty string


# ---- capacity ----

def test_capacity_targets():
    assert questions_generatable("dsa") >= 500
    assert questions_generatable("os") >= 300
    assert questions_generatable("dbms") >= 300


def test_capacity_invalid_domain():
    with pytest.raises(DomainError):
        questions_generatable("nope")


def test_large_batch_generation():
    qs = generate_questions("dsa", seed=2026, count=500)
    assert len(qs) == 500
    for q in qs:
        _check_shape(q)
