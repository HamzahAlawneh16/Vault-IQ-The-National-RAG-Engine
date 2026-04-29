import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Leadership Principle: Operational Excellence.
    Centralized configuration management.
    """
    PROJECT_NAME: str = "National RAG System"
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = 6333
    EMBEDDING_MODEL_NAME: str = "paraphrase-multilingual-MiniLM-L12-v2"
    
    class Config:
        case_sensitive = True

settings = Settings()