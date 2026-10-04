# Part 2 — Code Execution Engine: TESTING

**Rule: no feature is "done" until BOTH lanes pass. Security tests are blocking —
a single containment failure stops the release.**

## Lane 1 — Agent lane (run on the agent's end, evidence attached)

### Unit tests (domain core, no Docker)
```bash
cd runner-service && python -m pytest tests/unit -q
```
Must cover: verdict classification, limit validation, plagiarism normalizer +
fingerprinter on the labeled eval set, identifier canonicalization.

### Integration tests (real Docker, local daemon)
```bash
cd runner-service && python -m pytest tests/integration -q
# requires: docker daemon running; pulls python:3.12-slim, gcc:13, openjdk:17-slim once
```
Must cover: `POST /v1/run` per language, compile-error path, stdin/stdout
round-trip, grading batch, async job lifecycle, `X-Request-ID` echo.

### Malicious-code battery (BLOCKING — all must be contained)
```bash
cd runner-service && python -m pytest tests/security -q
```
| Attack | Code | Must observe |
|---|---|---|
| Fork bomb | `:(){ :|:& };:` (bash) / multiprocessing spawn loop (py) | container killed via pids-limit; host load flat |
| Network exfil | `socket.connect(("8.8.8.8",53))` / `curl` | connection fails; no packets leave (no network) |
| Disk fill | write 2GB to /tmp | capped at tmpfs limit; container dies cleanly |
| Memory bomb | `[0]*10**10` | OOM-killed → `MLE`; host RAM flat |
| Infinite loop | `while True: pass` | killed at wall-time → `TLE` |
| Output flood | print 100MB | truncated at 1MB, `truncated: true` |

**Evidence required:** pytest output + host `docker stats` / load snapshot during
the battery, attached to the phase report. If Docker is unavailable in the
agent sandbox, the battery runs on the dev VPS and logs are attached instead —
it is never skipped.

### Plagiarism eval set
```bash
cd runner-service && python -m pytest tests/plagiarism -q
# 30 labeled pairs: verbatim copies, renamed-identifier clones, reordered logic,
# independent solutions, starter-code-only pairs
```
Gate: precision ≥ 0.9 at threshold 0.85; starter-only pairs must NOT flag.

## Lane 2 — Developer lane (user's Codespace checklist)

Run on the user's machine; check each box honestly:

- [ ] `docker compose up runner` starts; `GET /v1/health` returns
      `{"status":"ok","docker":"reachable"}`.
- [ ] Python fibonacci via `POST /v1/run` returns output in < 8s.
- [ ] `while True: pass` returns `TLE` (not a hang).
- [ ] C++ "hello world" compiles and runs; a syntax error returns
      `COMPILE_ERROR` with the compiler message.
- [ ] A socket-connect program fails to reach the network.
- [ ] Editor page: type code on a phone-width viewport (360px), press Run,
      read the output without zooming or horizontal scroll.
- [ ] Two near-identical submissions via `/v1/plagiarism/check` → flagged with
      fingerprints shown; two different solutions → clear.

**What "working" looks like:** runs return in seconds, bad code is killed (not
hung), the host is untouched by hostile code, and the editor is usable on a
phone. If any box fails, the phase is not done — file it in BUGS.md.

## Regression rule

Every bug fixed gets a test that would have caught it, in the matching lane.
Security regressions go in `tests/security/` permanently.
