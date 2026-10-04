# Part 1 — SkillForge Core: BUGS

Bug log. Format: ID · title · severity · status · linked PR · regression test.
New bugs go to the top of "Open". Nothing closes without a test.

## Open

- **BUG-001 · Results page crashes after assessment submit (blank screen).**
  S1 · OPEN · PR #28 (`fix/27-results-contract`). Cause: submit response used
  a `percentage` key with no confidence; frontend `AttemptResult` expects
  `mastery_percentage`/`confidence_percentage`; `.toFixed()` on undefined →
  React crash. Fix is additive (both key sets emitted). Regression test:
  contract test asserting the results payload matches the TS type.
- **BUG-002 · `uvicorn` missing from backend/requirements.txt.** S1 · OPEN ·
  PR #29 (`fix/uvicorn-missing-dep`). Fresh installs can't boot the API.
  Regression: CI install-from-requirements smoke step.
- **BUG-003 · Old UI still live (pre-Aurora).** S2 · OPEN · PR #30
  (`feat/v2-a1-aurora-design-system`). Dashboard/login on old styling; new
  system implemented, awaiting user review/merge.
- **BUG-004 · Thin question bank: 36 seeded questions.** S2 · OPEN (content
  gap, not code bug). Coverage too shallow for real assessments. Mitigation:
  Phase B hybrid bank (curated ingestion + AI generation + validation).

## Fixed (with regression tests)

- (none yet in v2 Core — M0–M9 fixes predate this log; their tests live in CI)
