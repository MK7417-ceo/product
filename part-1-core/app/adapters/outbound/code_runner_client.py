"""Outbound adapter: HTTP client for the Part 2 Code Execution Engine.

The browser never talks to the engine directly — Core proxies, so auth,
rate-limiting and audit stay in one place, and the engine host stays
isolated. Uses only the stdlib (urllib): no new dependencies.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Callable

from app.ports.outbound import CodeEngineError

ENGINE_TIMEOUT_S = 45  # engine wall-time max 30s + compile + margin


def _default_transport(url: str, payload: dict, headers: dict,
                       timeout: int, method: str = "POST") -> tuple[int, dict]:
    data = json.dumps(payload).encode() if method == "POST" else None
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", **headers},
        method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode())
        except Exception:
            body = {"message": exc.reason}
        return exc.code, body
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise CodeEngineError("engine_unreachable",
                              f"code engine unreachable: {exc}")


class HttpCodeRunnerClient:
    def __init__(self, base_url: str,
                 transport: Callable = _default_transport) -> None:
        self._base = base_url.rstrip("/")
        self._transport = transport

    def run(self, language: str, code: str, stdin: str,
            limits: dict, request_id: str) -> dict:
        status, body = self._transport(
            f"{self._base}/v1/run",
            {"language": language, "code": code, "stdin": stdin,
             "limits": limits or {}},
            {"X-Request-ID": request_id}, ENGINE_TIMEOUT_S)
        if status == 400:
            raise CodeEngineError(body.get("error", "bad_request"),
                                  body.get("message", "engine rejected the run"),
                                  status=400)
        if status != 200:
            raise CodeEngineError("engine_error",
                                  f"engine returned HTTP {status}")
        return body

    def languages(self) -> list[dict]:
        status, body = self._transport(f"{self._base}/v1/languages", {},
                                       {}, ENGINE_TIMEOUT_S, "GET")
        if status != 200:
            raise CodeEngineError("engine_error",
                                  f"engine returned HTTP {status}")
        return body.get("languages", [])
