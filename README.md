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

## Build delle immagini custom

Da eseguire una volta, o ogni volta che si modifica il codice:

```bash
# immagine pipeline di ingestion + dbt
docker build -f docker/Dockerfile -t data-platform:latest .

# immagine Superset con driver DuckDB
docker build -f docker/Dockerfile.superset -t superset-custom:latest .
```

## Avvio dell'infrastruttura

```bash
cd docker
docker compose up -d
```

### Importare il flow in Kestra

Dopo ogni riavvio di Kestra, importare manualmente il flow tramite API:

```bash
curl -X POST \
  -u "tuaemail@kestra.dev:tuapassword" \
  -H "Content-Type: application/x-yaml" \
  --data-binary @docker/flows/data_platform_pipeline.yml \
  "http://localhost:8080/api/v1/main/flows"
```

> **Nota:** Kestra usa `repository: type: memory` — i flow non persistono tra riavvii.
> Questo è un workaround temporaneo; in futuro si passerà a PostgreSQL come repository persistente.


## Roadmap
- [x] Ingestion pipeline (Alpha Vantage → MinIO)
- [x] DuckDB + dbt (trasformazioni e data mart)
- [x] Kestra (orchestrazione completa)
- [ ] Superstor (dashboard)
- [ ] CI/CD con GitHub Actions