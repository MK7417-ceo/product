"""Tests for the OOP curriculum seed: counts, integrity, determinism."""
from app.adapters.outbound.oop_curriculum_seed import (
    MODULE_MAP,
    SIBLING_DOMAIN_SLUG,
    summary,
    verify_counts,
)


def test_domain_slug():
    assert SIBLING_DOMAIN_SLUG == "oop"


def test_counts():
    c = verify_counts()
    assert c["modules"] == 6
    assert c["lessons"] == 36
    assert c["questions"] == 228


def test_per_module_breakdown():
    c = verify_counts()
    pm = c["per_module"]
    assert pm["oop-basics"] == (6, 38)
    assert pm["oop-inheritance"] == (6, 38)
    assert pm["oop-polymorphism"] == (6, 38)
    assert pm["oop-advanced"] == (6, 38)
    assert pm["oop-patterns"] == (7, 44)
    assert pm["oop-practice"] == (5, 32)


def test_no_narrow_lessons():
    c = verify_counts()
    assert c["narrow_lessons"] == [], f"narrow: {c['narrow_lessons']}"


def test_all_modules_mapped():
    c = verify_counts()
    assert c["unmapped_modules"] == []
    assert set(MODULE_MAP) == {
        "oop-basics", "oop-inheritance", "oop-polymorphism",
        "oop-advanced", "oop-patterns", "oop-practice",
    }


def test_visual_lessons():
    c = verify_counts()
    assert set(c["visual_lessons"]) == {"oop-what-is-oop", "oop-solid-srp"}


def test_important_lessons_present():
    c = verify_counts()
    assert len(c["important_lessons"]) >= 10


def test_summary_shape():
    s = summary()
    assert s["domain"] == "oop"
    assert s["modules"] == 6
    assert s["lessons"] == 36
    assert s["questions"] == 228
