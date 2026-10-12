"""Domain: certificates. PURE.

Certificates are EARNED, never self-issued: the service checks eligibility
server-side (e.g. every task of the roadmap is completed) before issuing.
A verification code (SF-XXXXXXXX) lets employers check authenticity via a
public endpoint — no account needed.
"""
from __future__ import annotations

import secrets
import string
from dataclasses import dataclass

from app.domain.user import DomainError

CODE_ALPHABET = string.ascii_uppercase + string.digits
CODE_PREFIX = "SF-"

# kind -> (title template, eligibility description)
KINDS = {
    "roadmap": ("Roadmap Completion — {ref_title}",
                "all tasks of the roadmap completed"),
}


def new_verification_code() -> str:
    return CODE_PREFIX + "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))


@dataclass(frozen=True)
class Certificate:
    id: str
    user_id: str
    kind: str
    title: str
    ref_id: str
    verification_code: str
    issued_at: str
    detail: str = ""

    def validate(self) -> None:
        if self.kind not in KINDS:
            raise DomainError(f"unknown certificate kind: {self.kind}")
        if not self.ref_id.strip():
            raise DomainError("ref_id required")


def check_roadmap_eligible(roadmap) -> tuple[bool, str]:
    """True when every task of the roadmap is completed."""
    if roadmap is None:
        return False, "roadmap not found"
    tasks = list(roadmap.tasks)
    if not tasks:
        return False, "roadmap has no tasks"
    done = [t for t in tasks if t.status == "completed"]
    if len(done) < len(tasks):
        return False, f"{len(done)}/{len(tasks)} tasks completed"
    return True, ""
