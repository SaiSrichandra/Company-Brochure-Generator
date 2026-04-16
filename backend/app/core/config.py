from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General
    APP_NAME: str = "AI Brochure Generator"
    ENVIRONMENT: str = Field("development", description="Environment: dev, staging, prod")

    # OpenAI
    OPENAI_API_KEY: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]  # Frontend origin(s)

    # JWT
    SECRET_KEY: str = "change-this-to-a-random-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # SQLite DB path
    DATABASE_URL: str = "sqlite:///./brochure.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
