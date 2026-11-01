from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SkillForge Core"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./skillforge.db"
    SECRET_KEY: str  # no default: fail fast, never ship a hardcoded key
    ACCESS_TOKEN_MINUTES: int = 30
    REFRESH_TOKEN_DAYS: int = 7
    # Google OAuth — empty until the operator configures them (F2/A2)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    CODE_ENGINE_URL: str = "http://localhost:8028"
    # AI/RAG (DB-first, API-on-miss). Keys are operator-supplied via env
    # only — never hardcoded, never committed. Empty key = the layer still
    # works from the DB + local RAG, with an honest fallback on a miss.
    AI_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    AI_DB_MIN_SCORE: float = 0.55
    AI_RAG_MIN_SCORE: float = 0.45
    # Password reset email (Resend). FROM_EMAIL is the PROJECT's address —
    # never a personal email. Empty RESEND_API_KEY = dev mode (no send).
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@skillforge.app"
    FRONTEND_URL: str = "http://localhost:5173"
    # Public origin where the SEO pages live, used ONLY for sitemap URLs.
    # Leave empty for same-origin deployments (falls back to the request
    # URL). Set it when the frontend and API are on different origins.
    PUBLIC_BASE_URL: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


try:
    settings = Settings()
except Exception as exc:
    raise RuntimeError(
        "SECRET_KEY is required. Set it in the environment or a .env file "
        "(e.g. SECRET_KEY=$(python -c 'import secrets;print(secrets.token_hex(32))'))."
    ) from exc
