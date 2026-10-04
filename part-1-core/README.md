# Part 1 — SkillForge Core

FastAPI modular monolith. **Clean/Hexagonal:** `domain/` holds pure business
logic (no framework imports); `ports/` holds interfaces; `adapters/` holds
implementations; `api/` holds FastAPI routers (inbound adapters).

```
app/
  core/        # config, database, logging (infrastructure)
  domain/      # PURE logic — no FastAPI, no SQLAlchemy, no HTTP
  ports/       # inbound.py (what the world may ask) / outbound.py (what core needs)
  adapters/
    inbound/   # services implementing inbound ports
    outbound/  # DB probes, and later: repos, LLM clients, payment clients
  api/v1/      # FastAPI routers — call inbound ports only
```

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# GET /api/v1/health
```

## Test

```bash
pytest -q
```

Full dossier: `docs/part-1-core/`.
