# Configurazione per l'ingestion dei dati finanziari da Alpha Vantage e il loro storage su MinIO.

import os # Per accedere alle variabili d'ambiente
from dotenv import load_dotenv # Per caricare le variabili d'ambiente da un file .env

load_dotenv()  # Carica le variabili dal .env nel processo Python corrente

# ---------------------------------------------------------------------------
# Alpha Vantage
# ---------------------------------------------------------------------------
API_KEY  = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

# Paniere ristretto - Magnificent 7
TICKERS = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "GOOGL",  # Alphabet
    "META",   # Meta
    "AMZN",   # Amazon
    "NVDA",   # NVIDIA
    "TSLA",   # Tesla
]

# ---------------------------------------------------------------------------
# MinIO
# ---------------------------------------------------------------------------
MINIO_ENDPOINT   = os.getenv("MINIO_ENDPOINT", "localhost:9000") # endpoint di default per sviluppo locale
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin") # chiave di accesso di default per sviluppo locale
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin") # chiave segreta di default per sviluppo locale
MINIO_SECURE     = False  # True se HTTPS è abilitato, False per HTTP (sviluppo locale)

# Bucket
BUCKET_RAW     = "raw"
BUCKET_STAGING = "staging"

# Prefissi per endpoint
PREFIX_PRICES   = "prices"
PREFIX_OVERVIEW = "overview"
PREFIX_EARNINGS = "earnings"