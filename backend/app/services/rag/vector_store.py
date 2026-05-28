from pathlib import Path
import json
from typing import Any, Dict, List

import faiss
import numpy as np

from app.services.rag.embeddings import EmbeddingsProvider


class VectorStore:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.storage_path / "faiss.index"
        self.metadata_path = self.storage_path / "metadata.json"
        self.embedding_provider = EmbeddingsProvider()
        self.dimension = 1536
        self.index = self._load_or_create_index()
        self.metadata: List[Dict[str, Any]] = self._load_metadata()

    def _load_or_create_index(self) -> faiss.IndexFlatL2:
        if self.index_path.exists():
            try:
                return faiss.read_index(str(self.index_path))
            except Exception:
                pass
        return faiss.IndexFlatL2(self.dimension)

    def _load_metadata(self) -> List[Dict[str, Any]]:
        if self.metadata_path.exists():
            try:
                with self.metadata_path.open("r", encoding="utf-8") as metadata_file:
                    return json.load(metadata_file)
            except Exception:
                return []
        return []

    def persist(self) -> None:
        faiss.write_index(self.index, str(self.index_path))
        with self.metadata_path.open("w", encoding="utf-8") as metadata_file:
            json.dump(self.metadata, metadata_file, ensure_ascii=False, indent=2)

    def add_documents(self, pages: List[dict], source: str) -> None:
        if not pages:
            return

        texts = [page["content"] for page in pages]
        vectors = self.embedding_provider.embed_texts(texts)
        if not vectors:
            return

        self.index.add(np.array(vectors, dtype="float32"))
        for page in pages:
            self.metadata.append({
                "source": source,
                "page_number": page["page_number"],
                "content": page["content"],
            })
        self.persist()

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        if self.index.ntotal == 0:
            return []

        query_embedding = self.embedding_provider.embed_texts([query])[0]
        query_vector = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(query_vector, top_k)
        results: List[Dict[str, Any]] = []
        for idx in indices[0].tolist():
            if idx < 0 or idx >= len(self.metadata):
                continue
            results.append(self.metadata[idx])
        return results

    def list_documents(self) -> List[Dict[str, Any]]:
        return self.metadata
