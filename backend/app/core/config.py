from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
from functools import lru_cache


class Settings(BaseSettings):
    # 基本设置
    PROJECT_NAME: str = "Polaris Knowledge Graph"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS设置
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # PostgreSQL配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "polaris123"
    POSTGRES_DB: str = "polaris"
    POSTGRES_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Neo4j配置
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "your_password"
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: set[str] = {
        "pdf", "doc", "docx", "ppt", "pptx", 
        "txt", "md", "html", "htm"
    }

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings() 