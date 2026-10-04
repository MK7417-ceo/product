# SKILLFORGE v2 — Feature Inventory

Every feature = one working logic of the application. For each: the hexagonal
flow (inbound port → domain → outbound ports → adapters) and the build phase.
Phases: **F0** foundation ✅ done · **F1** auth · **F2** OAuth+onboarding ·
**B** question bank · **D** tracks/practice · **P2.1–P2.4** code engine ·
**P3.1–P3.5** launchpad.

Conventions used below: `Svc` = inbound port (service interface),
`Repo`/`*Provider`/`*Client` = outbound ports, adapters in brackets.

---

## Part 1 — Core

### Auth & Authorization

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-001 | Register with email/password | `AuthSvc.register` → domain validates → `PasswordHasher.hash` → `UserRepo.save` → `TokenIssuer.issue` | F1 |
| F1-002 | Login | `AuthSvc.login` → `UserRepo.find_by_email` → `PasswordHasher.verify` → `TokenIssuer.issue` (access+refresh) | F1 |
| F1-003 | Logout | `AuthSvc.logout` → revoke refresh token in `TokenStore` | F1 |
| F1-004 | Refresh token rotation | `AuthSvc.refresh` → validate old → `TokenIssuer.issue` new pair → revoke old (rotation, reuse = theft signal) | F1 |
| F1-005 | Get current user | Router reads JWT → `AuthSvc.me` → `UserRepo.get` (no password hash leaves the core) | F1 |
| F1-006 | Google OAuth login | `OAuthProvider.exchange_code` (Google adapter) → link-or-create user → `TokenIssuer.issue` | F2 |
| F1-007 | Assign role (admin) | `AuthSvc.set_role` → admin-only guard → `UserRepo.update_role` | F1 |
| F1-008 | Export account data | `UserSvc.export` → aggregate via repos → JSON without secrets | F1 |
| F1-009 | Delete account | `UserSvc.delete` → cascade via `UserRepo.delete_cascade` | F1 |
| F1-010 | RBAC guard | Router dependency → `AuthSvc.authorize(user, required_role)` → 403 or pass | F1 |

### Users & Profiles

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-011 | Resume-style registration | `UserSvc.complete_profile` → store education/experience/skills/targets; levels NEVER derived from form | F2 |
| F1-012 | Update profile | `UserSvc.update_profile` → `UserRepo.update` (owner only) | F2 |
| F1-013 | Link existing portfolio URL | `UserSvc.set_portfolio_link` → stored as-is, kept separate | F2 |
| F1-014 | View skill profile | `ProfileSvc.get` → verified evidence only → levels + plain-language explanations | F1 |
| F1-015 | List ranked skill gaps | `GapSvc.ranked_gaps` → priority + one-line reasons | F1 |
| F1-016 | Recompute profile after grading | Scoring emits event → `ProfileSvc.recompute` (never from self-report) | F1 |

### Skill Graph

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-017 | Define skill | `SkillGraphSvc.add_skill` → `SkillRepo.save` | F1 |
| F1-018 | Add prerequisite edge | `SkillGraphSvc.add_edge` → cycle check in domain → `SkillRepo.save_edge` | F1 |
| F1-019 | Version skill graph | `SeedSvc.snapshot` → `seed_versions` row | F1 |
| F1-020 | Idempotent seeding | `SeedSvc.seed_all` → skip if version present | F1 |

### Question Bank

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-021 | Ingest curated question (user links) | `QuestionSvc.ingest` → normalize → level/domain tag → paraphrase → `QuestionRepo.save` | B |
| F1-022 | AI-generate question | `QuestionGenProvider.generate` → validation pipeline → save or quarantine | B |
| F1-023 | Validate generated question | Domain: schema check → answer-key check → business rules → confidence gate | B |
| F1-024 | Report bad question | `QuestionSvc.report` → `ReviewQueue.add` | B |
| F1-025 | Compose hybrid set | `AssessmentComposer.compose` → X% AI-fresh + Y% curated → set-hash ensures no identical repeat | B |
| F1-026 | Tag question level/domain | `QuestionSvc.tag` → `QuestionRepo.update_tags` | B |
| F1-027 | Version question bank | `SeedSvc.snapshot` (bank version stamped on every session) | B |

