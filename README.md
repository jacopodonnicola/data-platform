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
docker build -f docker/Dockerfile.pipeline -t pipeline:latest .

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

### Completato
- [x] Ingestion pipeline (Alpha Vantage → MinIO)
- [x] DuckDB + dbt (trasformazioni e data mart)
- [x] Kestra (orchestrazione completa con scheduling)
- [x] Superset (dashboard)

### Evoluzioni future
- [x] Architettura medallion completa — separare ingestion (JSON → raw/) e trasformazione (raw/ → staging/) in due fasi distinte in `main.py`
- [x] Caricamento automatico dei flow di Kestra all’avvio
- [x] CI/CD con GitHub Actions (lint, test, validazione dbt su PR)
- [x] Git flow con branch feature per nuove funzionalità
- [ ] Superset Reports — invio schedulato dashboard via email (richiede Redis + Celery)


# Architettura Target v2

## Obiettivo
Stock screening su universo allargato di ticker con pipeline giornaliera incrementale.

## Sorgenti dati
- **IB Gateway** — lista giornaliera ticker con filtri base (currency, volume, exchange)
- **Yahoo Finance o equivalente** — storico OHLCV giornaliero per i ticker selezionati
- requisito: supporto ingestion ~70k record/giorno (7k ticker × 10 giorni overlap)

## Strategia di ingestion
- **Precarico iniziale** — caricamento manuale su MinIO dello storico 1-2 anni per tutti i ticker
- **Run giornaliero incrementale** — ultimi 10 giorni per ogni ticker (overlap intenzionale per resilienza)
- **Cleanup periodico** — eliminazione partizioni MinIO più vecchie di 2 anni (task Kestra)

## Architettura Medallion
raw/
├── ib_screener/date=YYYY-MM-DD/ ← lista ticker giornaliera da IB
└── prices/date=YYYY-MM-DD/ ← OHLCV grezzo per tutti i ticker

staging/
├── stg_screener/ ← ticker list pulita
└── stg_prices/ ← OHLCV Parquet partizionato per data

warehouse/ (DuckDB)
├── staging/
├── intermediate/
│ ├── int_active_tickers ← join screener + prices
│ └── int_price_metrics ← rendimenti, volatilità, medie mobili
└── marts/
├── fact_daily_prices ← finestra mobile 1 anno, tutti i ticker attivi
├── dim_ticker ← anagrafica ticker con metadati IB
└── fact_screening ← output screening giornaliero (~50 ticker)


## Finestra dati
- MinIO: 2 anni (gestito da cleanup periodico)
- DuckDB warehouse: 1 anno (filtro in dbt)
- Superset dashboard: ~50 ticker selezionati dallo screening

## Note
- Batch download per ottimizzare le chiamate API (es. yfinance supporta download multi-ticker)
- Parallelismo nei task Kestra per gestire il volume giornaliero
- Repo attuale come base — stessa struttura, sorgenti e volumi diversi
Commit finale e chiudiamo?