"""Inbound adapter: implements the RoadmapService port."""
from __future__ import annotations

import uuid

from app.domain.roadmap import (
    Roadmap,
    SkillGap,
    generate_tasks,
    regenerate_tasks,
)
from app.domain.user import DomainError


def _to_gaps(gaps: list[dict]) -> list[SkillGap]:
    if not isinstance(gaps, list) or not gaps:
        raise DomainError("at least one skill gap is required")
    out: list[SkillGap] = []
    for g in gaps:
        if not isinstance(g, dict) or "skill" not in g or "mastery_pct" not in g:
            raise DomainError("each gap needs skill and mastery_pct")
        try:
            pct = float(g["mastery_pct"])
        except (TypeError, ValueError):
            raise DomainError("mastery_pct must be a number")
        out.append(SkillGap(skill=str(g["skill"]), mastery_pct=pct))
    return out


class RoadmapServiceImpl:
    def __init__(self, roadmaps) -> None:
        self._roadmaps = roadmaps

    def generate(self, user_id: str, gaps: list[dict], title: str = "", source: str = "manual") -> Roadmap:
        gap_objs = _to_gaps(gaps)
        roadmap = Roadmap(
            id=uuid.uuid4().hex,
            user_id=user_id,
            version=self._roadmaps.max_version(user_id) + 1,
            title=title.strip() or f"Roadmap v{self._roadmaps.max_version(user_id) + 1}",
            source=source,
            tasks=generate_tasks(gap_objs),
        )
        self._roadmaps.save(roadmap)
        return roadmap

    def get_current(self, user_id: str) -> Roadmap:
        roadmap = self._roadmaps.get_current(user_id)
        if not roadmap:
            raise DomainError("no roadmap yet — generate one first")
        return roadmap

    def list_versions(self, user_id: str) -> list[Roadmap]:
        return self._roadmaps.list_versions(user_id)

    def update_task(self, user_id: str, task_id: str, status: str) -> object:
        roadmap = self.get_current(user_id)
        task = next((t for t in roadmap.tasks if t.id == task_id), None)
        if not task:
            raise DomainError("task not found in current roadmap")
        task.transition(status)
        self._roadmaps.save(roadmap)
        return task

    def regenerate(self, user_id: str, gaps: list[dict]) -> Roadmap:
        current = self.get_current(user_id)
        gap_objs = _to_gaps(gaps)
        roadmap = Roadmap(
            id=uuid.uuid4().hex,
            user_id=user_id,
            version=current.version + 1,
            title=f"Roadmap v{current.version + 1}",
            source="regenerated",
            tasks=regenerate_tasks(current, gap_objs),
        )
        self._roadmaps.save(roadmap)
        return roadmap
