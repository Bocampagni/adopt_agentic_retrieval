from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

# Backend root = directory containing config/ (where pyproject.toml lives)
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _BACKEND_DIR.parent


class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = Field(description="OpenRouter API key")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", description="OpenRouter base URL")
    MODEL_TEMPERATURE: float = Field(default=0.7, description="Temperature for the model")

    model_config = {
        "env_file": ".env",
    }


# Single instance: use Settings.OPENROUTER_API_KEY etc. without ever calling Settings()
Config = Settings()  # type: ignore[call-arg]