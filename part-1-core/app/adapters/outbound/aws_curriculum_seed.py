"""Seed script: AWS Cloud curriculum (tech domain, expert level).

Assembles the part-files (aws_part_m1 / aws_part_m2m3 / aws_part_m4m5) into
validated domain objects from app.domain.curriculum, ready for the curriculum
table loader (sibling workstream).

What this script guarantees on top of the raw parts:
- deterministic option shuffle per question (seeded by question id), so the
  correct answer is uniformly distributed across positions instead of
  clustering at index 0;
- cross-part integrity checks (unique ids, valid lesson/module references,
  difficulty 1-10, module slugs unique).

Content: 5 modules, 35 lessons, 210 MCQs, difficulty ramp 1-9.
Covers interview questions + AWS Solutions Architect Associate topics.
All theory and explanations are written originally for SkillForge.

Usage:
    from app.adapters.outbound.aws_curriculum_seed import (
        AWS_DOMAIN, AWS_MODULES, AWS_LESSONS, AWS_QUESTIONS, seed_payload, summary,
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
    from .aws_part_m1 import MODULES as _M1_MODS, LESSONS as _M1_LESSONS, QUESTIONS as _M1_QS
    from .aws_part_m2m3 import MODULES as _M23_MODS, LESSONS as _M23_LESSONS, QUESTIONS as _M23_QS
    from .aws_part_m4m5 import MODULES as _M45_MODS, LESSONS as _M45_LESSONS, QUESTIONS as _M45_QS
except ImportError:  # direct script execution
    from aws_part_m1 import MODULES as _M1_MODS, LESSONS as _M1_LESSONS, QUESTIONS as _M1_QS
    from aws_part_m2m3 import MODULES as _M23_MODS, LESSONS as _M23_LESSONS, QUESTIONS as _M23_QS
    from aws_part_m4m5 import MODULES as _M45_MODS, LESSONS as _M45_LESSONS, QUESTIONS as _M45_QS


AWS_DOMAIN = CurriculumDomain(
    id="aws",
    slug="aws",
    name="AWS Cloud",
    icon="☁️",
    description=(
        "Amazon Web Services, expert level: EC2 & compute, S3 storage, Lambda "
        "serverless, IAM & VPC security, RDS & monitoring. 35 lessons, 210 "
        "questions — interview prep + Solutions Architect Associate topics, "
        "difficulty ramping 1 to 9."
    ),
    category="tech-domain",
    order_index=30,
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


AWS_MODULES = sorted(
    list(_M1_MODS) + list(_M23_MODS) + list(_M45_MODS),
    key=lambda m: m.order_index,
)
AWS_LESSONS = list(_M1_LESSONS) + list(_M23_LESSONS) + list(_M45_LESSONS)
AWS_QUESTIONS = [shuffle_options(q) for q in list(_M1_QS) + list(_M23_QS) + list(_M45_QS)]


def _check_integrity() -> list[str]:
    """Return a list of integrity problems (empty = clean)."""
    problems: list[str] = []
    for name, items in (("modules", AWS_MODULES), ("lessons", AWS_LESSONS), ("questions", AWS_QUESTIONS)):
        ids = [i.id for i in items]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            problems.append(f"duplicate {name} ids: {sorted(dupes)[:5]}")
    mod_ids = {m.id for m in AWS_MODULES}
    mod_slugs = [m.slug for m in AWS_MODULES]
    if len(set(mod_slugs)) != len(mod_slugs):
        problems.append("duplicate module slugs")
    les_ids = {lz.id for lz in AWS_LESSONS}
    for lz in AWS_LESSONS:
        if lz.module_id not in mod_ids:
            problems.append(f"lesson {lz.id} references unknown module {lz.module_id}")
    mod_slug_set = set(mod_slugs)
    for q in AWS_QUESTIONS:
        if q.lesson_id not in les_ids:
            problems.append(f"question {q.id} references unknown lesson {q.lesson_id}")
        if q.module_slug not in mod_slug_set:
            problems.append(f"question {q.id} references unknown module slug {q.module_slug}")
        if q.domain_slug != AWS_DOMAIN.slug:
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
    for lz in AWS_LESSONS:
        les_by_mod.setdefault(lz.module_id, []).append(lz)
    q_by_les: dict[str, list] = {}
    for q in AWS_QUESTIONS:
        q_by_les.setdefault(q.lesson_id or "", []).append(q)
    for m in AWS_MODULES:
        lessons = les_by_mod.get(m.id, [])
        qs = [q for lz in lessons for q in q_by_les.get(lz.id, [])]
        diffs = sorted(set(q.difficulty for q in qs))
        by_module[m.id] = {
            "name": m.name,
            "lessons": len(lessons),
            "questions": len(qs),
            "difficulty": dict(sorted(Counter(q.difficulty for q in qs).items())),
            "difficulty_span": f"{min(diffs)}-{max(diffs)}" if diffs else "none",
            "estimated_days": m.estimated_days,
        }
    return {
        "domain": AWS_DOMAIN.slug,
        "modules": len(AWS_MODULES),
        "lessons": len(AWS_LESSONS),
        "questions": len(AWS_QUESTIONS),
        "answer_positions": dict(sorted(Counter(q.answer_index for q in AWS_QUESTIONS).items())),
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
            "id": AWS_DOMAIN.id,
            "slug": AWS_DOMAIN.slug,
            "name": AWS_DOMAIN.name,
            "icon": AWS_DOMAIN.icon,
            "description": AWS_DOMAIN.description,
            "category": AWS_DOMAIN.category,
            "order_index": AWS_DOMAIN.order_index,
            "is_active": AWS_DOMAIN.is_active,
        },
        "modules": [
            {
                "id": m.id, "domain_slug": m.domain_slug, "slug": m.slug,
                "name": m.name, "description": m.description,
                "order_index": m.order_index, "estimated_days": m.estimated_days,
            }
            for m in AWS_MODULES
        ],
        "lessons": [
            {
                "id": lz.id, "module_id": lz.module_id, "slug": lz.slug,
                "title": lz.title, "content": lz.content,
                "order_index": lz.order_index,
                "estimated_minutes": lz.estimated_minutes,
                "has_visual": lz.has_visual,
            }
            for lz in AWS_LESSONS
        ],
        "questions": [q_to_dict(q) for q in AWS_QUESTIONS],
    }


if __name__ == "__main__":
    import json

    s = summary()
    print(json.dumps(s, indent=2, ensure_ascii=False))
