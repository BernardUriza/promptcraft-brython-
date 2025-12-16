# PromptCraft - Configuration
# Using Pydantic Settings for type-safe config

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    PROJECT_NAME: str = "PromptCraft"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://promptcraft:promptcraft@localhost:5432/promptcraft"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Security
    SECRET_KEY: str = "change-this-in-production-min-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Gamification Settings
    XP_LESSON_COMPLETE: int = 50
    XP_PUZZLE_EASY: int = 30
    XP_PUZZLE_MEDIUM: int = 50
    XP_PUZZLE_HARD: int = 75
    XP_DAILY_GOAL: int = 20
    XP_STREAK_BONUS_MULTIPLIER: float = 0.1

    # Streak Settings
    STREAK_RESET_HOUR: int = 4  # 4 AM local time
    MAX_STREAK_FREEZES: int = 3
    STREAK_FREEZE_COST: int = 200  # XP cost


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
