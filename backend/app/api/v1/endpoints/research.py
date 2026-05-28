from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import get_research_service
from app.models.schemas import ResearchResponse, TopicRequest, ReportRequest
from app.services.research_service import ResearchService
from app.utils.openai_client import AIServiceError

router = APIRouter()


@router.post("/start", response_model=ResearchResponse)
async def start_research(
    payload: TopicRequest,
    service: ResearchService = Depends(get_research_service),
) -> ResearchResponse:
    try:
        result = await service.start_research(payload)
    except AIServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if not result:
        raise HTTPException(status_code=500, detail="Research workflow failed")
    return result


@router.post("/report", response_model=ResearchResponse)
async def generate_report(
    payload: ReportRequest,
    service: ResearchService = Depends(get_research_service),
) -> ResearchResponse:
    try:
        return await service.generate_report(payload)
    except AIServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
