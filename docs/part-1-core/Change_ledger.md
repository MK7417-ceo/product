# Part 1 — SkillForge Core: Change_ledger

Decisions with rationale + rejected alternatives. Newest first.

## 2026-10-04 — Clean/Hexagonal architecture for all parts

Rationale: famous, proven (Cockburn/Martin); add/remove/update any feature via
ports without touching callers; testable domain core with fake adapters.
Rejected: microservices-everything (3–5× ops burden for our scale; classic
premature-complexity trap). Exception: code runner stays a separate service
(Part 2) — security forces physical isolation.

## 2026-10-04 — 3-part split (Core / Code Engine / Career Launchpad)

Rationale: project too big for one track; each part independently runnable,
demoable, documented. Rejected: single mega-plan (unreviewable, big-bang risk).

## 2026-10-04 — MVP-first launch

Rationale: real feedback fast; small releases = fewer errors; revenue earlier.
Rejected: full-app-at-once (months of work, zero feedback, big-bang defects).

## 2026-10-04 — Hybrid question strategy

Rationale: AI-fresh questions per attempt (no identical sets) + curated real
interview questions (level-tagged, trusted). Rejected: AI-only (hallucination
risk) and curated-only (stale, repeatable sets).

## 2026-10-04 — Aurora Dark UI direction

Rationale: user picked design 1 of 3 for attractive + expert feel. Rejected:
Paper Light, Command Center (kept as future themes).

## 2026-10-04 — Founder-skills gates (PLAN → agent lane → developer lane)

Rationale: user's mandate — every feature planned, actually run on the agent's
end AND the developer's end, never "just code". No phase closes until both
lanes pass.

## 2026-10-03 — Modular monolith kept (not rewritten)

Rationale: M0–M9 backend is tested (544 green) and security-hardened;
rewriting reintroduces fixed bugs (auth holes, fake scores, fake verification).
Frontend IS being rebuilt fresh in phases (A1 done).
