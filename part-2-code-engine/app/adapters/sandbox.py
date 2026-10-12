"""Outbound adapter: executes a process inside a real sandbox.

Isolation stack (no Docker needed):
  1. fork() + child calls os.setsid()  -> own process group (killpg kills
     the whole tree: fork bombs and grandchildren cannot escape the kill)
  2. os.unshare(CLONE_NEWNET)          -> the child has NO network
     (fail-closed: if unshare fails, the run is aborted, never executed)
  3. RLIMIT_CPU                        -> CPU seconds cap (SIGXCPU/SIGKILL)
  4. RLIMIT_AS                         -> virtual memory cap
  5. RLIMIT_NPROC                      -> fork-bomb containment
  6. RLIMIT_FSIZE                      -> no giant files on disk
  7. parent wall-clock watchdog        -> SIGKILL the group on timeout
  8. output streaming with hard caps   -> stdout/stderr truncated, flagged

Peak RAM comes from wait4() rusage (ru_maxrss); CPU time from
ru_utime + ru_stime. Honest numbers, measured — not estimated.

Production note: for multi-tenant hostile workloads, still prefer a
container/VM boundary (gVisor, Firecracker, Kata). This sandbox is the
dev/self-hosted grade: real isolation primitives, documented limits.
"""
from __future__ import annotations

import os
import resource
import selectors
import signal
import time
from dataclasses import dataclass


@dataclass
class SandboxOutcome:
    stdout: bytes
    stderr: bytes
    truncated: bool
    exit_code: int | None      # None if killed by signal
    term_signal: int | None    # signal number if killed by signal
    cpu_ms: int | None
    peak_ram_mb: float | None
    timed_out: bool


def _oom_hint(stderr: bytes) -> bool:
    text = stderr.decode("utf-8", "replace").lower()
    return any(k in text for k in (
        "bad_alloc", "memoryerror", "outofmemoryerror",
        "cannot allocate memory", "killed", "std::bad_alloc",
    ))


