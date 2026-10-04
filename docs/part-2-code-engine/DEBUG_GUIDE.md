# Part 2 — Code Execution Engine: DEBUG GUIDE

Bug-finding playbook. Follow the order; don't guess.

## The loop

1. **Reproduce** — get the exact failing input (language, code, stdin,
   limits) and the `X-Request-ID`. If it doesn't reproduce with the same
   request ID's inputs, it's a flake: note it, don't "fix" it.
2. **Isolate the layer** — editor UI → Core forwarding → runner API →
   container runtime → limits/supervisor. Test each boundary with curl:
   - `curl POST <runner>/v1/health` — is the runner alive, Docker reachable?
   - `curl POST <runner>/v1/run` with a trivial program — is execution itself OK?
   - Same request through Core's route — is forwarding faithful (code, stdin,
     request ID unchanged)?
3. **Logs** — runner structured logs filtered by `request_id`; then
   `docker logs` of the specific container (if still alive); then host
   `dmesg | grep -i oom` for OOM kills.
4. **Minimal repro** — shrink the program to the smallest code that still
   fails; keep it as the regression test.
5. **Fix + regression test** — every fix ships with a test (TESTING.md rule).

## Common failure catalog

| Symptom | Likely layer | First check |
|---|---|---|
| `SYSTEM_ERROR`, container never starts | container runtime | `docker info`; image present? daemon disk full? (`docker system df`) |
| Run hangs, no result | limits/supervisor | wall-time killer alive? zombie containers: `docker ps` accumulating? |
| `MLE` on small programs | limits | memory limit misconfigured per language (JVM needs headroom: set `-Xmx` < container limit) |
| Output cut mid-line | output cap | expected: 1MB truncation; if earlier, check stream buffering (`python -u`) |
| `COMPILE_ERROR` with empty stderr | compile step | capture both stdout+stderr of compiler; Java: class must be `Main` |
| 429 on modest traffic | queue/rate limit | queue depth metric; per-user vs per-IP limit hit? |
| Plagiarism false flag | normalizer | was starter code excluded? check the fingerprints in the report |
| Editor shows stale output | UI | request ID mismatch: response matched to wrong run (race on rapid Run clicks — disable button while running) |

## Zombie-process drill

If `docker ps` shows exited-but-unreaped containers growing: the supervisor
isn't reaping. Check: container `--init` flag set? (Use `tini`.) Fix at the
runtime adapter level, add a test asserting zero leftover containers after
100 runs.

## Severity levels

- **S0 (stop the release):** any sandbox escape, host impact, data leak of
  another user's code, plagiarism auto-punishment occurring.
- **S1:** wrong verdicts (AC marked WA), sustained p95 > 15s, queue stuck.
- **S2:** single-language breakage, UI glitches, misleading error text.
- **S3:** cosmetic, docs.

S0/S1 fixes require re-running the full security battery before merge.
