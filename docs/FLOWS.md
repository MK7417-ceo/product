# SKILLFORGE v2 — Flow Diagrams (Mermaid)

Paste-ready Mermaid. GitHub renders these as visuals automatically.
Brainstorming set: review each flow, then we lock it before coding.

---

## 1. System overview — the 3 parts and how they talk

```mermaid
flowchart LR
    U[User browser] --> FE[Aurora Dark Frontend]

    subgraph P1 [Part 1 — Core · FastAPI monolith]
        API1[/api/v1]
        PORTS1[Inbound ports]
        DOM1[Domain core]
        OUT1[Outbound ports]
        API1 --> PORTS1 --> DOM1 --> OUT1
    end

    subgraph P2 [Part 2 — Code Engine · separate host]
        API2[Runner API]
        DOCK[Docker sandbox<br/>no network · CPU/RAM/time caps]
        API2 --> DOCK
    end

    subgraph P3 [Part 3 — Launchpad · monolith modules]
        BILL[Billing]
        RES[Resume]
        PORT[Portfolio]
        HIRE[Hiring prep]
    end

    FE --> API1
    OUT1 -->|CodeRunnerClient port| API2
    API1 --> BILL & RES & PORT & HIRE
    OUT1 --> DB[(Postgres)]
    OUT1 --> LLM[LLM provider<br/>budget-capped]
    PORT -->|GitHubPublisher port| GH[(User's GitHub<br/>repo + Pages)]
    BILL -->|PaymentGateway port| PAY[Razorpay / Stripe]

    style P2 fill:#1a0f0f,stroke:#f87171
```

> The red box is deliberate: Part 2 is the only part that touches untrusted
> code, so it lives on an isolated host. Everything else talks through ports.

---

## 2. Hexagonal anatomy — one feature, the full path

```mermaid
flowchart TD
    subgraph Outside
        HTTP[HTTP request]
        EXT[External service]
    end
    subgraph Hexagon[Application hexagon]
        IP[Inbound port<br/>e.g. AuthSvc.register]
        DOM[Domain core<br/>pure logic, no frameworks]
        OP[Outbound port<br/>e.g. UserRepo]
    end
    subgraph Adapters
        RTR[FastAPI router]
        SQL[SQLAlchemy repo]
        CLI[HTTP client]
    end

    HTTP --> RTR --> IP --> DOM --> OP
    OP --> SQL
    OP --> CLI --> EXT

    note[Rules<br/>• Router calls ports, never domain internals<br/>• Domain calls ports, never adapters<br/>• Swap adapter = zero caller changes]
```

---

## 3. Request lifecycle — F1-001 Register (sequence)

```mermaid
sequenceDiagram
    participant U as User
    participant R as Router<br/>(inbound adapter)
    participant S as AuthSvc<br/>(inbound port)
    participant D as Domain
    participant H as PasswordHasher<br/>(outbound port)
    participant UR as UserRepo<br/>(outbound port)
    participant T as TokenIssuer<br/>(outbound port)

    U->>R: POST /api/v1/auth/register {email, password}
    R->>S: register(email, password)
    S->>D: validate(email, password)
    D-->>S: ok
    S->>H: hash(password)
    H-->>S: hash
    S->>UR: save(user)
    UR-->>S: user id
    S->>T: issue(user)
    T-->>S: access + refresh
    S-->>R: {user, tokens}
    R-->>U: 201 + X-Request-ID
```

---

## 4. Auth flows — F1-002 login · F1-004 refresh · F1-003 logout

```mermaid
sequenceDiagram
    participant U as User
    participant S as AuthSvc
    participant UR as UserRepo
    participant H as PasswordHasher
    participant T as TokenIssuer
    participant TS as TokenStore

    Note over U,TS: LOGIN (F1-002)
    U->>S: login(email, password)
    S->>UR: find_by_email(email)
    S->>H: verify(password, hash)
    S->>T: issue(user)
    S->>TS: store(refresh)
    S-->>U: access + refresh

    Note over U,TS: REFRESH ROTATION (F1-004)
    U->>S: refresh(old_refresh)
    S->>TS: validate(old_refresh)
    S->>T: issue(user)
    S->>TS: revoke(old) + store(new)
    S-->>U: new access + new refresh

    Note over U,TS: LOGOUT (F1-003)
    U->>S: logout(refresh)
    S->>TS: revoke(refresh)
    S-->>U: 204
```

