"""Outbound adapter: Google OAuth 2.0.

Real implementation, but it only activates when the operator configures
GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / GOOGLE_REDIRECT_URI.
Otherwise every call raises DomainError('google oauth not configured').
"""
from __future__ import annotations

import secrets
from urllib.parse import urlencode

import httpx

from app.domain.user import DomainError

_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
_TOKEN_URL = "https://oauth2.googleapis.com/token"
_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


class GoogleOAuthProvider:
    def __init__(self, client_id: str = "", client_secret: str = "", redirect_uri: str = "") -> None:
        self._id = client_id
        self._secret = client_secret
        self._redirect = redirect_uri

    @property
    def configured(self) -> bool:
        return bool(self._id and self._secret and self._redirect)

    def _require_config(self) -> None:
        if not self.configured:
            raise DomainError(
                "google oauth not configured: set GOOGLE_CLIENT_ID, "
                "GOOGLE_CLIENT_SECRET and GOOGLE_REDIRECT_URI"
            )

    def auth_url(self, state: str = "") -> str:
        self._require_config()
        params = {
            "client_id": self._id,
            "redirect_uri": self._redirect,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state or secrets.token_urlsafe(16),
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{_AUTH_URL}?{urlencode(params)}"

    def exchange(self, code: str) -> str:
        """Exchange an authorization code for the user's verified email."""
        self._require_config()
        try:
            token_resp = httpx.post(
                _TOKEN_URL,
                data={"client_id": self._id, "client_secret": self._secret,
                      "redirect_uri": self._redirect, "grant_type": "authorization_code",
                      "code": code},
                timeout=15,
            )
            token_resp.raise_for_status()
            access = token_resp.json()["access_token"]
            user_resp = httpx.get(
                _USERINFO_URL,
                headers={"Authorization": f"Bearer {access}"},
                timeout=15,
            )
            user_resp.raise_for_status()
            info = user_resp.json()
            if not info.get("email_verified", True):
                raise DomainError("google email not verified")
            return info["email"]
        except DomainError:
            raise
        except Exception as exc:
            raise DomainError(f"google oauth exchange failed: {exc}") from exc
