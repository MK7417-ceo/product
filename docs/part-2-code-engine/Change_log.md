# Part 2 — Code Execution Engine: Change Log

Dated history of the part. Newest first.

## 2026-10-04 — Dossier created (P2.0)

- Requirements locked from the v2 spec: self-hosted sandbox runner using
  standard GCC/Python/etc. toolchains in isolated Docker containers; hard
  limits (no network; CPU/RAM/output/wall-time caps); **separate runner host**
  from the main app (security); GFG/W3Schools-like in-browser editor,
  mobile-friendly (user is phone-first).
- Plagiarism contract locked: strip comments/whitespace, normalize identifiers,
  compare structural fingerprints (not shared syntax); **flag for human review,
  never auto-punish**.
- Integration contract locked: one versioned HTTP API; Core consumes only via
  the `CodeRunnerClient` outbound port (swappable/mockable).
- Architecture locked (user-approved): Clean/Hexagonal for all 3 parts.
- 10-file dossier written: PRD, TRD, PLAN, SPECS, TESTING, DEBUG_GUIDE, BUGS,
  ProgressTracker, Change_log, Change_ledger. No code written (docs-first gate).
- Next: user reviews dossier → P2.1 PLAN approval → contract-first API design.
