import asyncio

from app.models.schemas import TopicRequest
from app.services.research_service import ResearchService


def test_start_research_returns_response():
    service = ResearchService()

    async def fake_analysis(payload):
        return {"output": "Analysis", "metadata": payload}

    async def fake_summary(payload):
        return {"output": "Summary", "metadata": {"topic": payload["topic"]}}

    async def fake_report(payload):
        return {"output": "Report", "metadata": {"topic": payload["topic"]}}

    service.analysis_agent.run = fake_analysis
    service.summary_agent.run = fake_summary
    service.report_agent.run = fake_report

    request = TopicRequest(topic="AI in healthcare", enable_web_search=False, include_documents=False)
    result = asyncio.run(service.start_research(request))
    assert result.topic == "AI in healthcare"
    assert len(result.results) >= 2
    assert result.summary
