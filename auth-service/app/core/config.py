from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SERVICE_PORT: int = 8001

    class Config:
        env_file = ".env"

settings = Settings()
