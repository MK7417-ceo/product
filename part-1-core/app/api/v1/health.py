"""Inbound adapter (HTTP): FastAPI router. Calls the inbound port only."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health(request: Request):
    service = request.app.state.health_service  # HealthService port
    status = service.get_status()
    content = {
        "ok": status.ok,
        "summary": status.summary(),
        "components": [
            {"name": c.name, "ok": c.ok, "detail": c.detail} for c in status.components
        ],
    }
    return JSONResponse(status_code=200 if status.ok else 503, content=content)
