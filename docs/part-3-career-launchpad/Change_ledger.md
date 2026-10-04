# Change_ledger — Part 3: Career Launchpad

Decision ledger: what was decided, why, and what was rejected. Newest first.

## D1 (2026-10-04) — Subscription tiers + pricing

- **Decision:** Free ₹0 / Pro ₹249/mo (₹1,999/yr) / Expert ₹599/mo (₹4,999/yr);
  Razorpay for India, Stripe for international; provider-hosted checkout only.
- **Rationale:** India-first pricing; break-even math — small-level infra
  ≈ $45/mo (≈ ₹3,750/mo) is covered by **~20 Pro monthly subs**; every sub
  beyond that funds growth. Razorpay fee ≈ 2% + GST per transaction.
- **Rejected:** single flat tier (doesn't segment students vs abroad
  aspirants); in-house card processing (PCI burden, unjustifiable).

## D2 (2026-10-04) — Portfolio published to the user's GitHub

- **Decision:** builder generates a repo on the USER's GitHub via OAuth;
  GitHub Pages serves it live. Existing-portfolio link kept separate.
- **Rationale:** user owns the code (can `git pull` anytime), sees UI on
  GitHub, and hosting costs us ₹0 — vs per-user static hosting we'd pay for.
- **Rejected:** hosting portfolios ourselves (cost + ownership confusion).

## D3 (2026-10-04) — Trend watcher is semi-automatic

- **Decision:** monitor flags emerging skills/fields; human-curated ingestion
  (skill graph + seed questions + roadmap template) ships the domain.
- **Rationale:** fully-automatic ingestion is dishonest — new domains need
  curated graphs/questions. Flagging is automatable; quality isn't.
- **Rejected:** "auto-update new fields" as a hands-free promise.

## D4 (2026-10-04) — Camera-ON with consent, no retention

- **Decision:** proctored interviews/mocks require explicit consent (timestamp
  stored); frames processed in-memory; no video retained; tab-switch flags
  recorded; no-camera practice mode always available.
- **Rationale:** user's choice (camera-ON) balanced with privacy law and
  trust; retention is the liability, not the camera.
- **Rejected:** recording storage for "review later" (privacy risk, cost).

## D5 (2026-10-04) — No LinkedIn/LeetCode auto-post promises

- **Decision:** OAuth linking + one-click share/export + LeetCode deep-link
  nudge ("paste your solution on problem #N").
- **Rationale:** their APIs don't permit free automatic posting; promising it
  would be a lie discovered at launch.
- **Rejected:** fake "auto-sync everywhere" marketing.

## D6 (2026-10-04) — Entitlements before features (build order)

- **Decision:** P3.1 billing/entitlements is the critical path; every gated
  endpoint checks entitlements from day one.
- **Rationale:** bolting payments on later is how "paid but locked out"
  S1 bugs are born. Per-user quotas even on paid tiers keep unit economics
  positive at scale.
