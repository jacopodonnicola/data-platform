import time

import config # carica le variabili di configurazione definite in config.py
from extractors.prices import extract_prices # importa la funzione extract_prices dal modulo extractors.prices.
from extractors.overview import extract_overview
from extractors.earnings import extract_earnings
from transformers.prices import transform_prices
from transformers.overview import transform_overview
from transformers.earnings import transform_earnings
from loaders.minio_loader import get_minio_client, save_parquet

def is_valid_response(data: dict, expected_key: str) -> bool:
    """
    Verifica che la risposta dell'API contenga i dati attesi
    e non un messaggio di errore.
    """
    if "Information" in data or "Note" in data:
        print(f"⚠️ API rate limit raggiunto: {data.get('Information') or data.get('Note')}")
        return False
    if expected_key not in data:
        print(f"⚠️ Chiave attesa '{expected_key}' non trovata nella risposta")
        return False
    return True


def main():
    # inizializza client MinIO
    client = get_minio_client(
        endpoint=config.MINIO_ENDPOINT,
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=config.MINIO_SECURE
    )

    for ticker in config.TICKERS:
        print(f"Processing {ticker}...")

        # prices
        raw_prices = extract_prices(ticker, config.API_KEY, config.BASE_URL)
        if is_valid_response(raw_prices, "Time Series (Daily)"):
            df_prices = transform_prices(raw_prices, ticker)
            save_parquet(client, config.BUCKET_STAGING, f"{config.PREFIX_PRICES}/{ticker}_prices.parquet", df_prices)
        time.sleep(2)  # aspetta 2 secondi


        # overview
        raw_overview = extract_overview(ticker, config.API_KEY, config.BASE_URL)
        if is_valid_response(raw_overview, "Symbol"):
            df_overview = transform_overview(raw_overview, ticker)
            save_parquet(client, config.BUCKET_STAGING, f"{config.PREFIX_OVERVIEW}/{ticker}_overview.parquet", df_overview)
        time.sleep(2)  # aspetta 2 secondi

        # earnings
        raw_earnings = extract_earnings(ticker, config.API_KEY, config.BASE_URL)
        if is_valid_response(raw_earnings, "quarterlyEarnings"):
            df_earnings = transform_earnings(raw_earnings, ticker)
            save_parquet(client, config.BUCKET_STAGING, f"{config.PREFIX_EARNINGS}/{ticker}_earnings.parquet", df_earnings)
        time.sleep(2)  # aspetta 2 secondi

        print(f"✅ {ticker} completato")

if __name__ == "__main__":
    main()