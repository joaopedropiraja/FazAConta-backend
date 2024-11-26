from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )

    # MongoDB Settings
    mongo_uri: str = Field(default="mongodb://my_mongo_host:27017")
    database_name: str = Field(default="fazaconta_db")

    # Redis Settings
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
