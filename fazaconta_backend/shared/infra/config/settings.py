from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )

    # MongoDB Settings
    mongo_uri: str = "mongodb://localhost:27017"
    database_name: str = "fazaconta_db"

    # Redis Settings
    redis_host: str = "localhost"
    redis_port: int = 6379
