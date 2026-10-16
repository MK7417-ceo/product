"""English Communication track seed for SkillForge — start to expert, industry-focused.

A complete communication learning track for Indian professionals, NOT just
quiz questions: foundations, workplace vocabulary, speaking skills, email
writing (with real templates), meetings, presentations, interviews, and
advanced workplace communication (persuasion, feedback, cross-cultural,
networking).

8 content modules, 41 lessons, 200+ practice items (MCQs + speaking /
writing / listening exercises), difficulty ramping 1-10 inside every
lesson.

Content lives in part files:
  english_part_m1m2.py — Foundations, Workplace Vocabulary
  english_part_m3m4.py — Speaking Skills, Email Writing
  english_part_m5m6.py — Meetings, Presentations
  english_part_m7m8.py — Interviews, Advanced

Unlike other tracks, there is no pre-seeded `english` domain in the
migrations, so seed() creates the domain + its 8 modules idempotently
(deterministic uuid5 ids) — a migration-less seed using the curriculum
tables directly.

Question dicts use qtype: mcq | speaking | writing | listening.
Non-MCQ items carry the model answer / practice guidance in `explanation`.
Each lesson carries `practice_type` (also embedded as an HTML comment at
the top of its theory_md) so the frontend can render the right UI.

Usage:
  from app.adapters.outbound.english_comm_seed import seed, CURRICULUM
  seed(session)   # idempotent ORM insert via real models
  python -m app.adapters.outbound.english_comm_seed  # verify counts

Quality rule (user): no filler. Every lesson and exercise must be
genuinely useful for an Indian professional — real templates, real
scenarios, real mistakes to fix. Quality over quantity.
"""

from __future__ import annotations

import json
import sys

try:  # package import (normal)
    from .english_part_m1m2 import MODULES as _M1M2
    from .english_part_m3m4 import MODULES as _M3M4
    from .english_part_m5m6 import MODULES as _M5M6
    from .english_part_m7m8 import MODULES as _M7M8
except ImportError:  # direct script execution
    from english_part_m1m2 import MODULES as _M1M2
    from english_part_m3m4 import MODULES as _M3M4
    from english_part_m5m6 import MODULES as _M5M6
    from english_part_m7m8 import MODULES as _M7M8


DOMAIN = {
    "slug": "english",
    "name": "English Communication",
    "icon": "🗣️",
    "category": "language",
    "order_index": 27,
    "description": (
        "From hesitant to fluent: sentence foundations, workplace "
        "vocabulary, speaking drills, email templates, meetings, "
        "presentations, interviews, and advanced workplace communication. "
        "Built for Indian professionals — real mistakes fixed, real "
        "templates, real scenarios."
    ),
}

MODULES = _M1M2 + _M3M4 + _M5M6 + _M7M8

CURRICULUM = {"domain": DOMAIN, "modules": MODULES}

SIBLING_DOMAIN_SLUG = "english"

# content module -> curriculum module slug (identity: this seed owns its modules)
MODULE_MAP = {m["slug"]: m["slug"] for m in MODULES}

VALID_QTYPES = {"mcq", "speaking", "writing", "listening"}
VALID_PRACTICE_TYPES = {"mcq", "speaking", "writing", "listening"}


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------

def _validate():
    seen_slugs = set()
    assert len(MODULES) == 8, f"expected 8 modules, got {len(MODULES)}"
    for m in MODULES:
        assert m["slug"] in MODULE_MAP, f"module {m['slug']} missing from MODULE_MAP"
        for les in m["lessons"]:
            s = les["slug"]
            assert s not in seen_slugs, f"duplicate lesson slug: {s}"
            seen_slugs.add(s)
            assert les.get("practice_type") in VALID_PRACTICE_TYPES, (
                f"lesson {s}: bad/missing practice_type")
            assert "<!-- practice_type:" in les["theory_md"], (
                f"lesson {s}: practice_type not embedded in theory_md")
            qs = les["questions"]
            assert 3 <= len(qs) <= 6, (
                f"lesson {s}: need 3-6 items, got {len(qs)}")
            has_mcq = False
            for q in qs:
                assert q["qtype"] in VALID_QTYPES, f"bad qtype in {s}"
                assert 1 <= q["difficulty"] <= 10, f"bad difficulty in {s}"
                assert q["prompt"], f"missing prompt in {s}"
                assert q["explanation"], f"missing explanation/model answer in {s}"
                assert q["company_tags"], f"missing company_tags in {s}"
                if q["qtype"] == "mcq":
                    has_mcq = True
                    assert q["choices"] is not None and len(q["choices"]) == 4, (
                        f"need 4 choices: {q['prompt'][:40]}")
                    assert 0 <= q["answer_index"] <= 3
                else:
                    assert q["choices"] is None, (
                        f"practice item must not have choices: {q['prompt'][:40]}")
                    assert q["answer_index"] is None, (
                        f"practice item must not have answer_index: {q['prompt'][:40]}")
            assert has_mcq, f"lesson {s}: no MCQ — every lesson needs at least one"
            diffs = [q["difficulty"] for q in qs]
            assert max(diffs) - min(diffs) >= 4, (
                f"lesson {s}: difficulty spread too narrow "
                f"({min(diffs)}-{max(diffs)})")
            assert les["difficulty_min"] == min(diffs)
            assert les["difficulty_max"] == max(diffs)


_validate()


# ---------------------------------------------------------------------------
# row iteration (deterministic ids)
# ---------------------------------------------------------------------------

import uuid as _uuid
from datetime import datetime, timezone as _tz


