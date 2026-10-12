"""Inbound ports — what the outside world may ask the domain core to do.

API routers depend on these protocols, never on concrete services.
"""
from __future__ import annotations

from typing import Protocol

from app.domain.health import SystemStatus
from app.domain.user import AuthResult, User


class HealthService(Protocol):
    def get_status(self) -> SystemStatus:
        """Return the current system status."""
        ...


class AuthService(Protocol):
    def register(self, email: str, password: str) -> AuthResult:
        """Create a user and issue tokens. Raises DomainError on bad input/dupe."""
        ...

    def login(self, email: str, password: str) -> AuthResult:
        """Verify credentials and issue tokens. Raises DomainError on failure."""
        ...

    def refresh(self, refresh_token: str) -> AuthResult:
        """Rotate a refresh token: new pair issued, old one revoked."""
        ...

    def logout(self, refresh_token: str) -> None:
        """Revoke a refresh token. Idempotent."""
        ...

    def get_user(self, user_id: str) -> User:
        """Fetch a user by id. Raises DomainError if missing."""
        ...

    def set_role(self, target_user_id: str, role: str) -> User:
        """Change a user's role. Caller must have checked admin rights."""
        ...

    def export_data(self, user_id: str) -> dict:
        """Export a user's data. Never includes password hashes."""
        ...

    def delete_account(self, user_id: str) -> None:
        """Delete a user and their tokens."""
        ...

    def register_oauth(self, email: str) -> AuthResult:
        """Find-or-create a user from an OAuth identity. No password set."""
        ...


class OnboardingService(Protocol):
    def save_profile(self, user_id: str, **fields) -> object:
        """Create or replace the user's resume-style profile."""
        ...

    def get_profile(self, user_id: str) -> object:
        """Raises DomainError if the user has no profile yet."""
        ...

    def start_placement(self, user_id: str, topic: str, claimed_level: str) -> tuple[object, list[dict]]:
        """Open a placement session; returns (session, public questions)."""
        ...

    def submit_placement(self, user_id: str, placement_id: str, answers: dict[str, int]) -> object:
        """Score answers and stamp the verified level. Session closes."""
        ...


class AssessmentService(Protocol):
    def start_assessment(self, user_id: str, topic: str, level: str, count: int = 6) -> tuple[object, list[dict]]:
        """Open an assessment session; returns (session, public questions)."""
        ...

    def submit_assessment(self, user_id: str, assessment_id: str, answers: dict[str, int]) -> object:
        """Score answers server-side and return the result with gap report."""
        ...

    def get_assessment(self, user_id: str, assessment_id: str) -> object:
        """Raises DomainError if missing or owned by someone else."""
class RoadmapService(Protocol):
    def generate(self, user_id: str, gaps: list[dict], title: str = "", source: str = "manual") -> object:
        """Build roadmap v1 from skill gaps. Raises DomainError on bad input."""
        ...

    def get_current(self, user_id: str) -> object:
        """Latest roadmap version. Raises DomainError if none exists."""
        ...

    def list_versions(self, user_id: str) -> list[object]:
        """All roadmap versions, newest first."""
        ...

    def update_task(self, user_id: str, task_id: str, status: str) -> object:
        """Move a task of the current roadmap to a new status."""
        ...

    def regenerate(self, user_id: str, gaps: list[dict]) -> object:
        """New version from fresh gaps; completed tasks are preserved."""
        ...


class EvidenceService(Protocol):
    def submit(self, user_id: str, task_id: str, kind: str, content: str) -> object:
        """Submit proof of work for an in-progress task; completes the task."""
        ...

    def list_for_task(self, user_id: str, task_id: str) -> list[object]:
        """All evidence ever submitted for a task. Never deleted."""
        ...
