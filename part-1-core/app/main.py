"""Application factory — the ONLY place where adapters get wired to ports."""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from starlette.middleware.gzip import GZipMiddleware

from app.adapters.inbound.assessment_service import AssessmentServiceImpl
from app.adapters.inbound.auth_service import JwtAuthService
from app.adapters.inbound.health_service import SystemHealthService
from app.adapters.inbound.onboarding_service import OnboardingServiceImpl
from app.adapters.outbound.assessment_repository import SqlAlchemyAssessmentRepository
from app.adapters.inbound.evidence_service import EvidenceServiceImpl
from app.adapters.inbound.practice_service import PracticeServiceImpl
from app.adapters.inbound.search_service import SearchServiceImpl
from app.adapters.inbound.content_service import ContentServiceImpl
from app.adapters.outbound.content_repository import SqlAlchemyContentRepository
from app.adapters.inbound.curriculum_service import CurriculumServiceImpl
from app.adapters.outbound.curriculum_repository import SqlAlchemyCurriculumRepository
from app.adapters.inbound.roadmap_service import RoadmapServiceImpl
from app.adapters.outbound.google_oauth import GoogleOAuthProvider
from app.adapters.outbound.profile_repository import (
    SqlAlchemyPlacementRepository,
    SqlAlchemyProfileRepository,
)
from app.adapters.outbound.evidence_repository import SqlAlchemyEvidenceRepository
from app.adapters.outbound.roadmap_repository import SqlAlchemyRoadmapRepository
from app.adapters.outbound.search_repository import SqlAlchemySearchRepository
from app.adapters.outbound.code_runner_client import HttpCodeRunnerClient
from app.adapters.inbound.launchpad_service import LaunchpadServiceImpl
from app.adapters.outbound.resume_repository import SqlAlchemyResumeRepository
from app.adapters.outbound.certificate_repository import SqlAlchemyCertificateRepository
from app.adapters.outbound.user_repository import SqlAlchemyUserRepository
from app.adapters.outbound.question_bank import StaticQuestionBank
from app.adapters.outbound.security import BcryptPasswordHasher, DbTokenStore, JwtTokenIssuer
from app.adapters.outbound.system_probe import SqlAlchemyDatabaseProbe
from app.adapters.outbound.link_repository import SqlAlchemyAccountLinkRepository
from app.api.v1 import auth as auth_api
from app.api.v1 import assessments as assessments_api
from app.api.v1 import account as account_api
from app.api.v1 import code as code_api
from app.api.v1 import launchpad as launchpad_api
from app.api.v1 import prep as prep_api
from app.api.v1 import english as english_api
from app.api.v1 import health as health_api
from app.api.v1 import oauth as oauth_api
from app.api.v1 import onboarding as onboarding_api
from app.api.v1 import evidence as evidence_api
from app.api.v1 import practice as practice_api
from app.api.v1 import search as search_api
from app.api.v1 import roadmaps as roadmaps_api
from app.api.v1 import content as content_api
from app.api.v1 import curriculum as curriculum_api
from app.api.v1 import study_plans as study_plans_api
from app.api.v1 import streak as streak_api
from app.api.v1 import taxonomy as taxonomy_api
from app.api.v1 import coins as coins_api
from app.api.v1 import news as news_api
from app.api.v1 import placement as placement_api
from app.api.v1 import trends as trends_api
from app.api.v1 import weekly_tests as weekly_tests_api
from app.api.v1 import simulator as simulator_api
from app.api.v1 import seo as seo_api
from app.api.v1 import ai as ai_api
from app.adapters.inbound.ai_answer_service import (
    AiAnswerServiceImpl,
    GeminiProvider,
    NullProvider,
)
from app.adapters.outbound.ai_answer_repository import SqlAlchemyAiAnswerRepository
from app.api.v1 import battles as battles_api
from app.adapters.inbound.streak_service import StreakServiceImpl
from app.adapters.inbound.weekly_test_service import WeeklyTestServiceImpl
from app.adapters.outbound.weekly_test_repository import SqlAlchemyWeeklyTestRepository
from app.adapters.inbound.simulator_service import SimulatorServiceImpl
from app.adapters.outbound.simulator_repository import SqlAlchemySimulatorRepository
from app.adapters.inbound.password_reset_service import PasswordResetServiceImpl
from app.adapters.inbound.battle_service import BattleServiceImpl
from app.adapters.outbound.battle_repository import SqlAlchemyBattleRepository
from app.adapters.outbound.password_reset_repository import SqlAlchemyPasswordResetRepository
from app.adapters.outbound.email_service import send_password_reset_email
from app.adapters.outbound.streak_repository import SqlAlchemyStreakRepository
from app.adapters.inbound.coin_service import CoinServiceImpl
from app.adapters.outbound.coin_repository import SqlAlchemyCoinRepository
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.logging import configure_logging

