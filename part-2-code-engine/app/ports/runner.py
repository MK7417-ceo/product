"""Ports: the CodeRunnerService inbound port.

Core (part-1) consumes Part 2 only through this contract; the HTTP API
and the sandbox are adapters behind it.
"""
from __future__ import annotations

from typing import Protocol

from app.domain.execution import ExecutionRequest, ExecutionResult


class CodeRunnerService(Protocol):
    def run(self, request: ExecutionRequest) -> ExecutionResult:
        """Compile (if needed) + execute inside the sandbox. Blocking."""
        ...

    def languages(self) -> list[dict]:
        """Supported languages + toolchain info."""
        ...
