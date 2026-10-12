"""Domain: evidence of completed roadmap tasks. PURE.

The loop closes here: a task is complete only when evidence is submitted.
Evidence is never deleted — it is the permanent proof of work behind the
user's verified skills. v1 feedback is deterministic (checklist-based);
AI/human review arrives in a later slice.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.user import DomainError

EVIDENCE_KINDS = ("code", "text", "url")
MAX_CONTENT_CHARS = 20000


@dataclass
class Evidence:
    id: str
    user_id: str
    roadmap_id: str
    task_key: str  # logical task id (t0001…), stable across versions
    kind: str  # code | text | url
    content: str
    feedback: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def validate_evidence(kind: str, content: str) -> str:
    """Returns deterministic v1 feedback. Raises DomainError on bad input."""
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


def _feedback_for(kind: str, text: str) -> str:
    if kind == "code":
        lines = len(text.splitlines())
        return (
            f"Received {lines} lines of code. It will be checked by the code "
            f"runner and similarity analysis when those land; for now it is "
            f"stored as your proof of work."
        )
    if kind == "url":
        return (
            "Link received and stored as your proof of work. "
            "Make sure it stays accessible — it backs your verified skills."
        )
    words = len(text.split())
    return (
        f"Received {words} words of notes. Writing it in your own words is "
        f"exactly how concepts stick — stored as your proof of work."
    )
