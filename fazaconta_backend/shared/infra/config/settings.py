from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )

    ENV: str = "development"

    # MongoDB Settings
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "fazaconta_db"

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # AWS S3 Settings
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"
    AWS_REGION: str = "eu-west-1"
    AWS_BUCKET_NAME: str = "fazaconta"
    AWS_S3_URL: str = "http://localhost:4566"
