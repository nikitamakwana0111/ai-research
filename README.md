# Multi-Agent AI Research Assistant

A production-ready AI research workspace built with:

- Frontend: React + TypeScript + Tailwind + Vite
- Backend: FastAPI + Python
- AI: OpenAI API
- Multi-agent framework: CrewAI
- RAG: LangChain-style FAISS integration
- PDF parsing: PyMuPDF

## Project Structure

- `backend/` - FastAPI backend, agent orchestration, RAG pipeline, PDF ingestion
- `frontend/` - React dashboard and chat UI

## Getting Started

### Backend

1. `cd backend`
2. Copy `.env.example` to `.env` and set `GROQ_API_KEY`. The default model is `MODEL_NAME=llama-3.3-70b-versatile`.
3. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Start the backend:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Open API docs at `http://localhost:8000/docs`

### Frontend

1. `cd frontend`
2. Copy `.env.example` to `.env`
3. Install dependencies:

```bash
npm install
```

4. Start the frontend:

```bash
npm run dev
```

5. Visit `http://localhost:5173`

### Docker

Run both services together:

```bash
docker-compose up --build
```
