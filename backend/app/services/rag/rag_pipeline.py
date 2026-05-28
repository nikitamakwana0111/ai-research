from typing import Any, List, Tuple

from app.core.config import settings
from app.services.rag.vector_store import VectorStore
from app.utils.openai_client import OpenAIClient


class RAGPipeline:
    def __init__(self) -> None:
        self.vector_store: Any | None = None
        self.llm = OpenAIClient()

    def _ensure_vector_store(self) -> VectorStore:
        if self.vector_store is None:
            self.vector_store = VectorStore(settings.vector_store_path)
        return self.vector_store

    def retrieve(self, query: str) -> List[dict]:
        return self._ensure_vector_store().search(query)

    def answer_query(self, query: str, session_id: str | None = None) -> Tuple[str, List[dict]]:
        sources = self.retrieve(query)
        source_texts = "\n\n".join(
            [f"Source {item['source']} (page {item['page_number']}): {item['content']}" for item in sources]
        )
        prompt = (
            f"You are an AI research assistant with access to uploaded documents. "
            f"Answer the following question using the documents below and be explicit about sources.\n\n"
            f"Documents:\n{source_texts}\n\nQuestion: {query}"
        )
        answer = self.llm.complete(prompt, temperature=0.2)
        return answer, sources
