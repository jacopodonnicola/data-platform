FROM python:3.12-slim

WORKDIR /app

# installa uv
RUN pip install uv

# copia i file di dipendenze prima del codice (ottimizzazione cache layer Docker)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# copia il resto del progetto
COPY ingestion/ ./ingestion/
COPY dbt/ ./dbt/

# crea la cartella per i dati di warehouse
RUN mkdir -p /app/warehouse

# rende eseguibili gli script tramite il venv creato da uv
ENV PATH="/app/.venv/bin:$PATH"