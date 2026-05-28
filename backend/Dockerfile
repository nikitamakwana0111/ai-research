FROM python:3.11-slim

WORKDIR /app

COPY ./pyproject.toml ./
COPY ./app ./app
COPY ./start.sh ./start.sh

RUN pip install --no-cache-dir pip --upgrade \
    && pip install --no-cache-dir . \
    && chmod +x ./start.sh

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["./start.sh"]
