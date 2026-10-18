"""Tests for the English Communication track seed (english_comm_seed)."""
from collections import Counter

import pytest

from app.adapters.outbound.english_comm_seed import (
    MODULE_MAP,
    MODULES,
    summary,
    verify_counts,
)


def _all_lessons():
    for m in MODULES:
        for les in m["lessons"]:
            yield m, les


def test_module_and_lesson_counts():
    c = verify_counts()
    assert c["modules"] == 8
    assert c["lessons"] == 41
    assert c["items"] >= 200
    assert not c["narrow_lessons"]
    assert not c["unmapped_modules"]


def test_every_module_mapped():
    for m in MODULES:
        assert m["slug"] in MODULE_MAP


def test_lesson_slugs_unique():
    seen = set()
    for _, les in _all_lessons():
        assert les["slug"] not in seen
        seen.add(les["slug"])


def test_practice_type_present_and_embedded():
    for _, les in _all_lessons():
        assert les["practice_type"] in {"mcq", "speaking", "writing", "listening"}
        assert "<!-- practice_type:" in les["theory_md"]


def test_items_have_model_answers():
    for _, les in _all_lessons():
        for q in les["questions"]:
            assert q["prompt"]
            assert q["explanation"], f"missing model answer in {les['slug']}"
            assert q["company_tags"]


def test_mcq_shape_and_answer_positions():
    pos = Counter()
    n = 0
    for _, les in _all_lessons():
        for q in les["questions"]:
            if q["qtype"] != "mcq":
                continue
            n += 1
            assert len(q["choices"]) == 4
            assert 0 <= q["answer_index"] < 4
            pos[q["answer_index"]] += 1
    assert n > 0
    # no clustering: every position used substantially
    for i in range(4):
        assert pos[i] >= n * 0.15, f"answer position {i} underused: {dict(pos)}"


def test_practice_items_have_no_choices():
    for _, les in _all_lessons():
        for q in les["questions"]:
            if q["qtype"] != "mcq":
                assert q["choices"] is None
                assert q["answer_index"] is None


def test_difficulty_spread_and_bounds_match():
    for _, les in _all_lessons():
        diffs = [q["difficulty"] for q in les["questions"]]
        assert max(diffs) - min(diffs) >= 4
        assert les["difficulty_min"] == min(diffs)
        assert les["difficulty_max"] == max(diffs)
        assert all(1 <= d <= 10 for d in diffs)


def test_summary_shape():
    s = summary()
    assert s["domain"] == "english"
    assert s["lessons"] == 41
    assert s["items"] >= 200


def test_seed_idempotent_on_migrated_db():
    """Seed into a migrated sqlite DB twice; second run skips everything."""
    import os
    import re
    import subprocess
    import sys
    import tempfile
    from pathlib import Path

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.adapters.outbound.english_comm_seed import seed
    from app.adapters.outbound.models import (
        CurriculumLessonModel,
        CurriculumQuestionModel,
    )

    # Resolve part-1-core/ from this file's location — no machine-specific paths,
    # so the test also passes on CI runners.
    core_dir = Path(__file__).resolve().parent.parent
    tmp = Path(tempfile.mkdtemp(prefix="eng_comm_seed_test_"))
    db = tmp / "seed.db"

    # Temp alembic.ini pointed at the throwaway sqlite DB.
    ini = tmp / "alembic.ini"
    ini_text = (core_dir / "alembic.ini").read_text()
    ini_text, n_url = re.subn(
        r"(?m)^sqlalchemy\.url\s*=.*$",
        f"sqlalchemy.url = sqlite:///{db}",
        ini_text,
    )
    assert n_url == 1, "sqlalchemy.url line not found in alembic.ini"
    ini_text, n_loc = re.subn(
        r"(?m)^script_location\s*=.*$",
        f"script_location = {core_dir / 'alembic'}",
        ini_text,
    )
    assert n_loc == 1, "script_location line not found in alembic.ini"
    ini.write_text(ini_text)

    # Run migrations to get real tables, using this same python env's alembic.
    env = dict(os.environ, SECRET_KEY="test12345678901234567890123456789012")
    subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(ini), "upgrade", "head"],
        check=True, cwd=core_dir, env=env, capture_output=True, text=True,
    )
    engine = create_engine(f"sqlite:///{db}")
    s = sessionmaker(bind=engine)()
    lessons_before = s.query(CurriculumLessonModel).count()
    questions_before = s.query(CurriculumQuestionModel).count()
    r1 = seed(s)
    assert r1["domains"] == 1
    assert r1["modules"] == 8
    assert r1["lessons"] == 41
    assert r1["questions"] >= 200
    assert s.query(CurriculumLessonModel).count() == lessons_before + 41
    r2 = seed(s)
    assert r2["lessons"] == 0 and r2["questions"] == 0
    assert r2["skipped"] > 0
    assert s.query(CurriculumQuestionModel).count() == questions_before + r1["questions"]
