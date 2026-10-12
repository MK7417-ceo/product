"""Inbound adapter: implements the EvidenceService port."""
from __future__ import annotations

import uuid

from app.domain.evidence import Evidence, validate_evidence
from app.domain.user import DomainError


class EvidenceServiceImpl:
    def __init__(self, evidence, roadmaps) -> None:
        self._evidence = evidence
        self._roadmaps = roadmaps

    def _current_task(self, user_id: str, task_id: str):
        roadmap = self._roadmaps.get_current(user_id)
        if not roadmap:
            raise DomainError("no roadmap yet — generate one first")
        task = next((t for t in roadmap.tasks if t.id == task_id), None)
        if not task:
            raise DomainError("task not found in current roadmap")
        return roadmap, task

    def submit(self, user_id: str, task_id: str, kind: str, content: str) -> Evidence:
        roadmap, task = self._current_task(user_id, task_id)
        if task.status != "in_progress":
            raise DomainError(
                f"evidence needs an in-progress task (current: {task.status})"
            )
        feedback = validate_evidence(kind, content)
        evidence = Evidence(
            id=uuid.uuid4().hex,
            user_id=user_id,
            roadmap_id=roadmap.id,
            task_key=task.id,
            kind=kind,
            content=content.strip(),
            feedback=feedback,
        )
        self._evidence.save(evidence)
        # proof submitted -> the loop closes, task is complete
        task.transition("completed")
        self._roadmaps.save(roadmap)
        return evidence

    def list_for_task(self, user_id: str, task_id: str) -> list[Evidence]:
        self._current_task(user_id, task_id)  # ownership check
        return self._evidence.list_for_task(user_id, task_id)
