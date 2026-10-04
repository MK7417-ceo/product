# Part 2 — Code Execution Engine: PLAN

**Status:** PROPOSED (2026-10-04). No phase starts until its PLAN section is
approved; no phase closes until both testing lanes pass (see TESTING.md).

## Contract-first rule (P2.1 gate)

Before any container code is written, Core and the runner agree the v1 HTTP
contract (`POST /v1/run`, `GET /v1/run/{id}`, error shapes, `X-Request-ID`).
Core builds against a **mock** `CodeRunnerClient`; the real runner must satisfy
the same contract. Contract tests are shared.

## Phase P2.1 — Runner MVP (Python-only, sync API)

- **Goal:** untrusted Python executes safely in Docker behind `POST /v1/run`.
- **Features:** FastAPI service skeleton; `DockerContainerRuntime` adapter;
  Python 3.12 image; limits table enforced; `RunJob`/`RunResult` domain;
  `HttpCodeRunnerClient` in Core (mock-first); request IDs + structured logs.
- **Done-criteria:** malicious-code battery contained (fork bomb, network
  exfil, disk fill); p95 < 8s on 100 sample runs; contract tests green.
- **Demo:** `curl POST /v1/run` with a Python fibonacci + a `while True` (TLE).

## Phase P2.2 — Multi-language + async jobs

- **Goal:** C, C++, Java join the matrix; long runs go async.
- **Features:** gcc C11 / g++ C++17 / OpenJDK 17 images; compile-error verdict
  path; `POST /v1/jobs` + `GET /v1/jobs/{job_id}`; `POST /v1/grade` (test-case
  batch); queue depth bound + 429.
- **Done-criteria:** all 4 languages pass the verdict matrix
  (AC/WA/TLE/MLE/RE/CE each demonstrated); async job survives a 25s run.
- **Demo:** C++ solution graded against 5 cases; one TLE case shown.

## Phase P2.3 — Plagiarism check

- **Goal:** flag-only similarity signal with evidence, never auto-punish.
- **Features:** normalizer (strip comments/whitespace, canonicalize
  identifiers, exclude starter code); structural fingerprint (token n-grams +
  AST-shape hash for Python; token-based for C/C++/Java); `POST
  /v1/plagiarism/check`; `SimilarityReport` with both fingerprints and reasons.
- **Done-criteria:** labeled eval set (30 pairs: copies, paraphrases, originals)
  → precision ≥ 0.9 at flag threshold 0.85; paraphrase (renamed vars) still
  flagged; starter-code-only pairs NOT flagged.
- **Demo:** two "different-looking, same-logic" submissions flagged with
  evidence shown.

## Phase P2.4 — Editor UX polish + mobile

- **Goal:** GFG/W3Schools-like editor the user can run on their phone.
- **Features:** Aurora Dark editor page in Core frontend: code editor, language
  picker, stdin box, Run button, output panel with verdict badge, sample-case
  runner; line numbers, font-size control; 360px-width operability; loading and
  error states; `prefers-reduced-motion`.
- **Done-criteria:** developer-lane checklist passes on a real phone viewport;
  no horizontal scroll; run→result readable without zoom.
- **Demo:** screen recording of phone-viewport run (screenshot evidence).

## Gates

1. PLAN approved → 2. build on task branch → 3. agent-lane tests (actually run,
   evidence attached) → 4. developer-lane check (user's Codespace checklist) →
   5. review → 6. next phase. Security tests are blocking at every gate.

## Dependencies

- Core (Part 1) consumes via the `CodeRunnerClient` port; contract agreed P2.1.
- Needs a runner VPS at deploy time (not on managed app hosting); local Docker
  suffices for dev/test.
- P2.3 needs the labeled eval set (built in-phase, reviewed by a human).
