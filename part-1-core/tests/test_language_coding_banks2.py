"""Tests for the C, JavaScript and Go coding problem banks."""
from __future__ import annotations

import pytest

from app.adapters.outbound.c_coding_bank import (
    get_problem as c_get,
    get_problems as c_problems,
    list_topics as c_topics,
    _C_BANK,
)
from app.adapters.outbound.js_coding_bank import (
    get_problem as js_get,
    get_problems as js_problems,
    list_topics as js_topics,
    _JS_BANK,
)
from app.adapters.outbound.go_coding_bank import (
    get_problem as go_get,
    get_problems as go_problems,
    list_topics as go_topics,
    _GO_BANK,
)

BANKS = [
    ("c", _C_BANK, c_get, c_problems, c_topics, 40, {"c"}),
    ("js", _JS_BANK, js_get, js_problems, js_topics, 40, {"javascript"}),
    ("go", _GO_BANK, go_get, go_problems, go_topics, 30, {"go"}),
]


@pytest.mark.parametrize("name,bank,get,probs,topics,expected,langs", BANKS)
def test_bank_counts(name, bank, get, probs, topics, expected, langs):
    assert len(bank) == expected, f"{name}: expected {expected}, got {len(bank)}"


@pytest.mark.parametrize("name,bank,get,probs,topics,expected,langs", BANKS)
def test_unique_ids(name, bank, get, probs, topics, expected, langs):
    ids = [p.id for p in bank]
    assert len(set(ids)) == len(ids), f"{name}: duplicate ids"


@pytest.mark.parametrize("name,bank,get,probs,topics,expected,langs", BANKS)
def test_valid_starter_code(name, bank, get, probs, topics, expected, langs):
    for p in bank:
        assert set(p.starter_code.keys()) == langs, f"{name}/{p.id}: bad starter_code keys"
        for lang, code in p.starter_code.items():
            assert code and code.strip(), f"{name}/{p.id}: empty starter code"


@pytest.mark.parametrize("name,bank,get,probs,topics,expected,langs", BANKS)
def test_examples_valid(name, bank, get, probs, topics, expected, langs):
    for p in bank:
        assert len(p.examples) >= 1, f"{name}/{p.id}: no examples"
        for ex in p.examples:
            assert ex["input"] is not None and ex["output"], f"{name}/{p.id}: bad example"
            assert ex["explanation"], f"{name}/{p.id}: empty explanation"


@pytest.mark.parametrize("name,bank,get,probs,topics,expected,langs", BANKS)
def test_fields_complete(name, bank, get, probs, topics, expected, langs):
    for p in bank:
        assert p.title and p.description, f"{name}/{p.id}: missing title/desc"
        assert p.difficulty in {"basic", "easy", "medium", "hard"}, f"{name}/{p.id}: bad difficulty"
        assert p.theory and len(p.hints) >= 1, f"{name}/{p.id}: missing theory/hints"
        assert isinstance(p.constraints, list), f"{name}/{p.id}: constraints not a list"


@pytest.mark.parametrize("name,bank,get,probs,topics,expected,langs", BANKS)
def test_accessors(name, bank, get, probs, topics, expected, langs):
    first = bank[0]
    assert get(first.id) is first
    assert get("no-such-id") is None
    assert len(probs()) == expected
    topic = bank[0].topic
    filtered = probs(topic=topic)
    assert filtered and all(p.topic == topic for p in filtered)
    easy = probs(difficulty="basic")
    assert all(p.difficulty == "basic" for p in easy)
    assert topics() == list(dict.fromkeys(p.topic for p in bank))


def test_c_topic_breakdown():
    counts = {}
    for p in _C_BANK:
        counts[p.topic] = counts.get(p.topic, 0) + 1
    assert counts == {"basics": 10, "pointers": 10, "memory": 10, "advanced": 10}


def test_js_topic_breakdown():
    counts = {}
    for p in _JS_BANK:
        counts[p.topic] = counts.get(p.topic, 0) + 1
    assert counts == {"basics": 10, "logic": 10, "advanced": 10, "practice": 10}


def test_go_topic_breakdown():
    counts = {}
    for p in _GO_BANK:
        counts[p.topic] = counts.get(p.topic, 0) + 1
    assert counts == {"basics": 10, "functions": 10, "concurrency": 10}


def test_go_concurrency_problems_present():
    ids = {p.id for p in _GO_BANK}
    for pid in ("go-c01", "go-c05", "go-c07", "go-c10"):
        assert pid in ids


KNOWN_COMPANIES = {
    "tcs", "infosys", "wipro", "tech-mahindra", "accenture", "cognizant",
    "hcl", "amazon", "google", "microsoft", "flipkart", "uber",
    "cloudflare", "dropbox",
}


@pytest.mark.parametrize("name,bank,get,probs,topics,expected,langs", BANKS)
def test_companies_tags_valid(name, bank, get, probs, topics, expected, langs):
    for p in bank:
        assert 1 <= len(p.companies) <= 3, f"{name}/{p.id}: need 1-3 companies"
        unknown = set(p.companies) - KNOWN_COMPANIES
        assert not unknown, f"{name}/{p.id}: unknown companies {unknown}"


def test_companies_survive_filters():
    p = c_problems(topic="pointers")[0]
    assert p.companies, "filtered problem lost its companies tags"
    assert c_get(p.id).companies == p.companies
