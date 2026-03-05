"""Application configuration loaded from environment variables."""

import json
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file or environment variables."""

    APP_NAME: str = "Philo Coffee Shop"
    DATABASE_URL: str = "sqlite:///./data/philo_coffee.db"
    TAX_RATE: float = 0.08
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:5173"]'
    LOW_STOCK_THRESHOLD: int = 10

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from JSON string."""
        try:
            return json.loads(self.CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return ["*"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
