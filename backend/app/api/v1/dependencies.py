from fastapi import Depends

from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.research_service import ResearchService


def get_research_service() -> ResearchService:
    return ResearchService()


def get_document_service() -> DocumentService:
    return DocumentService()


def get_chat_service() -> ChatService:
    return ChatService()
