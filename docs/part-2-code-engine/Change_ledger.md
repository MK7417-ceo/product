# Part 2 — Code Execution Engine: Change Ledger

Decision ledger: what was decided, why, and what was rejected. Decisions are
cheap to revisit only if the rationale is written down.

## D-1 — Standard toolchains in Docker, NOT a from-scratch compiler

- **Decision (2026-10-04, user briefed):** use GCC, CPython, OpenJDK inside
  containers. Never build a compiler/interpreter.
- **Rationale:** this is how the industry does it (all major judges are
  sandbox + standard toolchain); building a compiler is a multi-year project
  with worse correctness.
- **Rejected:** from-scratch compiler/interpreter (infeasible, dishonest to promise).

## D-2 — Separate runner host from the Core app

- **Decision (2026-10-04):** the runner is a physically separate service on its
  own host; untrusted code never shares a machine with user data.
- **Rationale:** defense in depth — even a container escape lands on a box
  with no user DB, no secrets, no Core process.
- **Rejected:** running containers on the app server (cheaper, catastrophically
  riskier); serverless-per-run (cost unpredictable at our scale).

## D-3 — Plagiarism: flag for human review, NEVER auto-punish

- **Decision (2026-10-04):** similarity scores produce flags + evidence
  (fingerprints, reasons) for a reviewer queue. No automatic bans, score
  deductions, or account actions.
- **Rationale:** false positives are inevitable (idiomatic short solutions,
  common patterns); auto-punishment would punish innocent learners and destroy
  trust.
- **Rejected:** auto-ban/auto-deduct on high similarity.

## D-4 — Contract-first API between Core and runner

- **Decision (2026-10-04):** agree the v1 HTTP contract (endpoints, shapes,
  `X-Request-ID`, error codes) in P2.1 before container code; Core builds
  against a mock `CodeRunnerClient`; shared contract tests.
- **Rationale:** the two parts are built by different lanes (agent + developer);
  the contract is the only coupling point — Hexagonal's `CodeRunnerClient` port
  made concrete.
- **Rejected:** building both sides against assumed shapes (integration bugs).

## D-5 — Deterministic plagiarism pipeline (no LLM)

- **Decision (2026-10-04):** normalization → structural fingerprints → Jaccard
  scoring, all deterministic.
- **Rationale:** explainable, reproducible, zero per-check cost, auditable
  evidence — an LLM "similarity opinion" would be none of these.
- **Rejected:** LLM-based similarity judgment.
