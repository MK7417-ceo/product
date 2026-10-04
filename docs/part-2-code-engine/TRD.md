# Part 2 — Code Execution Engine: TRD

**Status:** DRAFT for review (2026-10-04). **Build state: NOT BUILT.**

## Tech stack

- **Service:** FastAPI (Python 3.12) on a dedicated runner host (small VPS with
  Docker; e.g. Hetzner/DigitalOcean $6–12/mo at MVP scale).
- **Sandbox:** Docker containers, one container per run, removed after the run.
  Images prebuilt per language with standard toolchains only:
  `python:3.12-slim`, `gcc:13` (C11/C++17), `openjdk:17-slim`.
- **Core (Part 1):** FastAPI modular monolith; consumes the runner ONLY through
  the `CodeRunnerClient` outbound port (swappable, mockable).
- **Editor UX:** React + Vite + TS in the Core frontend (Aurora Dark), calling
  Core's `/api/v1/coderun/*` routes, which forward through the port.

## Hexagonal mapping

**Domain core (pure Python, no FastAPI/Docker imports):**
- Entities: `RunJob` (id, language, code, stdin, limits, status), `RunResult`
  (stdout, stderr, exit_code, verdict, cpu_ms, peak_ram_mb, timed_out),
  `Verdict` enum (ACCEPTED, WRONG_ANSWER, TLE, MLE, RUNTIME_ERROR,
  COMPILE_ERROR, SYSTEM_ERROR), `SimilarityReport` (score, fingerprint_a/b,
  flagged, reasons).
- Use-cases: `execute_code`, `grade_against_cases`, `check_plagiarism`.

**Inbound port:** `CodeRunnerService.execute(job: RunJob) -> RunResult`
(implemented by the runner service itself; Core never calls Docker directly).

**Outbound ports:**
- `ContainerRuntime` — `start_container(image, limits)`, `exec_run(...)`,
  `kill_container`, `remove_container`. (Docker is one adapter; a local
  subprocess "fake" adapter exists for unit tests.)
- `ResultStore` — persist run metadata (stdout truncated) for audit/replay.

**Adapters:**
- Inbound: FastAPI routers (`POST /v1/run`, `POST /v1/jobs`, `GET /v1/run/{id}`,
  `POST /v1/plagiarism/check`).
- Outbound: `DockerContainerRuntime` (docker SDK), `PostgresResultStore`
  (or SQLite for local dev), `HttpCodeRunnerClient` (used by Core's port).

## API endpoints (v1, versioned)

| Method | Path | Purpose |
|---|---|---|
| POST | `/v1/run` | Sync execute: `{language, code, stdin, limits?}` → `RunResult` |
| POST | `/v1/jobs` | Async execute (long runs) → `{job_id}` |
| GET | `/v1/jobs/{job_id}` | Poll async job status/result |
| GET | `/v1/run/{id}` | Fetch a past run's result |
| POST | `/v1/grade` | Run code against N test cases → per-case verdicts |
| POST | `/v1/plagiarism/check` | `{code_a, code_b, language, exclude_starter?}` → `SimilarityReport` |
| GET | `/v1/languages` | Supported language matrix + versions |
| GET | `/v1/health` | Liveness + Docker daemon reachability |

All endpoints: `X-Request-ID` required/echoed; Core→runner calls carry an
internal service token (never user JWTs); runner never talks to Core's DB.

## Data model

- `runs`: id (uuid), language, code_hash (sha256, not raw code beyond
  retention window), stdin_hash, verdict, cpu_ms, peak_ram_mb, timed_out,
  stdout_truncated (≤64KB), stderr_truncated (≤16KB), request_id, created_at.
  Raw code retained 7 days for debugging, then purged (privacy).
- `plagiarism_checks`: id, code_hash_a/b, language, score, flagged,
  fingerprint_a/b, created_at, reviewer_decision (nullable).

## Resource limits (per run, enforced by Docker + supervisor)

| Resource | Limit | Enforcement |
|---|---|---|
| Network | **none** | `--network none` |
| Wall time | 10s default, 30s max | supervisor timeout → TLE |
| CPU | 1.0 vCPU | `--cpus 1` |
| RAM | 256MB default, 512MB max | `--memory` + OOM → MLE |
| Output (stdout+stderr) | 1MB | truncated, flagged |
| Disk writes | 64MB tmpfs | `--tmpfs` size cap |
| Processes | 64 pids | `--pids-limit 64` (fork-bomb containment) |
| Container lifetime | killed + removed after run | no reuse across runs |

## NFRs

- **Security (blocking):** no network, read-only rootfs where possible,
  non-root user in container, seccomp default profile, separate host from Core,
  service-to-service token; any escape = release-stopper.
- **Timeouts:** API gateway 35s on sync `/v1/run`; async jobs for anything
  longer; queue depth bounded (429 when full).
- **Rate limits:** per-user 60 runs/hour default (configurable); per-IP burst cap.
- **Observability:** structured logs with request_id; metrics: runs/s, p50/p95
  latency, verdict histogram, OOM/TLE counts, plagiarism flag rate.
- **Budgets:** target ≤ $0.0004/run infra at MVP scale; monthly budget alert +
  kill switch (pause new runs, drain queue).
