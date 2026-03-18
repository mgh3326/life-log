from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "postgresql+asyncpg://mgh3326@localhost:5432/life_log"
    LOG_LEVEL: str = "INFO"
    MCP_AUTH_TOKEN: str = ""
    API_PORT: int = 8766  # auto_trader uses 8765


settings = Settings()
