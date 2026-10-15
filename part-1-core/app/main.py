"""Application factory — the ONLY place where adapters get wired to ports."""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request

from app.adapters.inbound.assessment_service import AssessmentServiceImpl
from app.adapters.inbound.auth_service import JwtAuthService
from app.adapters.inbound.health_service import SystemHealthService
from app.adapters.inbound.onboarding_service import OnboardingServiceImpl
from app.adapters.outbound.assessment_repository import SqlAlchemyAssessmentRepository
from app.adapters.inbound.evidence_service import EvidenceServiceImpl
from app.adapters.inbound.practice_service import PracticeServiceImpl
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
from app.adapters.inbound.streak_service import StreakServiceImpl
from app.adapters.inbound.weekly_test_service import WeeklyTestServiceImpl
from app.adapters.outbound.weekly_test_repository import SqlAlchemyWeeklyTestRepository
from app.adapters.outbound.streak_repository import SqlAlchemyStreakRepository
from app.adapters.inbound.coin_service import CoinServiceImpl
from app.adapters.outbound.coin_repository import SqlAlchemyCoinRepository
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
    app.state.content_service = ContentServiceImpl(
        SqlAlchemyContentRepository(SessionLocal))
    app.state.curriculum_service = CurriculumServiceImpl(
        SqlAlchemyCurriculumRepository(SessionLocal))
    app.state.streak_service = StreakServiceImpl(
        SqlAlchemyStreakRepository(SessionLocal))
    app.state.coin_service = CoinServiceImpl(
        SqlAlchemyCoinRepository(SessionLocal))
    app.state.weekly_test_service = WeeklyTestServiceImpl(
        SqlAlchemyWeeklyTestRepository(SessionLocal),
        SqlAlchemyCurriculumRepository(SessionLocal),
        app.state.coin_service)
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
    return app


app = create_app()
