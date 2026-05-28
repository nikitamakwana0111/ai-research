import asyncio
from typing import Any, Dict

from openai import OpenAI, OpenAIError

from app.core.config import settings
from app.services.agents.base_agent import BaseAgent
from app.utils.openai_client import AIServiceError


class SummaryAgent(BaseAgent):
    name = "Summary Agent"

    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        topic = payload["topic"]
        search = payload.get("search", "")
        analysis = payload.get("analysis", "")
        prompt = (
            f"Generate a concise executive summary for the topic: {topic}\n\n"
            "Generate:\n"
            "* Concise executive summary\n"
            "* Key findings\n"
            "* Important insights\n"
            "* Actionable recommendations\n\n"
            f"Research findings:\n{search}\n\n"
            f"Analysis:\n{analysis}"
        )
        output = await asyncio.to_thread(self._call_openai, prompt)
        return {"output": output, "metadata": {"topic": topic, "model": settings.MODEL_NAME}}

    @staticmethod
    def _call_openai(prompt: str) -> str:
        if not settings.GROQ_API_KEY.strip():
            raise AIServiceError("GROQ_API_KEY is missing. Add a valid key to backend/.env and restart the backend.")

        client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url=settings.GROQ_API_BASE
        )

        try:
            response = client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        except OpenAIError as exc:
            raise AIServiceError(f"Summary Agent Groq request failed: {exc}") from exc

        return (response.choices[0].message.content or "").strip()
