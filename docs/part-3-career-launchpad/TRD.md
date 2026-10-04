# TRD — Part 3: Career Launchpad

**Status:** DRAFT. **Architecture:** Clean/Hexagonal — domain core is pure
Python (+pydantic); FastAPI routers are inbound adapters; everything external
is an outbound port with swappable adapters.

## Tech stack

- Backend: Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, pydantic v2.
- Frontend: React + Vite + TS (Aurora Dark system from Part 1).
- DB: Postgres (Neon). Media: Cloudflare R2 (`MediaStore`).
- Payments: Razorpay (India) + Stripe (intl) — provider-hosted checkout only.
- GitHub: OAuth App + REST API for repo creation/Pages.
- AI eval: Part 1's M5 budget-capped evaluation infra (reused, not rebuilt).

## Hexagonal mapping

### Inbound ports (what the world may ask the core to do)

| Port | Responsibility |
|---|---|
| `BillingService` | create subscription, cancel, handle webhook events, resolve entitlements |
| `ResumeService` | generate JD-tailored ATS resume, list/download past resumes |
| `PortfolioService` | run builder steps, publish to GitHub, store existing-portfolio link |
| `HiringService` | start/grade typing & quant tests, run mock interviews (GD/PI/extempore/presentation), IELTS track sessions, issue challenges |
| `CertificateService` | issue, verify, revoke certificates |
| `AccountLinkService` | OAuth linking (Google/GitHub), share/export, LeetCode nudge |
| `TrendWatcherService` | flag emerging skills (admin), curate new domain intake |

### Outbound ports (what the core needs from the outside)

| Port | Adapters |
|---|---|
| `PaymentGateway` | `RazorpayAdapter`, `StripeAdapter`, `FakePaymentGateway` (tests) |
| `GitHubPublisher` | `GitHubApiAdapter` (repo create, file push, Pages enable), `FakeGitHubPublisher` (tests) |
| `ResumeRenderer` | `AtsPdfRenderer` (single-column PDF), `DocxRenderer` |
| `EmailSender` | `ResendAdapter` (receipts, mock reminders) |
| `MediaStore` | `R2MediaStore` (resume PDFs, certificates) |
| `AIEvalProvider` | reused from Part 1 (mock by default; OpenAI-compatible behind flag) |

### Adapter-swap examples (the "update anywhere" proof)

- Razorpay → Stripe: new `PaymentGateway` adapter, zero caller changes.
- GitHub Pages → Cloudflare Pages: new `GitHubPublisher`-style adapter.
- Real LLM → mock: config flag; domain core never knows.

## API endpoints (`/api/v1`, all auth'd; gated ones check entitlements)

- `POST /billing/checkout` → provider checkout session (test mode until KYC).
- `POST /billing/webhook/{provider}` → signature-verified event intake.
- `GET /billing/entitlements` → current user's feature matrix.
- `POST /resumes/from-jd` → JD in, tailored resume out (PDF/DOCX download).
- `GET/POST /portfolio/builder/steps`, `POST /portfolio/publish` →
  repo + Pages URL on the user's GitHub.
- `POST /hiring/mocks` → start mock (type: PI/GD/extempore/presentation/IELTS);
  `POST /hiring/mocks/{id}/complete` → dimension feedback.
- `POST /hiring/mocks/{id}/challenge` → human-review queue entry.
- `POST /hiring/typing|quant/attempts` → deterministic scoring.
- `POST /certificates/issue`, `GET /certificates/verify/{code}`.
- `POST /accounts/link/{provider}`, `POST /accounts/share`.

## Data model (new tables; migrations reversible)

- `subscriptions` (user_id, tier, provider, provider_sub_id, status,
  current_period_end) + `entitlements` (user_id, feature_key, quota, used).
- `billing_events` (webhook idempotency: provider_event_id UNIQUE, payload,
  signature_ok, applied_at).
- `resumes` (user_id, jd_hash, tailored_json, pdf_path, created_at).
- `portfolios` (user_id, builder_state JSON, repo_url, pages_url,
  existing_link separate nullable).
- `mock_sessions` (user_id, kind, consent_at, tab_switch_events JSON,
  feedback_json, challenged_at) — **no video column by design.**
- `certificates` (user_id, code UNIQUE, evidence_refs, issued_at, revoked_at).
- `trend_flags` (skill, signal_strength, source, status: flagged→curating→live).

## NFRs

- **Privacy:** camera consent modal before every proctored session (consent
  timestamp stored); frames processed in-memory/near-real-time; no video
  retained after session; M9 export/delete covers all Part 3 data.
- **PCI:** we never touch card data — provider-hosted checkout + webhooks
  only; webhook signatures verified with provider secret from env.
- **Reliability:** entitlement resolution is cached per request but
  recomputed on webhook events (no stale "paid but locked out").
- **Cost:** per-user quotas even on paid tiers (mock minutes, resume
  generations, AI eval tokens) — fair-use caps keep unit economics positive.
- **Audit:** every billing state change logged with request ID + provider
  event ID; admin-readable.
