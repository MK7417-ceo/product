"""Inbound adapter: Daily-DSA orchestration (implements the DailyDSAProvider port)."""
from __future__ import annotations

import uuid

from app.adapters.outbound.dsa_bank import BANK
from app.domain.dsa import grade_dsa, parse_day, pick_for_date, public_dsa
from app.domain.user import DomainError
from app.ports.outbound import CodeEngineError

SUPPORTED_LANGUAGES = ("python", "c", "cpp", "java")


class DSAServiceImpl:
    """Curated-bank implementation of the DailyDSAProvider port.

    When the user's own AI question generator is ready, it replaces this
    class behind the same port — no API or frontend change needed.
    """

    def __init__(self, bank=None, code_runner=None) -> None:
        self._bank = bank if bank is not None else BANK
        self._runner = code_runner

    def daily(self, raw_date: str = "") -> dict:
        day = parse_day(raw_date)
        q = pick_for_date(self._bank, day)
        out = public_dsa(q)
        out["date"] = day.isoformat()
        return out

    def submit(self, raw_date: str, language: str, code: str) -> dict:
        if language not in SUPPORTED_LANGUAGES:
            raise DomainError(f"unsupported language: {language}")
        if not code or not code.strip():
            raise DomainError("code must not be empty")
        if self._runner is None:
            raise DomainError("code engine not configured")
        day = parse_day(raw_date)
        q = pick_for_date(self._bank, day)
        request_id = uuid.uuid4().hex[:12]

        def run_one(lang: str, src: str, stdin: str):
            try:
                body = self._runner.run(lang, src, stdin, {}, request_id)
            except CodeEngineError as exc:
                return False, "", f"engine: {exc.code}"
            ok = body.get("verdict") == "ok" and (body.get("exit_code") in (0, None))
            err = "" if ok else (body.get("stderr") or body.get("verdict") or "run failed")
            return ok, body.get("stdout", ""), err

        verdict = grade_dsa(run_one, q, language, code)
        return {
            "date": day.isoformat(),
            "question_id": q.id,
            "passed": verdict.passed,
            "total": verdict.total,
            "verdict": verdict.verdict,
            "accepted": verdict.accepted,
            "failed_case": verdict.failed_case,
        }
