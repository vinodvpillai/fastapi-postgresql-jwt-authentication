from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

import os

class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    POSTGRES_SCHEMA: str
    
    DATABASE_URL: str
    
    CLIENT_ORIGIN: list
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"
    SECRET_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # type: ignore