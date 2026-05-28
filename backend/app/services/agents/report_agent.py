import asyncio
from typing import Any, Dict

from openai import OpenAI, OpenAIError

from app.core.config import settings
from app.services.agents.base_agent import BaseAgent
from app.utils.openai_client import AIServiceError


class ReportAgent(BaseAgent):
    name = "Report Generation Agent"

    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        topic = payload["topic"]
        search = payload.get("search", "")
        analysis = payload.get("analysis", "")
        summary = payload.get("summary", "")
        report_format = payload.get("report_format", "professional research report")
        prompt = (
            f"Generate a {report_format} for the topic: {topic}\n\n"
            "Include these sections:\n"
            "* Executive Summary\n"
            "* Overview\n"
            "* Key Findings\n"
            "* Trends\n"
            "* Opportunities\n"
            "* Risks\n"
            "* Recommendations\n"
            "* Conclusion\n\n"
            f"Research findings:\n{search}\n\n"
            f"Analysis:\n{analysis}\n\n"
            f"Summary:\n{summary}"
        )
        output = await asyncio.to_thread(self._call_openai, prompt)
        return {"output": output, "metadata": {"topic": topic, "format": report_format, "model": settings.MODEL_NAME}}

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
            raise AIServiceError(f"Report Agent Groq request failed: {exc}") from exc

        return (response.choices[0].message.content or "").strip()
