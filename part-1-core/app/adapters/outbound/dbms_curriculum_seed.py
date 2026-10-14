"""Seed script: DBMS curriculum (B.Tech CS core subject).

Assembles the part-files (dbms_part_m1 / dbms_part_m2m3 / dbms_part_m4m5m6) into
validated domain objects from app.domain.curriculum, ready for the curriculum
table loader (sibling workstream).

What this script guarantees on top of the raw parts:
- deterministic option shuffle per question (seeded by question id), so the
  correct answer is uniformly distributed across positions instead of
  clustering at index 0;
- cross-part integrity checks (unique ids, valid lesson/module references,
  difficulty 1-10, module slugs unique).

Content: 6 modules, 40 lessons, 240 MCQs, difficulty ramp 1-9.
All theory and explanations are written originally for SkillForge.

Usage:
    from app.adapters.outbound.dbms_curriculum_seed import (
        DBMS_DOMAIN, DBMS_MODULES, DBMS_LESSONS, DBMS_QUESTIONS, seed_payload, summary,
    )
"""
from __future__ import annotations

import hashlib
import random
from collections import Counter

from app.domain.curriculum import (
    CurriculumDomain,
    CurriculumQuestion,
    validate_curriculum_question,
    validate_difficulty,
)

try:  # package import (normal)
    from .dbms_part_m1 import MODULES as _M1_MODS, LESSONS as _M1_LESSONS, QUESTIONS as _M1_QS
    from .dbms_part_m2m3 import MODULES as _M23_MODS, LESSONS as _M23_LESSONS, QUESTIONS as _M23_QS
    from .dbms_part_m4m5m6 import MODULES as _M456_MODS, LESSONS as _M456_LESSONS, QUESTIONS as _M456_QS
except ImportError:  # direct script execution
    from dbms_part_m1 import MODULES as _M1_MODS, LESSONS as _M1_LESSONS, QUESTIONS as _M1_QS
    from dbms_part_m2m3 import MODULES as _M23_MODS, LESSONS as _M23_LESSONS, QUESTIONS as _M23_QS
    from dbms_part_m4m5m6 import MODULES as _M456_MODS, LESSONS as _M456_LESSONS, QUESTIONS as _M456_QS


DBMS_DOMAIN = CurriculumDomain(
    id="dbms",
    slug="dbms",
    name="Database Management Systems",
    icon="🗄️",
    description=(
        "Core B.Tech CS subject for placements: ER design, SQL, normalization, "
        "transactions, indexing and modern data systems. "
        "Gradual difficulty ramp from basics (1) to expert (9-10)."
    ),
    category="cs-core",
    order_index=2,
    is_active=True,
)


def shuffle_options(q: CurriculumQuestion) -> CurriculumQuestion:
    """Deterministically shuffle a question's options (seeded by question id).

    Keeps the correct answer correct while distributing answer positions
    uniformly. Stable across runs — same input always yields same output.
    """
    seed = int(hashlib.sha256(q.id.encode("utf-8")).hexdigest(), 16)
    rng = random.Random(seed)
    order = list(range(len(q.choices)))
    rng.shuffle(order)
    new_choices = tuple(q.choices[i] for i in order)
    new_answer = order.index(q.answer_index)
    validate_curriculum_question(q.qtype, q.prompt, q.difficulty, new_choices, new_answer)
    return CurriculumQuestion(
        id=q.id,
        domain_slug=q.domain_slug,
        module_slug=q.module_slug,
        lesson_id=q.lesson_id,
        difficulty=q.difficulty,
        qtype=q.qtype,
        prompt=q.prompt,
        choices=new_choices,
        answer_index=new_answer,
        explanation=q.explanation,
        company_tags=q.company_tags,
    )


DBMS_MODULES = sorted(
    list(_M1_MODS) + list(_M23_MODS) + list(_M456_MODS),
    key=lambda m: m.order_index,
)
DBMS_LESSONS = list(_M1_LESSONS) + list(_M23_LESSONS) + list(_M456_LESSONS)
DBMS_QUESTIONS = [shuffle_options(q) for q in list(_M1_QS) + list(_M23_QS) + list(_M456_QS)]


