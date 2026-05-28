from app.models.schemas import ChatQuery, ChatResponse
from app.services.rag.rag_pipeline import RAGPipeline


class ChatService:
    def __init__(self) -> None:
        self.rag = RAGPipeline()

    def query(self, payload: ChatQuery) -> ChatResponse:
        answer, sources = self.rag.answer_query(payload.message, session_id=payload.session_id)
        return ChatResponse(answer=answer, source_documents=sources)
