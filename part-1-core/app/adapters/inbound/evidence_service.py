"""Inbound adapter: evidence submission and reviewer workflow."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.domain.evidence import Evidence, validate_evidence, validate_review
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
        # Submission is not proof of quality. Task remains in progress until
        # an authorized reviewer verifies the submitted evidence.
        return evidence

    def list_for_task(self, user_id: str, task_id: str) -> list[Evidence]:
        self._current_task(user_id, task_id)
        return self._evidence.list_for_task(user_id, task_id)

    def list_pending(self) -> list[Evidence]:
        return self._evidence.list_pending()

    def review(self, reviewer_id: str, evidence_id: str,
               decision: str, note: str = "") -> Evidence:
        evidence = self._evidence.get_by_id(evidence_id)
        if not evidence:
            raise DomainError("evidence not found")
        if evidence.status != "pending_review":
            raise DomainError("only pending evidence can be reviewed")
        if evidence.user_id == reviewer_id:
            raise DomainError("reviewers cannot review their own evidence")
        cleaned_note = validate_review(decision, note)

        if decision == "verified":
            # Validate against the learner's current roadmap. The repository
            # then commits the review and task completion in one transaction.
            roadmap, task = self._current_task(evidence.user_id, evidence.task_key)
            if roadmap.id != evidence.roadmap_id:
                raise DomainError(
                    "evidence belongs to an older roadmap; resubmit against the current roadmap"
                )
            if task.status not in ("in_progress", "completed"):
                raise DomainError("task must be in progress before evidence can be verified")

        evidence.status = decision
        evidence.reviewed_by = reviewer_id
        evidence.reviewed_at = datetime.now(timezone.utc)
        evidence.review_note = cleaned_note
        saved = self._evidence.update_review(
            evidence, complete_task=(decision == "verified"))
        if not saved:
            raise DomainError("evidence or task changed during review; refresh and retry")
        return evidence
