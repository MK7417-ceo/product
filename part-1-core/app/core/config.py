from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SkillForge Core"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./skillforge.db"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