configure_logging()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # Speed: gzip-compress API responses >= 500 bytes when the client
    # accepts gzip (Starlette built-in, no new dependency). Small responses
    # (e.g. /health) are sent uncompressed — compressing them would cost
    # more than it saves. Static frontend assets are NOT covered here;
    # they are compressed by the production host/CDN, not this API server.
    app.add_middleware(GZipMiddleware, minimum_size=500)

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
    app.state.user_repo = users
    app.state.links_repo = SqlAlchemyAccountLinkRepository(SessionLocal)

    profiles = SqlAlchemyProfileRepository(SessionLocal)
    placements = SqlAlchemyPlacementRepository(SessionLocal)
    bank = StaticQuestionBank()
    app.state.onboarding_service = OnboardingServiceImpl(profiles, placements, bank)
    app.state.question_bank = bank
    app.state.assessment_repo = SqlAlchemyAssessmentRepository(SessionLocal)
    app.state.assessment_service = AssessmentServiceImpl(
        app.state.assessment_repo, bank)
    app.state.practice_service = PracticeServiceImpl(
        bank, SqlAlchemyRoadmapRepository(SessionLocal))
    app.state.search_service = SearchServiceImpl(
        SqlAlchemySearchRepository(SessionLocal))
    app.state.content_service = ContentServiceImpl(
        SqlAlchemyContentRepository(SessionLocal))
    app.state.curriculum_service = CurriculumServiceImpl(
        SqlAlchemyCurriculumRepository(SessionLocal))
    app.state.streak_service = StreakServiceImpl(
        SqlAlchemyStreakRepository(SessionLocal))
    app.state.coin_service = CoinServiceImpl(
        SqlAlchemyCoinRepository(SessionLocal))
    app.state.battle_service = BattleServiceImpl(
        SqlAlchemyBattleRepository(SessionLocal), bank, users,
        app.state.coin_service)
    app.state.weekly_test_service = WeeklyTestServiceImpl(
        SqlAlchemyWeeklyTestRepository(SessionLocal),
        SqlAlchemyCurriculumRepository(SessionLocal),
        app.state.coin_service)
    app.state.simulator_service = SimulatorServiceImpl(
        SqlAlchemySimulatorRepository(SessionLocal),
        app.state.coin_service)
    if settings.GEMINI_API_KEY:
        _llm_provider = GeminiProvider(
            api_key=settings.GEMINI_API_KEY, model=settings.GEMINI_MODEL)
    else:
        _llm_provider = NullProvider()
    app.state.ai_answer_service = AiAnswerServiceImpl(
        SqlAlchemyAiAnswerRepository(SessionLocal),
        _llm_provider,
        db_min_score=settings.AI_DB_MIN_SCORE,
        rag_min_score=settings.AI_RAG_MIN_SCORE)
    app.state.password_reset_service = PasswordResetServiceImpl(
        users,
        SqlAlchemyPasswordResetRepository(SessionLocal),
        hasher,
        email_sender=send_password_reset_email)
    app.state.code_runner = HttpCodeRunnerClient(settings.CODE_ENGINE_URL)
    app.state.launchpad_service = LaunchpadServiceImpl(
        SqlAlchemyResumeRepository(SessionLocal),
        SqlAlchemyRoadmapRepository(SessionLocal),
        SqlAlchemyCertificateRepository(SessionLocal),
        SqlAlchemyUserRepository(SessionLocal),
        SqlAlchemyEvidenceRepository(SessionLocal))
    app.state.roadmap_service = RoadmapServiceImpl(
        SqlAlchemyRoadmapRepository(SessionLocal), users)
    app.state.evidence_service = EvidenceServiceImpl(
        SqlAlchemyEvidenceRepository(SessionLocal),
        SqlAlchemyRoadmapRepository(SessionLocal),
    )
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
    app.include_router(account_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(code_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(launchpad_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(prep_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(english_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(oauth_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(onboarding_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(assessments_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(roadmaps_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(practice_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(search_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(evidence_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(content_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(study_plans_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(curriculum_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(streak_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(taxonomy_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(coins_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(news_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(placement_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(trends_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(weekly_tests_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(simulator_api.router, prefix=settings.API_V1_PREFIX)
    # SEO endpoints live at the site root (no /api/v1 prefix): crawlers
    # expect /sitemap.xml and /robots.txt there. In production the
    # frontend origin must proxy these two paths to the backend.
    app.include_router(seo_api.router)
    app.include_router(ai_api.router, prefix=settings.API_V1_PREFIX)
    app.include_router(battles_api.router, prefix=settings.API_V1_PREFIX)

    # Production single-service mode: when the frontend has been built
    # into frontend/dist (Docker stage 1), serve it from the backend so
    # the whole app runs on one origin (no CORS/proxy setup). Local dev
    # without a build is unaffected (dist simply does not exist).
    # Registered LAST so every API/SEO/docs route above wins over it.
    from pathlib import Path

    from fastapi.responses import FileResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles

    _dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
    if _dist.is_dir():
        app.mount("/assets", StaticFiles(directory=_dist / "assets"), name="assets")

        @app.get("/{full_path:path}")
        async def _spa_fallback(full_path: str):
            if full_path.startswith("api/") or full_path.startswith("assets/"):
                return JSONResponse({"detail": "Not Found"}, status_code=404)
            candidate = _dist / full_path
            if full_path and candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(_dist / "index.html")

    return app


app = create_app()
