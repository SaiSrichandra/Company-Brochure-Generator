from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General
    APP_NAME: str = "AI Brochure Generator"
    ENVIRONMENT: str = Field("development", description="Environment: dev, staging, prod")

    # OpenAI
    OPENAI_API_KEY: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # Frontend origin(s)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
