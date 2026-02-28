from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    AUTH_SERVICE_URL: str
    SERVICE_PORT: int = 8002

    class Config:
        env_file = ".env"

settings = Settings()
