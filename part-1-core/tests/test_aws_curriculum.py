"""Tests for the AWS curriculum seed: counts, integrity, determinism."""
from app.adapters.outbound.aws_curriculum_seed import (
    AWS_DOMAIN,
    AWS_LESSONS,
    AWS_MODULES,
    AWS_QUESTIONS,
    seed_payload,
    shuffle_options,
    summary,
)


def test_domain_shape():
    assert AWS_DOMAIN.slug == "aws"
    assert AWS_DOMAIN.category == "tech-domain"
    assert AWS_DOMAIN.is_active


def test_counts():
    assert len(AWS_MODULES) == 5
    assert len(AWS_LESSONS) == 35
    assert len(AWS_QUESTIONS) == 210


def test_per_module_breakdown():
    s = summary()
    assert s["integrity_problems"] == []
    bm = s["by_module"]
    assert bm["aws-m1"]["lessons"] == 8 and bm["aws-m1"]["questions"] == 48
    assert bm["aws-m2"]["lessons"] == 7 and bm["aws-m2"]["questions"] == 42
    assert bm["aws-m3"]["lessons"] == 7 and bm["aws-m3"]["questions"] == 42
    assert bm["aws-m4"]["lessons"] == 7 and bm["aws-m4"]["questions"] == 42
    assert bm["aws-m5"]["lessons"] == 6 and bm["aws-m5"]["questions"] == 36


def test_difficulty_spread_per_lesson():
    # every lesson must span at least 4 difficulty points (gradual ramp)
    by_lesson: dict[str, set] = {}
    for q in AWS_QUESTIONS:
        by_lesson.setdefault(q.lesson_id or "", set()).add(q.difficulty)
    narrow = {lid: ds for lid, ds in by_lesson.items() if max(ds) - min(ds) < 4}
    assert not narrow, f"lessons with narrow difficulty span: {narrow}"


def test_questions_have_explanations_and_tags():
    for q in AWS_QUESTIONS:
        assert q.explanation.strip(), q.id
        assert len(q.choices) == 4, q.id
        assert q.answer_index is not None and 0 <= q.answer_index <= 3, q.id
        assert len(q.company_tags) >= 1, q.id


def test_answer_positions_roughly_uniform():
    from collections import Counter
    c = Counter(q.answer_index for q in AWS_QUESTIONS)
    # 210 questions / 4 positions = 52.5 expected; allow wide band
    for pos in range(4):
        assert 35 <= c[pos] <= 70, f"position {pos}: {c[pos]}"


def test_shuffle_is_deterministic():
    q = AWS_QUESTIONS[0]
    a = shuffle_options(q)
    b = shuffle_options(q)
    assert a.choices == b.choices and a.answer_index == b.answer_index


def test_seed_payload_json_serializable():
    import json
    p = seed_payload()
    json.dumps(p)
    assert len(p["questions"]) == 210
    assert len(p["lessons"]) == 35
    assert len(p["modules"]) == 5
