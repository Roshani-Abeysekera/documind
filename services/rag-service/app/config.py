from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://documind:documind@localhost:5432/documind"
    embedding_model: str = "all-MiniLM-L6-v2"  # 384-dim, small and fast, no API key needed

settings = Settings()
