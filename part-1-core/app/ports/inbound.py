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
