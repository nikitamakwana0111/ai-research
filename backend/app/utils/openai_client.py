import logging
from typing import List

from openai import OpenAI, OpenAIError

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIServiceError(RuntimeError):
    pass


class OpenAIClient:
    def __init__(self) -> None:
        self.default_model = settings.MODEL_NAME

    def complete(self, prompt: str, temperature: float = 0.2, max_tokens: int = 512) -> str:
        self._ensure_api_key()
        client = OpenAI(api_key=settings.GROQ_API_KEY, base_url=settings.GROQ_API_BASE)
        logger.info("Generating completion with Groq model %s", self.default_model)
        try:
            response = client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except OpenAIError as exc:
            logger.warning("Groq completion failed: %s", exc)
            raise AIServiceError(self._format_openai_error(exc)) from exc
        return (response.choices[0].message.content or "").strip()

    def create_embeddings(self, texts: List[str], model: str) -> List[List[float]]:
        if not texts:
            return []

        self._ensure_api_key()
        client = OpenAI(api_key=settings.GROQ_API_KEY, base_url=settings.GROQ_API_BASE)
        logger.info("Creating embeddings for %s texts", len(texts))
        try:
            response = client.embeddings.create(
                model=model,
                input=texts,
            )
        except OpenAIError as exc:
            logger.warning("OpenAI embeddings failed: %s", exc)
            raise AIServiceError(self._format_openai_error(exc)) from exc
        return [item.embedding for item in response.data]

    @staticmethod
    def _ensure_api_key() -> None:
        if not settings.GROQ_API_KEY.strip():
            raise AIServiceError("GROQ_API_KEY is missing. Add a valid key to backend/.env and restart the backend.")

    @staticmethod
    def _format_openai_error(exc: OpenAIError) -> str:
        message = str(exc)
        if "insufficient_quota" in message or "exceeded your current quota" in message:
            return "Groq rejected the request because the configured API key has insufficient quota."
        return f"Groq request failed: {message}"
