FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VECTOR_STORE_PATH=/app/data/faiss_store \
    UPLOAD_FOLDER=/app/data/uploads \
    EMBEDDINGS_MODEL=local-hash-embedding

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

RUN mkdir -p /app/data/faiss_store /app/data/uploads

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
