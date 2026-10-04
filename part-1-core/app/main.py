"""Application factory — the ONLY place where adapters get wired to ports."""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request

from app.adapters.inbound.health_service import SystemHealthService
from app.adapters.outbound.system_probe import SqlAlchemyDatabaseProbe
from app.api.v1 import health as health_api
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.logging import configure_logging

configure_logging()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # ---- hexagonal wiring: ports <- adapters ----
    db_probe = SqlAlchemyDatabaseProbe(SessionLocal)
    app.state.health_service = SystemHealthService(db_probe)

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:12])
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    app.include_router(health_api.router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()
