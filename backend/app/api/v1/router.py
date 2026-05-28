from fastapi import APIRouter

from app.api.v1.endpoints import chat, documents, research

api_router = APIRouter()
api_router.include_router(research.router, prefix="/research", tags=["research"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
