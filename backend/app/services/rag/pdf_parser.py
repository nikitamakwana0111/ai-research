from pathlib import Path
from typing import List

try:
    import fitz
    from fitz import FileDataError
except ModuleNotFoundError:
    import pymupdf as fitz
    from pymupdf import FileDataError


class PDFParser:
    def __init__(self, max_pages: int = 50) -> None:
        self.max_pages = max_pages

    def extract_pages(self, path: Path) -> List[dict]:
        try:
            document = fitz.open(path)
        except FileDataError:
            return []

        pages: list[dict] = []
        try:
            for index, page in enumerate(document, start=1):
                if index > self.max_pages:
                    break
                text = page.get_text("text")
                if not text.strip():
                    continue
                pages.append({
                    "page_number": index,
                    "content": text,
                    "source": path.name,
                })
        finally:
            document.close()
        return pages
