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

## Railway Deployment

This repository includes a root `railway.toml` and root `Dockerfile` for deploying only the backend service from the monorepo.

1. Create a Railway service from this repository.
2. Keep the Railway service root as the repository root so Railway can read `railway.toml`.
3. Add these variables in Railway:

```bash
GROQ_API_KEY=your_groq_key
GROQ_API_BASE=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
EMBEDDINGS_MODEL=local-hash-embedding
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

Railway injects `PORT` automatically. The backend start script binds Uvicorn to `0.0.0.0:${PORT}`, which is required for Railway public networking.
