# Onboarding pages — integration guide (UX v2, Milestone 1)

Owner: ONBOARDING agent. Branch: `feat/ux-v2-onboarding`. All pages are
**default exports**; lazy-import them in the shell router. No page registers
itself in the sidebar — wizard steps/results are internal steppers/panels.

## Files

| File | Route | Purpose |
|---|---|---|
| `part-1-core/frontend/src/pages/onboarding/Welcome.tsx` | `/welcome` | Post-login resume nudge (Flow 1). Shows once. |
| `part-1-core/frontend/src/pages/onboarding/Resume.tsx` | `/resume` | JD matcher + guided resume builder (Flow 2). **Also mount as sidebar LAUNCH → Resume** (same component). |
| `part-1-core/frontend/src/pages/onboarding/Subscription.tsx` | `/subscription` | Free/Pro/Expert plans (Flow 1, step M). |
| `part-1-core/frontend/src/pages/onboarding/MakePlan.tsx` | `/plan` | Subject + level wizard → starts placement (Flow 3). |
| `part-1-core/frontend/src/pages/onboarding/Verification.tsx` | `/verification` | Placement test stepper + per-level results (Flow 3). |
| `part-1-core/frontend/src/pages/onboarding/lib.ts` | — | Shared types + localStorage contracts. |
| `part-1-core/frontend/src/pages/onboarding/onboarding.css` | — | UX v2 tokens + page styles, scoped under `.ob` (never touches shell styles). Imported by each page. |

Suggested router wiring (shell owns `main.tsx`):

```tsx
const Welcome = lazy(() => import('./pages/onboarding/Welcome'));
const Resume = lazy(() => import('./pages/onboarding/Resume'));
const Subscription = lazy(() => import('./pages/onboarding/Subscription'));
const MakePlan = lazy(() => import('./pages/onboarding/MakePlan'));
const Verification = lazy(() => import('./pages/onboarding/Verification'));
// inside the authenticated layout (or Welcome standalone — your call):
<Route path="welcome" element={<Welcome />} />
<Route path="resume" element={<Resume />} />        {/* also the LAUNCH → Resume sidebar entry */}
<Route path="subscription" element={<Subscription />} />
<Route path="plan" element={<MakePlan />} />
<Route path="verification" element={<Verification />} />
```

## Router-state contract: /verification

MakePlan navigates with `navigate('/verification', { state })`. Do not
deep-link to `/verification` — the page redirects to `/plan` when state is
absent (placement sessions are single-use; refresh loses the session by design).

```ts
interface VerificationState {
  placement_id: string;      // from POST /api/v1/placement/start
  topic: string;             // e.g. "python"
  claimed_level: string;     // "intermediate" | "advanced"
  questions: Array<{         // public questions — answer keys NEVER included
    id: string; topic: string; level: string;
    prompt: string; choices: string[];
  }>;
}
```

## localStorage contracts (shell must honor)

| Key | Values | Meaning |
|---|---|---|
| `sf_welcome_seen` | `"1"` | Set when the user clicks "Skip for now" on `/welcome`. The nudge shows exactly once; returning visits redirect to `/`. |
| `sf_plan` | `"pro"` \| `"expert"` \| absent | **DEMO SCAFFOLDING.** Shell's "Go Pro" popup + plan badge read this key: present → hide popup, show PRO/EXPERT badge. Absent → fall back to the backend subscription tier (`GET /api/v1/account/subscription`). |

## Demo-purchase scaffolding (remove when real checkout lands)

`Subscription.tsx` contains a clearly-labeled dashed "DEMO ONLY" panel with
**Simulate Pro purchase / Simulate Expert purchase / Reset to Free**. It only
writes `localStorage['sf_plan']` — no payment is faked, the backend tier is
untouched. The Upgrade buttons call the real `POST /api/v1/account/subscription/checkout`,
which returns **501** today; the UI shows an honest "Checkout coming soon —
we'll notify you" state. Delete the `.ob-demo` block when Razorpay/Stripe KYC
is done.

## Backend endpoints used (all verified live, Oct 13 2026)

- `GET /api/v1/launchpad/resume` → 404 `{error:"no_resume"}` when absent
- `PUT /api/v1/launchpad/resume` → `{title,summary,skills,experience[],projects[],education[],links{}}`
- `POST /api/v1/launchpad/jd-match` `{jd_text}` → `{score, jd_keyword_count, matched:[{keyword,jd_count}], missing:[...], suggestions:[...]}`
- `GET /api/v1/account/subscription` → `{subscription:{tier,name,price_inr,features}, tiers:{free,pro,expert}}` — prices rendered from this, never hardcoded (₹0 / ₹299 / ₹799 verified in `app/domain/billing.py`)
- `POST /api/v1/account/subscription/checkout` `{tier}` → **501** `{error:"payments_not_connected"}`
- `GET /api/v1/placement/topics` → `{topics:["ml-basics","python"]}`
- `POST /api/v1/placement/start` `{topic, claimed_level}` → `{placement_id, verification_skipped, verified_level, questions[], ...}`
- `POST /api/v1/placement/{id}/submit` `{answers:{qid:choiceIdx}}` → `{analysis:{claimed_level, verified_level, correct, total, summary, levels:{lvl:{correct,total,ratio}}}}`
- `GET /api/v1/roadmaps/current` → **400** `{detail:"no roadmap yet — generate one first"}` when none
- `POST /api/v1/roadmaps/generate` `{gaps:[{skill,mastery_pct}], title}` → 201

Gap mapping (Verification → "Generate my roadmap"): levels with ratio < 0.7 →
one gap `{skill: topic, mastery_pct: worst_ratio*100}`; if everything passed,
one gap for the *next* level `{skill: "<topic> (<next> track)", mastery_pct: 0}`.

## Design

- Tokens (exact var names, defined in `onboarding.css` under `.ob`): `--base #080B14`, `--surface #121A2B`, `--border rgba(255,255,255,.10)`, `--violet #8B5CF6`, `--cyan #36C5F0`, `--green #39D98A`, `--amber #F5B84B`, `--red #F06C75`, `--text #F5F7FB`, `--muted #9AA6BB`.
- **Green discipline:** green is used ONLY for the verified-level badge when a level beyond beginner was genuinely verified. ATS ring is violet→cyan; level bars are cyan/amber/red by ratio.
- All pages have loading / error / empty states. No mock data anywhere (demo purchase panel excepted, labeled).

## Verified

- `tsc -b` clean, `vite build` clean.
- Live-backend E2E via Playwright (real registered user, real tokens): register →
  /plan → topic+level → /verification (8 Qs, stepper, submit) → per-level results
  → /resume (seeded resume, JD paste → ATS 47 ring + matched/missing + suggestions)
  → /subscription (real tiers/prices, 501 checkout, demo-purchase sets `sf_plan=pro`
  and the Pro card flips to CURRENT) → /welcome nudge for a resume-less user.
- Screenshots: `~/workspace/your_files/skillforge-v2/output/ux-v2-{make-plan,verification,verification-result,resume-ats,subscription}.png`.

## Gaps / notes for the shell agent

- `src/App.tsx` does not exist in this worktree (routing lives in `main.tsx`); nothing outside `src/pages/onboarding/` + this file was touched. `vite.config.ts` proxy still targets `localhost:8000` (the standard backend port); the live test backend ran on `:8001` via a local TCP forward.
- `Welcome` works best as a full-page (no sidebar) route — your call in the router.
- If the shell shows a plan badge, read `localStorage['sf_plan']` first, backend tier second (demo override wins).
