import pytest
from pathlib import Path

from app.services.document_service import DocumentService


def test_save_pdf_and_index(tmp_path, monkeypatch):
    service = DocumentService()
    service.upload_folder = tmp_path
    service.vector_store = service.vector_store.__class__(tmp_path / "vector")

    class DummyUpload:
        filename = "test.pdf"
        content_type = "application/pdf"
        file = open(__file__, "rb")

    upload = DummyUpload()
    destination = service.save_pdf(upload, "doc-123")
    assert destination.exists()
    upload.file.close()

    # Test indexing path does not throw
    service.index_pdf(destination, "doc-123")
    assert service.vector_store.index.ntotal >= 0


def test_list_documents_returns_list():
    service = DocumentService()
    assert isinstance(service.list_documents(), list)
