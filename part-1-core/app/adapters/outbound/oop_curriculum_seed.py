"""OOP curriculum seed data for SkillForge — expert-level, gradual difficulty.

Deep content pack for the `oop` domain (sibling-seeded modules:
classes-objects, inheritance-poly, abstraction, design-patterns).
6 content modules, 36 lessons, 216 MCQs, difficulty ramping 1-10 inside
every lesson.

Content lives in part files (mirrors the github_*_part pattern):
  oop_part_m1m2.py  — OOP Basics, Inheritance
  oop_part_m3m4.py  — Polymorphism, Advanced Concepts (SOLID)
  oop_part_m5m6.py  — Design Patterns, OOP in Practice

Usage:
  from app.adapters.outbound.oop_curriculum_seed import seed, CURRICULUM
  seed(session)   # idempotent ORM insert via real models
  python -m app.adapters.outbound.oop_curriculum_seed  # verify counts

All content is original — every lesson theory and every question is
written from scratch with real, runnable Python/Java/C++ examples.
Interview-focused: pillars, SOLID, patterns, LLD basics.
"""

from __future__ import annotations

import json
import sys

try:  # package import (normal)
    from .oop_part_m1m2 import MODULES as _M1M2
    from .oop_part_m3m4 import MODULES as _M3M4
    from .oop_part_m5m6 import MODULES as _M5M6
except ImportError:  # direct script execution
    from oop_part_m1m2 import MODULES as _M1M2
    from oop_part_m3m4 import MODULES as _M3M4
    from oop_part_m5m6 import MODULES as _M5M6


DOMAIN = {
    "slug": "oop",
    "name": "Object Oriented Programming",
    "icon": "🧩",
    "description": (
        "The paradigm behind every interview: 6 modules, 36 lessons, 216 "
        "questions — from classes and objects to SOLID principles, design "
        "patterns, and LLD basics. Difficulty rises gradually 1 to 10 inside "
        "every lesson."
    ),
}

MODULES = _M1M2 + _M3M4 + _M5M6

CURRICULUM = {"domain": DOMAIN, "modules": MODULES}

SIBLING_DOMAIN_SLUG = "oop"

# content module -> sibling's seeded module slug
MODULE_MAP = {
    "oop-basics": "classes-objects",
    "oop-inheritance": "inheritance-poly",
    "oop-polymorphism": "inheritance-poly",
    "oop-advanced": "abstraction",
    "oop-patterns": "design-patterns",
    "oop-practice": "classes-objects",
}


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------

def _validate():
    seen_slugs = set()
    for m in MODULES:
        assert m["slug"] in MODULE_MAP, f"module {m['slug']} missing from MODULE_MAP"
        for les in m["lessons"]:
            s = les["slug"]
            assert s not in seen_slugs, f"duplicate lesson slug: {s}"
            seen_slugs.add(s)
            qs = les["questions"]
            assert 5 <= len(qs) <= 8, f"lesson {s}: need 5-8 questions, got {len(qs)}"
            for q in qs:
                assert q["qtype"] == "mcq"
                assert len(q["choices"]) == 4, f"need 4 choices: {q['prompt'][:40]}"
                assert 0 <= q["answer_index"] <= 3
                assert 1 <= q["difficulty"] <= 10, f"bad difficulty in {s}"
                assert q["explanation"], f"missing explanation in {s}"
                assert q["company_tags"], f"missing company_tags in {s}"
            diffs = [q["difficulty"] for q in qs]
            assert max(diffs) - min(diffs) >= 4, (
                f"lesson {s}: difficulty spread too narrow "
                f"({min(diffs)}-{max(diffs)})"
            )
            assert les["difficulty_min"] == min(diffs)
            assert les["difficulty_max"] == max(diffs)


_validate()


# ---------------------------------------------------------------------------
# row iteration (deterministic ids)
# ---------------------------------------------------------------------------

import uuid as _uuid
from datetime import datetime, timezone as _tz


def _lesson_id(slug):
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "skillforge:oop:lesson:" + slug))


def _question_id(lesson_slug, idx):
    return str(_uuid.uuid5(
        _uuid.NAMESPACE_URL, f"skillforge:oop:question:{lesson_slug}:{idx}"))


def _iter_rows():
    """Yield (kind, dict) for every lesson and question, mapped to the
    sibling's already-seeded oop modules."""
    order_per_module = {}
    for m in MODULES:
        sib = MODULE_MAP[m["slug"]]
        order_per_module.setdefault(sib, 100)
        for les in m["lessons"]:
            lid = _lesson_id(les["slug"])
            order_per_module[sib] += 1
            yield ("lesson", {
                "id": lid,
                "module_slug": sib,
                "slug": les["slug"],
                "title": les["title"],
                "content": les["theory_md"],
                "order_index": order_per_module[sib],
                "is_important": bool(les.get("is_important", False)),
                "has_visual": bool(les.get("has_visual", False)),
            })
            for qi, q in enumerate(les["questions"]):
                yield ("question", {
                    "id": _question_id(les["slug"], qi),
                    "lesson_id": lid,
                    "module_slug": sib,
                    "qtype": "mcq",
                    "difficulty": q["difficulty"],
                    "prompt": q["prompt"],
                    "choices": q["choices"],
                    "answer_index": q["answer_index"],
                    "explanation": q["explanation"],
                    "company_tags": q["company_tags"],
                })


def _now_iso():
    return datetime.now(_tz.utc).isoformat()


def _as_sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (list, dict)):
        v = json.dumps(v, ensure_ascii=False)
    return "'" + str(v).replace("'", "''") + "'"


