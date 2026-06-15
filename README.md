# Data Platform


## Obiettivo
Pipeline data engineering end-to-end a scopo didattico.


## Stack
- **MinIO** — object storage (S3-compatible)
- **Kestra** — orchestratore
- **DuckDB + dbt** — warehouse e trasformazioni
- **Metabase** — visualizzazione


## Architettura
Alpha Vantage API → ingestion (Python) → MinIO (Parquet) → DuckDB + dbt → Metabase


## Struttura del progetto
data-platform/

├── docker/          ← docker-compose.yml (MinIO + Kestra)

├── ingestion/       ← script Python per chiamate API

├── dbt/             ← modelli di trasformazione

└── warehouse/       ← configurazione DuckDB


## Sorgente dati
Alpha Vantage API — free tier (25 chiamate/giorno)
Paniere: AAPL, MSFT, GOOGL, META, AMZN, NVDA, TSLA

Endpoint:
- `TIME_SERIES_DAILY` — prezzi OHLCV giornalieri
- `OVERVIEW` — fondamentali aziendali
- `EARNINGS` — EPS trimestrale

## Setup

### Requisiti
- Docker
- Python 3.11
- uv

### Avvio infrastruttura
```bash
cd docker
docker compose up -d
```

### Configurazione variabili d'ambiente
Copia il file di esempio e crea il tuo `.env` locale:
```bash
cp .env.example .env
```
Apri `.env` e inserisci le credenziali richieste.

### Installazione dipendenze Python
```bash
uv sync
```

### Esecuzione ingestion
```bash
cd ingestion
uv run python main.py
```

## Roadmap
- [x] Ingestion pipeline (Alpha Vantage → MinIO)
- [ ] DuckDB + dbt (trasformazioni e data mart)
- [ ] Kestra (orchestrazione completa)
- [ ] Metabase (dashboard)
- [ ] CI/CD con GitHub Actions