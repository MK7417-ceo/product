# PLAN — Part 3: Career Launchpad

**Order is load-bearing:** billing/entitlements first (everything else gates
on it). No phase starts until its plan section is approved; no phase closes
until **both** testing lanes pass (agent lane + developer lane).

## P3.1 — Subscriptions & billing (critical path)

- **Goal:** tiers, checkout, webhooks, entitlements enforced on gated endpoints.
- **Features:** `BillingService` + `PaymentGateway` port; Razorpay adapter
  (test mode); Stripe adapter stubbed behind flag; `subscriptions`,
  `entitlements`, `billing_events` tables; `GET /billing/entitlements`;
  entitlement middleware returning 402 + upgrade hint.
- **Done when:** test-mode purchase → webhook → entitlement active → gated
  endpoint unlocks; cancel → entitlement revoked at period end; replayed
  webhook ignored (idempotency).
- **Demo:** agent runs test checkout; developer repeats in Codespace.

## P3.2 — Resume builder + JD matcher

- **Goal:** JD-specific ATS resumes (US1).
- **Features:** `ResumeService` + `ResumeRenderer`; JD keyword extraction
  (deterministic) + tailoring (AI behind budget cap); single-column PDF/DOCX;
  resume history; confidential-field placeholders.
- **Done when:** 3 sample JDs → resumes pass AC1 (format + ≥80% keywords or
  flagged gaps); no graphics/tables/fonts outside the ATS-safe list.
- **Demo:** paste a real JD, download PDF, run through a free ATS checker.

## P3.3 — Portfolio builder + GitHub publish

- **Goal:** 7-step builder → live portfolio on the user's GitHub (US4).
- **Features:** `PortfolioService` + `GitHubPublisher`; steps: template →
  about → verified skills import → projects import → experience → contact →
  review; OAuth repo create + static push + Pages enable; existing-link field
  kept separate.
- **Done when:** publish creates repo on the user's GitHub, Pages live,
  user can `git pull` it; builder resumable mid-way.
- **Demo:** developer publishes to their own GitHub from Codespace.

## P3.4 — Hiring prep modules

- **Goal:** realistic practice for every hiring phase (G1).
- **P3.4a (deterministic first):** typing test (WPM/accuracy), quant/aptitude
  (MCQ bank, server-scored).
- **P3.4b:** presentation + extempore (timed prompts, AI feedback).
- **P3.4c:** GD + PI mocks with camera consent flow + tab-switch flags; AI
  feedback on knowledge/confidence-proxy/expression/timing; challenge →
  human review.
- **P3.4d:** IELTS-level English track (weekly tests, progress graph).
- **Done when:** each module: start → attempt → feedback → history; camera
  consent enforced; no video retained; challenged feedback lands in review queue.
- **Demo:** developer runs one full mock interview in Codespace.

## P3.5 — Certificates, linking, trend watcher

- **Goal:** verifiable outcomes + honest integrations + future-proofing.
- **Features:** `CertificateService` (issue/verify/revoke, QR-coded page);
  `AccountLinkService` (Google/GitHub OAuth, one-click share/export,
  LeetCode deep-link nudge); `TrendWatcherService` (admin flag queue +
  curation flow → new domain intake).
- **Done when:** certificate verifies at public URL; share export works;
  trend flag → curated domain draft creatable by admin.
- **Demo:** issue + verify a certificate; flag a fake trend, curate it.

## Gates (apply to every phase)

1. PLAN section approved → 2. task branch + build → 3. agent-lane tests run
   with evidence → 4. developer-lane checklist in Codespace → 5. review →
   6. next phase. Failing gate = stop, fix, re-run. No skipping.
