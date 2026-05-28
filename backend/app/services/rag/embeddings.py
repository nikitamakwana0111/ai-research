import hashlib
import math
import re
from typing import List

from app.core.config import settings


class EmbeddingsProvider:
    def __init__(self) -> None:
        self.model = settings.embeddings_model
        self.dimension = 1536

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_text(text) for text in texts]

    def _embed_text(self, text: str) -> List[float]:
        vector = [0.0] * self.dimension
        tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
        if not tokens:
            return vector

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]
