from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.v1.dependencies import get_document_service
from app.models.schemas import DocumentUploadResponse
from app.services.document_service import DocumentService
from app.utils.openai_client import AIServiceError

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
) -> DocumentUploadResponse:
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    document_id = str(uuid4())
    saved_path = service.save_pdf(file, document_id)
    try:
        service.index_pdf(saved_path, document_id)
    except AIServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return DocumentUploadResponse(
        filename=file.filename,
        document_id=document_id,
        message="PDF uploaded and indexed successfully.",
    )


@router.get("/health")
def document_health(service: DocumentService = Depends(get_document_service)) -> dict:
    return {"status": "ready", "upload_folder": str(service.upload_folder.resolve())}
