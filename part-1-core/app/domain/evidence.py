"""Domain: append-only proof of work with an explicit review lifecycle."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.user import DomainError

EVIDENCE_KINDS = ("code", "text", "url")
EVIDENCE_STATUSES = ("legacy_unverified", "pending_review", "verified", "rejected", "needs_changes")
REVIEW_DECISIONS = ("verified", "rejected", "needs_changes")
MAX_CONTENT_CHARS = 20000
MAX_REVIEW_NOTE_CHARS = 2000


@dataclass
class Evidence:
    id: str
    user_id: str
    roadmap_id: str
    task_key: str
    kind: str
    content: str
    feedback: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "pending_review"
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    review_note: str = ""


def validate_evidence(kind: str, content: str) -> str:
    """Validate proof submission and return honest receipt feedback."""
    if kind not in EVIDENCE_KINDS:
        raise DomainError(f"unknown evidence kind: {kind}")
    text = (content or "").strip()
    if not text:
        raise DomainError("evidence content must not be empty")
    if len(text) > MAX_CONTENT_CHARS:
        raise DomainError("evidence content too long")
    if kind == "url" and not (
        text.startswith("http://") or text.startswith("https://")
    ):
        raise DomainError("url evidence must start with http:// or https://")
    if kind == "code" and len(text) < 10:
        raise DomainError("code evidence looks too short to be real")
    return _feedback_for(kind, text)


def validate_review(decision: str, note: str) -> str:
    if decision not in REVIEW_DECISIONS:
        raise DomainError(f"unknown evidence review decision: {decision}")
    cleaned = (note or "").strip()
    if len(cleaned) > MAX_REVIEW_NOTE_CHARS:
        raise DomainError("review note too long")
    if decision in ("rejected", "needs_changes") and not cleaned:
        raise DomainError("a review note is required for rejected or needs_changes evidence")
    return cleaned


def _feedback_for(kind: str, text: str) -> str:
    if kind == "code":
        return f"Received {len(text.splitlines())} lines of code. Your submission is pending review; it is not verified yet."
    if kind == "url":
        return "Link received. It is pending review; keep it accessible until the review is complete."
    return f"Received {len(text.split())} words of notes. Your submission is pending review; it is not verified yet."
