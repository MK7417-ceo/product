#!/bin/sh
# Production entrypoint: run DB migrations first (idempotent — a no-op
# when already at head), then start the server on Render's $PORT
# (default 8000 for local runs). Migrations are skipped when no
# DATABASE_URL is set (local sqlite dev flow).
set -e
if [ -n "$DATABASE_URL" ]; then
  ALEMBIC_DATABASE_URL="$DATABASE_URL" python -m alembic upgrade head
fi
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
