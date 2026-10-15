"""Domain: password reset — pure functions, no I/O.

Token lifecycle:
  1. generate_token() -> opaque token (sent to user via email link)
  2. hash_token(token) -> sha256 hex (the ONLY thing stored in the DB)
  3. On reset: hash the presented token, look up the hash, check
     expiry + single-use, then rotate the password.
"""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timezone

TOKEN_TTL_HOURS = 1
# Max forgot-password requests per email per rolling hour (abuse control).
FORGOT_RATE_LIMIT = 3


def generate_token() -> str:
    """Opaque, URL-safe reset token (~43 chars, 256 bits of entropy)."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """SHA-256 hex digest. The raw token is NEVER persisted."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def is_expired(expires_at: datetime, now: datetime | None = None) -> bool:
    """True when the token is past its expiry. Naive datetimes are
    assumed UTC (SQLite stores naive datetimes)."""
    now = now or datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return now >= expires_at
