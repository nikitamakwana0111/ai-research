from app.services.rag.rag_pipeline import RAGPipeline


def test_rag_pipeline_can_initialize():
    rag = RAGPipeline()
    assert rag.vector_store is not None


def test_answer_query_builds_prompt(monkeypatch):
    rag = RAGPipeline()

    def fake_complete(prompt, temperature=0.2, max_tokens=512):
        return "Test answer"

    monkeypatch.setattr(rag.llm, "complete", fake_complete)
    answer, sources = rag.answer_query("What is an AI research assistant?")
    assert answer == "Test answer"
    assert isinstance(sources, list)
