from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    RABBITMQ_URL: str
    ACCOUNT_SERVICE_URL: str
    LOAN_SERVICE_URL: str
    SERVICE_PORT: int = 8005

    class Config:
        env_file = ".env"

settings = Settings()
