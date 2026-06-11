import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "ANTIGRAVITY Backend Civilization"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    KINGDOM_ENVIRONMENT: str = "development"

    # Databases
    # Defaults are oriented around docker compose container names
    DATABASE_URL: str = "postgresql+asyncpg://king:kingdom_auth_key@localhost:5432/antigravity_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    QDRANT_URL: str = "http://localhost:6333"
    NEO4J_URL: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "kingdom_auth_key"

    # AI Models
    OPENAI_API_KEY: str = "mock-key"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    PRIMARY_LLM_MODEL: str = "gpt-4o-mini"

    # Encryption
    ENCRYPTION_KEY: str = "a-very-secure-random-32-byte-key-here-for-aes-encryption"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