---

## 5. Assessment submit → scoring → verified evidence (F1-030 → F1-031/032 → F1-038)

```mermaid
sequenceDiagram
    participant U as User
    participant S as AssessmentSvc
    participant SC as ScoringSvc
    participant AI as AIEvalProvider<br/>(budget-capped)
    participant Q as ReviewQueue
    participant E as EvidenceSvc

    U->>S: submit(session_id, answers, idempotency_key)
    S->>S: dedupe by idempotency_key
    S->>SC: score(answers)
    SC->>SC: deterministic: MCQ/numeric/code-tests
    SC->>AI: evaluate(short_reasoning)
    AI-->>SC: {score, confidence, quotes}
    alt confidence >= 0.75
        SC-->>S: graded
    else confidence < 0.75
        SC->>Q: add(session) → human review (F1-033)
    end
    S->>E: maybe_create_evidence(result)
    Note over E: domain rule: server-evaluated<br/>+ score ≥ 70% + trusted method<br/>→ verified, else nothing
    E-->>U: result + verified evidence
```

---

## 6. Placement / verification flow (F1-036)

```mermaid
flowchart TD
    A[User picks WHAT to learn<br/>language or domain] --> B[Self-declares level per topic<br/>beginner / intermediate / expert]
    B --> C{AssessmentSvc.verify}
    C --> D[Per-topic questions:<br/>theory + subjective + coding]
    D --> E[Score per topic<br/>from answers only]
    E --> F{Claimed vs measured}
    F -->|match| G[Confirm level]
    F -->|inflated| H[Expose gap:<br/>claimed expert → measured beginner]
    G & H --> I[Real-level report<br/>drives roadmap]
```

---

## 7. Code run — Core → Part 2 (F2-001 → F2-013)

```mermaid
sequenceDiagram
    participant FE as Frontend editor
    participant C as Core API
    participant P as CodeRunnerClient<br/>(outbound port)
    participant R as Part 2 Runner API
    participant D as Docker sandbox<br/>no network

    FE->>C: POST /api/v1/practice/run {code, lang, stdin}
    C->>P: execute(job)
    P->>R: POST /v1/run {code, lang, limits}
    R->>D: spawn container<br/>cpu/ram/time/output caps
    D-->>R: stdout / stderr / verdict<br/>(timeout · OOM · ok)
    R-->>P: RunResult
    P-->>C: RunResult
    C-->>FE: output + verdict

    Note over D: fork bomb, exfil, disk-fill<br/>all contained by design (F2-008..012)
```

---

## 8. Plagiarism pipeline (F2-014 → F2-017)

```mermaid
flowchart LR
    A[Submitted code] --> B[Normalize<br/>strip comments/whitespace<br/>canonicalize identifiers]
    B --> C[Fingerprint<br/>structural shape hash<br/>not shared syntax]
    C --> D[Pairwise compare<br/>fingerprint distance]
    D --> E{score ≥ threshold?}
    E -->|yes| F[Flag → human review<br/>NEVER auto-punish]
    E -->|no| G[Clear]
```

---

## 9. Checkout + webhook → entitlements (F3-002 → F3-004)

```mermaid
sequenceDiagram
    participant U as User
    participant B as BillingSvc
    participant G as PaymentGateway<br/>(Razorpay/Stripe adapter)
    participant W as Webhook router

    U->>B: choose plan (Pro ₹249)
    B->>G: create_order(amount, plan)
    G-->>U: hosted checkout (we never touch cards)
    U->>G: pay
    G->>W: webhook {order, payment, signature}
    W->>W: verify signature (reject on mismatch)
    W->>B: activate(user, plan) — idempotent
    B-->>U: Pro active

    Note over U,B: every gated feature calls<br/>EntitlementChecker.for(user, feature)
```

