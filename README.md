# product — SKILLFORGE v2

Skill-intelligence platform: learn → assess → verify → hire. Three
independently-running parts, one famous architecture: **Clean/Hexagonal
(Ports & Adapters)**.

## The 3 parts

| # | Directory | What | Runs as |
|---|---|---|---|
| 1 | `part-1-core/` | SkillForge Core — auth, profiles, skill graph, assessments, scoring, gaps, roadmaps, tracks, mocks | FastAPI monolith |
| 2 | `part-2-code-engine/` | Code Execution Engine — sandbox runner, editor UX, plagiarism check | Separate FastAPI service (isolated host) |
| 3 | `part-3-career-launchpad/` | Career Launchpad — hiring prep, resume/JD matcher, portfolio → GitHub, certificates, billing | Modules in the monolith |

## Docs

`docs/` holds the full program dossier: architecture decision, and per part
PRD / TRD / PLAN / SPECS / TESTING / DEBUG_GUIDE / BUGS / ProgressTracker /
Change_log / Change_ledger.

## Workflow

Clarify → PRD → TRD → PLAN → build in phases → agent-lane tests (run on the
agent's end, evidence in PR) → developer-lane check (your Codespace) →
review → merge. The agent never merges; the user merges every PR.
