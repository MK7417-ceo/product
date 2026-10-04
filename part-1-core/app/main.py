"""Application factory — the ONLY place where adapters get wired to ports."""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request

from app.adapters.inbound.auth_service import JwtAuthService
from app.adapters.inbound.health_service import SystemHealthService
from app.adapters.inbound.onboarding_service import OnboardingServiceImpl
from app.adapters.outbound.google_oauth import GoogleOAuthProvider
from app.adapters.outbound.profile_repository import (
    SqlAlchemyPlacementRepository,
    SqlAlchemyProfileRepository,
)
from app.adapters.outbound.question_bank import StaticQuestionBank
from app.adapters.outbound.security import BcryptPasswordHasher, DbTokenStore, JwtTokenIssuer
from app.adapters.outbound.system_probe import SqlAlchemyDatabaseProbe
from app.adapters.outbound.user_repository import SqlAlchemyUserRepository
from app.api.v1 import auth as auth_api
from app.api.v1 import health as health_api
from app.api.v1 import oauth as oauth_api
from app.api.v1 import onboarding as onboarding_api
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.logging import configure_logging

configure_logging()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # ---- hexagonal wiring: ports <- adapters ----
    db_probe = SqlAlchemyDatabaseProbe(SessionLocal)
    app.state.health_service = SystemHealthService(db_probe)

    users = SqlAlchemyUserRepository(SessionLocal)
    hasher = BcryptPasswordHasher()
    issuer = JwtTokenIssuer(
        secret=settings.SECRET_KEY,
        access_minutes=settings.ACCESS_TOKEN_MINUTES,
        refresh_days=settings.REFRESH_TOKEN_DAYS,
    )
    tokens = DbTokenStore(SessionLocal, refresh_days=settings.REFRESH_TOKEN_DAYS)
    app.state.auth_service = JwtAuthService(users, hasher, issuer, tokens)
    app.state.token_issuer = issuer  # for the auth dependency

    profiles = SqlAlchemyProfileRepository(SessionLocal)
    placements = SqlAlchemyPlacementRepository(SessionLocal)
    bank = StaticQuestionBank()
    app.state.onboarding_service = OnboardingServiceImpl(profiles, placements, bank)
    app.state.question_bank = bank
    app.state.oauth_provider = GoogleOAuthProvider(
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:12])
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    app.include_router(health_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(auth_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(oauth_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(onboarding_api.router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()
