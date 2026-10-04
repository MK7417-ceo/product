# SKILLFORGE v2 — Program Dossier

Big project, split into **3 independently-running parts**, built on a famous
architecture (Clean/Hexagonal — decided 2026-10-04, user-approved).

## The 3 parts

| # | Part | What it is | Runs as |
|---|---|---|---|
| 1 | `part-1-core/` | SkillForge Core — the learn & assess loop (auth, profiles, skill graph, hybrid question bank, assessments, deterministic + AI scoring, gaps, roadmaps, domain tracks, daily questions, weekly mocks) | Modular monolith (FastAPI) |
| 2 | `part-2-code-engine/` | Code Execution Engine — sandbox code runner, in-browser editor UX, plagiarism check | **Separate service** (FastAPI + Docker sandbox, isolated host — security) |
| 3 | `part-3-career-launchpad/` | Career Launchpad — hiring prep (GD/PI/extempore/presentation, typing, quant, IELTS), resume builder + JD matcher (ATS), portfolio builder → user's GitHub, certificates, subscriptions/billing | Modules in the monolith, behind ports |

Each part is independently runnable, independently demoable, and carries its
own 10-file dossier.

## Docs per part (10 files)

| File | Purpose |
|---|---|
| `PRD.md` | Product requirements: vision, personas, Must/Should/Won't, acceptance criteria, metrics |
| `TRD.md` | Technical requirements: hexagonal mapping (ports/adapters), APIs, data model, NFRs |
| `PLAN.md` | Phased implementation plan with gates |
| `SPECS.md` | Per-feature specs: inputs, behavior, outputs, edge cases |
| `TESTING.md` | **Two lanes:** Agent lane (run on agent's end, exact commands + evidence) and Developer lane (user's Codespace checklist). No feature is "done" until both lanes pass. |
| `DEBUG_GUIDE.md` | Bug-finding playbook: reproduce → isolate → logs → fix + regression test |
| `BUGS.md` | Bug log (open/fixed), seeded with real known issues |
| `ProgressTracker.md` | Phase/feature status, seeded with real current state |
| `Change_log.md` | Dated changelog, seeded with real history |
| `Change_ledger.md` | Decision ledger: decision, rationale, rejected alternatives |

## Shared

- `ARCHITECTURE.md` — the Clean/Hexagonal decision, the rules, and the
  non-negotiable conventions for all 3 parts.

## Workflow (founder-skills gates, mirrored here — no Claude Code needed)

```
clarify → PRD → TRD → PLAN → execute in phases →
  agent-lane testing (run on agent's end, evidence attached) →
  developer-lane check (your Codespace, checklist) →
  review → next phase
```

Premature coding is halted at the gates: no phase starts until its PLAN is
approved, no phase closes until both testing lanes pass.