### Assessments

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-028 | Start onboarding diagnostic (≤15 min) | `AssessmentSvc.start_diagnostic` → level-spread set → session | F2 |
| F1-029 | Start assessment | `AssessmentSvc.start` → `AssessmentComposer.compose` → session (idempotent) | F1 |
| F1-030 | Submit answers (idempotent) | `AssessmentSvc.submit` → `idempotency_key` dedupe → `ScoringSvc.score` | F1 |
| F1-031 | Deterministic scoring | Domain: MCQ/numeric/code-test scoring, no LLM | F1 |
| F1-032 | AI evaluation (short reasoning) | `AIEvalProvider.evaluate` → budget cap → cache by request-hash → schema+rule validation | F1 |
| F1-033 | Human review queue | confidence < 0.75 → `ReviewQueue.add` | F1 |
| F1-034 | Resolve review (reviewer) | `ReviewSvc.resolve` → reviewer role + never-own-items → apply result | F1 |
| F1-035 | Session lifecycle | Domain state machine: in_progress → completed (graded) | F1 |
| F1-036 | Placement/verification flow | Declare level per topic → `AssessmentSvc.verify` → per-topic questions → real-level report (exposes false "expert") | F2 |
| F1-037 | Get questions (keys hidden) | `AssessmentSvc.questions_for` → strips answer keys/rubrics | F1 |

### Evidence

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-038 | Create verified evidence | Domain rule: server-evaluated + score ≥ 70% + trusted method → `EvidenceRepo.save(verified)` | F1 |
| F1-039 | List evidence | `EvidenceSvc.list` → owner-scoped | F1 |

### Roadmaps

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-040 | Generate roadmap | `RoadmapSvc.generate` → dependency-aware ordering from gaps + graph | F1 |
| F1-041 | Version roadmaps | Every generation → new version row, history kept | F1 |
| F1-042 | Regenerate preserving history | `RoadmapSvc.regenerate` → reorder/change tasks, never delete completed/evidence | F1 |
| F1-043 | Start/complete roadmap task | `TaskSvc.transition` → state machine with acceptance criteria | D |
| F1-044 | Submit task evidence | `EvidenceSvc.submit_for_task` → links to F1-038 rule | D |

### Learning & Practice

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-045 | Enroll in domain track | `TrackSvc.enroll` → beginner→expert→job path | D |
| F1-046 | Track progress | `TrackSvc.progress` → completed tasks / total | D |
| F1-047 | Daily questions (2–5 + explanations) | `PracticeSvc.daily_set` → level-matched, pattern-weighted | D |
| F1-048 | Schedule weekly mocks | `MockSvc.schedule` → 1 compulsory + 1 optional/week | D |
| F1-049 | Take mock (camera notice+consent) | `MockSvc.start` → consent gate → session | D |
| F1-050 | Streak counting | `PracticeSvc.streak` → consecutive active days | D |
| F1-051 | GitHub workflow tutorials | `TutorialSvc.list/complete` → init/commit/push/PR lessons | D |
| F1-052 | Reassessment prompts | `PracticeSvc.due_for_reassessment` → nudge when stale | D |

### Cross-cutting (Part 1)

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F1-053 | Entitlement check (stub) | `EntitlementChecker.allow_all` → replaced by Part 3 adapter later | F1 |
| F1-054 | Health check | `HealthSvc.get_status` → `DatabaseProbe.check` → 200/503 | F0 ✅ |
| F1-055 | Request-ID tracing | Middleware → `X-Request-ID` → attached to logs | F0 ✅ |

---

## Part 2 — Code Engine (separate service)

### Execution

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F2-001 | Submit run job | `CodeRunnerSvc.execute` → validate → `ContainerRuntime.spawn` → job id | P2.1 |
| F2-002 | Run Python | `ContainerRuntime.spawn(image=python, ...)` | P2.1 |
| F2-003 | Run C (gcc) | toolchain adapter per language | P2.2 |
| F2-004 | Run C++ (g++) | toolchain adapter per language | P2.2 |
| F2-005 | Run Java | toolchain adapter per language | P2.2 |
| F2-006 | Poll job status | `CodeRunnerSvc.status` → `ResultStore.get` | P2.1 |
| F2-007 | Cancel job | `CodeRunnerSvc.cancel` → `ContainerRuntime.kill` | P2.2 |
| F2-008 | Enforce CPU limit | `ContainerRuntime.spawn(cpu_quota=…)` → kill on exceed | P2.1 |
| F2-009 | Enforce RAM limit | cgroup memory cap → OOM verdict | P2.1 |
| F2-010 | Enforce wall-time limit | watchdog → timeout verdict | P2.1 |
| F2-011 | Enforce output limit | byte cap → truncated verdict | P2.1 |
| F2-012 | Block network egress | container `network_mode: none` → exfil impossible | P2.1 |
| F2-013 | Grade against test cases | Domain: run × cases → pass/fail → verdict | P2.2 |

### Plagiarism

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F2-014 | Normalize code | Domain: strip comments/whitespace → canonicalize identifiers | P2.3 |
| F2-015 | Structural fingerprint | Domain: AST-ish token shape hash (syntax shared, structure compared) | P2.3 |
| F2-016 | Pairwise similarity score | `PlagiarismSvc.compare` → fingerprint distance → score | P2.3 |
| F2-017 | Flag for human review | score ≥ threshold → `ReviewQueue.add`; NEVER auto-punish (domain rule) | P2.3 |