# ---------------------------------------------------------------------------
# seed / emit_sql / verify
# ---------------------------------------------------------------------------


def seed(session=None):
    """Insert the deep OOP content pack.

    Uses the real SQLAlchemy models (app.adapters.outbound.models).
    Attaches lessons/questions to the sibling's seeded `oop` modules.
    Idempotent on lesson/question ids (deterministic uuid5) — skips existing.
    Returns counts dict.
    """
    from app.adapters.outbound.models import (
        CurriculumLessonModel, CurriculumQuestionModel, CurriculumModuleModel,
    )
    counts = {"lessons": 0, "questions": 0, "skipped": 0}
    mod_ids = {}
    for m in MODULES:
        sib = MODULE_MAP[m["slug"]]
        if sib not in mod_ids:
            mod = session.query(CurriculumModuleModel).filter_by(
                slug=sib, domain_slug=SIBLING_DOMAIN_SLUG).one()
            mod_ids[sib] = mod.id
    for kind, r in _iter_rows():
        if kind == "lesson":
            exists = session.query(CurriculumLessonModel).filter_by(
                id=r["id"]).first()
            if exists:
                counts["skipped"] += 1
                continue
            session.add(CurriculumLessonModel(
                id=r["id"], module_id=mod_ids[r["module_slug"]],
                slug=r["slug"], title=r["title"], content=r["content"],
                order_index=r["order_index"], estimated_minutes=30,
                has_visual=r["has_visual"], is_important=r["is_important"]))
            counts["lessons"] += 1
        else:
            exists = session.query(CurriculumQuestionModel).filter_by(
                id=r["id"]).first()
            if exists:
                counts["skipped"] += 1
                continue
            session.add(CurriculumQuestionModel(
                id=r["id"], domain_slug=SIBLING_DOMAIN_SLUG,
                module_slug=r["module_slug"], lesson_id=r["lesson_id"],
                difficulty=r["difficulty"], qtype=r["qtype"],
                prompt=r["prompt"],
                choices=json.dumps(r["choices"]) if r["choices"] else None,
                answer_index=r["answer_index"], explanation=r["explanation"],
                company_tags=json.dumps(r["company_tags"]),
                created_at=datetime.now(_tz.utc)))
            counts["questions"] += 1
    session.commit()
    return counts


def emit_sql(out=None):
    """Emit INSERTs against the real curriculum_* tables.

    Lessons attach to the sibling's already-seeded oop modules via a
    module_id subselect; questions carry domain/module slugs + lesson_id.
    """
    out = out or sys.stdout
    ts = _now_iso()
    for kind, r in _iter_rows():
        if kind == "lesson":
            out.write(
                "INSERT INTO curriculum_lessons "
                "(id, module_id, slug, title, content, order_index, "
                "estimated_minutes, has_visual, is_important) "
                "SELECT %s, m.id, %s, 30, %s, %s FROM curriculum_modules m "
                "WHERE m.slug = %s AND m.domain_slug = %s;\n"
                % (_as_sql_value(r["id"]),
                   ", ".join(_as_sql_value(r[k]) for k in
                             ("slug", "title", "content", "order_index")),
                   _as_sql_value(r["has_visual"]),
                   _as_sql_value(r["is_important"]),
                   _as_sql_value(r["module_slug"]),
                   _as_sql_value(SIBLING_DOMAIN_SLUG)))
        else:
            out.write(
                "INSERT INTO curriculum_questions "
                "(id, domain_slug, module_slug, lesson_id, difficulty, qtype, "
                "prompt, choices, answer_index, explanation, company_tags, "
                "created_at) VALUES (%s);\n"
                % ", ".join([
                    _as_sql_value(r["id"]),
                    _as_sql_value(SIBLING_DOMAIN_SLUG),
                    _as_sql_value(r["module_slug"]),
                    _as_sql_value(r["lesson_id"]),
                    str(r["difficulty"]),
                    _as_sql_value(r["qtype"]),
                    _as_sql_value(r["prompt"]),
                    _as_sql_value(r["choices"]),
                    _as_sql_value(r["answer_index"]),
                    _as_sql_value(r["explanation"]),
                    _as_sql_value(r["company_tags"]),
                    _as_sql_value(ts),
                ]))
    out.flush()


def verify_counts():
    modules = MODULES
    lessons = sum(len(m["lessons"]) for m in modules)
    mcqs = sum(len(les["questions"]) for m in modules for les in m["lessons"])
    per_module = {m["slug"]: (len(m["lessons"]),
                              sum(len(les["questions"]) for les in m["lessons"]))
                  for m in modules}
    narrow = [les["slug"] for m in modules for les in m["lessons"]
              if les["difficulty_max"] - les["difficulty_min"] < 4]
    unmapped = [m["slug"] for m in modules if m["slug"] not in MODULE_MAP]
    important = [les["slug"] for m in modules for les in m["lessons"]
                 if les.get("is_important")]
    visuals = [les["slug"] for m in modules for les in m["lessons"]
               if les.get("has_visual")]
    return {"modules": len(modules), "lessons": lessons, "questions": mcqs,
            "per_module": per_module, "narrow_lessons": narrow,
            "unmapped_modules": unmapped, "important_lessons": important,
            "visual_lessons": visuals}


def summary():
    c = verify_counts()
    return {
        "domain": SIBLING_DOMAIN_SLUG,
        "modules": c["modules"],
        "lessons": c["lessons"],
        "questions": c["questions"],
        "per_module": c["per_module"],
    }


if __name__ == "__main__":
    import pprint
    pprint.pprint(verify_counts())
