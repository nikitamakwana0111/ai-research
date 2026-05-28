from typing import List

from app.models.schemas import AgentResult, ReportRequest, ResearchResponse, TopicRequest
from app.services.agents.analysis_agent import AnalysisAgent
from app.services.agents.report_agent import ReportAgent
from app.services.agents.search_agent import SearchAgent
from app.services.agents.summary_agent import SummaryAgent
from app.services.crew.workflow import CrewWorkflow
from app.services.rag.rag_pipeline import RAGPipeline


class ResearchService:
    def __init__(self) -> None:
        self.rag = RAGPipeline()
        self.analysis_agent = AnalysisAgent()
        self.summary_agent = SummaryAgent()
        self.report_agent = ReportAgent()
        self.search_agent = SearchAgent()
        self.workflow = CrewWorkflow()

    async def start_research(self, request: TopicRequest) -> ResearchResponse:
        results: List[AgentResult] = []
        search_text = ""
        if request.enable_web_search:
            web_search_output = await self.search_agent.run({"topic": request.topic})
            search_text = web_search_output["output"]
            results.append(AgentResult(
                agent_name="Search Agent",
                output=web_search_output["output"],
                metadata=web_search_output.get("metadata"),
            ))

        analysis_output = await self.analysis_agent.run({"topic": request.topic, "search": search_text})
        results.append(AgentResult(
            agent_name="Analysis Agent",
            output=analysis_output["output"],
            metadata=analysis_output.get("metadata"),
        ))

        summary_output = await self.summary_agent.run({
            "topic": request.topic,
            "search": search_text,
            "analysis": analysis_output["output"],
        })
        results.append(AgentResult(
            agent_name="Summary Agent",
            output=summary_output["output"],
            metadata=summary_output.get("metadata"),
        ))

        report_output = await self.report_agent.run({
            "topic": request.topic,
            "search": search_text,
            "analysis": analysis_output["output"],
            "summary": summary_output["output"],
        })
        results.append(AgentResult(
            agent_name="Report Generation Agent",
            output=report_output["output"],
            metadata=report_output.get("metadata"),
        ))

        self.workflow.execute([result.model_dump() for result in results])

        return ResearchResponse(
            topic=request.topic,
            results=results,
            summary=summary_output["output"],
            report_url=None,
        )

    async def generate_report(self, request: ReportRequest) -> ResearchResponse:
        report_output = await self.report_agent.run({"topic": request.topic, "report_format": request.report_format})
        return ResearchResponse(
            topic=request.topic,
            results=[AgentResult(agent_name="Report Generation Agent", output=report_output["output"])],
            summary=report_output["output"],
            report_url=None,
        )