### Editor UX

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F2-018 | Run with stdin | Editor → `CodeRunnerSvc.execute(code, stdin)` → output panel | P2.4 |
| F2-019 | Output/error render | Adapter formats stdout/stderr/verdict for UI | P2.4 |
| F2-020 | Mobile editor layout | Frontend: 360px-first editor (no backend change) | P2.4 |

---

## Part 3 — Career Launchpad (monolith modules)

### Billing & Subscriptions

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F3-001 | View tiers | `BillingSvc.tiers` → Free ₹0 / Pro ₹249 / Expert ₹599 + quotas | P3.1 |
| F3-002 | Start checkout | `PaymentGateway.create_order` (Razorpay/Stripe adapter, hosted page — we never touch cards) | P3.1 |
| F3-003 | Handle payment webhook | Router → verify signature → `BillingSvc.activate` → idempotent | P3.1 |
| F3-004 | Check entitlement | `EntitlementChecker.for(user, feature)` → tier+quota → allow/deny | P3.1 |
| F3-005 | View subscription status | `BillingSvc.status` → plan, renew date, usage | P3.1 |
| F3-006 | Cancel subscription | `BillingSvc.cancel` → `PaymentGateway.cancel` → downgrade at period end | P3.1 |

### Resume

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F3-007 | Resume builder form | `ResumeSvc.build` → sections; confidential fields → placeholders | P3.2 |
| F3-008 | Paste JD → keyword alignment | `ResumeSvc.tailor_for_jd` → extract JD keywords → map to user evidence | P3.2 |
| F3-009 | Render ATS resume | `ResumeRenderer.render` → single-column, standard fonts, no graphics | P3.2 |
| F3-010 | Download resume | Adapter → PDF/file download | P3.2 |

### Portfolio

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F3-011 | Guided builder (7 steps, ~1 week) | `PortfolioSvc.guide` → template → about → skills → projects → contact → review → publish | P3.3 |
| F3-012 | Import verified skills/projects | `PortfolioSvc.import_verified` → pulls Part 1 verified evidence (never self-report) | P3.3 |
| F3-013 | Publish to user's GitHub | `GitHubPublisher.publish` → OAuth → create repo → push static site → enable Pages | P3.3 |
| F3-014 | Save existing portfolio link | `UserSvc.set_portfolio_link` → stored separate, never mixed | P3.3 |

### Hiring Prep

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F3-015 | Typing test | `HiringSvc.typing_test` → WPM/accuracy | P3.4 |
| F3-016 | Quant/aptitude test | `HiringSvc.quant_test` → timed sets | P3.4 |
| F3-017 | Presentation module | `HiringSvc.presentation` → prompt + AI feedback | P3.4 |
| F3-018 | Extempore | `HiringSvc.extempore` → random topic + timer | P3.4 |
| F3-019 | Group discussion | `HiringSvc.group_discussion` → prompt + rubric | P3.4 |
| F3-020 | PI mock (camera) | `HiringSvc.pi_mock` → consent gate → camera+tab-switch flags → session | P3.4 |
| F3-021 | IELTS track test | `HiringSvc.ielts_test` → band-mapped sections | P3.4 |
| F3-022 | AI feedback (4 dimensions) | `FeedbackSvc.score` → knowledge/confidence-proxy/expression/timing + confidence | P3.4 |
| F3-023 | Challenge feedback | `FeedbackSvc.challenge` → low-confidence/high-impact → human review | P3.4 |

### Accounts, Certificates, Trends

| ID | Feature | How it works (hexagonal) | Phase |
|---|---|---|---|
| F3-024 | Link GitHub/LinkedIn/LeetCode | `AccountLinkSvc.link` → OAuth where supported | P3.5 |
| F3-025 | One-click share/export | `ShareSvc.export` → achievements payload | P3.5 |
| F3-026 | LeetCode deep-link nudge | After solve → "paste on problem #N" + deep link (no fake auto-sync) | P3.5 |
| F3-027 | Issue certificate | `CertificateSvc.issue` → completion rules → signed record | P3.5 |
| F3-028 | List certificates | `CertificateSvc.list` → owner-scoped | P3.5 |
| F3-029 | Trend flag emerging skill | `TrendWatcher.scan` → job-posting signals → `trend_flags` | P3.5 |
| F3-030 | Admin curate domain | `TrendWatcher.promote` → human approves → skill graph + seed questions + track | P3.5 |

---

**Total: 55 + 20 + 30 = 105 features.** Each maps to exactly one phase;
no phase starts until its PLAN section is approved; no feature is done until
Agent lane + Developer lane both pass.
