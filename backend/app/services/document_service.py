from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from app.core.config import settings
from app.services.rag.pdf_parser import PDFParser
from app.services.rag.vector_store import VectorStore
from app.utils.pdf_utils import save_upload_file


class DocumentService:
    def __init__(self) -> None:
        self.upload_folder: Path = settings.upload_folder
        self.upload_folder.mkdir(parents=True, exist_ok=True)
        self.vector_store = VectorStore(settings.vector_store_path)
        self.parser = PDFParser(settings.max_pdf_pages)

    def save_pdf(self, upload_file: UploadFile, document_id: str) -> Path:
        destination = self.upload_folder / f"{document_id}.pdf"
        save_upload_file(upload_file, destination)
        return destination

    def index_pdf(self, file_path: Path, document_id: str) -> None:
        pages = self.parser.extract_pages(file_path)
        self.vector_store.add_documents(pages, source=document_id)

    def list_documents(self) -> list[dict]:
        return self.vector_store.list_documents()