---

## 10. Portfolio publish to user's GitHub (F3-013)

```mermaid
sequenceDiagram
    participant U as User
    participant P as PortfolioSvc
    participant GH as GitHubPublisher<br/>(outbound port)
    participant API as GitHub API

    U->>P: publish (after 7-step builder)
    P->>P: import verified skills + projects<br/>(Part 1 evidence — never self-report)
    P->>GH: publish(site_files)
    GH->>API: OAuth → create repo<br/>(e.g. user.github.io)
    GH->>API: push static site files
    GH->>API: enable Pages
    API-->>U: live URL — user owns repo,<br/>can git pull anytime
```

---

## 11. PI mock with camera + AI feedback (F3-020 → F3-023)

```mermaid
sequenceDiagram
    participant U as User
    participant H as HiringSvc
    participant F as FeedbackSvc
    participant Q as ReviewQueue

    U->>H: start PI mock
    H->>U: consent screen (camera ON, no long retention)
    U->>H: consent
    H->>H: session + tab-switch flags
    H->>F: score(transcript)
    F-->>H: knowledge / confidence-proxy /<br/>expression / timing + confidence
    alt confidence < 0.75 and high-impact
        F->>Q: human review
    end
    H-->>U: feedback (labeled as feedback,<br/>not objective truth)
    U->>H: challenge result?
    H->>Q: re-queue for human
```

---

## 12. Feature mindmap — all 105 features at a glance

```mermaid
mindmap
  root((SKILLFORGE v2<br/>105 features))
    Part 1 — Core
      Auth & RBAC
        F1-001 register
        F1-002 login
        F1-003 logout
        F1-004 refresh rotation
        F1-005 me
        F1-006 Google OAuth
        F1-007 roles
        F1-008 export
        F1-009 delete
        F1-010 guards
      Profiles & Gaps
        F1-011 resume registration
        F1-014 verified profile
        F1-015 ranked gaps
      Skill graph
        F1-017 skills
        F1-018 edges
        F1-019 versioning
      Questions
        F1-021 curated ingest
        F1-022 AI generation
        F1-023 validation
        F1-025 hybrid composer
      Assessments
        F1-028 diagnostic
        F1-030 idempotent submit
        F1-031 deterministic scoring
        F1-032 AI eval
        F1-033 review queue
        F1-036 placement verify
      Evidence
        F1-038 verified rule
      Roadmaps
        F1-040 generate
        F1-042 regenerate safe
      Practice
        F1-045 tracks
        F1-047 daily Qs
        F1-048 weekly mocks
        F1-050 streaks
    Part 2 — Code Engine
      Execution
        F2-001 submit job
        F2-002..005 languages
        F2-008..012 limits + no-net
        F2-013 grading
      Plagiarism
        F2-014 normalize
        F2-015 fingerprint
        F2-017 flag-only
      Editor
        F2-018 stdin run
        F2-020 mobile
    Part 3 — Launchpad
      Billing
        F3-001 tiers
        F3-002 checkout
        F3-003 webhook
        F3-004 entitlements
      Resume
        F3-007 builder
        F3-008 JD tailor
        F3-009 ATS render
      Portfolio
        F3-011 7-step builder
        F3-013 GitHub publish
      Hiring
        F3-015 typing
        F3-016 quant
        F3-017..019 presentation/extempore/GD
        F3-020 PI camera mock
        F3-021 IELTS
        F3-022 AI feedback
      Growth
        F3-024 account links
        F3-026 LeetCode nudge
        F3-027 certificates
        F3-029 trend flags
```

---

## How to use this for brainstorming

1. Read a diagram, trace the arrows, ask "what breaks if X fails?" — every
   answer becomes an edge case in `SPECS.md` and a test in `TESTING.md`.
2. Challenge each port: "could we swap this adapter?" — if not, the boundary
   is wrong.
3. When a flow is agreed, its phase in `FEATURE_INVENTORY.md` is locked and
   the PLAN gate opens.
