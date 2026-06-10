import requests

def extract_earnings(ticker: str, api_key: str, base_url: str) -> dict:
    """
    Chiama l'endpoint EARNINGS di Alpha Vantage
    e restituisce il JSON grezzo.
    """
    params = {
        "function": "EARNINGS",
        "symbol": ticker,
        "apikey": api_key
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    return response.json()