def _check_integrity() -> list[str]:
    """Return a list of integrity problems (empty = clean)."""
    problems: list[str] = []
    for name, items in (("modules", DBMS_MODULES), ("lessons", DBMS_LESSONS), ("questions", DBMS_QUESTIONS)):
        ids = [i.id for i in items]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            problems.append(f"duplicate {name} ids: {sorted(dupes)[:5]}")
    mod_ids = {m.id for m in DBMS_MODULES}
    mod_slugs = [m.slug for m in DBMS_MODULES]
    if len(set(mod_slugs)) != len(mod_slugs):
        problems.append("duplicate module slugs")
    les_ids = {lz.id for lz in DBMS_LESSONS}
    for lz in DBMS_LESSONS:
        if lz.module_id not in mod_ids:
            problems.append(f"lesson {lz.id} references unknown module {lz.module_id}")
    mod_slug_set = set(mod_slugs)
    for q in DBMS_QUESTIONS:
        if q.lesson_id not in les_ids:
            problems.append(f"question {q.id} references unknown lesson {q.lesson_id}")
        if q.module_slug not in mod_slug_set:
            problems.append(f"question {q.id} references unknown module slug {q.module_slug}")
        if q.domain_slug != DBMS_DOMAIN.slug:
            problems.append(f"question {q.id} has wrong domain_slug {q.domain_slug}")
        try:
            validate_difficulty(q.difficulty)
        except Exception as e:  # noqa: BLE001
            problems.append(f"question {q.id}: {e}")
    return problems


def summary() -> dict:
    """Per-module breakdown: lessons, questions, difficulty spread."""
    by_module: dict[str, dict] = {}
    les_by_mod: dict[str, list] = {}
    for lz in DBMS_LESSONS:
        les_by_mod.setdefault(lz.module_id, []).append(lz)
    q_by_les: dict[str, list] = {}
    for q in DBMS_QUESTIONS:
        q_by_les.setdefault(q.lesson_id or "", []).append(q)
    for m in DBMS_MODULES:
        lessons = les_by_mod.get(m.id, [])
        qs = [q for lz in lessons for q in q_by_les.get(lz.id, [])]
        by_module[m.id] = {
            "name": m.name,
            "lessons": len(lessons),
            "questions": len(qs),
            "difficulty": dict(sorted(Counter(q.difficulty for q in qs).items())),
            "estimated_days": m.estimated_days,
        }
    return {
        "domain": DBMS_DOMAIN.slug,
        "modules": len(DBMS_MODULES),
        "lessons": len(DBMS_LESSONS),
        "questions": len(DBMS_QUESTIONS),
        "answer_positions": dict(sorted(Counter(q.answer_index for q in DBMS_QUESTIONS).items())),
        "by_module": by_module,
        "integrity_problems": _check_integrity(),
    }


def seed_payload() -> dict:
    """JSON-serializable payload for the curriculum table loader.

    Returns plain dicts/lists only: {"domain": {...}, "modules": [...],
    "lessons": [...], "questions": [...]}.
    """
    def q_to_dict(q: CurriculumQuestion) -> dict:
        return {
            "id": q.id,
            "domain_slug": q.domain_slug,
            "module_slug": q.module_slug,
            "lesson_id": q.lesson_id,
            "difficulty": q.difficulty,
            "qtype": q.qtype,
            "prompt": q.prompt,
            "choices": list(q.choices),
            "answer_index": q.answer_index,
            "explanation": q.explanation,
            "company_tags": list(q.company_tags),
        }

    return {
        "domain": {
            "id": DBMS_DOMAIN.id,
            "slug": DBMS_DOMAIN.slug,
            "name": DBMS_DOMAIN.name,
            "icon": DBMS_DOMAIN.icon,
            "description": DBMS_DOMAIN.description,
            "category": DBMS_DOMAIN.category,
            "order_index": DBMS_DOMAIN.order_index,
            "is_active": DBMS_DOMAIN.is_active,
        },
        "modules": [
            {
                "id": m.id, "domain_slug": m.domain_slug, "slug": m.slug,
                "name": m.name, "description": m.description,
                "order_index": m.order_index, "estimated_days": m.estimated_days,
            }
            for m in DBMS_MODULES
        ],
        "lessons": [
            {
                "id": lz.id, "module_id": lz.module_id, "slug": lz.slug,
                "title": lz.title, "content": lz.content,
                "order_index": lz.order_index,
                "estimated_minutes": lz.estimated_minutes,
                "has_visual": lz.has_visual,
            }
            for lz in DBMS_LESSONS
        ],
        "questions": [q_to_dict(q) for q in DBMS_QUESTIONS],
    }


if __name__ == "__main__":
    import json

    s = summary()
    print(json.dumps(s, indent=2, ensure_ascii=False))
