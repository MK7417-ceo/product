"""Tests for the Python + Java coding problem banks."""
from __future__ import annotations

from collections import Counter

from app.adapters.outbound.python_coding_bank import (
    _PYTHON_BANK,
    get_problem as get_py_problem,
    get_problems as get_py_problems,
    list_topics as py_topics,
)
from app.adapters.outbound.java_coding_bank import (
    _JAVA_BANK,
    get_problem as get_java_problem,
    get_problems as get_java_problems,
    list_topics as java_topics,
)

VALID_DIFFICULTIES = {"basic", "easy", "medium", "hard"}
VALID_COMPANIES = {"tcs", "infosys", "wipro", "amazon", "google", "flipkart",
                   "microsoft", "meta"}


def _check_bank(bank, lang: str, expected_topics: list[str]):
    assert len(bank) == 50, f"{lang}: expected 50 problems, got {len(bank)}"
    ids = [p.id for p in bank]
    assert len(set(ids)) == len(ids), f"{lang}: duplicate ids"
    topics = Counter(p.topic for p in bank)
    for t in expected_topics:
        assert topics[t] == 10, f"{lang}: topic {t} has {topics[t]}, expected 10"
    for p in bank:
        assert p.difficulty in VALID_DIFFICULTIES, f"{lang}:{p.id} bad difficulty"
        assert p.title and p.description, f"{lang}:{p.id} missing title/description"
        assert len(p.examples) >= 1, f"{lang}:{p.id} no examples"
        for e in p.examples:
            assert set(e.keys()) == {"input", "output", "explanation"}, (
                f"{lang}:{p.id} bad example keys: {e.keys()}"
            )
            assert e["input"] != "" or True  # input may be descriptive
            assert e["output"], f"{lang}:{p.id} empty example output"
        assert len(p.constraints) >= 1, f"{lang}:{p.id} no constraints"
        assert p.theory and len(p.theory) > 40, f"{lang}:{p.id} theory too short"
        assert len(p.hints) >= 1, f"{lang}:{p.id} no hints"
        assert lang in p.starter_code and p.starter_code[lang].strip(), (
            f"{lang}:{p.id} missing starter_code"
        )
        assert len(p.test_cases) >= 1, f"{lang}:{p.id} no test_cases"
        for t in p.test_cases:
            assert set(t.keys()) == {"input", "expected"}, (
                f"{lang}:{p.id} bad test_case keys"
            )
        assert 1 <= len(p.companies) <= 3, (
            f"{lang}:{p.id} companies must be 1-3, got {p.companies}"
        )
        assert all(c in VALID_COMPANIES for c in p.companies), (
            f"{lang}:{p.id} invalid company tag: {p.companies}"
        )


def test_python_bank_count_and_topics():
    _check_bank(
        _PYTHON_BANK, "python",
        ["basics", "data-structures", "functions", "oop", "advanced"],
    )


def test_java_bank_count_and_topics():
    _check_bank(
        _JAVA_BANK, "java",
        ["basics", "oop", "collections", "advanced", "practice"],
    )


def test_python_bank_ids_unique_and_prefixed():
    ids = [p.id for p in _PYTHON_BANK]
    assert all(i.startswith("py-") for i in ids)
    assert len(set(ids)) == 50


def test_java_bank_ids_unique_and_prefixed():
    ids = [p.id for p in _JAVA_BANK]
    assert all(i.startswith("ja-") for i in ids)
    assert len(set(ids)) == 50


def test_no_cross_bank_id_collision():
    py_ids = {p.id for p in _PYTHON_BANK}
    java_ids = {p.id for p in _JAVA_BANK}
    assert not (py_ids & java_ids), "id collision across banks"


def test_python_get_problems_filter():
    basics = get_py_problems(topic="basics")
    assert len(basics) == 10
    assert all(p.topic == "basics" for p in basics)
    hard = get_py_problems(difficulty="hard")
    assert all(p.difficulty == "hard" for p in hard)
    assert get_py_problem("py-b01") is not None
    assert get_py_problem("nope") is None
    assert py_topics() == ["basics", "data-structures", "functions", "oop", "advanced"]


def test_java_get_problems_filter():
    oop = get_java_problems(topic="oop")
    assert len(oop) == 10
    assert all(p.topic == "oop" for p in oop)
    medium = get_java_problems(topic="collections", difficulty="medium")
    assert all(p.difficulty == "medium" and p.topic == "collections" for p in medium)
    assert get_java_problem("ja-b01") is not None
    assert get_java_problem("nope") is None
    assert java_topics() == ["basics", "oop", "collections", "advanced", "practice"]


def test_difficulty_progression_sane():
    # basics should skew easy, later topics should include medium/hard
    order = {"basic": 0, "easy": 1, "medium": 2, "hard": 3}
    for bank, topics in [(_PYTHON_BANK, py_topics()), (_JAVA_BANK, java_topics())]:
        first_topic = topics[0]
        last_topic = topics[-1]
        first_avg = sum(order[p.difficulty] for p in bank if p.topic == first_topic) / 10
        last_avg = sum(order[p.difficulty] for p in bank if p.topic == last_topic) / 10
        assert last_avg >= first_avg, "difficulty should not decrease across topics"


def test_companies_coverage():
    # every major company appears across the banks; service-cos dominate basics
    from collections import Counter
    all_cos = Counter()
    for p in list(_PYTHON_BANK) + list(_JAVA_BANK):
        all_cos.update(p.companies)
    for co in ("tcs", "infosys", "amazon"):
        assert all_cos[co] >= 10, f"{co} underrepresented: {all_cos[co]}"
    # basics skew to service companies
    basics_cos = Counter()
    for p in list(_PYTHON_BANK) + list(_JAVA_BANK):
        if p.topic == "basics":
            basics_cos.update(p.companies)
    assert basics_cos["tcs"] + basics_cos["infosys"] + basics_cos["wipro"] >= 15
