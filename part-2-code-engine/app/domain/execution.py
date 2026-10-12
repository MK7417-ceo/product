"""Part 2 — Code Execution Engine. Hexagonal architecture.

Domain layer: PURE. ExecutionRequest / ExecutionResult / verdicts.
No I/O, no subprocess, no FastAPI here — the sandbox lives in adapters.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# ---- contract constants (mirror docs/part-2-code-engine/SPECS.md) ----
LANGUAGES = ("python", "c", "cpp", "java")
MAX_CODE_BYTES = 100 * 1024
MAX_STDIN_BYTES = 1024 * 1024
MAX_STDOUT_BYTES = 64 * 1024
MAX_STDERR_BYTES = 16 * 1024
DEFAULT_WALL_TIME_S = 10
MAX_WALL_TIME_S = 30
DEFAULT_MEMORY_MB = 256
MAX_MEMORY_MB = 512
COMPILE_TIMEOUT_S = 15

# verdicts
OK = "OK"
COMPILE_ERROR = "COMPILE_ERROR"
RUNTIME_ERROR = "RUNTIME_ERROR"
TLE = "TLE"  # time limit exceeded
MLE = "MLE"  # memory limit exceeded


class ExecutionError(ValueError):
    """Raised for invalid requests (maps to HTTP 400)."""
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class Limits:
    wall_time_s: int = DEFAULT_WALL_TIME_S
    memory_mb: int = DEFAULT_MEMORY_MB

    def __post_init__(self) -> None:
        if not 1 <= self.wall_time_s <= MAX_WALL_TIME_S:
            raise ExecutionError("bad_limits",
                                 f"wall_time_s must be 1..{MAX_WALL_TIME_S}")
        if not 64 <= self.memory_mb <= MAX_MEMORY_MB:
            raise ExecutionError("bad_limits",
                                 f"memory_mb must be 64..{MAX_MEMORY_MB}")


@dataclass(frozen=True)
class ExecutionRequest:
    language: str
    code: str
    stdin: str = ""
    limits: Limits = field(default_factory=Limits)

    def __post_init__(self) -> None:
        if self.language not in LANGUAGES:
            raise ExecutionError("unsupported_language",
                                 f"language must be one of {LANGUAGES}")
        if not self.code or not self.code.strip():
            raise ExecutionError("empty_code", "code must not be empty")
        if len(self.code.encode("utf-8")) > MAX_CODE_BYTES:
            raise ExecutionError("code_too_large",
                                 f"code exceeds {MAX_CODE_BYTES} bytes")
        if len(self.stdin.encode("utf-8")) > MAX_STDIN_BYTES:
            raise ExecutionError("stdin_too_large",
                                 f"stdin exceeds {MAX_STDIN_BYTES} bytes")


@dataclass(frozen=True)
class ExecutionResult:
    run_id: str
    verdict: str
    stdout: str
    stderr: str
    truncated: bool
    exit_code: int | None
    cpu_ms: int | None
    peak_ram_mb: float | None
    timed_out: bool
