import requests # per fare richieste HTTP all'API di Alpha Vantage


def extract_prices(ticker: str, api_key: str, base_url: str) -> dict: # funzione per estrarre i dati dei prezzi da Alpha Vantage, prende in input il ticker, la chiave API e l'URL base dell'API, restituisce un dizionario con i dati dei prezzi
    """
    Chiama l'endpoint TIME_SERIES_DAILY di Alpha Vantage
    e restituisce il JSON grezzo.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": api_key
    }

    response = requests.get(base_url, params=params) # effettua la richiesta GET all'endpoint specificato con i parametri definiti
    response.raise_for_status()  # solleva eccezione se la chiamata fallisce
    
    return response.json() # restituisce il JSON grezzo della risposta, che contiene i dati dei prezzi giornalieri per il ticker specificato

