from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from neo4j import GraphDatabase

from app.core.config import get_settings

settings = get_settings()

# PostgreSQL
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Neo4j
neo4j_driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

def get_db():
    """获取PostgreSQL数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_neo4j():
    """获取Neo4j数据库会话"""
    try:
        yield neo4j_driver.session()
    finally:
        pass  # 会话将在上下文管理器中自动关闭 