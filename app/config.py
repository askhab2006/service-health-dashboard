from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    DEBUG: bool = False
    DEFAULT_CHECK_INTERVAL: int = 5
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[int] = None

    # Новый формат вместо class Config
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()