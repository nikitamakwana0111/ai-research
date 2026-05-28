from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_chat_service
from app.models.schemas import ChatQuery, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/query", response_model=ChatResponse)
def query_chat(
    payload: ChatQuery,
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    return service.query(payload)
