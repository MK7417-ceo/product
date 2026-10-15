"""Outbound adapter: transactional email via the Resend HTTP API.

CRITICAL: all mail is sent from the PROJECT's address (FROM_EMAIL env,
default noreply@skillforge.app) — never from anyone's personal email.

If RESEND_API_KEY is unset the service runs in dev mode: it logs and
returns False instead of raising, so the app never crashes on email.
"""
from __future__ import annotations

import logging
import os

import httpx

log = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"
DEFAULT_FROM = "noreply@skillforge.app"


def _from_email() -> str:
    return os.environ.get("FROM_EMAIL", DEFAULT_FROM)


def _api_key() -> str:
    return os.environ.get("RESEND_API_KEY", "")


def _reset_html(reset_link: str) -> str:
    return f"""<!doctype html>
<html><body style="font-family:Arial,sans-serif;background:#0b0f1a;color:#e8ecf4;margin:0;padding:32px">
<div style="max-width:560px;margin:0 auto;background:#121826;border-radius:12px;padding:32px">
<h2 style="color:#7c6cff;margin-top:0">SkillForge</h2>
<p>You asked to reset your password. Click the button below — the link
expires in <b>1 hour</b>.</p>
<p style="text-align:center;margin:28px 0">
<a href="{reset_link}" style="background:#7c6cff;color:#fff;text-decoration:none;
padding:12px 28px;border-radius:8px;font-weight:bold">Reset my password</a>
</p>
<p style="font-size:13px;color:#9aa3b2">Or paste this link into your browser:<br>
<span style="word-break:break-all">{reset_link}</span></p>
<p style="font-size:13px;color:#9aa3b2">If you didn't request this, just ignore
this email — your password stays the same.</p>
<hr style="border:none;border-top:1px solid:#232b3d;margin-top:24px">
<p style="font-size:12px;color:#6b7280">Sent by SkillForge · please don't reply
to this message.</p>
</div></body></html>"""


def send_password_reset_email(to_email: str, reset_link: str) -> bool:
    """Send the reset email via Resend. Returns True on success.

    Never raises: failures are logged and reported as False.
    """
    api_key = _api_key()
    if not api_key:
        log.warning("RESEND_API_KEY not set — skipping password reset email to %s", to_email)
        return False
    payload = {
        "from": f"SkillForge <{_from_email()}>",
        "to": [to_email],
        "subject": "Reset your SkillForge password",
        "html": _reset_html(reset_link),
    }
    try:
        resp = httpx.post(
            RESEND_API_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json=payload,
            timeout=15,
        )
        if resp.status_code >= 400:
            log.error("Resend API error %s: %s", resp.status_code, resp.text[:200])
            return False
        return True
    except Exception as exc:  # network, timeout, DNS — never crash the request
        log.error("Failed to send reset email via Resend: %s", exc)
        return False
