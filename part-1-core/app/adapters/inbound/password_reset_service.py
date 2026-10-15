"""Inbound adapter: forgot/reset password orchestration.

Flow:
  forgot_password(email):
    - validate email format (invalid -> DomainError, surfaced as 400)
    - look up user; ALWAYS behave the same whether the user exists or not
      (never reveal account existence) — the API returns 200 either way
    - rate limit: max FORGOT_RATE_LIMIT requests per user per rolling hour
    - create hashed token row (1h TTL), email the raw token link via Resend
  reset_password(token, new_password):
    - hash presented token, find row; reject unknown/expired/used tokens
    - validate + hash the new password, update user, mark token used
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from app.domain import password_reset as pr
from app.domain.user import DomainError, validate_email, validate_password


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _frontend_url() -> str:
    return os.environ.get("FRONTEND_URL", "http://localhost:5173").rstrip("/")


class PasswordResetServiceImpl:
    def __init__(self, users, reset_repo, hasher, email_sender=None) -> None:
        self._users = users
        self._resets = reset_repo
        self._hasher = hasher
        # email_sender(to_email, reset_link) -> bool; injectable for tests
        self._email_sender = email_sender

    # ---- forgot ----

    def forgot_password(self, email: str) -> dict:
        """Always returns the same shape — never reveals account existence."""
        try:
            email = validate_email(email)
        except DomainError as exc:
            raise exc
        user = self._users.find_by_email(email)
        if not user:
            # No account — behave identically, send nothing.
            return {"ok": True, "email_sent": False}

        # Rate limit: max N tokens per rolling hour.
        since = _utcnow() - timedelta(hours=1)
        if self._resets.count_recent_for_email(user.id, since) >= pr.FORGOT_RATE_LIMIT:
            raise DomainError("too many reset requests — try again later")

        token = pr.generate_token()
        expires_at = _utcnow() + timedelta(hours=pr.TOKEN_TTL_HOURS)
        self._resets.create(user_id=user.id, token_hash=pr.hash_token(token),
                            expires_at=expires_at)
        reset_link = f"{_frontend_url()}/reset-password?token={token}"
        sender = self._email_sender
        email_sent = bool(sender(to_email=email, reset_link=reset_link)) if sender else False
        return {"ok": True, "email_sent": email_sent}

    # ---- reset ----

    def reset_password(self, token: str, new_password: str) -> dict:
        validate_password(new_password)
        if not token:
            raise DomainError("invalid or expired reset token")
        row = self._resets.find_valid(pr.hash_token(token))
        if not row:
            raise DomainError("invalid or expired reset token")
        if row["used_at"] is not None:
            raise DomainError("reset link already used")
        if pr.is_expired(row["expires_at"]):
            raise DomainError("reset link expired")
        if not self._users.set_password_hash(row["user_id"],
                                             self._hasher.hash(new_password)):
            raise DomainError("account not found")
        self._resets.mark_used(row["id"])
        return {"ok": True}
