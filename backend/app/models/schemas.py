from typing import List, Optional

from pydantic import BaseModel, Field


class TopicRequest(BaseModel):
    topic: str = Field(..., title="Research topic", min_length=3)
    enable_web_search: bool = Field(True, title="Enable web search agent")
    include_documents: bool = Field(True, title="Include uploaded documents in RAG")


class ReportRequest(TopicRequest):
    report_format: str = Field("summary", title="Report format")


class ChatQuery(BaseModel):
    message: str = Field(..., title="Chat message")
    session_id: Optional[str] = Field(None, title="Session identifier")


class AgentResult(BaseModel):
    agent_name: str
    output: str
    metadata: Optional[dict] = None


class ResearchResponse(BaseModel):
    topic: str
    results: List[AgentResult]
    summary: str
    report_url: Optional[str] = None


class DocumentUploadResponse(BaseModel):
    filename: str
    document_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    source_documents: Optional[List[dict]] = None
