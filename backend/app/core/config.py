from pathlib import Path
from typing import List

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    project_name: str = "Multi-Agent AI Research Assistant"
    environment: str = "production"
    groq_api_key: str = ""
    groq_api_base: str = "https://api.groq.com/openai/v1"
    crewai_api_key: str = ""

    vector_store_path: Path = Path("./data/faiss_store")
    upload_folder: Path = Path("./data/uploads")

    allowed_origins: str = Field(
        default="https://ai-research-ebon.vercel.app,http://localhost:5173",
        description="Comma-separated list of allowed origins"
    )

    max_pdf_pages: int = 50
    model_name: str = "llama-3.3-70b-versatile"
    embeddings_model: str = "text-embedding-3-large"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

settings = Settings()