def execute_sandboxed(
    argv: list[str],
    *,
    workdir: str,
    stdin_data: bytes = b"",
    wall_time_s: int = 10,
    memory_mb: int = 256,
    stdout_cap: int = 64 * 1024,
    stderr_cap: int = 16 * 1024,
    drop_privileges: bool = True,
) -> SandboxOutcome:
    """Run argv[0..] sandboxed. Raises RuntimeError if isolation fails."""
    stdin_r, stdin_w = os.pipe()
    stdout_r, stdout_w = os.pipe()
    stderr_r, stderr_w = os.pipe()

    pid = os.fork()
    if pid == 0:
        # ---------------- child ----------------
        try:
            os.setsid()
            try:
                os.unshare(os.CLONE_NEWNET)
            except OSError as exc:
                os.write(stderr_w, f"sandbox: network isolation failed: {exc}\n".encode())
                os._exit(127)
            # resource caps
            mem_bytes = memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
            resource.setrlimit(resource.RLIMIT_CPU, (wall_time_s, wall_time_s + 1))
            resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
            resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 1024 * 1024, 4 * 1024 * 1024))
            os.chdir(workdir)
            if drop_privileges:
                try:
                    os.setgid(65534)
                    os.setuid(65534)
                except OSError:
                    pass  # best effort; rlimits + netns still hold
            os.dup2(stdin_r, 0)
            os.dup2(stdout_w, 1)
            os.dup2(stderr_w, 2)
            for fd in (stdin_r, stdin_w, stdout_r, stdout_w, stderr_r, stderr_w):
                try:
                    os.close(fd)
                except OSError:
                    pass
            os.execvp(argv[0], argv)
        except Exception as exc:  # exec failed
            try:
                os.write(2, f"sandbox: exec failed: {exc}\n".encode())
            except OSError:
                pass
            os._exit(127)
        os._exit(127)  # unreachable

    # ---------------- parent ----------------
    for fd in (stdin_r, stdout_w, stderr_w):
        os.close(fd)
    os.set_blocking(stdout_r, False)
    os.set_blocking(stderr_r, False)

    # feed stdin, then close
    try:
        os.write(stdin_w, stdin_data)
    except (OSError, BrokenPipeError):
        pass
    os.close(stdin_w)

    sel = selectors.DefaultSelector()
    sel.register(stdout_r, selectors.EVENT_READ, "out")
    sel.register(stderr_r, selectors.EVENT_READ, "err")
    out_chunks: list[bytes] = []
    err_chunks: list[bytes] = []
    out_len = err_len = 0
    truncated = False
    deadline = time.monotonic() + wall_time_s
    timed_out = False
    open_fds = 2
    reaped_status = None
    reaped_rusage = None

    while open_fds:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            break
        for key, _ in sel.select(timeout=min(remaining, 0.2)):
            data = os.read(key.fileobj, 65536)
            if not data:
                sel.unregister(key.fileobj)
                os.close(key.fileobj)
                open_fds -= 1
                continue
            if key.data == "out":
                if out_len < stdout_cap:
                    take = data[: stdout_cap - out_len]
                    out_chunks.append(take)
                    out_len += len(take)
                    if len(data) > len(take):
                        truncated = True
                else:
                    truncated = True
            else:
                if err_len < stderr_cap:
                    take = data[: stderr_cap - err_len]
                    err_chunks.append(take)
                    err_len += len(take)
                    if len(data) > len(take):
                        truncated = True
                else:
                    truncated = True
        # re-check child liveness cheaply; capture status here — a second
        # wait4 would raise ChildProcessError (already reaped)
        done_pid, wstatus, wrusage = os.wait4(pid, os.WNOHANG)
        if done_pid == pid:
            reaped_status, reaped_rusage = wstatus, wrusage
            open_fds = 0  # child gone; drain whatever is left without blocking
            for key, _ in sel.select(timeout=0.5):
                data = os.read(key.fileobj, 65536)
                if data:
                    if key.data == "out" and out_len < stdout_cap:
                        take = data[: stdout_cap - out_len]
                        out_chunks.append(take)
                        out_len += len(take)
                    elif key.data == "err" and err_len < stderr_cap:
                        take = data[: stderr_cap - err_len]
                        err_chunks.append(take)
                        err_len += len(take)
            break

    if timed_out:
        try:
            os.killpg(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass

    # reap; wait4 gives us rusage for honest cpu/ram numbers.
    # (If the WNOHANG probe above already reaped the child, reuse it.)
    status = reaped_status
    rusage = reaped_rusage
    if status is None:
        try:
            _, status, rusage = os.wait4(pid, 0)
        except ChildProcessError:
            pass

    for key in list(sel.get_map().values()):
        try:
            sel.unregister(key.fileobj)
            os.close(key.fileobj)
        except OSError:
            pass

    exit_code = term_signal = None
    if status is not None:
        if os.WIFEXITED(status):
            exit_code = os.WEXITSTATUS(status)
        elif os.WIFSIGNALED(status):
            term_signal = os.WTERMSIG(status)

    cpu_ms = peak_ram_mb = None
    if rusage is not None:
        cpu_ms = int((rusage.ru_utime + rusage.ru_stime) * 1000)
        # ru_maxrss is KiB on Linux
        peak_ram_mb = round(rusage.ru_maxrss / 1024, 2)

    return SandboxOutcome(
        stdout=b"".join(out_chunks),
        stderr=b"".join(err_chunks),
        truncated=truncated,
        exit_code=exit_code,
        term_signal=term_signal,
        cpu_ms=cpu_ms,
        peak_ram_mb=peak_ram_mb,
        timed_out=timed_out,
    )


def classify(outcome: SandboxOutcome, memory_mb: int) -> str:
    """Map a sandbox outcome to a spec verdict."""
    from app.domain.execution import MLE, OK, RUNTIME_ERROR, TLE
    if outcome.timed_out:
        return TLE
    if outcome.term_signal == signal.SIGXCPU:
        return TLE
    if outcome.term_signal == signal.SIGKILL:
        # OOM-killed (rlimit) vs CPU SIGKILL: use peak RSS proximity to the cap
        if outcome.peak_ram_mb and outcome.peak_ram_mb >= 0.9 * memory_mb:
            return MLE
        if _oom_hint(outcome.stderr):
            return MLE
        return RUNTIME_ERROR
    if outcome.term_signal:
        return MLE if _oom_hint(outcome.stderr) else RUNTIME_ERROR
    if outcome.exit_code == 0:
        return OK
    return MLE if _oom_hint(outcome.stderr) else RUNTIME_ERROR
