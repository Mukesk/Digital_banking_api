from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    AUTH_SERVICE_URL: str
    ACCOUNT_SERVICE_URL: str
    REDIS_URL: str
    RABBITMQ_URL: str
    SERVICE_PORT: int = 8003

    class Config:
        env_file = ".env"

settings = Settings()
