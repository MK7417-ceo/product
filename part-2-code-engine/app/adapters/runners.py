"""Inbound adapter: implements the CodeRunnerService port.

Per-language compile+run over the sandbox. Adding a language = one entry
in _LANGUAGES; no port changes.
"""
from __future__ import annotations

import os
import shutil
import tempfile
import uuid
from dataclasses import dataclass

from app.adapters.sandbox import classify, execute_sandboxed
from app.domain.execution import (
    COMPILE_ERROR,
    COMPILE_TIMEOUT_S,
    ExecutionError,
    ExecutionRequest,
    ExecutionResult,
    MAX_STDERR_BYTES,
    MAX_STDOUT_BYTES,
)


@dataclass(frozen=True)
class LanguageSpec:
    filename: str
    compile: tuple[str, ...] | None   # None = interpreted
    run: tuple[str, ...]
    toolchain_bins: tuple[str, ...]   # must exist on PATH


_LANGUAGES: dict[str, LanguageSpec] = {
    "python": LanguageSpec("solution.py", None, ("python3", "-u", "solution.py"), ("python3",)),
    "c": LanguageSpec("solution.c", ("gcc", "-std=c11", "-O2", "-o", "solution", "solution.c"),
                      ("./solution",), ("gcc",)),
    "cpp": LanguageSpec("solution.cpp", ("g++", "-std=c++17", "-O2", "-o", "solution", "solution.cpp"),
                        ("./solution",), ("g++",)),
    "java": LanguageSpec("Main.java", ("javac", "Main.java"), ("java", "Main"),
                         ("javac", "java")),
}


class CodeRunnerServiceImpl:
    def languages(self) -> list[dict]:
        return [
            {"id": lang,
             "compile": list(spec.compile) if spec.compile else None,
             "run": list(spec.run),
             "available": all(shutil.which(b) for b in spec.toolchain_bins)}
            for lang, spec in _LANGUAGES.items()
        ]

    def run(self, request: ExecutionRequest) -> ExecutionResult:
        spec = _LANGUAGES[request.language]
        missing = [b for b in spec.toolchain_bins if not shutil.which(b)]
        if missing:
            raise ExecutionError("toolchain_missing",
                                 f"{request.language} toolchain not installed: {', '.join(missing)}")
        run_id = uuid.uuid4().hex[:12]
        lim = request.limits
        stdin = request.stdin.encode("utf-8")

        with tempfile.TemporaryDirectory(prefix="sfrun_") as workdir:
            os.chmod(workdir, 0o777)  # sandboxed nobody-user must read sources
                                          # and write build artifacts; dir is per-run temp
            with open(f"{workdir}/{spec.filename}", "w", encoding="utf-8") as f:
                f.write(request.code)
            os.chmod(f"{workdir}/{spec.filename}", 0o644)

            # ---- compile (sandboxed, generous memory for the compiler) ----
            if spec.compile:
                cout = execute_sandboxed(
                    list(spec.compile), workdir=workdir,
                    wall_time_s=COMPILE_TIMEOUT_S, memory_mb=1024,
                    stdout_cap=MAX_STDOUT_BYTES, stderr_cap=MAX_STDERR_BYTES)
                if cout.exit_code != 0 or cout.term_signal:
                    return ExecutionResult(
                        run_id=run_id, verdict=COMPILE_ERROR,
                        stdout=cout.stdout.decode("utf-8", "replace"),
                        stderr=cout.stderr.decode("utf-8", "replace"),
                        truncated=cout.truncated, exit_code=cout.exit_code,
                        cpu_ms=cout.cpu_ms, peak_ram_mb=cout.peak_ram_mb,
                        timed_out=cout.timed_out)

            # ---- run (fully sandboxed: no network, capped cpu/mem/time) ----
            rout = execute_sandboxed(
                list(spec.run), workdir=workdir, stdin_data=stdin,
                wall_time_s=lim.wall_time_s, memory_mb=lim.memory_mb,
                stdout_cap=MAX_STDOUT_BYTES, stderr_cap=MAX_STDERR_BYTES)

        return ExecutionResult(
            run_id=run_id,
            verdict=classify(rout, lim.memory_mb),
            stdout=rout.stdout.decode("utf-8", "replace"),
            stderr=rout.stderr.decode("utf-8", "replace"),
            truncated=rout.truncated,
            exit_code=rout.exit_code,
            cpu_ms=rout.cpu_ms,
            peak_ram_mb=rout.peak_ram_mb,
            timed_out=rout.timed_out)
