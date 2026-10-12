"""Domain: learning roadmaps generated from skill gaps. PURE.

Rules (product guarantees):
- Roadmaps are generated deterministically from skill gaps (v1: templates).
- Regeneration creates a NEW version; completed tasks and their evidence
  are NEVER deleted — they are carried forward untouched.
- Task status flows forward: pending -> in_progress -> completed.
  completed is terminal (history cannot be rewritten).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.user import DomainError

TASK_STATUSES = ("pending", "in_progress", "completed")
PRIORITIES = ("high", "medium", "low")

_ALLOWED_TRANSITIONS = {
    "pending": ("in_progress",),
    "in_progress": ("pending", "completed"),
    "completed": (),
}


@dataclass(frozen=True)
class SkillGap:
    skill: str
    mastery_pct: float  # 0-100


@dataclass
class RoadmapTask:
    id: str
    title: str
    description: str
    why_it_matters: str
    target_skills: tuple[str, ...]
    prerequisites: tuple[str, ...]
    effort_minutes: int
    priority: str  # high | medium | low
    expected_evidence: str
    acceptance_criteria: str
    status: str = "pending"

    def transition(self, new_status: str) -> None:
        if new_status not in TASK_STATUSES:
            raise DomainError(f"unknown status: {new_status}")
        if new_status not in _ALLOWED_TRANSITIONS[self.status]:
            raise DomainError(
                f"cannot move task from {self.status} to {new_status}"
            )
        self.status = new_status


@dataclass
class Roadmap:
    id: str
    user_id: str
    version: int
    title: str
    source: str  # "manual" | "assessment:<id>"
    tasks: list[RoadmapTask] = field(default_factory=list)

    def completed_tasks(self) -> list[RoadmapTask]:
        return [t for t in self.tasks if t.status == "completed"]


# --- deterministic v1 task templates ---------------------------------------
# Each gap skill expands into Learn -> Practice -> Build. Per-skill overrides
# below; everything else falls back to the generic template.

_SKILL_OVERRIDES: dict[str, dict[str, str]] = {
    "python-basics": {
        "learn": "Functions, scopes and decorators",
        "practice": "15 function/decorator drills",
        "build": "CLI utility using decorators",
    },
    "data-structures": {
        "learn": "Lists vs tuples vs sets vs dicts",
        "practice": "20 DS drills (GFG-style)",
        "build": "LRU cache from scratch",
    },
    "oops": {
        "learn": "Classes, inheritance, dunder methods",
        "practice": "12 OOP design drills",
        "build": "Mini banking system with tests",
    },
    "ml-basics": {
        "learn": "Train/test split, overfitting, metrics",
        "practice": "Confusion-matrix + metric quizzes",
        "build": "End-to-end classifier on a real dataset",
    },
    "sql": {
        "learn": "JOINs, GROUP BY, subqueries",
        "practice": "25 SQL query drills",
        "build": "Analytics queries on a sample DB",
    },
}


def _priority_for(mastery_pct: float) -> str:
    if mastery_pct < 40:
        return "high"
    if mastery_pct < 70:
        return "medium"
    return "low"


def _tasks_for_gap(gap: SkillGap, seq_start: int) -> list[RoadmapTask]:
    skill = gap.skill.strip()
    if not skill:
        raise DomainError("gap skill must not be empty")
    if not 0 <= gap.mastery_pct <= 100:
        raise DomainError("mastery_pct must be 0-100")
    ov = _SKILL_OVERRIDES.get(skill, {})
    priority = _priority_for(gap.mastery_pct)
    seq = seq_start
    def _mk(kind: str, title: str, desc: str, minutes: int, evidence: str, criteria: str) -> RoadmapTask:
        nonlocal seq
        seq += 1
        return RoadmapTask(
            id=f"t{seq:04d}",
            title=title,
            description=desc,
            why_it_matters=(
                f"Your verified mastery in {skill} is {gap.mastery_pct:.0f}% — "
                f"below the 70% bar. This task closes that gap directly."
            ),
            target_skills=(skill,),
            prerequisites=(),
            effort_minutes=minutes,
            priority=priority,
            expected_evidence=evidence,
            acceptance_criteria=criteria,
            status="pending",
        )
    return [
        _mk("learn",
            f"Learn: {ov.get('learn', skill + ' fundamentals')}",
            f"Core concepts of {skill}, with notes in your own words.",
            45, "concept notes",
            "Can explain the concept without looking at notes."),
        _mk("practice",
            f"Practice: {ov.get('practice', '10 ' + skill + ' drills')}",
            f"Timed drills on {skill}; every answer checked.",
            60, "drill results",
            "At least 8/10 drills correct."),
        _mk("build",
            f"Build: {ov.get('build', skill + ' mini-project')}",
            f"Small project proving {skill} in a realistic setting.",
            120, "code submission",
            "Project runs and meets the stated requirements."),
    ]


def generate_tasks(gaps: list[SkillGap]) -> list[RoadmapTask]:
    """Deterministic v1 generator: worst gaps first."""
    if not gaps:
        raise DomainError("at least one skill gap is required")
    ordered = sorted(gaps, key=lambda g: g.mastery_pct)
    tasks: list[RoadmapTask] = []
    seq = 0
    for gap in ordered:
        new_tasks = _tasks_for_gap(gap, seq)
        seq += len(new_tasks)
        tasks.extend(new_tasks)
    # prerequisites: practice needs learn, build needs practice (per skill)
    by_skill: dict[str, list[RoadmapTask]] = {}
    for t in tasks:
        by_skill.setdefault(t.target_skills[0], []).append(t)
    for skill_tasks in by_skill.values():
        for prev, cur in zip(skill_tasks, skill_tasks[1:]):
            cur.prerequisites = (prev.id,)
    return tasks


def regenerate_tasks(old: Roadmap, gaps: list[SkillGap]) -> list[RoadmapTask]:
    """Build the next version's task list.

    Completed tasks are carried forward UNTOUCHED (same id, same status).
    Everything else is regenerated fresh from the current gaps.
    Nothing is ever deleted: completed work survives regeneration.
    """
    carried = [t for t in old.completed_tasks()]
    carried_ids = {t.id for t in carried}
    fresh = [t for t in generate_tasks(gaps) if t.id not in carried_ids]
    # re-sequence fresh ids so they don't collide with carried ones
    max_n = 0
    for t in carried:
        try:
            max_n = max(max_n, int(t.id[1:]))
        except ValueError:
            pass
    renumbered: list[RoadmapTask] = []
    for i, t in enumerate(fresh, start=max_n + 1):
        t.id = f"t{i:04d}"
        renumbered.append(t)
    return carried + renumbered
