"""Inbound adapter: implements the AuthService port.

Orchestrates domain rules + outbound ports. Contains no SQL, no JWT details,
no HTTP — those live in the adapters it calls.
"""
from __future__ import annotations

import uuid

from app.domain.user import (
    AuthResult,
    DomainError,
    User,
    new_user,
    validate_email,
    validate_password,
    validate_role,
)
from app.ports.outbound import PasswordHasher, TokenIssuer, TokenStore, UserRepository


class JwtAuthService:
    def __init__(
        self,
        users: UserRepository,
        hasher: PasswordHasher,
        issuer: TokenIssuer,
        tokens: TokenStore,
    ) -> None:
        self._users = users
        self._hasher = hasher
        self._issuer = issuer
        self._tokens = tokens

    def _issue_pair(self, user: User) -> AuthResult:
        access = self._issuer.issue_access(user)
        refresh = self._issuer.issue_refresh(user)
        self._tokens.store(refresh, user.id)
        return AuthResult(user=user, access_token=access, refresh_token=refresh)

    def register(self, email: str, password: str) -> AuthResult:
        email = validate_email(email)
        validate_password(password)
        if self._users.find_by_email(email):
            raise DomainError("email already registered")
        user = new_user(uuid.uuid4().hex, email, self._hasher.hash(password))
        self._users.save(user)
        return self._issue_pair(user)

    def register_oauth(self, email: str) -> AuthResult:
        """OAuth users have no password; password login will never verify."""
        email = validate_email(email)
        user = self._users.find_by_email(email)
        if not user:
            user = new_user(uuid.uuid4().hex, email, "")
            self._users.save(user)
        return self._issue_pair(user)

    def login(self, email: str, password: str) -> AuthResult:
        email = validate_email(email)
        user = self._users.find_by_email(email)
        if not user or not self._hasher.verify(password, user.password_hash):
            raise DomainError("invalid credentials")
        return self._issue_pair(user)

    def refresh(self, refresh_token: str) -> AuthResult:
        claims = self._issuer.decode(refresh_token)
        if claims.get("type") != "refresh":
            raise DomainError("not a refresh token")
        if self._tokens.is_revoked(refresh_token):
            raise DomainError("refresh token revoked")
        user_id = claims["sub"]
        user = self._users.get(user_id)
        if not user:
            raise DomainError("user not found")
        self._tokens.revoke(refresh_token)  # rotation: old dies here
        return self._issue_pair(user)

    def logout(self, refresh_token: str) -> None:
        self._tokens.revoke(refresh_token)  # idempotent by design

    def get_user(self, user_id: str) -> User:
        user = self._users.get(user_id)
        if not user:
            raise DomainError("user not found")
        return user

    def set_role(self, target_user_id: str, role: str) -> User:
        role = validate_role(role)
        user = self._users.update_role(target_user_id, role)
        if not user:
            raise DomainError("user not found")
        return user

    def export_data(self, user_id: str) -> dict:
        user = self.get_user(user_id)
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
            # password hashes never leave the core
        }

    def delete_account(self, user_id: str) -> None:
        self.get_user(user_id)  # raises if missing
        self._tokens.revoke_all_for_user(user_id)
        self._users.delete(user_id)