def _domain_id():
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "skillforge:english:domain"))


def _module_id(slug):
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "skillforge:english:module:" + slug))


def _lesson_id(slug):
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "skillforge:english:lesson:" + slug))


def _question_id(lesson_slug, idx):
    return str(_uuid.uuid5(
        _uuid.NAMESPACE_URL, f"skillforge:english:question:{lesson_slug}:{idx}"))


def _iter_rows():
    """Yield (kind, dict) for domain, modules, lessons and questions."""
    yield ("domain", {
        "id": _domain_id(),
        "slug": DOMAIN["slug"],
        "name": DOMAIN["name"],
        "icon": DOMAIN["icon"],
        "description": DOMAIN["description"],
        "category": DOMAIN["category"],
        "order_index": DOMAIN["order_index"],
    })
    for mi, m in enumerate(MODULES):
        yield ("module", {
            "id": _module_id(m["slug"]),
            "domain_slug": SIBLING_DOMAIN_SLUG,
            "slug": m["slug"],
            "name": m["name"],
            "description": m["description"],
            "order_index": mi + 1,
            "estimated_days": 7,
        })
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
                    "qtype": q["qtype"],
                    "difficulty": q["difficulty"],
                    "prompt": q["prompt"],
                    "choices": q["choices"],
                    "answer_index": q["answer_index"],
                    "explanation": q["explanation"],
                    "company_tags": q["company_tags"],
                })


def _now_iso():
    return datetime.now(_tz.utc).isoformat()


# ---------------------------------------------------------------------------
# seed / verify
# ---------------------------------------------------------------------------

def seed(session=None):
    """Insert the English Communication track.

    Creates the `english` domain + its 8 modules if missing (deterministic
    uuid5 ids — migration-less), then attaches lessons/questions.
    Idempotent on all ids — skips existing rows. Returns counts dict.
    """
    from app.adapters.outbound.models import (
        CurriculumDomainModel, CurriculumModuleModel,
        CurriculumLessonModel, CurriculumQuestionModel,
    )
    counts = {"domains": 0, "modules": 0, "lessons": 0, "questions": 0,
              "skipped": 0}
    mod_ids = {}
    for kind, r in _iter_rows():
        if kind == "domain":
            exists = session.query(CurriculumDomainModel).filter_by(
                slug=r["slug"]).first()
            if exists:
                counts["skipped"] += 1
                continue
            session.add(CurriculumDomainModel(
                id=r["id"], slug=r["slug"], name=r["name"], icon=r["icon"],
                description=r["description"], category=r["category"],
                order_index=r["order_index"], is_active=True))
            counts["domains"] += 1
        elif kind == "module":
            exists = session.query(CurriculumModuleModel).filter_by(
                id=r["id"]).first()
            if exists:
                counts["skipped"] += 1
            else:
                session.add(CurriculumModuleModel(
                    id=r["id"], domain_slug=r["domain_slug"], slug=r["slug"],
                    name=r["name"], description=r["description"],
                    order_index=r["order_index"],
                    estimated_days=r["estimated_days"]))
                counts["modules"] += 1
            mod_ids[r["slug"]] = r["id"]
        elif kind == "lesson":
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


def verify_counts():
    modules = MODULES
    lessons = sum(len(m["lessons"]) for m in modules)
    items = sum(len(les["questions"]) for m in modules for les in m["lessons"])
    mcqs = sum(1 for m in modules for les in m["lessons"]
               for q in les["questions"] if q["qtype"] == "mcq")
    practice = items - mcqs
    per_module = {m["slug"]: (len(m["lessons"]),
                              sum(len(les["questions"]) for les in m["lessons"]))
                  for m in modules}
    by_qtype = {}
    for m in modules:
        for les in m["lessons"]:
            for q in les["questions"]:
                by_qtype[q["qtype"]] = by_qtype.get(q["qtype"], 0) + 1
    narrow = [les["slug"] for m in modules for les in m["lessons"]
              if les["difficulty_max"] - les["difficulty_min"] < 4]
    unmapped = [m["slug"] for m in modules if m["slug"] not in MODULE_MAP]
    important = [les["slug"] for m in modules for les in m["lessons"]
                 if les.get("is_important")]
    return {"modules": len(modules), "lessons": lessons, "items": items,
            "mcqs": mcqs, "practice_items": practice, "by_qtype": by_qtype,
            "per_module": per_module, "narrow_lessons": narrow,
            "unmapped_modules": unmapped, "important_lessons": important}


def summary():
    c = verify_counts()
    return {
        "domain": SIBLING_DOMAIN_SLUG,
        "modules": c["modules"],
        "lessons": c["lessons"],
        "items": c["items"],
        "mcqs": c["mcqs"],
        "practice_items": c["practice_items"],
        "per_module": c["per_module"],
    }


if __name__ == "__main__":
    c = verify_counts()
    print("modules:", c["modules"])
    print("lessons:", c["lessons"])
    print("items:", c["items"], f"(mcq: {c['mcqs']}, practice: {c['practice_items']})")
    print("by qtype:", c["by_qtype"])
    print("\nper module (lessons, items):")
    for slug, (nl, nq) in c["per_module"].items():
        print(f"  {slug}: {nl} lessons, {nq} items")
    print("\nimportant lessons:", len(c["important_lessons"]))
    for s in c["important_lessons"]:
        print("  ⭐", s)
    if c["narrow_lessons"]:
        print("\nNARROW:", c["narrow_lessons"])
    if c["unmapped_modules"]:
        print("\nUNMAPPED:", c["unmapped_modules"])
