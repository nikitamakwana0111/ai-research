# Multi-Agent AI Research Assistant Backend

This backend powers the Multi-Agent AI Research Assistant with:

- FastAPI REST APIs
- OpenAI-driven multi-agent workflows
- CrewAI workflow orchestration
- LangChain-style RAG using FAISS
- PDF parsing via PyMuPDF
- Document chat and research endpoints

## Backend Layout

- `app/main.py` - FastAPI application entrypoint
- `app/api/v1/` - REST routes for research, documents, and chat
- `app/services/` - business logic and agent orchestration
- `app/services/rag/` - vector store, embeddings, and RAG pipeline
- `app/utils/` - OpenAI client wrapper and PDF utilities
- `tests/` - unit and integration test coverage

## Setup

1. Copy `.env.example` to `.env` and set `GROQ_API_KEY`. The default model is `MODEL_NAME=llama-3.3-70b-versatile`.
2. Install dependencies:

```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the service:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open API docs at `http://localhost:8000/docs`
