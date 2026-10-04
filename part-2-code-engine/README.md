# Part 2 — Code Execution Engine

**Status: planned, not built.** Full dossier: `docs/part-2-code-engine/`.

Sandbox code runner + in-browser editor UX + plagiarism check. Runs as a
**separate service on an isolated host** (security: untrusted code never
shares a host with user data).

```
# future layout (hexagonal, mirrors part-1-core)
app/
  domain/      # RunJob, RunResult, Verdict — pure
  ports/       # inbound: CodeRunnerService / outbound: ContainerRuntime, ResultStore
  adapters/    # Docker-backed ContainerRuntime, HTTP API
  api/v1/      # POST /v1/run, GET /v1/run/{id}
```

**Contract-first:** Part 1 Core consumes this service only through its
`CodeRunnerClient` outbound port. The HTTP API shape is agreed in P2.1 before
any sandbox is built; Core uses a mock adapter until Part 2 lands.
