from pydantic import BaseModel
import os

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    APP_ENV: str = os.getenv("APP_ENV", "local")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev")

settings = Settings()
